#!/usr/bin/env python3
"""
Working Browser Demo
This script demonstrates browser automation without the Pydantic issues.
"""

import asyncio
from playwright.async_api import async_playwright

async def working_browser_demo():
    """Working browser automation demo."""
    print("🚀 Working Browser Automation Demo")
    print("=" * 50)
    print("Opening browser and performing automation...")
    
    async with async_playwright() as p:
        # Launch browser (visible)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🌐 Browser launched!")
        
        # Navigate to a simple test page first
        await page.goto("https://httpbin.org/forms/post")
        print("📱 Navigated to test form page")
        
        # Wait a moment for page to load
        await asyncio.sleep(2)
        
        # Fill in some form fields
        await page.fill('input[name="custname"]', "John Doe")
        print("✍️  Filled name field")
        
        await page.fill('input[name="custtel"]', "555-123-4567")
        print("📞 Filled phone field")
        
        await page.fill('input[name="custemail"]', "john@example.com")
        print("📧 Filled email field")
        
        # Select an option
        await page.select_option('select[name="size"]', "large")
        print("🍕 Selected pizza size")
        
        # Check some checkboxes
        await page.check('input[value="bacon"]')
        await page.check('input[value="cheese"]')
        print("✅ Selected toppings")
        
        # Fill comments
        await page.fill('textarea[name="comments"]', "Extra cheese please!")
        print("💬 Filled comments")
        
        # Wait a moment to see the filled form
        await asyncio.sleep(3)
        
        # Take a screenshot
        await page.screenshot(path="working_demo_screenshot.png")
        print("📸 Took screenshot: working_demo_screenshot.png")
        
        # Navigate to another page
        await page.goto("https://www.example.com")
        print("🌐 Navigated to example.com")
        
        # Get page title
        title = await page.title()
        print(f"📄 Page title: {title}")
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Take another screenshot
        await page.screenshot(path="example_page_screenshot.png")
        print("📸 Took screenshot: example_page_screenshot.png")
        
        # Close browser
        await browser.close()
        print("🔒 Browser closed")
        
        print("\n🎉 Demo completed! Check the screenshot files for results.")

if __name__ == "__main__":
    asyncio.run(working_browser_demo()) 