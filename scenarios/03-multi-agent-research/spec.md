# Scenario 3: Multi-Agent Research System

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Agentic Architecture & Orchestration | 27% | Orchestrator-subagent, task decomposition, parallel coordination |
| Prompt Engineering & Structured Output | 20% | Subagent system prompts, explicit context passing |

## What This Demonstrates
An orchestrator agent that decomposes a complex research question into subtasks and delegates each to a specialized subagent (researcher, analyst, synthesizer). Each subagent runs as a separate API call with no shared memory — context is passed explicitly.

## Key Architectural Decisions
- **Orchestrator-subagent model**: Orchestrator owns the plan; subagents own execution
- **Explicit context passing**: Subagents have isolated contexts — every relevant detail is included in the task prompt, never assumed
- **Specialized system prompts**: Each subagent role has a tailored system prompt that shapes its behavior
- **Sequential then synthesize**: Researcher → Analyst → Synthesizer ordering enforced through tool design
- **No implicit state**: Results collected in `dict`, passed explicitly to next stage

## Subagent Roles
| Role | Responsibility | System Prompt Focus |
|------|---------------|---------------------|
| Researcher | Gather comprehensive information | Thorough, factual, breadth |
| Analyst | Extract patterns and insights | Structured analysis, conclusions |
| Synthesizer | Combine into final report | Clarity, actionability |

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Assuming subagents share context | Every subagent call includes full context |
| Untyped tool inputs | Each delegation tool has typed input schema |
| Free-form orchestration output | Orchestrator uses tools to delegate, not text |

## Learning Objectives
1. Implement orchestrator-subagent coordination with the Claude API
2. Design delegation tools with rich descriptions and typed schemas
3. Pass explicit context — never rely on implicit shared state
4. Structure subagent system prompts for specialized roles
5. Collect and route results between pipeline stages

## How to Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```

## Expected Output
Orchestrator delegates to researcher → analyst → synthesizer, printing each handoff. Final synthesized report printed at end.
