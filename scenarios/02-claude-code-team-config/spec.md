# Scenario 2: Claude Code Team Configuration

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Claude Code Configuration & Workflows | 20% | CLAUDE.md hierarchy, settings.json, rules, hooks |
| Tool Design & MCP Integration | 18% | MCP server wiring in dev workflows |

## What This Demonstrates
A production-grade Claude Code configuration for a full-stack team. Shows the CLAUDE.md hierarchy, path-specific rules, permission scoping, hook definitions, and MCP server integration.

## Key Architectural Decisions
- **CLAUDE.md hierarchy**: Root file for global norms; path rules in `.claude/rules/` for domain-specific guidance
- **settings.json permissions**: Least-privilege tool allowlist — Bash is scoped, not open
- **PostToolUse hooks**: Automated linting after every file write
- **MCP server config**: `.mcp.json` wires external tools into the developer workflow
- **Headless/CI mode**: `--output-format json` flag pattern for automated pipelines

## File Structure
```
02-claude-code-team-config/
├── CLAUDE.md                    # Root project instructions
├── .claude/
│   ├── settings.json            # Permissions, hooks, MCP
│   └── rules/
│       ├── backend.md           # Python/FastAPI norms
│       └── frontend.md          # React/TypeScript norms
├── .mcp.json                    # MCP server definitions
└── scripts/
    └── ci-review.sh             # Headless CI usage example
```

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Single monolithic CLAUDE.md | Hierarchical rules with path scoping |
| Open `bash: ["*"]` permissions | Scoped allow-lists per command |
| No hooks | PostToolUse hooks enforce formatting automatically |

## Learning Objectives
1. Structure CLAUDE.md hierarchy for a multi-domain project
2. Configure least-privilege permissions in settings.json
3. Wire PostToolUse hooks for automated quality gates
4. Integrate MCP servers in the developer workflow
5. Use headless mode for CI/CD automation

## How to Use
This scenario is configuration — no Python to run. Load the project in Claude Code:
```bash
cd 02-claude-code-team-config
claude  # Claude Code reads CLAUDE.md and settings.json automatically
```
