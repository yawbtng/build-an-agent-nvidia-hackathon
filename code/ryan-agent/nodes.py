"""
Nodes for the report generation agent.
"""

import asyncio
import logging

import prompts
from helpers import deduplicate_and_format_sources, invoke_structured_llm_with_retry
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from models import Queries, ReportState, Sections
from tavily import AsyncTavilyClient

_LOGGER = logging.getLogger(__name__)

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)
tavily_client = AsyncTavilyClient()


async def create_research_plan(state: ReportState) -> ReportState:
    """Create a research plan for the report."""
    _LOGGER.info("Creating research plan for report")

    structured_llm = llm.with_structured_output(Queries)
    system_instructions_query = prompts.report_planner_query_writer_instructions.format(
        topic=state.topic,
        report_organization=state.report_structure,
        number_of_queries=state.number_of_queries,
    )
    messages = [
        SystemMessage(content=system_instructions_query),
        HumanMessage(
            content="Generate search queries that will help with planning the sections of the report."
        ),
    ]
    results = invoke_structured_llm_with_retry(structured_llm, messages)

    _LOGGER.debug("Research plan: %s", results or [])
    state.research_plan = results or []  # type: ignore
    return state


async def tavily_search(state: ReportState) -> ReportState:
    """Search the web using the Tavily API."""
    _LOGGER.info("Searching the web using the Tavily API")
    search_tasks = []

    if not state.research_plan:
        _LOGGER.warning("No research plan found")
        return state

    for query in state.research_plan.queries:
        days = state.tavily_days if state.tavily_topic == "news" else None
        search_tasks.append(
            tavily_client.search(
                query,
                max_results=5,
                include_raw_content=True,
                topic=state.tavily_topic,
                days=days,  # type: ignore
            )
        )

    # Execute all searches concurrently
    search_docs = await asyncio.gather(*search_tasks)

    state.research_results = deduplicate_and_format_sources(
        search_docs, max_tokens_per_source=1000, include_raw_content=True
    )
    _LOGGER.debug("Research results: %s", state.research_results)
    return state


async def generate_report_outline(state: ReportState) -> ReportState:
    """Generate a report outline."""
    _LOGGER.info("Generating a report outline")

    structured_llm = llm.with_structured_output(Sections)
    system_instructions_query = prompts.report_planner_instructions.format(
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


if __name__ == "__main__":
    state = ReportState(
        topic="Give an overview of capabilities and specific use case examples for these processing units: CPU, GPU.",
        report_structure="""This report type focuses on comparative analysis.

The report structure should include:
1. Introduction (no research needed)
   - Brief overview of the topic area
   - Context for the comparison

2. Main Body Sections:
   - One dedicated section for EACH offering being compared in the user-provided list
   - Each section should examine:
     - Core Features (bulleted list)
     - Architecture & Implementation (2-3 sentences)
     - One example use case (2-3 sentences)
   
3. No Main Body Sections other than the ones dedicated to each offering in the user-provided list

4. Conclusion with Comparison Table (no research needed)
   - Structured comparison table that:
     * Compares all offerings from the user-provided list across key dimensions
     * Highlights relative strengths and weaknesses
   - Final recommendations""",
    )

    import asyncio

    logging.basicConfig(level=logging.INFO)
    _LOGGER.setLevel(logging.INFO)

    state = asyncio.run(create_research_plan(state))
    state = asyncio.run(tavily_search(state))
    state = asyncio.run(generate_report_outline(state))

    for section in state.sections:
        print(f"{'='*50}")
        print(f"Name: {section.name}")
        print(f"Description: {section.description}")
        print(f"Research: {section.research}")
