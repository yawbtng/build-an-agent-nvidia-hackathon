from typing import List, Optional, Literal, Annotated, Dict, Any, Union, TypeVar
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from tools import llm, deduplicate_and_format_sources, format_sections, tavily_search_async
from prompts import (
    report_planner_query_writer_instructions,
    report_planner_instructions,
    query_writer_instructions,
    section_writer_instructions,
    final_section_writer_instructions,
)

# Type variable for structured LLM results
T = TypeVar('T', bound=BaseModel)


class Section(BaseModel):
    name: str = Field(description="Name for this section of the report.")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    research: bool = Field(description="Whether to perform web research for this section of the report.")
    content: str = Field(default="", description="The content of the section.")


class Sections(BaseModel):
    sections: List[Section] = Field(description="Sections of the report.")


class SearchQuery(BaseModel):
    search_query: str = Field(description="Query for web search.")


class Queries(BaseModel):
    queries: List[SearchQuery] = Field(description="List of search queries.")


class ReportState(TypedDict):
    topic: str
    tavily_topic: Literal["general", "news"]
    tavily_days: Optional[int]
    report_structure: str
    number_of_queries: int
    sections: List[Section]
    completed_sections: Annotated[List[Section], ...]
    report_sections_from_research: str
    final_report: str


def invoke_structured_llm_with_retry(
    structured_llm: Any,
    messages: List[Union[HumanMessage, SystemMessage]],
    max_attempts: int = 3
) -> Optional[BaseModel]:
    """
    Invoke structured LLM with retry logic.

    Args:
        structured_llm: The structured LLM instance
        messages: Messages to send to the LLM
        max_attempts: Maximum number of retry attempts

    Returns:
        LLM response or None if all attempts fail
    """
    last_error: Optional[Exception] = None

    for attempt in range(max_attempts):
        try:
            results = structured_llm.invoke(messages)
            if results:
                return results
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")

    print(f"All {max_attempts} attempts failed. Last error: {last_error}")
    return None


async def generate_report_plan(state: ReportState) -> Dict[str, List[Section]]:
    """
    Generate a report plan including sections based on the topic and structure.

    Args:
        state: ReportState containing topic, structure, and other parameters

    Returns:
        Dictionary containing the generated sections
    """
    topic: str = state["topic"]
    report_structure: str = state["report_structure"]
    number_of_queries: int = state["number_of_queries"]
    tavily_topic: Literal["general", "news"] = state["tavily_topic"]
    tavily_days: Optional[int] = state.get("tavily_days", None)

    # Ensure report_structure is a string
    if isinstance(report_structure, dict):
        report_structure = str(report_structure)

    # Generate search queries for planning
    structured_llm = llm.with_structured_output(Queries)
    system_instructions_query: str = report_planner_query_writer_instructions.format(
        topic=topic,
        report_organization=report_structure,
        number_of_queries=number_of_queries
    )

    query_messages: List[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=system_instructions_query),
        HumanMessage(content="Generate search queries that will help with planning the sections of the report.")
    ]

    query_results = invoke_structured_llm_with_retry(structured_llm, query_messages)
    if not query_results or not isinstance(query_results, Queries):
        raise ValueError("Failed to generate search queries after multiple attempts")

    query_list: List[str] = [query.search_query for query in query_results.queries]

    # Perform web search
    try:
        search_docs = await tavily_search_async(query_list, tavily_topic, tavily_days)
        source_str: str = deduplicate_and_format_sources(
            search_docs,
            max_tokens_per_source=1000,
            include_raw_content=True
        )
    except Exception as e:
        print(f"Error during web search: {e}")
        source_str = "No search results available due to error."

    # Generate report sections
    system_instructions_sections: str = report_planner_instructions.format(
        topic=topic,
        report_organization=report_structure,
        context=source_str
    )

    structured_llm = llm.with_structured_output(Sections)
    section_messages: List[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=system_instructions_sections),
        HumanMessage(content="Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. Each section must have: name, description, research, and content fields.")
    ]

    report_sections = invoke_structured_llm_with_retry(structured_llm, section_messages)
    if not report_sections or not isinstance(report_sections, Sections):
        raise ValueError("Failed to generate report sections after multiple attempts")

    return {"sections": report_sections.sections}


def generate_section_queries(section: Section, number_of_queries: int) -> List[str]:
    """
    Generate search queries for a specific section.

    Args:
        section: Section object containing description
        number_of_queries: Number of queries to generate

    Returns:
        List of search query strings
    """
    structured_llm = llm.with_structured_output(Queries)
    system_instructions: str = query_writer_instructions.format(
        section_topic=section.description,
        number_of_queries=number_of_queries
    )

    messages: List[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=system_instructions),
        HumanMessage(content="Generate search queries on the provided topic.")
    ]

    queries = invoke_structured_llm_with_retry(structured_llm, messages)
    if not queries or not isinstance(queries, Queries):
        print(f"Failed to generate queries for section: {section.name}")
        return [section.description]  # Fallback to section description as query

    return [q.search_query for q in queries.queries]


def write_research_section(section: Section, sources_str: str) -> str:
    """
    Write a research-based section using provided sources.

    Args:
        section: Section object with name and description
        sources_str: Formatted string of source materials

    Returns:
        Generated section content
    """
    system_instructions: str = section_writer_instructions.format(
        section_title=section.name,
        section_topic=section.description,
        context=sources_str
    )

    messages: List[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=system_instructions),
        HumanMessage(content="Generate a report section based on the provided sources.")
    ]

    try:
        section_content: BaseMessage = llm.invoke(messages)
        # Ensure we return a string
        if isinstance(section_content.content, str):
            return section_content.content
        elif isinstance(section_content.content, list):
            # Handle list content by joining text parts
            text_parts = [part for part in section_content.content if isinstance(part, str)]
            return " ".join(text_parts) if text_parts else f"Error: Could not extract text content for section: {section.name}"
        else:
            return f"Error: Unexpected content type for section: {section.name}"
    except Exception as e:
        print(f"Error writing research section '{section.name}': {e}")
        return f"Error generating content for section: {section.name}"


def write_final_section(section: Section, completed_report_sections: str) -> str:
    """
    Write a final section (introduction/conclusion) based on completed sections.

    Args:
        section: Section object with name and description
        completed_report_sections: Formatted string of completed sections

    Returns:
        Generated section content
    """
    system_instructions: str = final_section_writer_instructions.format(
        section_title=section.name,
        section_topic=section.description,
        context=completed_report_sections
    )

    messages: List[Union[HumanMessage, SystemMessage]] = [
        SystemMessage(content=system_instructions),
        HumanMessage(content="Generate a report section based on the provided sources.")
    ]

    try:
        section_content: BaseMessage = llm.invoke(messages)
        # Ensure we return a string
        if isinstance(section_content.content, str):
            return section_content.content
        elif isinstance(section_content.content, list):
            # Handle list content by joining text parts
            text_parts = [part for part in section_content.content if isinstance(part, str)]
            return " ".join(text_parts) if text_parts else f"Error: Could not extract text content for section: {section.name}"
        else:
            return f"Error: Unexpected content type for section: {section.name}"
    except Exception as e:
        print(f"Error writing final section '{section.name}': {e}")
        return f"Error generating content for section: {section.name}"