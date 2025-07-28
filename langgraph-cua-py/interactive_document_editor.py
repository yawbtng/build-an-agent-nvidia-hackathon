#!/usr/bin/env python3
"""
Interactive Document Editor Agent
This script allows you to edit documents on web pages with real-time interaction.
"""

import asyncio
import re
import os
from playwright.async_api import async_playwright
from openai import OpenAI

async def process_text_with_ai(original_text, user_request):
    """Process text using OpenAI API for advanced text improvements."""
    try:
        # Check if OpenAI API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  No OpenAI API key found. Using simple text processing.")
            return original_text
        
        client = OpenAI(api_key=api_key)
        
        # Create a prompt for the AI
        prompt = f"""
        Please modify the following text according to this request: "{user_request}"
        
        Original text:
        {original_text}
        
        Please provide the modified text that follows the user's request. 
        Keep the same general structure and meaning, but apply the requested changes.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful text editor that modifies text according to user requests. Provide only the modified text without explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        modified_text = response.choices[0].message.content.strip()
        print("🤖 AI successfully processed the text!")
        return modified_text
        
    except Exception as e:
        print(f"⚠️  AI processing failed: {e}")
        return original_text

async def interactive_document_editor():
    """Interactive document editing with user input and confirmation."""
    print("🚀 Interactive Document Editor Agent")
    print("=" * 60)
    print("This agent will help you edit documents on web pages!")
    print("=" * 60)
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print("🌐 Browser launched!")
        
        # Step 1: Let user choose a document to edit
        print("\n📖 Step 1: Choose a document to edit")
        print("Available options:")
        print("1. Sample HTML page (httpbin.org/html)")
        print("2. Example.com page")
        print("3. Enter custom URL")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            url = "https://httpbin.org/html"
        elif choice == "2":
            url = "https://www.example.com"
        elif choice == "3":
            url = input("Enter URL: ").strip()
        else:
            url = "https://httpbin.org/html"
            print("Using default: httpbin.org/html")
        
        print(f"\n📱 Navigating to: {url}")
        await page.goto(url)
        await asyncio.sleep(2)
        
        # Extract text content
        original_content = await page.evaluate("""
            () => {
                const textContent = document.body.innerText || document.body.textContent || '';
                return textContent.trim();
            }
        """)
        
        # Clean up content
        original_content = re.sub(r'\s+', ' ', original_content).strip()
        print(f"\n📄 Original document content:")
        print(f"{'='*50}")
        print(original_content[:200] + "..." if len(original_content) > 200 else original_content)
        print(f"{'='*50}")
        
        # Take screenshot of original
        await page.screenshot(path="original_document.png")
        print("📸 Saved original document screenshot")
        
        # Step 2: Get user's editing request
        print("\n💡 Step 2: What would you like to change?")
        print("Examples:")
        print("- 'Make the text uppercase'")
        print("- 'Add a title at the top'")
        print("- 'Change all text to bold'")
        print("- 'Replace many words with skibidi and rizz'")
        print("- 'Make the text sound more modern and use better vocabulary'")
        print("- 'Rewrite this in a casual, friendly tone'")
        print("- 'Add more descriptive language and vivid imagery'")
        
        user_request = input("\nEnter your editing request: ").strip()
        
        if not user_request:
            user_request = "Make the text uppercase and add a title"
            print(f"Using default: {user_request}")
        
        # Step 3: Process the request and propose changes
        print(f"\n🔧 Processing request: {user_request}")
        
        # Try to use AI for advanced text processing
        proposed_content = await process_text_with_ai(original_content, user_request)
        
        # Fallback to simple text processing if AI fails
        if proposed_content == original_content:
            print("🤖 AI processing failed, using simple text processing...")
            
            if "uppercase" in user_request.lower() or "upper case" in user_request.lower():
                proposed_content = proposed_content.upper()
            
            if "lowercase" in user_request.lower() or "lower case" in user_request.lower():
                proposed_content = proposed_content.lower()
            
            if "title" in user_request.lower():
                proposed_content = f"# DOCUMENT TITLE\n\n{proposed_content}"
            
            if "bold" in user_request.lower():
                proposed_content = f"**{proposed_content}**"
            
            if "italic" in user_request.lower():
                proposed_content = f"*{proposed_content}*"
        
        # Step 4: Show the proposed changes
        print(f"\n✨ Proposed changes:")
        print(f"{'='*50}")
        print(f"Original: {original_content[:100]}...")
        print(f"Proposed: {proposed_content[:100]}...")
        print(f"{'='*50}")
        
        # Step 5: Ask for confirmation
        print("\n❓ Step 3: Do you want to apply these changes?")
        print("Options:")
        print("y - Apply changes")
        print("n - Cancel")
        print("m - Modify request")
        
        confirm = input("\nEnter your choice (y/n/m): ").strip().lower()
        
        if confirm == "y":
            print("✅ Applying changes...")
            
            # Create new page with edited content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Edited Document</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        margin: 40px; 
                        line-height: 1.6; 
                        background-color: #f5f5f5;
                    }}
                    h1 {{ 
                        color: #333; 
                        border-bottom: 2px solid #333; 
                        padding-bottom: 10px; 
                    }}
                    .content {{
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                </style>
            </head>
            <body>
                <div class="content">
                    {proposed_content.replace(chr(10), '<br>').replace(chr(13), '')}
                </div>
            </body>
            </html>
            """
            
            await page.set_content(html_content)
            await asyncio.sleep(2)
            
            # Take screenshot of edited document
            await page.screenshot(path="edited_document.png")
            print("📸 Saved edited document screenshot")
            
            print("✅ Changes applied successfully!")
            print("\n📸 Screenshots saved:")
            print("- original_document.png (before changes)")
            print("- edited_document.png (after changes)")
            
        elif confirm == "m":
            print("🔄 Let's modify the request...")
            new_request = input("Enter your new editing request: ").strip()
            if new_request:
                print(f"Processing new request: {new_request}")
                # Here you could add more processing logic
                print("(This would process the new request)")
            else:
                print("No new request provided, keeping original changes")
        else:
            print("❌ Changes cancelled")
        
        # Step 6: Ask if user wants to make more changes
        print("\n🔄 Would you like to make more changes to this document?")
        more_changes = input("Enter 'y' to continue editing, or any other key to finish: ").strip().lower()
        
        if more_changes == "y":
            print("🔄 Continuing with more edits...")
            # Here you could loop back to the editing process
            print("(This would allow for multiple rounds of editing)")
        
        # Close browser
        await browser.close()
        print("🔒 Browser closed")
        
        print("\n🎉 Interactive document editing completed!")
        print("You can now edit documents without touching them!")
    
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
    asyncio.run(interactive_document_editor()) 