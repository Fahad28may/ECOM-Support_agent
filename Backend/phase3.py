from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# A bigger set of pretend store facts (this becomes real data later)
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

# Embed all facts once, up front
fact_vectors = model.encode(store_facts)

def find_relevant_facts(question, top_k=3):
    """Return the top_k store facts most related to the question."""
    question_vector = model.encode(question)
    scores = util.cos_sim(question_vector, fact_vectors)[0]

    # Pair each fact with its score, sort highest-first
    ranked = sorted(zip(store_facts, scores), key=lambda x: x[1], reverse=True)

    return ranked[:top_k]

# Try it
question = "How long does delivery take to Lahore?"
results = find_relevant_facts(question)

print(f"Question: {question}\n")
for fact, score in results:
    print(f"{score:.3f}  |  {fact}")