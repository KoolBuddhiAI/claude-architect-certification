import anthropic
import json
import subprocess
from pathlib import Path

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

SANDBOX = Path("/tmp/dev-productivity-sandbox")
SANDBOX.mkdir(exist_ok=True)

tools = [
    {
        "name": "read_file",
        "description": (
            "Read the full contents of a file. "
            "Use for reviewing code, configs, or documentation before editing. "
            "Path is relative to the sandbox directory."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to sandbox, e.g. 'src/utils.py'"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": (
            "Write content to a file, creating it if it doesn't exist. "
            "Overwrites existing content. Creates parent directories automatically. "
            "Use for creating new files or fully replacing file contents."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to sandbox"},
                "content": {"type": "string", "description": "Full file content to write"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "run_bash",
        "description": (
            "Execute a shell command in the sandbox directory. "
            "Use for running tests (pytest, python -m unittest), linters (ruff, flake8), or build commands. "
            "Always provide a description of what the command does. "
            "Timeout: 30 seconds. Working directory: sandbox."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to run"},
                "description": {"type": "string", "description": "What this command does"},
            },
            "required": ["command", "description"],
        },
    },
    {
        "name": "list_files",
        "description": (
            "List all files in a directory recursively. "
            "Use to understand what's in the sandbox before reading or editing. "
            "Defaults to listing the entire sandbox if no path given."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path relative to sandbox (default: '.' = entire sandbox)",
                }
            },
        },
    },
]


def process_tool(tool_name: str, tool_input: dict) -> str:
    try:
        if tool_name == "read_file":
            fp = SANDBOX / tool_input["path"]
            return fp.read_text() if fp.exists() else f"Error: {tool_input['path']} not found"

        if tool_name == "write_file":
            fp = SANDBOX / tool_input["path"]
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(tool_input["content"])
            return f"Wrote {len(tool_input['content'])} chars to {tool_input['path']}"

        if tool_name == "run_bash":
            print(f"  [bash] {tool_input['description']}: {tool_input['command']}")
            result = subprocess.run(
                tool_input["command"],
                shell=True,
                cwd=SANDBOX,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = (result.stdout + result.stderr).strip()
            return output or "(no output)"

        if tool_name == "list_files":
            base = SANDBOX / tool_input.get("path", ".")
            files = [f.relative_to(SANDBOX) for f in base.rglob("*") if f.is_file()]
            return "\n".join(str(f) for f in files) if files else "(empty)"

    except subprocess.TimeoutExpired:
        return "Error: command timed out after 30s"
    except Exception as e:
        return f"Error: {e}"


def run_dev_agent(task: str) -> str:
    print(f"\nTask: {task}\n{'=' * 60}")
    messages = [{"role": "user", "content": task}]
    system = (
        "You are a developer productivity agent. Complete coding tasks using your tools.\n"
        "Workflow: list files to understand context → read relevant files → write code → run tests to verify.\n"
        "Always verify your work by running tests before reporting completion."
    )

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = process_tool(block.name, block.input)
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result}
                    )
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    task = (
        "Create a Python module `string_utils.py` with three functions:\n"
        "1. reverse_words(text) — reverses word order in a string\n"
        "2. count_vowels(text) — counts vowels (a e i o u, case-insensitive)\n"
        "3. is_palindrome(text) — checks if text is a palindrome (ignore case and spaces)\n\n"
        "Then write `test_string_utils.py` with tests for each function and run them with Python."
    )
    result = run_dev_agent(task)
    print(f"\n{'=' * 60}\nResult:\n{result}")
