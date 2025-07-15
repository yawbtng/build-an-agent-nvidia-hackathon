# Structured Report Generation
# This script is converted from a Jupyter notebook. All markdown cells are included as comments for context.
# To run, ensure you have all dependencies installed (see requirements.txt).

# --- Prerequisites ---
# Install dependencies: langgraph, langchain_community, langchain_core, tavily-python, langchain_nvidia_ai_endpoints

# --- API Key Setup ---
# The script expects NVIDIA_API_KEY, LANGCHAIN_API_KEY, and TAVILY_API_KEY as environment variables.

import os
import getpass
import asyncio
from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# Utility: Set environment variable if not already set
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

if not os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    nvapi_key = getpass.getpass("Enter your NVIDIA API key: ")
    assert nvapi_key.startswith("nvapi-"), f"{nvapi_key[:5]}... is not a valid key"
    os.environ["NVIDIA_API_KEY"] = nvapi_key

_set_env("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "report-mAIstro"
_set_env("TAVILY_API_KEY")

# --- Tavily Client Setup ---
from tavily import TavilyClient, AsyncTavilyClient
tavily_client = TavilyClient()
tavily_async_client = AsyncTavilyClient()

# --- NVIDIA LLM Setup ---
from langchain_nvidia_ai_endpoints import ChatNVIDIA
llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)

# --- Utility Classes and Functions ---
class Section(BaseModel):
    name: str = Field(description="Name for this section of the report.")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    research: bool = Field(description="Whether to perform web research for this section of the report.")
    content: str = Field(description="The content of the section.")

from agents import (
    generate_report_plan,
    generate_section_queries,
    write_research_section,
    write_final_section,
)
from tools import format_sections

async def main():
    report_structure = """This report type focuses on a simple summary.\n\nThe report structure should include:\n1. Introduction (no research needed)\n   - Brief overview of the topic area\n\n2. Main Body Section:\n   - Summarize the main features\n\n3. Conclusion (no research needed)\n   - Final thoughts\n"""
    report_topic = "Summarize the main features of Python."
    tavily_topic = "general"
    tavily_days = None
    number_of_queries = 1
    print("Generating report plan...")
    sections_dict = await generate_report_plan({
        "topic": report_topic,
        "report_structure": report_structure,
        "number_of_queries": number_of_queries,
        "tavily_topic": tavily_topic,
        "tavily_days": tavily_days
    })
    sections = sections_dict['sections']
    print("\nSections generated:")
    for section in sections:
        print(f"{'='*50}")
        print(f"Name: {section.name}")
        print(f"Description: {section.description}")
        print(f"Research: {section.research}")

    # --- Full Report Generation ---
    completed_sections = []
    # 1. Write research sections
    for section in sections:
        if section.research:
            print(f"\nResearching and writing section: {section.name}")
            queries = generate_section_queries(section, number_of_queries)
            import asyncio
            search_docs = await agents.tavily_search_async(queries, tavily_topic, tavily_days)
            from tools import deduplicate_and_format_sources
            sources_str = deduplicate_and_format_sources(search_docs, max_tokens_per_source=2000, include_raw_content=True)
            section.content = write_research_section(section, sources_str)
            completed_sections.append(section)
    # 2. Format completed research sections for context
    completed_report_sections = format_sections(completed_sections)
    # 3. Write non-research sections (intro/conclusion)
    for section in sections:
        if not section.research:
            print(f"\nSynthesizing section: {section.name}")
            section.content = write_final_section(section, completed_report_sections)
            completed_sections.append(section)
    # 4. Compile and print the final report
    # Sort sections to original order
    name_to_section = {s.name: s for s in completed_sections}
    ordered_sections = [name_to_section[s.name] for s in sections]
    print("\n================ FINAL REPORT ================\n")
    for section in ordered_sections:
        print(section.content)
        print("\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 