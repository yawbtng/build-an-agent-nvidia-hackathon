import asyncio
import logging

from .graph import report_graph
from .models import ReportState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the initial state for the report
state = ReportState(
    topic="Give an overview of capabilities and specific use case examples for these processing units: CPU, GPU.",
    report_structure="""This report type focuses on comparative analysis.

The report structure should include:
1. Introduction (no research needed)
- Brief overview of the topic area
- Context for the comparison

2. Main Body Sections:
- One dedicated section for EACH offering being compared in the user-provided list
- Each section should examine:
    - Core Features (bulleted list)
    - Architecture & Implementation (2-3 sentences)
    - One example use case (2-3 sentences)

3. No Main Body Sections other than the ones dedicated to each offering in the user-provided list

4. Conclusion with Comparison Table (no research needed)
- Structured comparison table that:
    * Compares all offerings from the user-provided list across key dimensions
    * Highlights relative strengths and weaknesses
- Final recommendations""",
)

# Run the report graph asynchronously
result_state = asyncio.run(report_graph.ainvoke(state))

# Print the formatted sections of the report
print(result_state["sections"])
