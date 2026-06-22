# AI-Native Data Engineering — Training Curriculum

## Who This Is For
Data engineers who want to stay relevant and deliver more value in an AI-accelerated world — without abandoning the rigor that enterprise environments demand.

## The Core Premise
> "The goal is not to replace the data engineer. It is to make one data engineer worth ten."

Enterprise data engineering with AI requires two things most training misses:
1. **A new mindset** — you are now an architect and orchestrator, not just a coder
2. **Disciplined methodology** — enterprise AI development needs structure, not vibes

## Curriculum Map

| Module | Topic | Format | Duration |
|--------|-------|--------|----------|
| 00 | The Mindset Shift | Slides + Guide | 2 hrs |
| 01 | AI Landscape for Data Engineers | Slides + Guide | 3 hrs |
| 06 | The Missing Phase: Problem → Requirements → Acceptance Criteria | Slides + Guide + Exercises | 3 hrs |
| 02 | BMAD for Data Engineering | Slides + Guide + Worksheet | 4 hrs |
| 03 | Workflow Transformation | Slides + Mapping Guide | 3 hrs |
| 04 | Open Stack Guide | Slides + TCO Analysis | 2 hrs |
| 05 | Enterprise Patterns | Slides + Guide | 3 hrs |

**Total**: ~20 hours of structured learning + hands-on labs (scenarios in `../`)

## Learning Path

```
Module 00 (Mindset)
    ↓
Module 01 (Landscape) ←── Read references/tools-catalog.md alongside
    ↓
Module 06 (The Missing Phase) ←── WHY process matters before you learn the process
    ↓
Module 02 (BMAD Methodology) ←── Core methodology — do not skip
    ↓
Module 03 (Workflow Mapping) ←── Apply to your current role
    ↓
Module 04 (Stack Guide) ←── Choose your tools
    ↓
Module 05 (Enterprise Patterns) ←── Production readiness
    ↓
Hands-on Labs: ../ scenarios 01–05
```

## Slide Deck Format
All `slides.md` files use [Marp](https://marp.app/) markdown — convert to PowerPoint or PDF with:
```bash
npx @marp-team/marp-cli slides.md --pptx   # PowerPoint
npx @marp-team/marp-cli slides.md --pdf    # PDF
```

## Reference Files
- `references/tools-catalog.md` — every tool, framework, MCP server worth knowing
- `references/skills-catalog.md` — Claude Code skills for data engineers
- `references/mcp-servers.md` — MCP server setup for common data stacks
- `references/further-reading.md` — articles, papers, videos, docs
