#!/usr/bin/env python3
"""
Bulletproof Browser Demo
This script demonstrates browser automation with robust error handling.
"""

import asyncio
from playwright.async_api import async_playwright

async def bulletproof_demo():
    """Bulletproof browser automation demo with error handling."""
    print("🚀 Bulletproof Browser Demo")
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
        
        # Navigate to form page
        await page.goto("https://httpbin.org/forms/post")
        print("📱 Navigated to test form")
        
        # Wait for page to load
        await asyncio.sleep(2)
        
        # Fill in form fields with error handling
        try:
            await page.fill('input[name="custname"]', "John Doe")
            print("✍️  Filled name field")
        except Exception as e:
            print(f"⚠️  Could not fill name field: {e}")
        
        try:
            await page.fill('input[name="custtel"]', "555-123-4567")
            print("📞 Filled phone field")
        except Exception as e:
            print(f"⚠️  Could not fill phone field: {e}")
        
        try:
            await page.fill('input[name="custemail"]', "john@example.com")
            print("📧 Filled email field")
        except Exception as e:
            print(f"⚠️  Could not fill email field: {e}")
        
        # Try to fill comments if available
        try:
            await page.fill('textarea[name="comments"]', "This is a test automation!")
            print("💬 Filled comments")
        except Exception as e:
            print(f"⚠️  Could not fill comments: {e}")
        
        # Wait a moment to see the filled form
        await asyncio.sleep(3)
        
        # Take another screenshot
        await page.screenshot(path="filled_form.png")
        print("📸 Took screenshot: filled_form.png")
        
        # Navigate to a simple search page (using a more reliable approach)
        await page.goto("https://www.google.com")
        print("🔍 Navigated to Google")
        
        # Wait for page to load
        await asyncio.sleep(3)
        
        # Try to search with multiple selector attempts
        search_success = False
        search_selectors = [
            'input[name="q"]',
            'textarea[name="q"]',
            'input[title="Search"]',
            'input[type="text"]'
        ]
        
        for selector in search_selectors:
            try:
                search_box = await page.wait_for_selector(selector, timeout=5000)
                await search_box.fill("LangGraph Computer Use Agent")
                print("✍️  Typed search query")
                
                # Press Enter to search
                await page.keyboard.press("Enter")
                print("🔍 Pressed Enter to search")
                
                # Wait a moment for results
                await asyncio.sleep(3)
                search_success = True
                break
                
            except Exception as e:
                print(f"⚠️  Search selector {selector} failed: {e}")
                continue
        
        if search_success:
            # Take final screenshot
            await page.screenshot(path="search_results.png")
            print("📸 Took screenshot: search_results.png")
        else:
            print("⚠️  Could not perform search, but continuing...")
        
        # Navigate to one more page to show navigation works
        await page.goto("https://httpbin.org/")
        print("🌐 Navigated to httpbin.org")
        
        # Wait a moment
        await asyncio.sleep(2)
        
        # Take final screenshot
        await page.screenshot(path="final_page.png")
        print("📸 Took screenshot: final_page.png")
        
        # Close browser
        await browser.close()
        print("🔒 Browser closed")
        
        print("\n🎉 Demo completed successfully!")
        print("📸 Screenshots taken:")
        print("- example_page.png")
        print("- filled_form.png")
        if search_success:
            print("- search_results.png")
        print("- final_page.png")
        print("\n✅ Browser automation is working! You can see the browser window opened and performed actions.")

if __name__ == "__main__":
    asyncio.run(bulletproof_demo()) 