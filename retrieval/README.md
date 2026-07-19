# ChromaDB + Qwen Retrieval Pipeline

## Quick start (pre-built index)

A pre-built ChromaDB index is included in `/chroma_db_v3/`.

```bash
pip install chromadb sentence-transformers
python retrieval/query.py --index chroma_db_v3/ --question "What does Seth say about the nature of the soul?"
```

##Build from scratch

If you want to rebuild the index from your own corpus:

Prepare annotated XML files (see corpus/README.md).


```bash
Run: python retrieval/build_index.py --input corpus/clean/ --output chroma_db_v3/
```

