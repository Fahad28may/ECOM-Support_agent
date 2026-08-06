from dotenv import load_dotenv
load_dotenv()

import os
import csv
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util

# --- Setup (runs once, when this module is imported) ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# --- Ingestion ---
def load_product_chunks(path):
    chunks = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock = "in stock" if row["in_stock"] == "yes" else "out of stock"
            chunk = (
                f"Product: {row['name']}. "
                f"Price: PKR {row['price']}. "
                f"Available colors: {row['colors']}. "
                f"Sizes: {row['sizes']}. "
                f"Currently {stock}. "
                f"Fabric: {row['fabric']}."
            )
            chunks.append(chunk)
    return chunks


def load_policy_chunks(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return [p.strip() for p in text.split("\n\n") if p.strip()]


# Build the knowledge base once
store_facts = load_product_chunks("data/products.csv") + load_policy_chunks("data/policies.txt")
fact_vectors = embed_model.encode(store_facts)
print(f"RAG engine ready: {len(store_facts)} chunks loaded.")


# --- Retrieval ---
def find_relevant_facts(question, top_k=3):
    question_vector = embed_model.encode(question)
    scores = util.cos_sim(question_vector, fact_vectors)[0]
    ranked = sorted(zip(store_facts, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]

def best_match_score(question):
    """Return the single highest similarity score for a question (0-1)."""
    question_vector = embed_model.encode(question)
    scores = util.cos_sim(question_vector, fact_vectors)[0]
    return float(scores.max())

# --- The agent ---
def answer_question(question):
    results = find_relevant_facts(question)
    retrieved_facts = "\n".join(f"- {fact}" for fact, score in results)

    system_prompt = (
        "You are a customer support assistant for an online clothing store. "
        "Answer the customer's question using ONLY the store facts provided below. "
        "If the facts do not contain the answer, say you don't have that information "
        "and offer to connect them with the team. Never guess or make up details "
        "like prices, stock, or delivery times.\n\n"
        f"STORE FACTS:\n{retrieved_facts}"
    )

    try:
        response = client.chat.completions.create(
            model="inclusionai/ling-3.0-flash:free",
            max_tokens=500,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            extra_body={
                "models": [
                    "inclusionai/ling-3.0-flash:free",
                    "google/gemma-4-26b-a4b-it:free",
                ],
                "route": "fallback",
            },
        )
    except Exception as e:
        return f"(API call failed: {e})"

    if not response.choices:
        return f"(No answer returned. Raw response: {response})"

    return response.choices[0].message.content

REFUSAL_MESSAGE = "I don't have that information. Let me connect you with our team."

def answer_with_threshold(question, threshold):
    """Refuse in code if the best retrieval score is below threshold;
    otherwise answer normally."""
    if best_match_score(question) < threshold:
        return REFUSAL_MESSAGE
    return answer_question(question)