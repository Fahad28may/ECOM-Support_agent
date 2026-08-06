from sentence_transformers import SentenceTransformer, util

# Load the embedding model (downloads once, then cached). Runs locally, free.
model = SentenceTransformer("all-MiniLM-L6-v2")

# Some pretend store facts
sentences = [
    "This shirt is available in black.",
    "Our return window is 30 days.",
    "We deliver across Pakistan in 3-5 working days.",
]

# A customer question
question = "Do you offer gift wrapping?"

# Turn everything into vectors (embeddings)
sentence_vectors = model.encode(sentences)
question_vector = model.encode(question)

# Measure how close the question is to each sentence (0 = unrelated, 1 = identical meaning)
scores = util.cos_sim(question_vector, sentence_vectors)

# Show each sentence with its similarity score
for sentence, score in zip(sentences, scores[0]):
    print(f"{score:.3f}  |  {sentence}")