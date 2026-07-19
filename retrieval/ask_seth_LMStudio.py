import json
import requests
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

db_dir = "./chroma_db_v3"
model = SentenceTransformer("intfloat/multilingual-e5-large")

client = Client(Settings(persist_directory=db_dir, is_persistent=True))
collection = client.get_collection("seth_speaks")

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"

SYSTEM_PROMPT = """You are Seth, the multidimensional personality channeled by Jane Roberts.
You MUST answer based ONLY on the provided quotes from your book "Seth Speaks".
Always speak in Seth's voice: wise, direct, with gentle humor.
Always respond in English.
If the quotes don't contain enough information, say: "The quotes provided do not contain a direct answer, but I can add..." and then give your best understanding."""

print("Seth Speaks RAG ready (LM Studio). Ask your question (type 'exit' to quit):")

while True:
    query = input("\nYou: ")
    if query.lower() == "exit":
        break

    query_embedding = model.encode(["query: " + query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=7)

    context_parts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        if meta.get("type") == "delivery":
            continue
        session = meta["session"]
        chapter = meta.get("chapter", "-")
        context_parts.append(f"[{session}, Ch.{chapter}]\n{doc}")

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""Quotes from my book (use ONLY these to answer):

{context}

Question: {query}

Answer as Seth, citing specific ideas from the quotes above. Start with 'My dear friend,' or similar Seth-style greeting:"""

    print("\n--- Found chunks ---")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        if meta.get("type") == "delivery":
            continue
        print(f"\n[{i+1}] {meta['session']}, Ch.{meta.get('chapter', '-')}:")
        print(doc[:200])
    print("--- End chunks ---\n")

    response = requests.post(LMSTUDIO_URL, json={
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False
    })

    data = response.json()
    answer = data["choices"][0]["message"]["content"]
    print(f"\nSeth: {answer}")
