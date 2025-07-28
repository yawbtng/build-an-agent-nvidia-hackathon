#!/usr/bin/env python3
"""
Simple Browser Demo
This script demonstrates browser automation with a single example.
"""

import asyncio
from playwright.async_api import async_playwright

async def demo_browser():
    """Simple browser automation demo."""
    print("🚀 Browser Automation Demo")
    print("=" * 40)
    print("Opening browser and performing a search...")
    
    async with async_playwright() as p:
        # Launch browser (visible)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🌐 Browser launched!")
        
        # Navigate to Google
        await page.goto("https://www.google.com")
        print("📱 Navigated to Google")
        
        # Find and fill search box
        search_box = await page.wait_for_selector('input[name="q"]')
        await search_box.fill("LangGraph Computer Use Agent")
        print("✍️  Typed search query")
        
        # Press Enter to search
        await page.keyboard.press("Enter")
        print("🔍 Pressed Enter to search")
        
        # Wait for results
        await page.wait_for_selector("#search")
        print("✅ Search results loaded!")
        
        # Wait a moment to see the results
        await asyncio.sleep(3)
        
        # Take a screenshot
        await page.screenshot(path="demo_screenshot.png")
        print("📸 Took screenshot: demo_screenshot.png")
        
        # Close browser
        await browser.close()
        print("🔒 Browser closed")
        
        print("\n🎉 Demo completed! Check demo_screenshot.png for the result.")

if __name__ == "__main__":
    asyncio.run(demo_browser()) 