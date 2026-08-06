from rag import answer_with_threshold, best_match_score, find_relevant_facts
from test_set import TEST_SET
from rag import answer_question, find_relevant_facts, REFUSAL_MESSAGE


def looks_like_refusal(answer):
    """True if the agent DECLINED to answer (not just used a negative word)."""
    # Exact code-level refusal is unambiguous
    if answer.strip() == REFUSAL_MESSAGE:
        return True

    low = answer.lower()

    # Phrases that specifically mean "I don't have / can't provide this info"
    decline_phrases = [
        "don't have information",
        "don't have that information",
        "do not have information",
        "don't have the",
        "not have that information",
        "no information about",
        "don't have any information",
        "i'm not able to find",
        "couldn't find",
    ]
    return any(p in low for p in decline_phrases)


def run_at_threshold(threshold):
    hallucinations = 0
    wrong_refusals = 0
    correct = 0

    for item in TEST_SET:
        q = item["question"]
        expected = item["expected_behavior"]

        answer = answer_with_threshold(q, threshold)
        refused = looks_like_refusal(answer)

        if expected == "refuse":
            if refused:
                correct += 1
            else:
                hallucinations += 1
        else:  # expected == "answer"
            if refused:
                wrong_refusals += 1
            else:
                correct += 1

    return correct, hallucinations, wrong_refusals


if __name__ == "__main__":
    # First, print the actual best-scores so we can see the natural split
    print("Best match score per question:\n")
    for item in TEST_SET:
        score = best_match_score(item["question"])
        print(f"  {score:.3f}  [{item['expected_behavior']:6}]  {item['question']}")

    print("\n" + "=" * 55)
    print(f"{'Threshold':>10} | {'Correct':>7} | {'Hallucin.':>9} | {'WrongRef':>8}")
    print("=" * 55)

    for t in [0.0, 0.15, 0.20, 0.25, 0.30, 0.35]:
        correct, halluc, wrong = run_at_threshold(t)
        print(f"{t:>10.2f} | {correct:>7} | {halluc:>9} | {wrong:>8}")