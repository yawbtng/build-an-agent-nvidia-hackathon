from typing import List, Optional, Literal, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from tools import llm, deduplicate_and_format_sources, format_sections, tavily_search_async
from prompts import (
    report_planner_query_writer_instructions,
    report_planner_instructions,
    query_writer_instructions,
    section_writer_instructions,
    final_section_writer_instructions,
)

class Section(BaseModel):
    name: str = Field(description="Name for this section of the report.")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    research: bool = Field(description="Whether to perform web research for this section of the report.")
    content: str = Field(description="The content of the section.")

class Sections(BaseModel):
    sections: List[Section] = Field(description="Sections of the report.")
class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query for web search.")
class Queries(BaseModel):
    queries: List[SearchQuery] = Field(description="List of search queries.")

class ReportState(TypedDict):
    topic: str
    tavily_topic: Literal["general", "news"]
    tavily_days: Optional[int]
    report_structure: str
    number_of_queries: int
    sections: list[Section]
    completed_sections: Annotated[list, ...]
    report_sections_from_research: str
    final_report: str

def invoke_structured_llm_with_retry(structured_llm, queries, max_attempts=3):
    for _ in range(max_attempts):
        results = structured_llm.invoke(queries)
        if results:
            return results
    return results

async def generate_report_plan(state: ReportState):
    topic = state["topic"]
    report_structure = state["report_structure"]
    number_of_queries = state["number_of_queries"]
    tavily_topic = state["tavily_topic"]
    tavily_days = state.get("tavily_days", None)
    if isinstance(report_structure, dict):
        report_structure = str(report_structure)
    structured_llm = llm.with_structured_output(Queries)
    system_instructions_query = report_planner_query_writer_instructions.format(topic=topic, report_organization=report_structure, number_of_queries=number_of_queries)
    results = invoke_structured_llm_with_retry(structured_llm,
                                              [SystemMessage(content=system_instructions_query)]+[HumanMessage(content="Generate search queries that will help with planning the sections of the report.")])
    query_list = [query.search_query for query in results.queries]
    search_docs = await tavily_search_async(query_list, tavily_topic, tavily_days)
    source_str = deduplicate_and_format_sources(search_docs, max_tokens_per_source=1000, include_raw_content=True)
    system_instructions_sections = report_planner_instructions.format(topic=topic, report_organization=report_structure, context=source_str)
    structured_llm = llm.with_structured_output(Sections)
    report_sections = invoke_structured_llm_with_retry(structured_llm,
                                                      [SystemMessage(content=system_instructions_sections)]+[HumanMessage(content="Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. Each section must have: name, description, plan, research, and content fields.")])
    return {"sections": report_sections.sections}

def generate_section_queries(section, number_of_queries):
    structured_llm = llm.with_structured_output(Queries)
    system_instructions = query_writer_instructions.format(section_topic=section.description, number_of_queries=number_of_queries)
    queries = invoke_structured_llm_with_retry(structured_llm,
                                              [SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate search queries on the provided topic.")])
    return [q.search_query for q in queries.queries]

def write_research_section(section, sources_str):
    system_instructions = section_writer_instructions.format(section_title=section.name, section_topic=section.description, context=sources_str)
    section_content = llm.invoke([SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate a report section based on the provided sources.")])
    return section_content.content

def write_final_section(section, completed_report_sections):
    system_instructions = final_section_writer_instructions.format(section_title=section.name, section_topic=section.description, context=completed_report_sections)
    section_content = llm.invoke([SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate a report section based on the provided sources.")])
    return section_content.content 