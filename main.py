from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import json
import os
from agent import ask_agent

FILENAME = 'tasks.json'
app = FastAPI()

class Task(BaseModel):
    id: int
    task: str
    done: bool = False

def load_tasks() -> List[Task]:
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            data = json.load(f)
            return [Task(**task) for task in data]
    return []

def save_tasks():
    with open(FILENAME, 'w') as f:
        json.dump([task.dict() for task in tasks], f, indent=4)

def get_next_id() -> int:
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1

tasks: List[Task] = load_tasks()

@app.get("/")
def home():
    return {"message": "To-do app running"}

@app.post("/add")
def add_task(data: Task):
    new_task = Task(id=get_next_id(), task=data.task, done=False)
    tasks.append(new_task)
    save_tasks()
    return {"message": "Task added", "task": new_task}

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}

@app.put("/done/{id}")
def mark_done(id: int):
    for task in tasks:
        if task.id == id:
            task.done = True
            save_tasks()
            return {"message": "Task marked as done", "task": task}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/clear")
def all_clear():
    tasks.clear()
    save_tasks()
    return {"message": "Tasks cleared"}


@app.post("/chat")
async def chat(prompt: str):
    try:
        response = ask_agent(prompt)
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
