#!/usr/bin/env python3
"""
Simple Coding Agent using Mistral (locally via Ollama)
with read_file, write_file, and run_command tools.

Each tool call requires user confirmation before execution.
"""

import json
import subprocess
import requests
import sys
from pathlib import Path

# ── Ollama endpoint ──────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral"

# ── Tool definitions (sent to the model) ────────────────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file from disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative path to the file."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file on disk (creates or overwrites).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path where the file will be written."},
                    "content": {"type": "string", "description": "Text content to write into the file."},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command and return its stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run."}
                },
                "required": ["command"],
            },
        },
    },
]

# ── Tool implementations ─────────────────────────────────────────────────────

def read_file(path: str) -> str:
    """Return file contents, or an error string."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as exc:
        return f"ERROR: {exc}"


def write_file(path: str, content: str) -> str:
    """Write content to path; return confirmation or error."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"OK: wrote {len(content)} characters to '{path}'."
    except Exception as exc:
        return f"ERROR: {exc}"


def run_command(command: str) -> str:
    """Run a shell command; return combined stdout + stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            timeout=30,
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += result.stderr
        if not output:
            output = "(no output)"
        return output
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out after 30 s."
    except Exception as exc:
        return f"ERROR: {exc}"


# ── Permission gate ──────────────────────────────────────────────────────────

def ask_permission(tool_name: str, args: dict) -> bool:
    """
    Show the proposed tool call to the user and ask for confirmation.
    Returns True if the user approves.
    """
    print("\n" + "=" * 60)
    print(f"  🤖  Agent wants to call: {tool_name}")
    print("  Arguments:")
    for k, v in args.items():
        # Truncate long values for readability
        display = str(v)
        if len(display) > 300:
            display = display[:300] + "… [truncated]"
        print(f"    {k}: {display}")
    print("=" * 60)
    while True:
        answer = input("  Allow this call? [y/N] ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("", "n", "no"):
            return False
        print("  Please answer y or n.")


# ── Dispatch a tool call ─────────────────────────────────────────────────────

def dispatch_tool(tool_name: str, args: dict) -> str:
    """Execute the named tool with the given arguments."""
    if tool_name == "read_file":
        return read_file(**args)
    elif tool_name == "write_file":
        return write_file(**args)
    elif tool_name == "run_command":
        return run_command(**args)
    else:
        return f"ERROR: unknown tool '{tool_name}'."


# ── Single LLM call ──────────────────────────────────────────────────────────

def call_model(messages: list) -> dict:
    """Send messages to Ollama and return the response dict."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


def extract_tool_calls_from_text(text: str) -> list:
    """
    Fallback parser: Mistral sometimes emits tool calls as raw JSON in its
    reply text instead of the structured tool_calls field.  We look for every
    JSON object that contains a "name" key matching one of our tools.
    Returns a list in the same shape as the official tool_calls field.
    """
    found = []
    # Find all {...} blobs in the text, handling nested braces
    i = 0
    while i < len(text):
        if text[i] == '{':
            depth = 0
            start = i
            for j in range(i, len(text)):
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                    if depth == 0:
                        blob = text[start:j + 1]
                        try:
                            obj = json.loads(blob)
                            name = obj.get("name") or obj.get("function", {}).get("name", "")
                            args = (
                                obj.get("arguments")
                                or obj.get("parameters")
                                or obj.get("function", {}).get("arguments")
                                or {}
                            )
                            if name in ("read_file", "write_file", "run_command"):
                                if isinstance(args, str):
                                    args = json.loads(args)
                                found.append({
                                    "function": {"name": name, "arguments": args}
                                })
                        except (json.JSONDecodeError, Exception):
                            pass
                        i = j
                        break
        i += 1
    return found


# ── Main agent loop ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an autonomous coding agent. You MUST complete tasks by calling tools.

You have exactly three tools:
- read_file(path)         → read a file from disk
- write_file(path, content) → write/create a file on disk
- run_command(command)    → execute a shell command

RULES — follow them strictly:
1. NEVER just describe or explain code in text. Always call write_file to actually create files.
2. After writing a file, always call run_command to run/test it.
3. Do not ask the user questions. Make reasonable choices and act.
4. Only write a plain-text summary AFTER all tool calls are done and the task is complete.
"""

def run_agent(user_task: str) -> None:
    """Drive the agent until it produces a final answer (no more tool calls)."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_task},
    ]

    print(f"\n🚀  Task: {user_task}\n")

    step = 0
    while True:
        step += 1
        print(f"── Step {step}: calling model …")
        response = call_model(messages)

        message = response.get("message", {})
        tool_calls = message.get("tool_calls") or []

        # Append the assistant turn to history
        messages.append({"role": "assistant", "content": message.get("content", ""), "tool_calls": tool_calls})

        if not tool_calls:
            # No more tool calls → final answer
            final = message.get("content", "").strip()
            print("\n✅  Agent finished.\n")
            print("─" * 60)
            print(final)
            print("─" * 60)
            break

        # Process each tool call
        for tc in tool_calls:
            fn = tc.get("function", {})
            tool_name = fn.get("name", "")
            raw_args = fn.get("arguments", {})

            # Ollama may return arguments as a JSON string
            if isinstance(raw_args, str):
                try:
                    raw_args = json.loads(raw_args)
                except json.JSONDecodeError:
                    raw_args = {}

            # Ask user for permission
            approved = ask_permission(tool_name, raw_args)

            if approved:
                print(f"  ▶ Running {tool_name} …")
                result = dispatch_tool(tool_name, raw_args)
                print(f"  ◀ Result: {result[:200]}{'…' if len(result) > 200 else ''}")
            else:
                result = "Tool call was DENIED by the user."
                print(f"  ✗ Denied.")

            # Feed the result back as a tool message
            messages.append({
                "role": "tool",
                "content": result,
            })


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = input("Enter your task for the agent: ").strip()
        if not task:
            print("No task provided. Exiting.")
            sys.exit(0)

    run_agent(task)
