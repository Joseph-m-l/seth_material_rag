# Exploring the Seth Material via Local LLMs

*A personal attempt to understand complex mid-20th-century philosophy using tools I'm familiar with: Python, embeddings, and open-source LLMs.*

This repository is a personal research log and experimental playground for studying the "Seth Material" texts by Jane Roberts using local open-source Large Language Models.

## The Problem

Philosophical and esoteric texts from the mid-20th century present unique challenges for modern NLP:

- **Highly abstract terminology** that lacks direct analogues in standard datasets.
- **Non-linear narrative structures** where context spans across multiple sessions and books.
- **Semantic ambiguity** that breaks generic embedding models like MiniLM.

## Current Status & Methodology

**I am not building a product; I am conducting an experiment** to see how well current open-source models can grasp non-classical ontologies.

| Component               | Detail                                                                                          |
|:------------------------|:------------------------------------------------------------------------------------------------|
|**Current Scope**        | *"Seth Speaks"*, Chapters 1–9 (Sessions 511–537, excluding personal sessions)                   |
| **Pipeline**            | Manual OCR cleaning → XML annotation (Qwen2.5-Coder-14B-Instruct) → Tag verification (DeepSeek) |
| **Chunking Strategy**   | Strictly by speaker (`SETH` segments)                                                           |
| **Vectorization**       | `❌ all-MiniLM-L6-v2` — Failed: semantic drift on metaphysical concepts                         |
|                         | `✅ multilingual-e5-large` — Success: captures deep conceptual links                            |
| **Storage & Retrieval** | ChromaDB + Qwen2.5-32B-Instruct (served via LM Studio)                                          |


**A note on language:** Both the embedding model (`multilingual-e5-large`) and the retrieval LLM (`Qwen2.5-32B-Instruct`), served locally via LM Studio are multilingual by design. The source material is English, but a reader asking questions in Russian, Spanish, or any other language should receive equally coherent answers. The structure of reality — if these texts describe it — is not supposed to be language-dependent.

## Why This Matters for NLP

Most embedding benchmarks (MTEB, BEIR) measure performance on news, Wikipedia, or StackOverflow — texts that describe objects, events, and relationships *within* a shared consensual reality.

This project tests a blind spot: **texts that attempt to describe the structure of reality itself** rather than its contents. When a term like *"framework"*, *"identity"*, or *"dimension"* refers not to social constructs or physical spaces but to underlying layers of existence, the semantic ground shifts beneath the model.

There is no guarantee that off-the-shelf embeddings can follow this shift without projecting it back onto familiar, mundane meanings. Finding out whether they can — and where they break — is the point of this experiment.

## Repository Structure

├── corpus/ # Data preparation guide and scripts (source texts not hosted)

├── annotations/ # XML annotation schemas and labeled data

├── embeddings/ # Vectorization scripts and evaluation notes

├── retrieval/ # ChromaDB + Qwen retrieval pipeline

└── notes/ # Working notes, observations, dead ends

> **Note on corpus/:** Source texts are not hosted in this repository due to copyright restrictions. To reproduce the experiment, obtain legal copies of the Seth Material by Jane Roberts and follow the data preparation guide in `corpus/README.md`.

## Preliminary Results

- General-purpose embeddings (`all-MiniLM-L6-v2`) collapse on metaphysical concepts, producing high similarity scores for semantically unrelated passages.
- Multilingual E5 (`multilingual-e5-large`) shows significantly better alignment with human-annotated conceptual clusters.
- Hybrid retrieval (dense embeddings + LLM reranking) yields the most coherent answers when querying across session boundaries.
- A pre-built ChromaDB index is included in `/chroma_db_v3/` so you can start querying immediately without processing the corpus yourself.

## Disclaimer

This is a work-in-progress hobby project. Expect bugs, broken scripts, and evolving schemas. Everything here is provisional and subject to revision.

## Support

If you find this experiment useful or interesting, you can support further research via Lightning Network:

> bc1q0fz8hks4vg7rmm63jsr25xfdaxehcnzmf85wj7

## License

Source texts © respective rights holders (used for research purposes).
All code and annotations in this repository: MIT License.
