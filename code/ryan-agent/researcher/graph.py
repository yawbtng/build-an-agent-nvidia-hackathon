"""
Graph for the research agent.
"""

from langgraph.graph import END, START, StateGraph

from .models import ResearchState
from .nodes import create_research_plan, tavily_search

_builder = StateGraph(ResearchState)

_builder.add_node("create_research_plan", create_research_plan)
_builder.add_node("tavily_search", tavily_search)

_builder.add_edge(START, "create_research_plan")
_builder.add_edge("create_research_plan", "tavily_search")
_builder.add_edge("tavily_search", END)

research_graph = _builder.compile()
