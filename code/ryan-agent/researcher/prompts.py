"""
Nodes for the report generation agent.
"""

from typing import Final

# fmt: off
# This prompt is used to generate the initial discovery research plane
query_writer_instructions_discovery: Final[str] = """
You are an expert technical writer, helping to plan a report.

The report will be focused on the following topic:
{topic}

Your goal is to generate {number_of_queries} search queries that will help gather comprehensive
information for planning the report sections.

The query should:
1. Be related to the topic
2. Help satisfy the requirements specified in the report organization

Make the query specific enough to find high-quality, relevant sources while covering the breadth
needed for the report structure.
"""

# This prompt is used to generate the detailed research plan on a specific topic
query_writer_instructions_detail: Final[str] = """
Your goal is to generate targeted web search queries that will gather comprehensive
information for writing a technical report section.

Topic for this section:
{topic}

When generating {number_of_queries} search queries, ensure they:
1. Cover different aspects of the topic (e.g., core features, real-world applications, technical architecture)
2. Include specific technical terms related to the topic
3. Target recent information by including year markers where relevant (e.g., "2024")
4. Look for comparisons or differentiators from similar technologies/approaches
5. Search for both official documentation and practical implementation examples

Your queries should be:
- Specific enough to avoid generic results
- Technical enough to capture detailed implementation information
- Diverse enough to cover all aspects of the section plan
- Focused on authoritative sources (documentation, technical blogs, academic papers)"""
# fmt: on
