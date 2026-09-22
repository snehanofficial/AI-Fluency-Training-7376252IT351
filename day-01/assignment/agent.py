"""System 3: An AI Agent combining LLM reasoning, tools, and execution loop."""
import json
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are an intelligent corporate IT Asset & Procurement Agent for TechCorp. "
    "You have access to tools to query private IT asset pricing and calculate exact costs. "
    "Rule 1: NEVER guess prices. Always use get_asset_price or list_all_assets for accurate private data. "
    "Rule 2: Use calculator for any mathematical computations or total calculations. "
    "Rule 3: If no tool is needed (e.g. creative writing), answer directly. "
    "Follow a clear plan: reason step-by-step, call tools as needed, observe outputs, and synthesize the final answer."
)

def agent(question: str, max_steps: int = 6, verbose: bool = True) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(1, max_steps + 1):
        # 1. REASON: LLM determines whether to call tools or respond
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )
        message = response.choices[0].message

        # 2. Check if agent finished without requesting tools
        if not message.tool_calls:
            return message.content.strip()

        # Record assistant tool requests in message history
        messages.append({
            "role": "assistant",
            "content": message.content or "",
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

        # 3. ACT & OBSERVE: execute functions and pass results back to loop
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
                result = f"Error: Tool '{tool_name}' not found."
            
            if verbose:
                print(f"   [Step {step} Tool Call] {tool_name}({kwargs}) -> {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    return "Agent terminated: maximum execution steps reached."

if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT (LLM + Tools + ReAct Loop)")
    for idx, question in enumerate(QUESTIONS, 1):
        print(f"Q{idx}: {question}")
        answer = agent(question, verbose=True)
        print("Final Answer:", answer)
        print("-" * 75)
