import operator
from typing import Annotated, List, Literal, Optional, TypedDict

from pydantic import BaseModel, Field


class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )
    research: bool = Field(
        description="Whether to perform web research for this section of the report."
    )
    content: str = Field(description="The content of the section.")


class Sections(BaseModel):
    sections: List[Section] = Field(
        description="Sections of the report.",
    )


class Queries(BaseModel):
    queries: List[str] = Field(
        description="List of search queries.",
    )


class ReportState(BaseModel):
    # User input
    topic: str = Field(description="Report topic")
    report_structure: str = Field(
        description="A description of how the report should be formatted."
    )

    # Tavily config
    tavily_topic: Literal["general", "news"] = Field(
        description="Tavily search topic", default="general"
    )
    tavily_days: Optional[int] = Field(
        description="Only applicable for news topic", default=None
    )
    number_of_queries: int = Field(
        description="Number of search queries to generate per section", default=5
    )

    # Researcher
    research_plan: Optional[Queries] = Field(
        description="List of search queries for tavily research", default=None
    )
    research_results: Optional[str] = Field(
        description="Results from the research.", default=None
    )

    # Report
    sections: list[Section] = Field(description="List of report sections", default=[])
    # completed_sections: Annotated[list, operator.add] # Send() API key
    # report_sections_from_research: str # String of any completed sections from research to write final sections
    # final_report: str # Final report
