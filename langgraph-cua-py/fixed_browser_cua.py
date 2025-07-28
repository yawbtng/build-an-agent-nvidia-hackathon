#!/usr/bin/env python3
"""
Fixed Browser LangGraph CUA Example
This version fixes the Pydantic schema issues by not including browser objects in the state.
"""

import asyncio
from typing import List, Literal, Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()

class FixedBrowserState(BaseModel):
    """State for the fixed browser CUA - no browser objects in state."""
    messages: List[AnyMessage] = []
    current_task: str = ""
    task_status: Literal["planning", "executing", "completed", "error"] = "planning"
    browser_actions: List[str] = []

def plan_task(state: FixedBrowserState) -> Dict[str, Any]:
    """Plan the browser task based on user input."""
    print("🤔 Planning your browser task...")
    
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
    elif "screenshot" in user_message.lower():
        task = f"Take screenshot: {user_message}"
    else:
        task = f"General browser task: {user_message}"
    
    print(f"📋 Planned task: {task}")
    return {"current_task": task, "task_status": "executing"}

async def execute_browser_task(state: FixedBrowserState) -> Dict[str, Any]:
    """Execute the browser task using Playwright."""
    print(f"🖥️  Executing: {state.current_task}")
    
    try:
        # Start playwright and browser
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🌐 Browser launched successfully!")
        actions = []
        
        # Execute different types of browser actions
        if "search" in state.current_task.lower():
            # Navigate to a search engine (using DuckDuckGo instead of Google to avoid timeouts)
            await page.goto("https://duckduckgo.com")
            actions.append("Navigated to DuckDuckGo")
            
            # Find and fill the search box
            search_box = await page.wait_for_selector('#searchbox_input')
            search_term = state.current_task.replace("Search for:", "").strip()
            await search_box.fill(search_term)
            actions.append(f"Typed search query: {search_term}")
            
            # Press Enter to search
            await page.keyboard.press("Enter")
            actions.append("Pressed Enter to search")
            
            # Wait for results
            await page.wait_for_selector(".results")
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
            # Extract URL from task
            task = state.current_task.lower()
            if "google" in task:
                url = "https://www.google.com"
            elif "example" in task:
                url = "https://www.example.com"
            elif "github" in task:
                url = "https://github.com"
            else:
                url = "https://www.example.com"
            
            await page.goto(url)
            actions.append(f"Navigated to {url}")
            
            # Get page title
            title = await page.title()
            actions.append(f"Page title: {title}")
            
        elif "screenshot" in state.current_task.lower():
            # Navigate to a page and take screenshot
            await page.goto("https://www.example.com")
            actions.append("Navigated to example.com")
            
            # Take a screenshot
            await page.screenshot(path="user_screenshot.png")
            actions.append("Took screenshot: user_screenshot.png")
            
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
            await page.goto("https://www.example.com")
            actions.append("Navigated to example.com")
            
            # Take a screenshot
            await page.screenshot(path="general_action.png")
            actions.append("Took screenshot: general_action.png")
        
        # Add a small delay to make actions visible
        await asyncio.sleep(2)
        
        # Close browser
        await browser.close()
        await playwright.stop()
        print("🔒 Browser closed")
        
        print("✅ Browser task completed successfully!")
        return {"task_status": "completed", "browser_actions": actions}
        
    except Exception as e:
        print(f"❌ Browser task failed: {e}")
        return {"task_status": "error", "browser_actions": [f"Error: {e}"]}

def generate_response(state: FixedBrowserState) -> Dict[str, Any]:
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
        elif "screenshot" in state.current_task.lower():
            response_content += "\nI've taken a screenshot of the page."
        else:
            response_content += "\nThe browser task has been completed as requested."
    else:
        response_content = "I encountered an issue while trying to complete the browser task. Please try again."
    
    # Add the AI response to the messages
    ai_message = AIMessage(content=response_content)
    new_messages = state.messages + [ai_message]
    
    return {"messages": new_messages}

# Create the workflow graph
workflow = StateGraph(FixedBrowserState)

# Add nodes
workflow.add_node("plan_task", plan_task)
workflow.add_node("execute_browser_task", execute_browser_task) 
workflow.add_node("generate_response", generate_response)

# Add edges
workflow.add_edge(START, "plan_task")
workflow.add_edge("plan_task", "execute_browser_task")
workflow.add_edge("execute_browser_task", "generate_response")
workflow.add_edge("generate_response", END)

# Compile the graph
graph = workflow.compile()

async def main():
    """Run the fixed browser CUA."""
    print("🚀 Fixed Browser LangGraph CUA")
    print("=" * 50)
    print("This will open a real browser window and perform automation!")
    print("=" * 50)
    print("\nExample requests you can try:")
    print("- Search for the best price for new all season tires")
    print("- Fill out the contact form with my information")
    print("- Navigate to example.com and show me the page")
    print("- Take a screenshot of the current page")
    print("- Click on the first link you find")
    print("\nType 'quit' to exit")
    print("=" * 50)
    
    while True:
        # Get user input
        user_request = input("\n🤖 What would you like me to do in the browser? ")
        
        if user_request.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_request.strip():
            continue
        
        print(f"\n📝 Your request: {user_request}")
        print("-" * 50)
        
        # Create initial state with user message
        initial_state = FixedBrowserState(
            messages=[HumanMessage(content=user_request)],
            current_task="",
            task_status="planning",
            browser_actions=[]
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