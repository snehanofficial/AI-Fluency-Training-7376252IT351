"""Direct Prompting implementation for Day 02 assignment.
Direct prompting asks the LLM to give the final answer immediately without step-by-step reasoning or tool access.
"""
from config import client, MODEL

DIRECT_SYSTEM_PROMPT = (
    "You are Apex Logistics Assistant. Answer the user's question directly and concisely. "
    "Do NOT show any step-by-step reasoning, calculations, or chain of thought. "
    "Provide only the final answer directly."
)

def run_direct_prompting(question: str, temperature: float = 0.0) -> str:
    messages = [
        {"role": "system", "content": DIRECT_SYSTEM_PROMPT},
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
    banner("DIRECT PROMPTING BASELINE")
    for q in QUESTIONS:
        print(f"[{q['id']}] Question: {q['text']}")
        ans = run_direct_prompting(q["text"])
        print(f"Direct Response:\n{ans}\n")
        print("-" * 70)
