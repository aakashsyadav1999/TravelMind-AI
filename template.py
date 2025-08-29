import os


list_of_files = [

    "README.md",
    "state/state.py",
    "tools/general_agent.py",
    "tools/internet_search_agent.py",
    "node/general_agent_node.py",
    "prompt/general_agent_prompt.py",
    "node/internet_search_node.py",
    "prompt/internet_search_prompt.py",
    "memories/memories.py",
    "workflow/langgraph_workflow.py",
    "utils/llm.py",
    "utils/conversion_summarizer.py",
    "requirements.txt",
    ".env",
    ".env.template"
    ]


def create_file(file_path):
    """Create a file if it doesn't exist."""
    dir_path = os.path.dirname(file_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Create an empty file
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")

if __name__ == "__main__":
    for file in list_of_files:
        create_file(file)