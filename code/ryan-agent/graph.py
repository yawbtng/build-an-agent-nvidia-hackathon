"""
Nodes for the report generation agent.
"""

from langgraph.graph import END, START, StateGraph

from .models import ReportState
from .nodes import generate_report_outline, preform_discovery_research

_builder = StateGraph(ReportState)

_builder.add_node("preform_discovery_research", preform_discovery_research)
_builder.add_node("generate_report_outline", generate_report_outline)

_builder.add_edge(START, "preform_discovery_research")
_builder.add_edge("preform_discovery_research", "generate_report_outline")
_builder.add_edge("generate_report_outline", END)

report_graph = _builder.compile()
