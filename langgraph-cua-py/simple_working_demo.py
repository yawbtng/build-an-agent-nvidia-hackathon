#!/usr/bin/env python3
"""
Simple Working Browser Demo
This script demonstrates browser automation with reliable actions.
"""

import asyncio
from playwright.async_api import async_playwright

async def simple_working_demo():
    """Simple, reliable browser automation demo."""
    print("🚀 Simple Working Browser Demo")
    print("=" * 50)
    print("Opening browser and performing reliable automation...")
    
    async with async_playwright() as p:
        # Launch browser (visible)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🌐 Browser launched!")
        
        # Navigate to a simple, reliable page
        await page.goto("https://www.example.com")
        print("📱 Navigated to example.com")
        
        # Wait for page to load
        await asyncio.sleep(2)
        
        # Get page title
        title = await page.title()
        print(f"📄 Page title: {title}")
        
        # Take a screenshot
        await page.screenshot(path="example_page.png")
        print("📸 Took screenshot: example_page.png")
        
        # Navigate to another page
        await page.goto("https://httpbin.org/forms/post")
        print("📱 Navigated to test form")
        
        # Wait for page to load
        await asyncio.sleep(2)
        
        # Fill in some simple form fields
        await page.fill('input[name="custname"]', "John Doe")
        print("✍️  Filled name field")
        
        await page.fill('input[name="custtel"]', "555-123-4567")
        print("📞 Filled phone field")
        
        await page.fill('input[name="custemail"]', "john@example.com")
        print("📧 Filled email field")
        
        # Wait a moment to see the filled form
        await asyncio.sleep(3)
        
        # Take another screenshot
        await page.screenshot(path="filled_form.png")
        print("📸 Took screenshot: filled_form.png")
        
        # Navigate to a search engine
        await page.goto("https://duckduckgo.com")
        print("🔍 Navigated to DuckDuckGo")
        
        # Wait for page to load
        await asyncio.sleep(2)
        
        # Fill search box
        search_box = await page.wait_for_selector('#searchbox_input')
        await search_box.fill("LangGraph Computer Use Agent")
        print("✍️  Typed search query")
        
        # Press Enter to search
        await page.keyboard.press("Enter")
        print("🔍 Pressed Enter to search")
        
        # Wait for results
        await page.wait_for_selector(".results")
        print("✅ Search results loaded!")
        
        # Wait a moment to see results
        await asyncio.sleep(3)
        
        # Take final screenshot
        await page.screenshot(path="search_results.png")
        print("📸 Took screenshot: search_results.png")
        
        # Close browser
        await browser.close()
        print("🔒 Browser closed")
        
        print("\n🎉 Demo completed! Check the screenshot files:")
        print("- example_page.png")
        print("- filled_form.png") 
        print("- search_results.png")

if __name__ == "__main__":
    asyncio.run(simple_working_demo()) 