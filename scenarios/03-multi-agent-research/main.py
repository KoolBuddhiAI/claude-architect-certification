import anthropic
import json

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

SUBAGENT_PROMPTS = {
    "researcher": (
        "You are a research specialist. Gather comprehensive, factual information on the given topic. "
        "Be thorough and cover multiple angles. Cite key points clearly."
    ),
    "analyst": (
        "You are a data analyst. Extract patterns, trends, and insights from the provided information. "
        "Provide structured analysis with clear, evidence-backed conclusions."
    ),
    "synthesizer": (
        "You are a synthesis expert. Combine multiple pieces of research and analysis into a coherent, "
        "well-structured final report. Prioritize clarity and actionable takeaways."
    ),
}

orchestrator_tools = [
    {
        "name": "run_researcher",
        "description": (
            "Delegate a research task to the researcher subagent. "
            "Use to gather broad, factual coverage of a topic or subtopic. "
            "Always run before analysis. "
            "Include full context in 'topic' and 'focus' — subagent has no memory of prior steps."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The subject to research"},
                "focus": {"type": "string", "description": "Specific aspect or angle to emphasize"},
            },
            "required": ["topic", "focus"],
        },
    },
    {
        "name": "run_analyst",
        "description": (
            "Delegate an analysis task to the analyst subagent. "
            "Use to extract patterns, insights, and conclusions from gathered research. "
            "Pass the full research text in 'data' — subagent has no memory of prior steps."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "Full research text to analyze"},
                "question": {"type": "string", "description": "The analytical question to answer"},
            },
            "required": ["data", "question"],
        },
    },
    {
        "name": "run_synthesizer",
        "description": (
            "Delegate synthesis to the synthesizer subagent. "
            "Use after research and analysis are complete to produce the final report. "
            "Pass ALL prior results in 'inputs' — subagent has no memory of prior steps."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "inputs": {"type": "string", "description": "All research and analysis text to synthesize"},
                "format": {"type": "string", "description": "Desired output format or structure for the report"},
            },
            "required": ["inputs", "format"],
        },
    },
]


def run_subagent(role: str, task: str, context: str = "") -> str:
    content = f"{context}\n\nTask: {task}" if context else task
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SUBAGENT_PROMPTS[role],
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text


def run_orchestrator(research_question: str) -> str:
    print(f"\nResearch Question: {research_question}\n{'=' * 60}")

    messages = [{"role": "user", "content": f"Research this question thoroughly: {research_question}"}]
    system = (
        "You are a research orchestrator. Decompose complex research questions and coordinate subagents:\n"
        "1. Use run_researcher to gather information on specific subtopics\n"
        "2. Use run_analyst to extract insights from research\n"
        "3. Use run_synthesizer to produce the final report\n\n"
        "CRITICAL: Subagents have NO shared memory. Pass all relevant context explicitly in every call."
    )

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system,
            tools=orchestrator_tools,
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
                    print(f"\n[Orchestrator → {block.name}]")

                    if block.name == "run_researcher":
                        result = run_subagent(
                            "researcher",
                            f"Research '{block.input['focus']}' about: {block.input['topic']}",
                        )
                    elif block.name == "run_analyst":
                        result = run_subagent(
                            "analyst",
                            block.input["question"],
                            context=block.input["data"],
                        )
                    elif block.name == "run_synthesizer":
                        result = run_subagent(
                            "synthesizer",
                            f"Synthesize into: {block.input['format']}",
                            context=block.input["inputs"],
                        )
                    else:
                        result = "Unknown tool"

                    print(f"  [preview] {result[:120]}...")
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result}
                    )

            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    question = "What are the key architectural patterns for building reliable multi-agent AI systems?"
    report = run_orchestrator(question)
    print(f"\n{'=' * 60}\nFINAL REPORT\n{'=' * 60}\n{report}")
