import anthropic
import json
import os

client = anthropic.Anthropic()
MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = (
    "You are a data extraction specialist. Extract structured information from unstructured text.\n\n"
    "Rules:\n"
    "- Extract only what is explicitly stated — never infer or fabricate values\n"
    "- Use null for optional fields that are absent or ambiguous\n"
    "- Set confidence: 0.9+ for clearly stated data, 0.5-0.89 for partially clear, <0.5 for ambiguous\n"
    "- Always call the extraction tool with your findings"
)


def make_extraction_tool(schema_name: str, description: str, schema: dict) -> dict:
    return {"name": f"extract_{schema_name}", "description": description, "input_schema": schema}


INVOICE_TOOL = make_extraction_tool(
    "invoice",
    "Extract structured invoice data from unstructured text. Call once with all found data.",
    {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string"},
            "date": {"type": "string", "description": "ISO 8601 format (YYYY-MM-DD)"},
            "vendor": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "address": {"type": "string"},
                    "tax_id": {"type": "string"},
                },
                "required": ["name"],
            },
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "total": {"type": "number"},
                    },
                    "required": ["description", "total"],
                },
            },
            "subtotal": {"type": "number"},
            "tax_amount": {"type": "number"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string"},
            "payment_terms": {"type": "string"},
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Extraction confidence: 0.9+ clear, 0.5-0.89 partial, <0.5 ambiguous",
            },
        },
        "required": ["vendor", "line_items", "total_amount", "confidence"],
    },
)


def extract_structured_data(raw_text: str, tool: dict, max_retries: int = 3) -> dict:
    messages = [{"role": "user", "content": f"Extract structured data from this text:\n\n{raw_text}"}]
    last_result = None

    for attempt in range(1, max_retries + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=[tool],
            tool_choice={"type": "any"},
            messages=messages,
        )

        tool_block = next((b for b in response.content if b.type == "tool_use"), None)
        if not tool_block:
            break

        last_result = tool_block.input
        confidence = last_result.get("confidence", 1.0)

        if confidence >= 0.3:
            print(f"Extracted on attempt {attempt} (confidence: {confidence:.2f})")
            return last_result

        print(f"Attempt {attempt}: low confidence ({confidence:.2f}), retrying...")
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": "Confidence too low. Re-examine the source text more carefully before re-extracting.",
            }],
        })

    print(f"Returning best attempt (confidence: {last_result.get('confidence', 0):.2f})")
    return last_result or {}


if __name__ == "__main__":
    raw_invoice = """
    INVOICE

    TechSupplies Co., Ltd.
    123 Industrial Ave, San Francisco, CA 94105
    Tax ID: 12-3456789

    Bill To: Acme Corp

    Invoice #: INV-2026-0847
    Date: June 15, 2026
    Payment Terms: Net 30

    ITEMS:
    - MacBook Pro 14" M4 (x2) ............ $3,199.00 each = $6,398.00
    - USB-C Hub 7-port (x5) .............. $49.99 each = $249.95
    - Annual Software License ............. $1,200.00

    Subtotal: $7,847.95
    Tax (8.5%): $667.08
    TOTAL DUE: $8,515.03 USD

    Please remit payment within 30 days to avoid late fees.
    """

    print("Extracting invoice data...\n")
    result = extract_structured_data(raw_invoice, INVOICE_TOOL)
    print(json.dumps(result, indent=2))
