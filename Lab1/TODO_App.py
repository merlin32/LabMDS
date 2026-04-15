import json
import sys
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tasks.json")

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
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, "r") as f:
        data = json.load(f)
        return [Task.from_dict(t) for t in data]

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def create_task(title: str):
    tasks = load_tasks()
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task(new_id, title, datetime.now().isoformat())
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task created with ID: {new_id}")

def mark_solved(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.solved = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as solved")
            return
    print(f"Task {task_id} not found")

def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found")
        return
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted")

def display_tasks(start_date: str = None, end_date: str = None):
    tasks = load_tasks()
    if start_date:
        start = datetime.fromisoformat(start_date)
        tasks = [t for t in tasks if datetime.fromisoformat(t.created_at) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        tasks = [t for t in tasks if datetime.fromisoformat(t.created_at) <= end]
    
    if not tasks:
        print("No tasks found")
        return
    
    for task in tasks:
        status = "[x]" if task.solved else "[ ]"
        print(f"{status} {task.id}: {task.title} (created: {task.created_at})")

def list_all():
    tasks = load_tasks()
    if not tasks:
        print("No tasks")
        return
    for task in tasks:
        status = "[x]" if task.solved else "[ ]"
        print(f"{status} {task.id}: {task.title} (created: {task.created_at})")

def repl():
    print("TODO List REPL - Commands: add, solve, delete, list, filter, exit")
    while True:
        try:
            cmd = input("\n> ").strip().strip('\r\n')
            if not cmd:
                continue
            
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == "exit":
                print("Goodbye!")
                break
            elif action == "add":
                if len(parts) > 1:
                    create_task(" ".join(parts[1:]))
                else:
                    print("Usage: add <title>")
            elif action == "solve":
                if len(parts) > 1:
                    mark_solved(int(parts[1]))
                else:
                    print("Usage: solve <id>")
            elif action == "delete":
                if len(parts) > 1:
                    delete_task(int(parts[1]))
                else:
                    print("Usage: delete <id>")
            elif action == "list":
                list_all()
            elif action == "filter":
                if len(parts) >= 3:
                    start = parts[1] if parts[1] != "none" else None
                    end = parts[2] if parts[2] != "none" else None
                    display_tasks(start, end)
                else:
                    print("Usage: filter <start_date> <end_date> (use 'none' for no bound)")
            else:
                print("Unknown command. Use: add, solve, delete, list, filter, exit")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()
