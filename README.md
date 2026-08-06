# E-Commerce Support Agent

An AI-powered customer support agent for online stores, built with Retrieval-Augmented Generation (RAG). It answers customer questions using **only** a store's own product catalogue and policies, and declines gracefully when the data doesn't contain an answer — avoiding the confident hallucinations that make generic chatbots unreliable for real stores.

Final Year Project — a grounded, full-stack AI application.

## What it does

- Answers product and policy questions from a store's own data (prices, colours, sizes, delivery, returns)
- **Refuses to guess** — if the data doesn't cover a question, it says so and offers to connect the customer with the team, rather than inventing an answer
- Ingests data from simple files, so adding a product or updating a policy needs no code changes

## How it works

The system uses Retrieval-Augmented Generation:

1. **Ingest** — product catalogue (CSV) and policy documents (text) are loaded and split into chunks
2. **Embed** — each chunk is converted into a semantic vector using a local embedding model
3. **Retrieve** — for each question, the most semantically relevant chunks are found via cosine similarity
4. **Ground** — the retrieved facts are passed to a language model with strict instructions to answer only from them
5. **Answer** — the model responds from the provided facts, or refuses if they don't cover the question

## Tech stack

**Backend:** Python, FastAPI, sentence-transformers (local embeddings), OpenRouter (LLM access)
**Frontend:** Next.js, TypeScript, Tailwind CSS

## Project structure

├── Backend/ # Python RAG engine + FastAPI server
│ ├── rag.py # Core RAG logic: ingestion, embedding, retrieval, answering
│ ├── main.py # FastAPI app exposing the /ask endpoint
│ ├── data/ # Store data (products.csv, policies.txt)
│ ├── evaluate.py # Evaluation against a gold-standard test set
│ └── test_set.py # Test questions with expected behaviour
└── Frontend/ # Next.js chat interface

## Running it locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai) API key (free tier works)

### Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in `Backend/` (see `.env.example`):

OPENROUTER_API_KEY=your-key-here

Run the server:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000` (interactive docs at `/docs`).

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Evaluation

The system was tested against a purpose-built set of answerable, unanswerable, and edge-case questions:

- **94% correct behaviour** with **zero hallucinations**
- Grounding enforced through two independent safeguards: prompt-level instructions and a retrieval-level similarity check

## Limitations & future work

- Questions requiring comparison across multiple records (e.g. "what's your cheapest product?") are constrained by top-k retrieval
- Currently single-store; multi-store support and an owner dashboard are planned
- Potential extensions: multilingual support (Urdu/Roman Urdu), WhatsApp integration, order-status lookup