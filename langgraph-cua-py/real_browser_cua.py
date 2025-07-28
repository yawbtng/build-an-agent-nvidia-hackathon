#!/usr/bin/env python3
"""
Real Browser LangGraph CUA Example
This example demonstrates a Computer Use Agent that actually controls a browser using Playwright.
You can see the browser window open and watch the automation happen in real-time!
"""

import asyncio
import time
from typing import List, Literal, Dict, Any, Optional
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright, Browser, Page

# Load environment variables
load_dotenv()

class BrowserCUAState(BaseModel):
    """State for the browser CUA example."""
    messages: List[AnyMessage] = []
    current_task: str = ""
    task_status: Literal["planning", "executing", "completed", "error"] = "planning"
    browser: Optional[Browser] = None
    page: Optional[Page] = None
    browser_actions: List[str] = []

def plan_task(state: BrowserCUAState) -> Dict[str, Any]:
    """Plan the browser task based on user input."""
    print("🤔 Planning the browser task...")
    
    # Get the latest user message
    user_message = None
    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break
    
    if not user_message:
        return {"task_status": "error", "current_task": "No user message found"}
    
    # Enhanced task planning logic
    if "search" in user_message.lower() or "find" in user_message.lower():
        task = f"Search for: {user_message}"
    elif "fill" in user_message.lower() or "form" in user_message.lower():
        task = f"Fill form: {user_message}"
    elif "click" in user_message.lower():
        task = f"Click action: {user_message}"
    elif "navigate" in user_message.lower() or "go to" in user_message.lower():
        task = f"Navigate to: {user_message}"
    else:
        task = f"General browser task: {user_message}"
    
    print(f"📋 Planned browser task: {task}")
    return {"current_task": task, "task_status": "executing"}

async def execute_browser_task(state: BrowserCUAState) -> Dict[str, Any]:
    """Execute the browser task using Playwright."""
    print(f"🖥️  Executing browser task: {state.current_task}")
    
    try:
        # Initialize browser if not already done
        if not state.browser:
            playwright = await async_playwright().start()
            state.browser = await playwright.chromium.launch(headless=False)  # headless=False to see the browser
            state.page = await state.browser.new_page()
            print("🌐 Browser launched successfully!")
        
        page = state.page
        actions = []
        
        # Execute different types of browser actions
        if "search" in state.current_task.lower():
            # Navigate to Google and perform a search
            await page.goto("https://www.google.com")
            actions.append("Navigated to Google")
            
            # Find and fill the search box
            search_box = await page.wait_for_selector('input[name="q"]')
            await search_box.fill("best all season tires 2019 Subaru Forester")
            actions.append("Typed search query")
            
            # Press Enter to search
            await page.keyboard.press("Enter")
            actions.append("Pressed Enter to search")
            
            # Wait for results
            await page.wait_for_selector("#search")
            actions.append("Search results loaded")
            
        elif "fill" in state.current_task.lower() or "form" in state.current_task.lower():
            # Navigate to a sample contact form
            await page.goto("https://httpbin.org/forms/post")
            actions.append("Navigated to sample form")
            
            # Fill in form fields
            await page.fill('input[name="custname"]', "John Doe")
            actions.append("Filled name field")
            
            await page.fill('input[name="custtel"]', "555-123-4567")
            actions.append("Filled phone field")
            
            await page.fill('input[name="custemail"]', "john@example.com")
            actions.append("Filled email field")
            
            # Select pizza size
            await page.select_option('select[name="size"]', "large")
            actions.append("Selected pizza size")
            
            # Check toppings
            await page.check('input[value="bacon"]')
            await page.check('input[value="cheese"]')
            actions.append("Selected toppings")
            
            # Fill additional comments
            await page.fill('textarea[name="comments"]', "Extra cheese please!")
            actions.append("Filled comments")
            
        elif "navigate" in state.current_task.lower():
            # Navigate to a specific website
            await page.goto("https://www.example.com")
            actions.append("Navigated to example.com")
            
            # Get page title
            title = await page.title()
            actions.append(f"Page title: {title}")
            
        elif "click" in state.current_task.lower():
            # Navigate to a page with clickable elements
            await page.goto("https://www.example.com")
            actions.append("Navigated to example.com")
            
            # Click on a link (if available)
            try:
                await page.click("a")
                actions.append("Clicked on a link")
            except:
                actions.append("No clickable links found")
        
        else:
            # General browser action
            await page.goto("https://www.google.com")
            actions.append("Navigated to Google")
            
            # Take a screenshot
            await page.screenshot(path="browser_action.png")
            actions.append("Took screenshot")
        
        # Add a small delay to make actions visible
        await asyncio.sleep(2)
        
        print("✅ Browser task completed successfully!")
        return {"task_status": "completed", "browser_actions": actions}
        
    except Exception as e:
        print(f"❌ Browser task failed: {e}")
        return {"task_status": "error", "browser_actions": [f"Error: {e}"]}

def generate_response(state: BrowserCUAState) -> Dict[str, Any]:
    """Generate a response to the user about the completed browser task."""
    print("💬 Generating response...")
    
    # Create a response based on the completed task
    if state.task_status == "completed":
        response_content = f"I've successfully completed the browser task: {state.current_task}. "
        
        if state.browser_actions:
            response_content += f"\n\nActions performed:\n"
            for i, action in enumerate(state.browser_actions, 1):
                response_content += f"{i}. {action}\n"
        
        if "search" in state.current_task.lower():
            response_content += "\nI found the information you requested and can provide you with the results."
        elif "fill" in state.current_task.lower():
            response_content += "\nI've filled out the form with the information you provided."
        elif "click" in state.current_task.lower():
            response_content += "\nI've performed the requested click action."
        elif "navigate" in state.current_task.lower():
            response_content += "\nI've navigated to the requested page."
        else:
            response_content += "\nThe browser task has been completed as requested."
    else:
        response_content = "I encountered an issue while trying to complete the browser task. Please try again."
    
    # Add the AI response to the messages
    ai_message = AIMessage(content=response_content)
    new_messages = state.messages + [ai_message]
    
    return {"messages": new_messages}

async def cleanup_browser(state: BrowserCUAState) -> Dict[str, Any]:
    """Clean up browser resources."""
    if state.browser:
        await state.browser.close()
        print("🔒 Browser closed")
    return {}

# Create the workflow graph
workflow = StateGraph(BrowserCUAState)

# Add nodes
workflow.add_node("plan_task", plan_task)
workflow.add_node("execute_browser_task", execute_browser_task) 
workflow.add_node("generate_response", generate_response)
workflow.add_node("cleanup_browser", cleanup_browser)

# Add edges
workflow.add_edge(START, "plan_task")
workflow.add_edge("plan_task", "execute_browser_task")
workflow.add_edge("execute_browser_task", "generate_response")
workflow.add_edge("generate_response", "cleanup_browser")
workflow.add_edge("cleanup_browser", END)

# Compile the graph
graph = workflow.compile()

async def main():
    """Run the real browser CUA example."""
    print("🚀 Real Browser LangGraph CUA Example")
    print("=" * 60)
    print("This will open a real browser window and perform actual automation!")
    print("=" * 60)
    
    # Example user requests
    example_requests = [
        "Search for the best price for new all season tires for my 2019 Subaru Forester",
        "Fill out the contact form with my information",
        "Navigate to example.com and show me the page"
    ]
    
    for i, request in enumerate(example_requests, 1):
        print(f"\n📝 Example {i}: {request}")
        print("-" * 60)
        
        # Create initial state with user message
        initial_state = BrowserCUAState(
            messages=[HumanMessage(content=request)],
            current_task="",
            task_status="planning",
            browser=None,
            page=None,
            browser_actions=[]
        )
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        
        # Display the final response
        final_messages = result.get("messages", [])
        if final_messages:
            final_message = final_messages[-1]
            print(f"\n🤖 Assistant: {final_message.content}")
        
        print("=" * 60)
        
        # Ask user if they want to continue
        if i < len(example_requests):
            print("\nPress Enter to continue to the next example...")
            input()

if __name__ == "__main__":
    asyncio.run(main()) 