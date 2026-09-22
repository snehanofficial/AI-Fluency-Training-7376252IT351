"""System 1: A plain LLM chatbot. No tools, no access to private TechCorp IT asset data."""
from config import client, MODEL, QUESTIONS, banner

def chatbot(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful IT corporate assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    banner("SYSTEM 1: PLAIN CHATBOT (No Tools / Private Data)")
    for idx, question in enumerate(QUESTIONS, 1):
        print(f"Q{idx}: {question}")
        print("A:", chatbot(question))
        print("-" * 75)
