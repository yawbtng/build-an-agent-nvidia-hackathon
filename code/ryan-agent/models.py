"""
Models for the report agent.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from .researcher.models import ResearchState


class Section(BaseModel):
    """A section of the report."""

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
    """Collection of sections of the report."""

    sections: List[Section] = Field(
        description="Sections of the report.",
    )


class ReportState(ResearchState):
    """State for the report agent."""

    # User input
    report_structure: str = Field(
        description="A description of how the report should be formatted."
    )

    # Report
    discovery_results: Optional[str] = Field(
        default=None, description="Document level research from the research agent."
    )
    sections: list[Section] = Field(description="List of report sections", default=[])
    # completed_sections: Annotated[list, operator.add] # Send() API key
    # report_sections_from_research: str # String of any completed sections from research to write final sections
    # final_report: str # Final report
