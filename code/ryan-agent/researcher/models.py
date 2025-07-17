"""
State for the research agent.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Queries(BaseModel):
    """A single step in the research plan."""

    queries: List[str] = Field(
        description="List of search queries.",
    )


class BaseResearchState(BaseModel):
    """Base state for the research agent."""

    # Inputs
    topic: str = Field(description="Topic of the research plan.")
    mode: Literal["discovery", "detail"] = Field(
        description="Mode of the research plan.", default="discovery"
    )

    # Research Configuration
    tavily_topic: Literal["news", "general"] = Field(
        description="Tavily search topic", default="general"
    )
    tavily_days: int = Field(description="Only applicable for news topic", default=30)
    number_of_queries: int = Field(
        description="Number of search queries to generate per section", default=5
    )


class ResearchState(BaseResearchState):
    """State for the research agent."""

    # Research State
    research_plan: Optional[Queries] = Field(
        default=None, description="List of search queries."
    )
    research_results: Optional[str] = Field(
        default=None, description="Results from the research."
    )
