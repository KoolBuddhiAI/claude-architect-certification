# Scenario 6: Structured Data Extraction

## CCA-F Domain Alignment
| Domain | Weight | Coverage |
|--------|--------|----------|
| Prompt Engineering & Structured Output | 20% | JSON schema tools, validation-retry loop, schema enforcement |
| Context Management & Reliability | 15% | Retry logic, confidence scoring, graceful degradation |
| Tool Design & MCP Integration | 18% | Extraction tool schema design |

## What This Demonstrates
A production-grade data extraction pipeline that pulls structured data from unstructured text using schema-enforced tool use. Includes a confidence-scored validation-retry loop that re-prompts the model when extraction quality is too low.

## Key Architectural Decisions
- **Tool-as-schema**: The extraction target is defined as a tool's `input_schema` — the model fills it like a form, guaranteeing structure
- **Confidence field**: Model self-reports extraction confidence (0–1); low scores trigger retry
- **Validation-retry loop**: Up to `max_retries` attempts; each retry includes the previous tool result + corrective instruction
- **Null for missing**: System prompt instructs model to use `null` rather than fabricate values
- **Reusable factory**: `make_extraction_tool()` generates tools for any target schema — not hardcoded to invoices

## Retry Logic
```
attempt 1 → confidence < 0.3 → retry with correction prompt
attempt 2 → confidence >= 0.3 → return result
```
Even at max retries, returns best attempt rather than crashing — caller decides how to handle low-confidence results.

## Anti-Patterns Avoided
| Anti-Pattern | Correct Approach |
|---|---|
| Parsing JSON from response text with regex | Schema-enforced tool use |
| Crashing on extraction failure | Return best attempt with confidence score |
| Fabricating missing fields | System prompt instructs: use `null` for unknowns |
| Single-shot extraction | Validation-retry loop with corrective feedback |

## Learning Objectives
1. Use tools as output schemas for guaranteed structure
2. Implement validation-retry loops with corrective feedback
3. Add confidence scoring to guide downstream decisions
4. Build a reusable extraction factory for different document types
5. Handle partial extraction gracefully

## How to Run
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python main.py
```

## Expected Output
Structured JSON invoice object extracted from the sample unstructured invoice text, with confidence score and all detected line items.

## Extending to Other Document Types
```python
# Example: Extract job posting data
JOB_TOOL = make_extraction_tool("job_posting", "Extract job posting data", {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "company": {"type": "string"},
        "salary_range": {"type": "object", ...},
        "requirements": {"type": "array", ...}
    }
})
result = extract_structured_data(raw_job_text, JOB_TOOL)
```
