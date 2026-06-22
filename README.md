# Claude Architect Certification — Study Workspace

Prep material for the **Claude Certified Architect – Foundations (CCA-F)** exam, plus runnable
reference scenarios that demonstrate each architecture concept against a live Claude(-compatible) API.

---

## 📚 Visual study series (artifacts)

Interactive, single-page study notes — one per scenario, in a shared blueprint-schematic design.
Start at the index, skim the cheat sheet, then go deep where you're weakest.

> **Note:** these are **private artifacts** on your claude.ai account (logged in as `buddhi@bistecglobal.com`).
> They open in the browser. Use the artifact UI's share control if you want teammates to access them.

| | Page | Core thesis | Exam domains |
|---|------|-------------|--------------|
| 📚 | **[Index — the whole series](https://claude.ai/code/artifact/a9a869d8-46e1-443a-af80-7c5261873f09)** | start here | — |
| 🎯 | **[Cheat sheet](https://claude.ai/code/artifact/3ae09c1f-bd4a-4867-b702-83a1b21a0661)** | highest-yield facts, all domains | all |
| 🔁 | [01 · The Agentic Loop](https://claude.ai/code/artifact/4d601d58-77e0-477a-aad7-cd63f7d799ba) | *Exit on the signal, not the sentence.* | Agentic 27% · Tool 18% |
| ⚙️ | [02 · Team Configuration](https://claude.ai/code/artifact/89c2a28c-75da-4c3a-990d-a6d8602eb811) | *Memory shapes behavior. Hooks enforce it.* | Claude Code 20% · Tool/MCP 18% |
| 🕸️ | [03 · Multi-Agent Research](https://claude.ai/code/artifact/e46bf12e-7989-4666-add3-8dd9640fad06) | *Subagents start blind. The brief is everything.* | Agentic 27% · Structured 20% |
| 🛠️ | [04 · Developer Productivity](https://claude.ai/code/artifact/79ff12d1-130f-4cce-9a7a-17b70a003e1d) | *Give the agent hands — inside a sandbox.* | Agentic 27% · Claude Code 20% · Tool 18% |
| 🚦 | [05 · Claude Code in CI/CD](https://claude.ai/code/artifact/8487e0e0-5a4a-4f49-ab4a-0fca264e5eb5) | *The gate is in code, not the model's judgment.* | Claude Code 20% · Structured 20% · Tool 18% |
| 📑 | [06 · Structured Data Extraction](https://claude.ai/code/artifact/efc533d7-4f20-4635-9ab0-1445c93c4ba1) | *Valid JSON isn't correct data.* | Structured 20% · Tool 18% · Context 15% |

Source HTML for each page is in the session scratchpad; the published artifacts are the canonical copies.

---

## 📖 Source guide

`Docs/claude-architect-exam-guide.epub` — the community CCA-F Foundations study guide. The study pages
above distill its chapters:

| Guide chapter | Scenario(s) |
|---|---|
| 1 · API Fundamentals & Output Control | 01, 05, 06 |
| 2 · Designing Tool Interfaces | 01, 04 |
| 3 · Error Handling in Agent Tools | 01, 04 |
| 4 · Structured Data Extraction & Validation | 06 |
| 7 · Model Context Protocol (MCP) | 02 |
| 8 · Agentic Patterns & Task Decomposition | 03, 04 |
| 9 · Customer Service & Production Workflow | 01 |
| 10 · Claude Code & Agent SDK Workflows | 02, 04, 05 |
| 12 · Model Selection & Inference Controls | 05 |
| 16 · Quick Reference Cheat Sheet | cheat sheet |

---

## ▶️ Running the scenarios

Scenarios 01, 03, 04, 05, 06 are runnable Python (scenario 02 is Claude Code config — no script).
They use the `anthropic` SDK, pointed at a **MiniMax Anthropic-compatible endpoint**.

### One-time setup

```bash
# from this directory
python3 -m venv .venv
./.venv/bin/pip install -r scenarios/requirements.txt

cp env.example .env          # then edit .env and paste your MiniMax API key
```

`.env` (gitignored) holds:

```ini
ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic   # MiniMax intl Anthropic-compatible API
ANTHROPIC_API_KEY=<your_minimax_key>
MODEL=MiniMax-M3
```

The `anthropic` SDK reads `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` automatically; each `main.py`
reads `MODEL` from the environment (default `claude-sonnet-4-6` if unset). To run against the real
Anthropic API instead, point those three vars at Anthropic and a `claude-*` model.

### Run

```bash
./run.sh          # all runnable scenarios (01, 03, 04, 05, 06)
./run.sh 05       # just one
```

`run.sh` sources `.env`, activates the venv, and prints each scenario's output and exit code.

---

## Layout

```
claude-architect-certification/
├── README.md                 # this file
├── CLAUDE.md                 # project instructions for Claude Code
├── Docs/                     # CCA-F study guide (epub)
├── env.example               # copy to .env, add MiniMax key
├── run.sh                    # run scenarios against MiniMax
└── scenarios/
    ├── requirements.txt
    ├── 01-customer-support-agent/    # agentic loop, stop_reason, escalation
    ├── 02-claude-code-team-config/   # CLAUDE.md, rules, hooks, permissions, MCP (config only)
    ├── 03-multi-agent-research/      # orchestrator → researcher/analyst/synthesizer
    ├── 04-developer-productivity/    # sandboxed Read/Write/Bash agent
    ├── 05-ci-cd-automation/          # headless review, tool_choice, exit codes
    └── 06-structured-data-extraction/ # tool-as-schema + validation-retry loop
```

---

*Independent study material — not affiliated with or endorsed by Anthropic. Verify model ids, limits,
and prices against [docs.claude.com](https://docs.claude.com) at exam time.*
