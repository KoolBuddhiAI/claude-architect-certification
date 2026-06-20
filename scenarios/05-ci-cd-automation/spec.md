# Scenario 5: Claude Code in CI/CD

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Claude Code Configuration & Workflows | 20% | Headless mode, JSON output, CI integration |
| Prompt Engineering & Structured Output | 20% | Schema enforcement, tool_choice forcing, validation |
| Tool Design & MCP Integration | 18% | Review tool schema design |

## What This Demonstrates
An automated code reviewer that runs in a CI/CD pipeline. Takes a git diff, produces a structured JSON review via schema-enforced tool use, and exits with the correct code (0 = approved, 1 = blocked). Designed to run headlessly with no interactive output.

## Key Architectural Decisions
- **`tool_choice: {"type": "any"}`**: Forces tool use on every call — prevents free-text fallback that would break JSON parsing downstream
- **Schema-enforced output**: Review structure defined as a JSON Schema; model cannot produce invalid output
- **CI exit codes**: `sys.exit(1)` on critical issues; `sys.exit(0)` on approval — integrates with any CI system
- **Severity taxonomy**: `critical > major > minor > suggestion` with only `critical` blocking approval
- **Programmatic enforcement**: Approval gate is in code, not in the model's judgment alone

## Review Schema Fields
| Field | Type | Purpose |
|-------|------|---------|
| `approved` | boolean | CI gate decision |
| `score` | 0–100 | Quality metric for dashboards |
| `issues[].severity` | enum | Determines if PR is blocked |
| `issues[].category` | enum | Routes to correct team/tool |
| `required_changes` | string[] | Actionable blocklist |

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Parsing approval from response text | `approved` boolean field in schema |
| No exit code | `sys.exit(1)` on critical issues |
| Untyped free-form output | Full JSON Schema with enums |
| `tool_choice` omitted | `{"type": "any"}` forces structured output |

## Learning Objectives
1. Use `tool_choice` to enforce structured output in CI contexts
2. Design a review schema with severity taxonomy and approval gate
3. Map tool output to CI exit codes
4. Write system prompts calibrated for automated (non-interactive) contexts

## How to Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
echo "Exit code: $?"
```

## CI Integration Example
```yaml
# .github/workflows/review.yml
- name: AI Code Review
  run: python scenarios/05-ci-cd-automation/main.py
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```
