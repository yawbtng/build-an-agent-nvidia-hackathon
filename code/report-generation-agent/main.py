#!/usr/bin/env python3
"""
Structured Report Generation

This script generates structured reports using LangChain, NVIDIA AI, and Tavily search.
Converted from a Jupyter notebook with all markdown cells included as comments for context.

Prerequisites:
- Install dependencies: langgraph, langchain_community, langchain_core, tavily-python, langchain_nvidia_ai_endpoints
- Set environment variables: NVIDIA_API_KEY, LANGCHAIN_API_KEY, TAVILY_API_KEY
"""

import asyncio
from typing import List, Optional, Literal, Dict, Any, cast

# Setup environment and initialize tools
from tools import setup_environment, format_sections, tavily_search_async, deduplicate_and_format_sources
from agents import (
    generate_report_plan,
    generate_section_queries,
    write_research_section,
    write_final_section,
    Section,
    ReportState,
)


async def generate_full_report(
    report_topic: str,
    report_structure: str,
    tavily_topic: Literal["general", "news"] = "general",
    tavily_days: Optional[int] = None,
    number_of_queries: int = 1
) -> List[Section]:
    """
    Generate a complete report with all sections.

    Args:
        report_topic: The main topic for the report
        report_structure: Structure guidelines for the report
        tavily_topic: Type of search ("general" or "news")
        tavily_days: Number of days for news search
        number_of_queries: Number of search queries per section

    Returns:
        List of completed Section objects
    """
    print("Generating report plan...")

    # Generate report plan and sections
    # Note: We need to create a properly typed ReportState but some fields are not available yet
    report_state: Dict[str, Any] = {
        "topic": report_topic,
        "report_structure": report_structure,
        "number_of_queries": number_of_queries,
        "tavily_topic": tavily_topic,
        "tavily_days": tavily_days,
        "sections": [],  # Will be populated
        "completed_sections": [],  # Will be populated
        "report_sections_from_research": "",  # Will be populated
        "final_report": "",  # Will be populated
    }

    sections_dict: Dict[str, List[Section]] = await generate_report_plan(cast(ReportState, report_state))

    sections: List[Section] = sections_dict['sections']
    print(f"\nGenerated {len(sections)} sections:")
    for section in sections:
        print(f"{'='*50}")
        print(f"Name: {section.name}")
        print(f"Description: {section.description}")
        print(f"Research: {section.research}")

    completed_sections: List[Section] = []

    # 1. Write research sections first
    print("\n" + "="*60)
    print("WRITING RESEARCH SECTIONS")
    print("="*60)

    for section in sections:
        if section.research:
            print(f"\nResearching and writing section: {section.name}")

            # Generate search queries for this section
            queries: List[str] = generate_section_queries(section, number_of_queries)
            print(f"Generated queries: {queries}")

            # Perform web search
            search_docs: List[Dict[str, Any]] = await tavily_search_async(queries, tavily_topic, tavily_days)

            # Format sources
            sources_str: str = deduplicate_and_format_sources(
                search_docs,
                max_tokens_per_source=2000,
                include_raw_content=True
            )

            # Write section content
            section.content = write_research_section(section, sources_str)
            completed_sections.append(section)

    # 2. Format completed research sections for context
    completed_report_sections: str = format_sections(completed_sections)

    # 3. Write non-research sections (intro/conclusion)
    print("\n" + "="*60)
    print("WRITING SYNTHESIS SECTIONS")
    print("="*60)

    for section in sections:
        if not section.research:
            print(f"\nSynthesizing section: {section.name}")
            section.content = write_final_section(section, completed_report_sections)
            completed_sections.append(section)

    # 4. Sort sections back to original order
    name_to_section: Dict[str, Section] = {s.name: s for s in completed_sections}
    ordered_sections: List[Section] = [name_to_section[s.name] for s in sections]

    return ordered_sections


def print_final_report(sections: List[Section]) -> None:
    """Print the final report in a formatted way."""
    print("\n" + "="*80)
    print("FINAL REPORT")
    print("="*80)

    for section in sections:
        print(section.content)
        print("\n")


async def main() -> None:
    """Main function to run the report generation."""
    # Setup environment
    setup_environment()

    # Report configuration
    report_structure: str = """This report type focuses on a simple summary.

The report structure should include:
1. Introduction (no research needed)
   - Brief overview of the topic area

2. Main Body Section:
   - Summarize the main features

3. Conclusion (no research needed)
   - Final thoughts
"""

    report_topic: str = "Summarize the main features of Python."
    tavily_topic: Literal["general", "news"] = "general"
    tavily_days: Optional[int] = None
    number_of_queries: int = 1

    try:
        # Generate the full report
        sections: List[Section] = await generate_full_report(
            report_topic=report_topic,
            report_structure=report_structure,
            tavily_topic=tavily_topic,
            tavily_days=tavily_days,
            number_of_queries=number_of_queries
        )

        # Print the final report
        print_final_report(sections)

    except Exception as e:
        print(f"Error generating report: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())