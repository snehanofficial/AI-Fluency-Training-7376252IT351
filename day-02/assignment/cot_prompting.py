"""Chain-of-Thought (CoT) Prompting implementation for Day 02 assignment.
CoT prompting forces the model to generate explicit step-by-step reasoning before providing its final response.
"""
from config import client, MODEL

COT_SYSTEM_PROMPT = (
    "You are Apex Logistics Assistant. "
    "Reason step-by-step before providing your final answer. "
    "Break down the question into clear logical steps: Step 1, Step 2, Step 3... "
    "Show all intermediate logic and calculations before concluding with 'Final Answer:'."
)

def run_cot_prompting(question: str, temperature: float = 0.0) -> str:
    messages = [
        {"role": "system", "content": COT_SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    from config import QUESTIONS, banner
    banner("CHAIN-OF-THOUGHT (CoT) PROMPTING")
    for q in QUESTIONS:
        print(f"[{q['id']}] Question: {q['text']}")
        ans = run_cot_prompting(q["text"])
        print(f"CoT Response:\n{ans}\n")
        print("-" * 70)
