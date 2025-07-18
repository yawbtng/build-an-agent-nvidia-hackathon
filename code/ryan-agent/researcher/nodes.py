"""
Nodes for the report generation agent.
"""

import asyncio
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from tavily import AsyncTavilyClient

from ..helpers import deduplicate_and_format_sources, invoke_structured_llm_with_retry
from .models import Queries, ResearchState
from .prompts import (
    query_writer_instructions_detail,
    query_writer_instructions_discovery,
)

_LOGGER = logging.getLogger(__name__)

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)
tavily_client = AsyncTavilyClient()


async def create_research_plan(state: ResearchState) -> ResearchState:
    """Create a research plan for the report."""
    _LOGGER.info("Creating research plan for report")

    # Configure structured output to get the research plan steps
    structured_llm = llm.with_structured_output(Queries)

    # create the system instructions based on research mode
    if state.mode == "discovery":
        system_instructions_query = query_writer_instructions_discovery.format(
            topic=state.topic, number_of_queries=state.number_of_queries
        )
    else:
        system_instructions_query = query_writer_instructions_detail.format(
            topic=state.topic, number_of_queries=state.number_of_queries
        )

    # create the messages for the LLM
    messages = [
        SystemMessage(content=system_instructions_query),
        HumanMessage(
            content="Generate search queries that will help with planning the sections of the report."
        ),
    ]

    # invoke the LLM
    results = invoke_structured_llm_with_retry(structured_llm, messages)

    # update the state with the research plan
    _LOGGER.debug("Research plan: %s", results or [])
    state.research_plan = results or []  # type: ignore
    return state


async def tavily_search(state: ResearchState) -> ResearchState:
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
