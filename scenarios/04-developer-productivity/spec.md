# Scenario 4: Developer Productivity Tools

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Tool Design & MCP Integration | 18% | Tool descriptions, error handling, least-privilege |
| Claude Code Configuration & Workflows | 20% | Read/Write/Bash tool patterns, sandboxed execution |
| Agentic Architecture & Orchestration | 27% | Agentic loop, task completion detection |

## What This Demonstrates
A developer productivity agent that uses Read, Write, and Bash tools to complete a coding task end-to-end — creates files, writes tests, and verifies correctness by running them. Models the same tool patterns Claude Code uses internally.

## Key Architectural Decisions
- **Sandboxed execution**: All file I/O and Bash commands restricted to `/tmp/dev-productivity-sandbox`
- **Tool descriptions with scope**: Each tool description specifies what it does, when to use it, and constraints
- **Least-privilege Bash**: Command execution has a 30-second timeout and sandbox working directory
- **Agentic loop**: Agent decides when the task is done — not the caller
- **Error surfacing**: Tool errors returned as strings, not exceptions — keeps the agent loop running

## Tool Design Principles Shown
| Tool | Description Quality | Why It Matters |
|------|--------------------|-|
| `read_file` | States purpose + format expectation | Prevents misuse for non-code files |
| `write_file` | Includes parent-dir creation note | Prevents cascading failures |
| `run_bash` | Requires `description` field | Forces model to state intent before acting |
| `list_files` | Explicit default value documented | Prevents ambiguous empty input |

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Generic `"Execute a command"` description | Description states constraints and purpose |
| Raising exceptions from tools | Return error strings to keep agent loop alive |
| Unrestricted file system access | Sandbox directory enforced at tool layer |

## Learning Objectives
1. Design Read/Write/Bash tool analogs with production-quality descriptions
2. Implement sandboxed execution with proper constraints
3. Surface tool errors gracefully without breaking the agent loop
4. Observe how an agent plans, executes, and verifies a coding task

## How to Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```

## Expected Output
Agent creates `string_utils.py`, writes `test_string_utils.py`, runs the tests, and reports results. Files land in `/tmp/dev-productivity-sandbox/`.
