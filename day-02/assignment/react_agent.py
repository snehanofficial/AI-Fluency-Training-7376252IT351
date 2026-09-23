"""ReAct Agent implementation for Day 02 assignment.
The ReAct Agent interleaves Thought, Action (tool call), Observation (tool result), and synthesis.
"""
import json
from config import client, MODEL, banner
from tools import TOOLS, TOOL_FUNCTIONS

REACT_SYSTEM_PROMPT = (
    "You are Apex Logistics AI Agent. You reason step-by-step and have access to external tools "
    "for private tariff lookup, port congestion statistics, and precise tariff calculations.\n"
    "Rule 1: NEVER guess private data (customs duty rates or port congestion delays). Always call the corresponding tool.\n"
    "Rule 2: For calculations, use the calculate_duty_and_total tool.\n"
    "Rule 3: Follow the ReAct cycle: Reason (Thought) -> Call Tool (Action) -> Inspect Result (Observation) -> Synthesize Final Answer.\n"
    "If no tool is needed, answer directly."
)

def run_react_agent(question: str, max_steps: int = 6, verbose: bool = True) -> dict:
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    trace = []

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )
        message = response.choices[0].message
        content = message.content or ""

        if content and verbose:
            print(f"  [Step {step} Thought] {content}")
        trace.append({"step": step, "thought": content, "tool_calls": []})

        if not message.tool_calls:
            return {
                "final_answer": content.strip(),
                "trace": trace,
                "steps": step
            }

        # Assistant tool requests
        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # Execute tool calls
        for call in message.tool_calls:
            tool_name = call.function.name
            try:
                kwargs = json.loads(call.function.arguments or "{}")
            except Exception:
                kwargs = {}
            
            fn = TOOL_FUNCTIONS.get(tool_name)
            if fn:
                result = fn(**kwargs)
            else:
                result = {"status": "error", "message": f"Tool '{tool_name}' not found"}

            if verbose:
                print(f"  [Step {step} Action] Call {tool_name}({kwargs})")
                print(f"  [Step {step} Observation] {result}")

            trace[-1]["tool_calls"].append({
                "tool": tool_name,
                "args": kwargs,
                "result": result
            })

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)
            })

    return {
        "final_answer": "ReAct agent reached maximum step limit without resolving.",
        "trace": trace,
        "steps": max_steps
    }

if __name__ == "__main__":
    from config import QUESTIONS
    banner("REACT AGENT DEMONSTRATION")
    for q in QUESTIONS:
        print(f"[{q['id']}] Question: {q['text']}")
        res = run_react_agent(q["text"], verbose=True)
        print(f"\nFinal Answer:\n{res['final_answer']}\n")
        print("=" * 80)
