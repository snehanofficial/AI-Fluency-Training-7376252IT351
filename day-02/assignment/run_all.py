"""Master script to run all experiments for Day 02 Assignment.
Executes Direct Prompting, Chain-of-Thought, ReAct Agent, and Self-Consistency.
"""
from config import QUESTIONS, banner
from direct_prompting import run_direct_prompting
from cot_prompting import run_cot_prompting
from react_agent import run_react_agent
from self_consistency import run_self_consistency_experiment

def main():
    banner("DAY 02 ASSIGNMENT: DIRECT PROMPTING vs CoT vs REACT AGENT")

    print("\n" + "#" * 80)
    print(" SECTION 1: QUESTION-BY-QUESTION EVALUATION ACROSS ALL 3 PARADIGMS")
    print("#" * 80 + "\n")

    for q in QUESTIONS:
        qid = q["id"]
        qtype = q["type"]
        qtext = q["text"]

        print("=" * 80)
        print(f" QUESTION [{qid}] ({qtype}):")
        print(f" \"{qtext}\"")
        print("=" * 80)

        # 1. Direct Prompting
        print("\n--- [PARADIGM 1: DIRECT PROMPTING] ---")
        direct_res = run_direct_prompting(qtext)
        print(direct_res)

        # 2. Chain-of-Thought
        print("\n--- [PARADIGM 2: CHAIN-OF-THOUGHT (CoT)] ---")
        cot_res = run_cot_prompting(qtext)
        print(cot_res)

        # 3. ReAct Agent
        print("\n--- [PARADIGM 3: REACT AGENT] ---")
        react_res = run_react_agent(qtext, verbose=True)
        print(f"\n>> Final Synthesized Answer:\n{react_res['final_answer']}")

        print("\n" + "-" * 80 + "\n")

    print("\n" + "#" * 80)
    print(" SECTION 2: SELF-CONSISTENCY EXPERIMENT ON COT REASONING")
    print("#" * 80 + "\n")
    run_self_consistency_experiment(num_trials=10, temperature=0.7)

if __name__ == "__main__":
    main()
