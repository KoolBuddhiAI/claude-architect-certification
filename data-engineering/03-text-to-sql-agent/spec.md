# Scenario DE-03: Text-to-SQL Agent

## What This Demonstrates
An agent that translates natural language questions into validated, executable SQL against a live schema — using runtime schema introspection and a validation-retry loop to handle generation errors.

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Tool Design & MCP Integration | 18% | Runtime schema introspection, SQL execution tool |
| Context Management & Reliability | 15% | Validation-retry loop, graceful error handling |
| Prompt Engineering | 20% | Schema-in-context, correction prompting |

## Key Architectural Decisions

### Runtime Schema Introspection
`get_schema` fetches the live database schema at query time rather than embedding it in the system prompt. This means:
- Schema changes are reflected immediately
- No stale column names in the prompt
- Token usage scales with query complexity, not total schema size

### Validation-Retry Loop
```
generate SQL → validate_sql (syntax check) → execute_sql → if error → retry with error context
```
Max 3 retries. Each retry includes the previous SQL, the error, and a corrective instruction. Returns last attempt even if all retries fail — caller decides how to handle.

### Dry-Run Before Execute
`validate_sql` runs `EXPLAIN QUERY PLAN` on the generated SQL before execution. Catches:
- Syntax errors
- References to non-existent tables/columns
- Missing JOIN conditions

### Structured Result Output
`execute_sql` returns rows as JSON arrays with column names. Limits to 100 rows by default to prevent runaway result sets.

## Sample Questions Demonstrated
1. "How many orders did each customer place in June 2026?"
2. "What are the top 3 products by total revenue?"
3. "Show customers who haven't placed an order in the last 30 days"

## Database Schema
```sql
customers(id, name, email, created_at)
products(id, name, category, price)
orders(id, customer_id, created_at, status, total_amount)
order_items(id, order_id, product_id, quantity, unit_price)
```

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Static schema in system prompt | `get_schema` tool at runtime |
| Execute SQL immediately | `validate_sql` before `execute_sql` |
| Crash on SQL error | Retry with error context, return last attempt |
| No row limit | Default LIMIT 100 in execute_sql |

## Learning Objectives
1. Implement runtime schema introspection as a tool
2. Build validation-retry loop for generated code
3. Design correction prompts that include error context
4. Limit blast radius of tool execution (row caps, dry-runs)

## How to Run
```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```
