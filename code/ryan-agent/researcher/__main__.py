"""
Test the research agent.
"""

import asyncio
import logging

from researcher.graph import research_graph
from researcher.models import ResearchState

_LOGGER = logging.getLogger(__name__)


def test():
    """Test the research agent."""
    state = ResearchState(
        topic="Give an overview of capabilities and specific use case examples for these processing units: CPU, GPU.",
        mode="detail",
        number_of_queries=5,
    )
    return asyncio.run(research_graph.ainvoke(state))


logging.basicConfig(level=logging.DEBUG)
_LOGGER.setLevel(logging.DEBUG)
_ = test()
