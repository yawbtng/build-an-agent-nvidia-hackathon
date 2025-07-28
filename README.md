# Hands-Free Computer-Use Agent

Welcome to the **Hands-Free Computer-Use Agent** project for the NVIDIA Build-an-Agent Hackathon! This project creates an intelligent AI agent that can perform complex computer tasks using natural language commands, specifically designed to help people with motor impairments.

## What This Agent Does

By the end of this project, you'll have an agent that can:

* **Understand natural language commands** and convert them into browser actions
* **Fill forms automatically** using accessibility-friendly selectors
* **Navigate web pages** using keyboard-equivalent actions
* **Handle validation errors** and perform corrective actions
* **Maintain conversation context** across multiple interactions
* **Make intelligent decisions** about next steps based on available information

## Primary Use Case: Form Autofill & Submit

The MVP focuses on automating form filling on public contact/support forms:

- **Input**: Typed natural-language commands (e.g., "Fill the contact form with name 'Joshua Boateng', email 'joshua@example.com', message 'Requesting accommodation info.' Then submit.")
- **Output**: Agent identifies form fields by accessibility-friendly selectors, fills them, and submits
- **Error Handling**: Detects validation errors and performs one corrective round

## Technical Architecture

- **Orchestration**: LangGraph Computer Use Agent framework
- **Browser Control**: Scrapybara for accessibility-aware selectors
- **Reasoning Model**: NVIDIA NIM-hosted LLM for planning and decision-making
- **Tool Surface**: Minimal, predictable tools for reading pages, typing, clicking, and submitting

## Success Criteria

- Complete form fill and submit in < 15 seconds
- Handle one validation error automatically
- Narrate actions via text output

## Project Structure

```
code/
├── handsfree_agent/          # Main agent implementation
│   ├── agent.py             # Core agent logic
│   ├── tools.py             # Browser automation tools
│   ├── prompts.py           # Agent prompts
│   └── __main__.py          # Entry point
├── langgraph-cua-py/        # LangGraph CUA framework
└── examples/                # Example usage and demos
```

## Getting Started

1. Set up your environment variables
2. Install dependencies
3. Run the agent with a test form

## About

This project addresses the accessibility challenges faced by millions of people with motor impairments when using computers. By converting plain-language requests into reliable keyboard-like browser actions, we aim to reduce motor effort and improve computer accessibility.


