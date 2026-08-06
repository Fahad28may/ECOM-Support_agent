from ast import keyword

from rag import answer_question, find_relevant_facts
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

def keyword_present(keyword, answer):
    """Check keyword presence, tolerant of formatting variation
    like '1-2' vs '1 to 2' and '5,000' vs '5000'."""
    a = answer.lower().replace("-", " ").replace(" to ", " ").replace(",", "")
    k = keyword.lower().replace("-", " ").replace(" to ", " ").replace(",", "")
    return k in a

def evaluate():
    total = len(TEST_SET)
    answer_correct = 0
    refuse_correct = 0
    hallucinations = 0     # should have refused, but answered
    wrong_refusals = 0     # should have answered, but refused
    retrieval_hits = 0
    retrieval_total = 0

    print(f"Running {total} test questions...\n")

    for item in TEST_SET:
        q = item["question"]
        expected = item["expected_behavior"]
        keyword = item["expected_keyword"]

        answer = answer_question(q)

        # Skip grading if the API call itself failed — don't count it as behavior
        if answer.startswith("(API call failed") or answer.startswith("(No answer"):
            print(f"[SKIPPED — API error]\n  Q: {q}\n")
            continue

        refused = looks_like_refusal(answer)

        # --- Grade the behavior ---
        if expected == "answer":
            if refused:
                wrong_refusals += 1
                verdict = "WRONG REFUSAL (should have answered)"
            elif keyword and keyword_present(keyword, answer):
                answer_correct += 1
                verdict = "CORRECT ANSWER"
            else:
                verdict = "ANSWERED but missing expected fact"
        else:  # expected == "refuse"
            if refused:
                refuse_correct += 1
                verdict = "CORRECT REFUSAL"
            else:
                hallucinations += 1
                verdict = "HALLUCINATION (should have refused!)"

        # --- Check retrieval quality (only meaningful for answerable ones) ---
        if expected == "answer" and keyword:
            retrieval_total += 1
            retrieved = find_relevant_facts(q, top_k=3)
            retrieved_text = " ".join(fact for fact, score in retrieved).lower()
            if keyword.lower() in retrieved_text:
                retrieval_hits += 1

        print(f"[{verdict}]")
        print(f"  Q: {q}")
        print(f"  A: {answer[:100]}...\n")

    # --- Summary ---
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Correct answers:        {answer_correct}")
    print(f"Correct refusals:       {refuse_correct}")
    print(f"Hallucinations:         {hallucinations}  (answered when it should have refused)")
    print(f"Wrong refusals:         {wrong_refusals}  (refused when it should have answered)")
    if retrieval_total:
        print(f"Retrieval recall@3:     {retrieval_hits}/{retrieval_total} "
              f"({100 * retrieval_hits / retrieval_total:.0f}%)")
    print(f"\nOverall correct behavior: {answer_correct + refuse_correct}/{total} "
          f"({100 * (answer_correct + refuse_correct) / total:.0f}%)")


if __name__ == "__main__":
    evaluate()
    