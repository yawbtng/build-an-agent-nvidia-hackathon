#!/usr/bin/env python3
"""
Hybrid Document Editor Agent
This script combines simple word replacement with AI processing for advanced text editing.
"""

import asyncio
import re
import os
import random
import requests
import json
from playwright.async_api import async_playwright

# Load environment variables from secrets.env
def load_env_vars():
    """Load environment variables from secrets.env file."""
    try:
        with open('../secrets.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Loaded environment variables from secrets.env")
    except Exception as e:
        print(f"⚠️  Could not load secrets.env: {e}")

# Load environment variables at startup
load_env_vars()

def process_text_with_nvidia(original_text, user_request):
    """Process text using NVIDIA's API for advanced text improvements."""
    try:
        # Check if NVIDIA API key is available
        api_key = os.getenv('NVIDIA_API_KEY')
        if not api_key:
            print("⚠️  No NVIDIA API key found.")
            return original_text
        
        # NVIDIA API endpoint for the specific model
        url = "https://api.nvcf.nvidia.com/v2/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Create a prompt for the AI
        prompt = f"""
        Please modify the following text according to this request: "{user_request}"
        
        Original text:
        {original_text}
        
        Please provide the modified text that follows the user's request. 
        Keep the same general structure and meaning, but apply the requested changes.
        Only return the modified text without explanations.
        """
        
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful text editor that modifies text according to user requests. Provide only the modified text without explanations."},
                {"role": "user", "content": prompt}
            ],
            "model": "nvidia/llama-3_3-nemotron-super-49b-v1",  # Using the specific NVIDIA model
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        print(f"🤖 Calling NVIDIA API with model: {data['model']}")
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        print(f"🤖 Response status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            modified_text = result['choices'][0]['message']['content'].strip()
            print("🤖 NVIDIA AI successfully processed the text!")
            return modified_text
        else:
            print(f"⚠️  NVIDIA API error: {response.status_code}")
            print(f"⚠️  Response: {response.text}")
            return original_text
        
    except Exception as e:
        print(f"⚠️  NVIDIA AI processing failed: {e}")
        return original_text

def process_text_with_advanced_rules(original_text, user_request):
    """Process text using advanced rule-based patterns for complex requests."""
    print("🤖 Using advanced rule-based processing...")
    
    request_lower = user_request.lower()
    modified_text = original_text
    
    # 1. Translation patterns
    if any(word in request_lower for word in ["translate", "spanish", "french", "german", "italian", "portuguese"]):
        if "spanish" in request_lower:
            # Simple Spanish translation patterns
            spanish_translations = {
                'the': 'el/la',
                'and': 'y',
                'of': 'de',
                'in': 'en',
                'to': 'a',
                'for': 'para',
                'with': 'con',
                'that': 'que',
                'this': 'este/esta',
                'is': 'es',
                'are': 'son',
                'was': 'era',
                'were': 'eran',
                'will': 'será',
                'can': 'puede',
                'have': 'tener',
                'has': 'tiene',
                'had': 'tenía',
                'good': 'bueno',
                'great': 'excelente',
                'beautiful': 'hermoso',
                'wonderful': 'maravilloso',
                'amazing': 'increíble',
                'fantastic': 'fantástico'
            }
            
            for english, spanish in spanish_translations.items():
                pattern = re.compile(r'\b' + re.escape(english) + r'\b', re.IGNORECASE)
                modified_text = pattern.sub(spanish, modified_text)
            
            print("🔄 Applied Spanish translation patterns")
    
    # 2. Style transformation patterns
    if "shakespeare" in request_lower or "elizabethan" in request_lower:
        shakespeare_replacements = {
            'you': 'thou',
            'your': 'thy',
            'are': 'art',
            'is': 'be',
            'am': 'be',
            'have': 'hast',
            'has': 'hath',
            'will': 'shall',
            'can': 'may',
            'good': 'fair',
            'great': 'noble',
            'beautiful': 'fair',
            'wonderful': 'marvelous',
            'amazing': 'wondrous',
            'fantastic': 'magnificent'
        }
        
        for modern, shakespeare in shakespeare_replacements.items():
            pattern = re.compile(r'\b' + re.escape(modern) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(shakespeare, modified_text)
        
        # Add some Shakespearean phrases
        modified_text = "Verily, " + modified_text
        modified_text = modified_text.replace(".", ", methinks.")
        
        print("🔄 Applied Shakespearean style")
    
    # 3. Pirate speak patterns
    if "pirate" in request_lower:
        pirate_replacements = {
            'hello': 'ahoy',
            'hi': 'ahoy',
            'yes': 'aye',
            'no': 'nay',
            'friend': 'matey',
            'friends': 'mateys',
            'you': 'ye',
            'your': 'yer',
            'are': 'be',
            'is': 'be',
            'am': 'be',
            'good': 'fine',
            'great': 'mighty',
            'beautiful': 'comely',
            'wonderful': 'splendid',
            'amazing': 'astonishing'
        }
        
        for normal, pirate in pirate_replacements.items():
            pattern = re.compile(r'\b' + re.escape(normal) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(pirate, modified_text)
        
        # Add pirate phrases
        modified_text = "Arr, " + modified_text
        modified_text = modified_text.replace(".", ", me hearties!")
        
        print("🔄 Applied pirate speak")
    
    # 4. Technical manual style
    if "technical" in request_lower or "manual" in request_lower:
        technical_replacements = {
            'good': 'adequate',
            'great': 'optimal',
            'wonderful': 'satisfactory',
            'amazing': 'notable',
            'fantastic': 'exceptional',
            'beautiful': 'well-designed',
            'nice': 'suitable',
            'cool': 'efficient',
            'awesome': 'impressive'
        }
        
        for casual, technical in technical_replacements.items():
            pattern = re.compile(r'\b' + re.escape(casual) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(technical, modified_text)
        
        # Add technical phrases
        modified_text = "This document provides the following information: " + modified_text
        modified_text = modified_text.replace(".", ". Please refer to the documentation for additional details.")
        
        print("🔄 Applied technical manual style")
    
    # 5. Paragraph splitting
    if "paragraph" in request_lower and any(word in request_lower for word in ["3", "three", "split", "divide"]):
        sentences = modified_text.split('. ')
        if len(sentences) > 1:
            # Split into roughly equal paragraphs
            total_sentences = len(sentences)
            sentences_per_paragraph = max(1, total_sentences // 3)
            
            paragraphs = []
            for i in range(0, total_sentences, sentences_per_paragraph):
                paragraph = '. '.join(sentences[i:i + sentences_per_paragraph])
                if paragraph:
                    paragraphs.append(paragraph)
            
            modified_text = '\n\n'.join(paragraphs)
            print("🔄 Split text into paragraphs")
    
    # 6. Formal tone
    if "formal" in request_lower or "professional" in request_lower:
        formal_replacements = {
            'good': 'excellent',
            'great': 'outstanding',
            'wonderful': 'exceptional',
            'amazing': 'remarkable',
            'fantastic': 'superior',
            'nice': 'satisfactory',
            'cool': 'impressive',
            'awesome': 'notable'
        }
        
        for casual, formal in formal_replacements.items():
            pattern = re.compile(r'\b' + re.escape(casual) + r'\b', re.IGNORECASE)
            modified_text = pattern.sub(formal, modified_text)
        
        print("🔄 Applied formal tone")
    
    return modified_text

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
        print("🤖 No simple patterns matched, trying advanced processing...")
        
        # First try NVIDIA AI
        nvidia_result = process_text_with_nvidia(original_text, user_request)
        
        # If NVIDIA failed, try advanced rule-based processing
        if nvidia_result == original_text:
            print("🤖 NVIDIA AI failed, trying advanced rule-based processing...")
            modified_text = process_text_with_advanced_rules(original_text, user_request)
        else:
            modified_text = nvidia_result
    
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
        print("- 'Make the text sound more modern and use better vocabulary'")
        print("- 'Rewrite this in a casual, friendly tone'")
        print("- 'Add more descriptive language and vivid imagery'")
        print("- 'Translate the second paragraph to Spanish'")
        print("- 'Rewrite this in Shakespearean style'")
        print("- 'Convert this to pirate speak'")
        print("- 'Make this sound like a technical manual'")
        
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