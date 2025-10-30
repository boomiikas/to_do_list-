from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
import os

# Initialize model
llm = OllamaLLM(model="llama3.1")

# Prompt template
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that manages a to-do list.

Here is the user's current to-do list:

{tasks}

User: {input}
Assistant:
""")

FILENAME = "tasks.json"

def load_tasks():
    """Load and return list of task dictionaries."""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            data = json.load(f)
            # Safely handle both formats (list or dict)
            if isinstance(data, dict) and "tasks" in data:
                return data["tasks"]
            elif isinstance(data, list):
                return data
    return []

def ask_agent(prompt_text: str):
    """Send user query + task list to model."""
    tasks = load_tasks()

    formatted_tasks = "\n".join(
        [f"{t.get('id', '?')}. {t.get('task', 'Unknown task')} - {'✅ Done' if t.get('done') else '🕓 Pending'}"
         for t in tasks]
    ) or "No tasks available."

    full_prompt = prompt.format(input=prompt_text, tasks=formatted_tasks)

    result = llm.invoke(full_prompt)
    return result
