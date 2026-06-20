import anthropic
import json
from typing import Any

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

ORDERS = {
    "ORD-001": {"status": "shipped", "item": "Laptop", "delivery": "2026-06-22"},
    "ORD-002": {"status": "processing", "item": "Headphones", "delivery": "2026-06-25"},
    "ORD-003": {"status": "delivered", "item": "Mouse", "delivery": "2026-06-18"},
}

POLICIES = {
    "return": "Items can be returned within 30 days of delivery with original packaging.",
    "shipping": "Standard shipping takes 3-5 business days. Expedited takes 1-2 days.",
    "warranty": "All electronics come with a 1-year manufacturer warranty.",
}

tools = [
    {
        "name": "lookup_order",
        "description": (
            "Look up the status and details of a customer order by order ID. "
            "Input: order_id like 'ORD-001'. Use when a customer references an order number. "
            "Returns status, item, and estimated delivery. Returns an error if order not found."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, e.g. ORD-001"}
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "check_policy",
        "description": (
            "Retrieve the company policy for a given topic. "
            "Topics: 'return' (eligibility window and conditions), "
            "'shipping' (timeframes and options), 'warranty' (coverage duration). "
            "Use before answering policy questions rather than relying on assumptions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": ["return", "shipping", "warranty"],
                    "description": "Policy topic to retrieve",
                }
            },
            "required": ["topic"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Escalate this conversation to a human support agent. "
            "Use when: the customer is frustrated or upset, the issue requires manual intervention, "
            "policy exceptions are needed, or the situation is outside automated resolution scope. "
            "Do NOT use for simple queries you can answer directly."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Why human escalation is needed"},
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "high = frustrated customer or refund >$500, medium = complex policy exception, low = general inquiry",
                },
            },
            "required": ["reason", "priority"],
        },
    },
]


def process_tool_call(tool_name: str, tool_input: dict) -> Any:
    if tool_name == "lookup_order":
        order_id = tool_input["order_id"]
        return ORDERS.get(order_id, {"error": f"Order {order_id} not found"})
    if tool_name == "check_policy":
        topic = tool_input["topic"]
        return {"policy": POLICIES.get(topic, "Policy not found")}
    if tool_name == "escalate_to_human":
        ticket_id = f"TKT-{abs(hash(tool_input['reason'])) % 100000:05d}"
        return {
            "escalated": True,
            "ticket_id": ticket_id,
            "message": f"Escalated ({tool_input['priority']} priority). A human agent will contact you shortly.",
        }


def run_support_agent(customer_query: str) -> str:
    print(f"\nCustomer: {customer_query}")
    messages = [{"role": "user", "content": customer_query}]
    system = [
        {
            "type": "text",
            "text": (
                "You are a helpful customer support agent. Use the available tools to resolve queries. "
                "Always look up order status before discussing it. Always check policy before quoting it. "
                "Escalate to a human when the customer is upset, when a policy exception is needed, "
                "or when you cannot resolve the issue. Be empathetic and professional."
            ),
            "cache_control": {"type": "ephemeral"},
        }
    ]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [tool] {block.name}({json.dumps(block.input)})")
                    result = process_tool_call(block.name, block.input)
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                    )
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    queries = [
        "What's the status of my order ORD-001?",
        "I want to return my mouse from ORD-003 but it was delivered 2 months ago and I'm really frustrated!",
        "What's your return policy?",
    ]
    for query in queries:
        answer = run_support_agent(query)
        print(f"Agent: {answer}\n{'=' * 60}")
