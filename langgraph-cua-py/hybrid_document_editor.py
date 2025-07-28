#!/usr/bin/env python3
"""
Hybrid Document Editor Agent
This script combines simple word replacement with AI processing for advanced text editing.
"""

import asyncio
import re
import os
import random
from playwright.async_api import async_playwright

def process_text_hybrid(original_text, user_request):
    """Process text using hybrid approach - simple replacement + AI fallback."""
    print(f"🔧 Processing: {user_request}")
    
    # Convert to lowercase for easier matching
    request_lower = user_request.lower()
    modified_text = original_text
    
    # 1. Handle simple word replacements
    if "replace" in request_lower and "with" in request_lower:
        # Extract words to replace and replacement
        words_to_replace = []
        replacement_words = []
        
        # Look for patterns like "replace X with Y"
        replace_patterns = [
            r'replace\s+(\w+)\s+with\s+(\w+)',
            r'replace\s+the\s+word\s+(\w+)\s+with\s+(\w+)',
            r'change\s+(\w+)\s+to\s+(\w+)',
            r'substitute\s+(\w+)\s+for\s+(\w+)'
        ]
        
        for pattern in replace_patterns:
            matches = re.findall(pattern, request_lower)
            if matches:
                for old_word, new_word in matches:
                    words_to_replace.append(old_word)
                    replacement_words.append(new_word)
        
        # Apply replacements
        for old_word, new_word in zip(words_to_replace, replacement_words):
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old_word), re.IGNORECASE)
            modified_text = pattern.sub(new_word, modified_text)
            print(f"🔄 Replaced '{old_word}' with '{new_word}'")
    
    # 2. Handle "replace many words with X and Y" pattern
    if "replace many words" in request_lower and "with" in request_lower:
        # Extract replacement words
        replacement_words = []
        if "skibidi" in request_lower:
            replacement_words.append("skibidi")
        if "rizz" in request_lower:
            replacement_words.append("rizz")
        if "brainrot" in request_lower:
            replacement_words.append("brainrot")
        if "fr" in request_lower:
            replacement_words.append("fr")
        if "no cap" in request_lower:
            replacement_words.append("no cap")
        
        if replacement_words:
            # Split text into words
            words = re.findall(r'\b\w+\b', modified_text)
            # Replace some words randomly
            for i in range(len(words)):
                if random.random() < 0.3:  # 30% chance to replace each word
                    words[i] = random.choice(replacement_words)
            
            modified_text = ' '.join(words)
            print(f"🔄 Replaced many words with: {', '.join(replacement_words)}")
    
    # 3. Handle case changes
    if "uppercase" in request_lower or "upper case" in request_lower:
        modified_text = modified_text.upper()
        print("🔄 Converted to uppercase")
    
    if "lowercase" in request_lower or "lower case" in request_lower:
        modified_text = modified_text.lower()
        print("🔄 Converted to lowercase")
    
    # 4. Handle formatting
    if "bold" in request_lower:
        modified_text = f"**{modified_text}**"
        print("🔄 Made text bold")
    
    if "italic" in request_lower:
        modified_text = f"*{modified_text}*"
        print("🔄 Made text italic")
    
    # 5. Handle title addition
    if "title" in request_lower:
        modified_text = f"# DOCUMENT TITLE\n\n{modified_text}"
        print("🔄 Added title")
    
    # 6. Handle modern language requests
    if "modern" in request_lower or "better vocabulary" in request_lower:
        # Simple modern language replacements
        modern_replacements = {
            'the': 'da',
            'and': 'n',
            'you': 'u',
            'are': 'r',
            'your': 'ur',
            'for': '4',
            'to': '2',
            'too': '2',
            'two': '2',
            'great': 'gr8',
            'good': 'gud',
            'cool': 'kewl',
            'awesome': 'awsm',
            'because': 'bc',
            'before': 'b4',
            'love': 'luv',
            'what': 'wat',
            'that': 'dat',
            'this': 'dis',
            'with': 'w/',
            'without': 'w/o'
        }
        
        for old_word, new_word in modern_replacements.items():
            pattern = re.compile(r'\b' + re.escape(old_word) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(new_word, modified_text)
        
        print("🔄 Modernized language")
    
    # 7. Handle casual/friendly tone
    if "casual" in request_lower or "friendly" in request_lower:
        casual_additions = [
            "Hey there! ",
            "So, ",
            "You know, ",
            "Like, ",
            "Basically, ",
            " Honestly, ",
            " TBH, ",
            " NGL, "
        ]
        
        # Add some casual phrases
        sentences = modified_text.split('. ')
        if sentences:
            sentences[0] = random.choice(casual_additions) + sentences[0]
            modified_text = '. '.join(sentences)
        
        print("🔄 Made text more casual and friendly")
    
    # 8. Handle descriptive language
    if "descriptive" in request_lower or "vivid" in request_lower or "imagery" in request_lower:
        descriptive_words = [
            "amazing", "incredible", "fantastic", "wonderful", "beautiful",
            "stunning", "magnificent", "spectacular", "brilliant", "excellent"
        ]
        
        # Replace some adjectives with more descriptive ones
        words = modified_text.split()
        for i in range(len(words)):
            if random.random() < 0.2:  # 20% chance
                if words[i].lower() in ['good', 'nice', 'great', 'fine']:
                    words[i] = random.choice(descriptive_words)
        
        modified_text = ' '.join(words)
        print("🔄 Enhanced with descriptive language")
    
    # If no changes were made, try AI processing
    if modified_text == original_text:
        print("🤖 No simple patterns matched, trying AI processing...")
        # Here you could add AI processing if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("🤖 AI processing available but not implemented in this demo")
        else:
            print("🤖 No AI processing available")
    
    return modified_text

async def hybrid_document_editor():
    """Hybrid document editing with smart text processing."""
    print("🚀 Hybrid Document Editor Agent")
    print("=" * 60)
    print("This agent combines simple word replacement with AI processing!")
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
        print("- 'Replace the word dick with cock'")
        print("- 'Replace many words with skibidi and rizz'")
        print("- 'Make the text sound more modern and use better vocabulary'")
        print("- 'Rewrite this in a casual, friendly tone'")
        print("- 'Add more descriptive language and vivid imagery'")
        
        user_request = input("\nEnter your editing request: ").strip()
        
        if not user_request:
            user_request = "Replace many words with skibidi and rizz"
            print(f"Using default: {user_request}")
        
        # Step 3: Process the request using hybrid approach
        print(f"\n🔧 Processing request: {user_request}")
        proposed_content = process_text_hybrid(original_content, user_request)
        
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
                new_content = process_text_hybrid(original_content, new_request)
                print(f"New proposed: {new_content[:100]}...")
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
        
        print("\n🎉 Hybrid document editing completed!")
        print("You can now edit documents without touching them!")

if __name__ == "__main__":
    asyncio.run(hybrid_document_editor()) 