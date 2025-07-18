"""
Nodes for the report generation agent.
"""

import asyncio
import logging
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph

from .helpers import invoke_structured_llm_with_retry
from .models import ReportState, Sections
from .prompts import report_planner_instructions
from .researcher import ResearchState, research_graph

_LOGGER = logging.getLogger(__name__)

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)


async def preform_discovery_research(state: ReportState) -> ReportState:
    """Preform discovery research."""
    _LOGGER.info("Preforming discovery research")

    discover_state = ResearchState(
        topic=state.topic,
        mode="discovery",
        number_of_queries=state.number_of_queries,
        tavily_topic=state.tavily_topic,
        tavily_days=state.tavily_days,
    )

    discovery_state = await research_graph.ainvoke(discover_state)
    discovery_state = cast(ResearchState, discover_state)

    state.discovery_results = discovery_state.research_results
    _LOGGER.debug("Discovery research results: %s", state.discovery_results)
    return state


async def generate_report_outline(state: ReportState) -> ReportState:
    """Generate a report outline."""
    _LOGGER.info("Generating a report outline")

    structured_llm = llm.with_structured_output(Sections)
    system_instructions_query = report_planner_instructions.format(
        topic=state.topic,
        report_organization=state.report_structure,
        context=state.research_results,
    )
    messages = [
        SystemMessage(content=system_instructions_query),
        HumanMessage(content="Generate the outline of the report."),
    ]
    results = invoke_structured_llm_with_retry(structured_llm, messages)
    _LOGGER.debug("Report outline: %s", results or [])
    state.sections = results.sections or Sections(sections=[])  # type: ignore
    return state
