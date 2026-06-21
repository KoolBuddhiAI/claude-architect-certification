# Scenario DE-04: Schema Evolution Agent

## What This Demonstrates
An agent that compares two versions of a database schema, classifies each change as breaking or non-breaking, and generates safe migration SQL with rollback statements.

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Agentic Architecture & Orchestration | 27% | Multi-step analysis: diff → classify → generate → validate |
| Prompt Engineering & Structured Output | 20% | Schema-enforced migration report |
| Tool Design & MCP Integration | 18% | Diff and generation tools |

## Key Architectural Decisions

### Breaking vs Non-Breaking Classification
| Change Type | Classification | Why |
|---|---|---|
| Add nullable column | Non-breaking | Existing queries unaffected |
| Add NOT NULL column without default | Breaking | Existing INSERT statements fail |
| Remove column | Breaking | Existing SELECT/WHERE may reference it |
| Change column type (widening) | Non-breaking | e.g. INT → BIGINT |
| Change column type (narrowing) | Breaking | Data loss risk |
| Add index | Non-breaking | Read-only performance change |
| Drop index | Non-breaking | Performance regression only |
| Add foreign key constraint | Potentially breaking | Existing data may violate it |
| Rename column | Breaking | All references must update |

### Migration Safety Rules
- Every `ALTER TABLE ADD COLUMN` includes a DEFAULT or is nullable
- Every destructive change (`DROP COLUMN`) generates both forward and rollback SQL
- NOT NULL additions always use a two-step migration (add nullable → backfill → add constraint)

### Structured Migration Output
`submit_migration_plan` enforces: change list with classifications, forward SQL, rollback SQL, deployment risk level, and pre-deployment checklist.

## Schema Versions in This Example
**V1 → V2 Changes:**
- `orders`: Add `discount_amount DECIMAL(10,2)` column (non-breaking)
- `orders`: Remove `legacy_ref TEXT` column (breaking)
- `customers`: Change `phone VARCHAR(15)` → `phone VARCHAR(20)` (non-breaking widening)
- `products`: Add NOT NULL `sku VARCHAR(50)` column without default (breaking)
- New table: `promotions` (non-breaking)

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Treating all changes as equal | Explicit breaking/non-breaking taxonomy |
| Forward migration only | Every destructive change has rollback SQL |
| Adding NOT NULL directly | Two-step: add nullable → backfill → constraint |
| Manual schema comparison | `diff_schemas` tool with structured output |

## Learning Objectives
1. Implement schema diffing as a structured tool
2. Classify changes with explicit breaking/non-breaking reasoning
3. Generate safe multi-step migrations for destructive changes
4. Produce deployment checklists from schema analysis

## How to Run
```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```
