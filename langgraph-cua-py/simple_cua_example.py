#!/usr/bin/env python3
"""
Simple LangGraph CUA Example
This example demonstrates the concept of a Computer Use Agent using a standard model.
Note: This is a simplified version that doesn't require the specialized 'computer-use-preview' model.
"""

import asyncio
from typing import List, Literal, Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

class SimpleCUAState(BaseModel):
    """State for the simple CUA example."""
    messages: List[AnyMessage] = []
    current_task: str = ""
    task_status: Literal["planning", "executing", "completed", "error"] = "planning"

def plan_task(state: SimpleCUAState) -> Dict[str, Any]:
    """Plan the computer task based on user input."""
    print("🤔 Planning the task...")
    
    # Get the latest user message
    user_message = None
    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break
    
    if not user_message:
        return {"task_status": "error", "current_task": "No user message found"}
    
    # Simple task planning logic
    if "search" in user_message.lower() or "find" in user_message.lower():
        task = f"Search for: {user_message}"
    elif "fill" in user_message.lower() or "form" in user_message.lower():
        task = f"Fill form: {user_message}"
    elif "click" in user_message.lower():
        task = f"Click action: {user_message}"
    else:
        task = f"General task: {user_message}"
    
    print(f"📋 Planned task: {task}")
    return {"current_task": task, "task_status": "executing"}

def execute_task(state: SimpleCUAState) -> Dict[str, Any]:
    """Simulate executing the computer task."""
    print(f"🖥️  Executing: {state.current_task}")
    
    # Simulate different types of computer actions
    if "search" in state.current_task.lower():
        actions = [
            "Opening web browser",
            "Navigating to search engine",
            "Typing search query",
            "Clicking search button",
            "Reading search results"
        ]
    elif "fill" in state.current_task.lower():
        actions = [
            "Locating form fields",
            "Filling in name field",
            "Filling in email field", 
            "Filling in message field",
            "Clicking submit button"
        ]
    elif "click" in state.current_task.lower():
        actions = [
            "Locating target element",
            "Moving mouse to element",
            "Clicking element",
            "Verifying action completed"
        ]
    else:
        actions = [
            "Analyzing task requirements",
            "Determining best approach",
            "Executing general computer action",
            "Verifying completion"
        ]
    
    # Simulate the actions
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
        # In a real implementation, this would call actual browser automation tools
    
    print("✅ Task completed successfully!")
    return {"task_status": "completed"}

def generate_response(state: SimpleCUAState) -> Dict[str, Any]:
    """Generate a response to the user about the completed task."""
    print("💬 Generating response...")
    
    # Create a response based on the completed task
    if state.task_status == "completed":
        response_content = f"I've successfully completed the task: {state.current_task}. "
        
        if "search" in state.current_task.lower():
            response_content += "I found the information you requested and can provide you with the results."
        elif "fill" in state.current_task.lower():
            response_content += "I've filled out the form with the information you provided."
        elif "click" in state.current_task.lower():
            response_content += "I've performed the requested click action."
        else:
            response_content += "The computer task has been completed as requested."
    else:
        response_content = "I encountered an issue while trying to complete the task. Please try again."
    
    # Add the AI response to the messages
    ai_message = AIMessage(content=response_content)
    new_messages = state.messages + [ai_message]
    
    return {"messages": new_messages}

# Create the workflow graph
workflow = StateGraph(SimpleCUAState)

# Add nodes
workflow.add_node("plan_task", plan_task)
workflow.add_node("execute_task", execute_task) 
workflow.add_node("generate_response", generate_response)

# Add edges
workflow.add_edge(START, "plan_task")
workflow.add_edge("plan_task", "execute_task")
workflow.add_edge("execute_task", "generate_response")
workflow.add_edge("generate_response", END)

# Compile the graph
graph = workflow.compile()

async def main():
    """Run the simple CUA example."""
    print("🚀 Simple LangGraph CUA Example")
    print("=" * 50)
    
    # Example user requests
    example_requests = [
        "Search for the best price for new all season tires for my 2019 Subaru Forester",
        "Fill out the contact form with my name 'John Doe', email 'john@example.com', and message 'Requesting information about your services'",
        "Click the submit button on the current page"
    ]
    
    for i, request in enumerate(example_requests, 1):
        print(f"\n📝 Example {i}: {request}")
        print("-" * 50)
        
        # Create initial state with user message
        initial_state = SimpleCUAState(
            messages=[HumanMessage(content=request)],
            current_task="",
            task_status="planning"
        )
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        
        # Display the final response
        final_messages = result.get("messages", [])
        if final_messages:
            final_message = final_messages[-1]
            print(f"\n🤖 Assistant: {final_message.content}")
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 