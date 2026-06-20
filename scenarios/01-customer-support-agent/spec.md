# Scenario 1: Customer Support Resolution Agent

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Agentic Architecture & Orchestration | 27% | Agent loop, stop_reason, escalation |
| Tool Design & MCP Integration | 18% | Tool descriptions, error responses |

## What This Demonstrates
An agent that resolves customer queries using tools, recognizes when to escalate to a human, and never terminates based on parsing response text — it uses `stop_reason == "end_turn"` as the correct completion signal.

## Key Architectural Decisions
- **stop_reason guard**: Loop continues only while `stop_reason == "tool_use"`; exits cleanly on `"end_turn"`
- **Escalation tool**: Explicit tool with priority levels — not inferred from conversation text
- **Rich tool descriptions**: Each tool specifies input formats, edge cases, and when to prefer it over alternatives
- **No shared state**: Each tool call is stateless; context lives in the message thread

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| `if "I'll escalate" in response.text` | Dedicated `escalate_to_human` tool |
| Loop breaks after N iterations | Loop breaks only on `stop_reason == "end_turn"` |
| Vague tool descriptions | Descriptions include edge cases and when-to-use guidance |

## Learning Objectives
1. Implement a correct agentic loop using `stop_reason`
2. Design escalation as a first-class tool, not a text pattern
3. Write tool descriptions that prevent model confusion
4. Handle tool results correctly in the message thread

## How to Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```

## Expected Output
Three customer queries processed, showing tool calls and final agent responses. One query triggers escalation.
