import json
import re
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from types import SimpleNamespace

TASKS_FILE = Path("tasks.json")
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class Task:
    def __init__(self, id: int, title: str, created_at: str, solved: bool = False):
        self.id = id
        self.title = title
        self.created_at = created_at
        self.solved = solved

    def to_dict(self):
        return {"id": self.id, "title": self.title, "created_at": self.created_at, "solved": self.solved}

    @staticmethod
    def from_dict(data):
        return Task(data["id"], data["title"], data["created_at"], data.get("solved", False))

def load_tasks():
    if not TASKS_FILE.exists(): return []
    with open(TASKS_FILE, "r") as f:
        try: return [Task.from_dict(t) for t in json.load(f)]
        except: return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def create_task(title: str):
    tasks = load_tasks()
    new_id = max([t.id for t in tasks], default=0) + 1
    tasks.append(Task(new_id, title, datetime.now().isoformat()))
    save_tasks(tasks)
    return f"Success: Task {new_id} created."

def mark_solved(task_id: int):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.solved = True
            save_tasks(tasks)
            return f"Success: Task {task_id} marked as solved."
    return f"Error: Task {task_id} not found."

def delete_task(task_id: int):
    tasks = load_tasks()
    initial_len = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if len(tasks) == initial_len: return f"Error: Task {task_id} not found."
    save_tasks(tasks)
    return f"Success: Task {task_id} deleted."

def list_all():
    tasks = load_tasks()
    if not tasks: return "List is empty."
    return "\n".join([f"{'[x]' if t.solved else '[ ]'} {t.id}: {t.title}" for t in tasks])

tools = [
    {"type": "function", "function": {"name": "create_task", "description": "Add task", "parameters": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}}},
    {"type": "function", "function": {"name": "mark_solved", "description": "Solve by ID", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_task", "description": "Delete by ID", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "list_all", "description": "List all", "parameters": {"type": "object", "properties": {}}}}
]

def execute_tool(name, args):
    # Încărcăm task-urile curente pentru a putea mapa indexul la ID
    current_tasks = load_tasks()
    
    # Extragem ID-ul sau valoarea numerică primită de la AI
    val = int(args.get("task_id", 0))

    # Logica de mapare: dacă userul cere "al doilea task", AI-ul va trimite task_id=2.
    # Verificăm dacă 'val' este un index valid în listă (1, 2, 3...) 
    # în loc să fie neapărat ID-ul bazei de date.
    if name in ["mark_solved", "delete_task"]:
        if 1 <= val <= len(current_tasks):
            # Mapăm indexul de la 1 la ID-ul real al task-ului de pe acea poziție
            actual_id = current_tasks[val - 1].id
            if name == "mark_solved": return mark_solved(actual_id)
            if name == "delete_task": return delete_task(actual_id)
    
    # Fallback: dacă nu este index, încercăm direct ca ID (sau pentru restul funcțiilor)
    if name == "create_task": return create_task(args.get("title", ""))
    if name == "mark_solved": return mark_solved(val)
    if name == "delete_task": return delete_task(val)
    if name == "list_all": return list_all()
    
    return "Unknown action."

def run_agent():
    print("TODO Agent Active. (May 9, 2026)")
    system_prompt = {
        "role": "system", 
        "content": "You are a task automation tool. You MUST use functions for every request. If a user wants to finish/check/solve a task, use mark_solved with the correct ID. Today is May 9, 2026."
    }
    
    while True:
        user_input = input("\nUser: ").strip()
        if user_input.lower() in ["exit", "quit"]: break
        
        current_state = list_all()
        messages = [
            system_prompt,
            {"role": "system", "content": f"CURRENT TASKS:\n{current_state}"},
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat.completions.create(model="mistral", messages=messages, tools=tools, temperature=0)
        msg = response.choices[0].message
        
        tool_calls = []
        if msg.tool_calls:
            tool_calls = msg.tool_calls
        else:
            json_match = re.search(r'(\w+)\(\s*(\{.*?\}|.*?)?\s*\)', msg.content or "")
            if json_match:
                name = json_match.group(1)
                raw_args = json_match.group(2)
                try:
                    args = json.loads(raw_args) if "{" in raw_args else {"task_id": re.sub(r'\D', '', raw_args)}
                    tool_calls.append(SimpleNamespace(function=SimpleNamespace(name=name, arguments=json.dumps(args))))
                except: pass

        if tool_calls:
            for tc in tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                    print(f"AI: {execute_tool(tc.function.name, args)}")
                except: print("AI: Error executing command.")
        elif msg.content:
            print(f"AI: {msg.content.strip()}")

if __name__ == "__main__":
    run_agent()
