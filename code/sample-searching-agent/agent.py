"""
The main agent that orchestrates the report generation process.
"""

import asyncio
import logging
import os
from typing import Annotated, Any, Sequence, cast

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import author, researcher
from .prompts import report_planner_instructions

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3
_QUERIES_PER_SECTION = 5
_THROTTLE_LLM_CALLS = os.getenv("THROTTLE_LLM_CALLS", "0")

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)


class Report(BaseModel):
    title: str
    sections: list[author.Section]


class AgentState(BaseModel):
    topic: str
    report_structure: str
    report_plan: Report | None = None
    report: str | None = None
    messages: Annotated[Sequence[Any], add_messages] = []


async def topic_discovery(state: AgentState, config: RunnableConfig):
    """Discover the topic of the document."""
    _LOGGER.info("Performing initial topic research.")

    researcher_state = researcher.ResearcherState(
        topic=state.topic,
        number_of_queries=_QUERIES_PER_SECTION,
        messages=state.messages,
    )

    research = await researcher.graph.ainvoke(researcher_state, config)

    return {"messages": research.get("messages", [])}


async def report_planner(state: AgentState, config: RunnableConfig):
    """Call the model."""
    _LOGGER.info("Calling report planner.")

    model = llm.with_structured_output(Report)  # type: ignore

    system_prompt = report_planner_instructions.format(
        topic=state.topic,
        report_structure=state.report_structure,
    )
    for count in range(_MAX_LLM_RETRIES):
        messages = [{"role": "system", "content": system_prompt}] + list(state.messages)
        response = await model.ainvoke(messages, config)
        if response:
            response = cast(Report, response)
            state.report_plan = response
            return state
        _LOGGER.debug(
            "Retrying LLM call. Attempt %d of %d", count + 1, _MAX_LLM_RETRIES
        )

    raise RuntimeError("Failed to call model after %d attempts.", _MAX_LLM_RETRIES)


async def section_writer(state: AgentState, config: RunnableConfig):
    """Write the sections of the report."""
    if not state.report_plan:
        raise ValueError("Report plan is not set.")

    _LOGGER.info("Writing the sections of the report.")

    writers = []
    for idx, section in enumerate(state.report_plan.sections):
        _LOGGER.info("Creating writer agent for section: %s", section.name)

        section_writer_state = author.SectionWriterState(
            index=idx,
            section=section,
            topic=state.topic,
            messages=state.messages,
        )
        writers.append(author.graph.ainvoke(section_writer_state, config))

    all_sections = []
    if _THROTTLE_LLM_CALLS == "1":
        # Throttle LLM calls by writing one section at a time
        _LOGGER.info("Throttling LLM calls.")
        for writer in writers:
            all_sections.append(await writer)
            await asyncio.sleep(30)
    else:
        # Without throttling, write all sections at once
        all_sections = await asyncio.gather(*writers)
    all_sections = cast(list[dict[str, Any]], all_sections)

    for section in all_sections:
        index = section["index"]
        content = section["section"].content
        state.report_plan.sections[index].content = content
        _LOGGER.info("Finished section: %s", state.report_plan.sections[index].name)

    return state


async def report_writer(state: AgentState, config: RunnableConfig):
    """Write the report."""
    if not state.report_plan:
        raise ValueError("Report plan is not set.")

    _LOGGER.info("Writing the report.")

    output = f"# {state.report_plan.title}\n\n"
    for section in state.report_plan.sections:
        output += section.content
        output += "\n\n"

    state.report = output
    return state


workflow = StateGraph(AgentState)

workflow.add_node("topic_discovery", topic_discovery)
workflow.add_node("report_planner", report_planner)
workflow.add_node("section_writer", section_writer)
workflow.add_node("report_writer", report_writer)

workflow.add_edge(START, "topic_discovery")
workflow.add_edge("topic_discovery", "report_planner")
workflow.add_edge("report_planner", "section_writer")
workflow.add_edge("section_writer", "report_writer")
workflow.add_edge("report_writer", END)

graph = workflow.compile()
