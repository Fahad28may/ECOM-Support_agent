from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util

# --- Setup (runs once) ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

store_facts = [
    "This shirt is available in black, white, and navy blue.",
    "Our standard return window is 30 days from delivery.",
    "We deliver across Pakistan in 3-5 working days.",
    "Cash on delivery is available for all orders.",
    "Express delivery to Lahore and Karachi takes 1-2 days.",
    "Items on final sale cannot be returned or exchanged.",
    "We offer free shipping on orders above PKR 5000.",
    "Sizes available are Small, Medium, Large, and Extra Large.",
]
fact_vectors = embed_model.encode(store_facts)


# --- Retrieval ---
def find_relevant_facts(question, top_k=3):
    question_vector = embed_model.encode(question)
    scores = util.cos_sim(question_vector, fact_vectors)[0]
    ranked = sorted(zip(store_facts, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


# --- The full agent ---
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


# --- Try it ---
if __name__ == "__main__":
    question = "Do you offer gift wrapping?"
    print(f"Customer: {question}\n")
    print(f"Agent: {answer_question(question)}")