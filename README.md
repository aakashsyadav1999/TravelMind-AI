# Traveler Planner Agent

A smart AI-powered travel planning agent that uses LangGraph workflows to help users plan their trips with intelligent research and recommendations.

## Overview

This project implements an AI agent system that can help users plan travels by leveraging internet search capabilities and intelligent conversation flows. The system uses a modular architecture with specialized agents and nodes for different functionalities.

## Project Structure

```
traveler_planner_agent/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (not in repo)
├── .env.template                      # Environment variables template
├── template.py                        # Project structure generator
├── state/
│   └── state.py                       # Application state management
├── tools/
│   ├── general_agent.py               # General purpose agent tools
│   └── internet_search_agent.py       # Internet search capabilities
├── node/
│   ├── general_agent_node.py          # General agent workflow nodes
│   └── internet_search_node.py        # Internet search workflow nodes
├── prompt/
│   ├── general_agent_prompt.py        # Prompts for general agent
│   └── internet_search_prompt.py      # Prompts for search agent
├── memories/
│   └── memories.py                    # Conversation and context memory
├── workflow/
│   └── langgraph_workflow.py          # Main LangGraph workflow definition
└── utils/
    ├── llm.py                         # LLM configuration and utilities
    └── conversion_summarizer.py       # Text conversion and summarization
```

## Features

- **Intelligent Travel Planning**: AI-powered agent that understands travel requirements
- **Internet Search Integration**: Real-time web search for up-to-date travel information
- **Memory System**: Maintains context and conversation history
- **Modular Architecture**: Extensible design with specialized agents and tools
- **LangGraph Workflows**: Advanced workflow management for complex agent interactions

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd traveler_planner_agent
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    cp .env.template .env
    # Edit .env file with your API keys and configurations
    ```

## Configuration

Copy `.env.template` to `.env` and configure the following variables:

```env
# Add your API keys and configuration here
OPENAI_API_KEY=your_openai_api_key
SEARCH_API_KEY=your_search_api_key
# Add other required environment variables
```

## Usage

### Quick Start

```python
from workflow.langgraph_workflow import TravelerPlannerWorkflow

# Initialize the workflow
planner = TravelerPlannerWorkflow()

# Start planning a trip
result = planner.plan_trip("I want to visit Japan for 10 days in spring")
print(result)
```

### Project Setup

If you're setting up the project structure from scratch, run:

```bash
python template.py
```

This will create all the necessary directories and files.

## Architecture

### Components

- **State Management**: Centralized state handling for agent interactions
- **Agent Tools**: Specialized tools for different functionalities
- **Workflow Nodes**: Individual processing units in the LangGraph workflow
- **Prompts**: Carefully crafted prompts for different agent types
- **Memory System**: Context preservation across conversations
- **Utilities**: Helper functions for LLM operations and text processing

### Workflow

1. User provides travel requirements
2. General agent processes the request
3. Internet search agent gathers relevant information
4. Information is processed and summarized
5. Comprehensive travel plan is generated
6. Results are stored in memory for future reference

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions and support, please [add contact information or issue tracking details].
