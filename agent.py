from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence

# Initialize Llama model
llm = OllamaLLM(model="llama3.1")

# Prompt defines how the agent should behave
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that manages a to-do list.
You can help with:
- Adding new tasks
- Listing tasks
- Marking tasks as done
- Deleting tasks

User: {input}
""")

# Combine the prompt + model into a runnable pipeline
agent = RunnableSequence(prompt | llm)

def ask_agent(prompt_text: str):
    """Send a message to the LLM and return its response."""
    result = agent.invoke({"input": prompt_text})
    return result
