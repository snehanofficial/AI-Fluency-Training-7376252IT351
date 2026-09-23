"""Self-Consistency evaluation for Day 02 assignment.
Runs CoT prompting on Question 2 across multiple trials at T=0.7 vs T=0.0 to observe self-consistency majority voting.
"""
from collections import Counter
import re
from config import QUESTIONS, banner
from cot_prompting import run_cot_prompting

QUESTION_2 = QUESTIONS[1]["text"] # Cargo payload math question

def extract_key_metrics(response_text: str) -> str:
    """Parses response text to extract payload verdict (Within/Exceeded) and average value per kg."""
    text = response_text.lower()
    
    payload_status = "Within limit" if ("within" in text or "yes" in text or "under" in text) and "exceeded" not in text else "Unknown/Exceeded"
    
    # Search for monetary per kg values like $4.00, $4, 4.00/kg
    match = re.search(r'\$\s*(\d+(?:\.\d+)?)', response_text)
    val_per_kg = f"${match.group(1)}" if match else "N/A"
    
    return f"Payload: {payload_status} | Avg Value/kg: {val_per_kg}"

def run_self_consistency_experiment(num_trials: int = 10, temperature: float = 0.7):
    banner(f"SELF-CONSISTENCY EXPERIMENT (T={temperature}, {num_trials} Trials)")
    print(f"Target Question: {QUESTION_2}\n")
    
    responses = []
    extracted_answers = []

    for i in range(1, num_trials + 1):
        ans = run_cot_prompting(QUESTION_2, temperature=temperature)
        responses.append(ans)
        metric = extract_key_metrics(ans)
        extracted_answers.append(metric)
        print(f"--- Trial {i:02d} ---")
        print(f"Extracted Summary: {metric}")
        print(f"Snippet: {ans[:150].replace('\n', ' ')}...\n")

    counter = Counter(extracted_answers)
    majority_ans, majority_count = counter.most_common(1)[0]
    
    print("=" * 80)
    print(f"RESULTS FOR T={temperature}:")
    print(f"Total Trials: {num_trials}")
    for ans_pattern, count in counter.most_common():
        pct = (count / num_trials) * 100
        print(f"  - '{ans_pattern}': {count}/{num_trials} ({pct:.1f}%)")
    print(f"\nMajority Answer: {majority_ans} ({majority_count}/{num_trials})")
    
    # Run at T=0.0 for comparison
    print("\n" + "=" * 80)
    print("RUNNING AT TEMPERATURE T=0.0 (Deterministic Baseline):")
    ans_t0 = run_cot_prompting(QUESTION_2, temperature=0.0)
    metric_t0 = extract_key_metrics(ans_t0)
    print(f"T=0.0 Summary: {metric_t0}")
    print(f"T=0.0 Full Response:\n{ans_t0}")
    
    return {
        "trials": num_trials,
        "temperature": temperature,
        "extracted_answers": extracted_answers,
        "majority_ans": majority_ans,
        "majority_count": majority_count,
        "t0_summary": metric_t0,
        "t0_full": ans_t0
    }

if __name__ == "__main__":
    run_self_consistency_experiment(num_trials=10, temperature=0.7)
