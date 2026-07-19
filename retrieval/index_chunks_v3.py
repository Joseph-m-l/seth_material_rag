import json
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

input_file = "seth_chunks.jsonl"
db_dir = "./chroma_db_v3"

model = SentenceTransformer("C:/SP/Workbook/models/multilingual-e5-large")

client = Client(Settings(persist_directory=db_dir, is_persistent=True))
collection = client.get_or_create_collection("seth_speaks")

chunks = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        chunks.append(json.loads(line))

texts = ["passage: " + c["text"] for c in chunks]
ids = [f"chunk_{i}" for i in range(len(chunks))]
metadatas = [{"session": c["session"], "chapter": c["chapter"], "type": c["type"]} for c in chunks]

embeddings = model.encode(texts).tolist()
collection.add(embeddings=embeddings, documents=texts, ids=ids, metadatas=metadatas)

print(f"Done. {len(chunks)} chunks indexed with multilingual-e5-large.")