# Hybrid-RAG: Private Document Intelligence System
### Orchestrating Watsonx.ai and Local M4 Inference for Cost-Optimized RAG

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)
![IBM Watsonx](https://img.shields.io/badge/Cloud-IBM%20Watsonx-be95ff.svg)
![Apple M4](https://img.shields.io/badge/Hardware-Apple%20M4%20(Local%20Inference)-silver.svg)

## 📌 Project Overview
This repository contains a production-ready Retrieval-Augmented Generation (RAG) pipeline designed for high-security and cost-sensitive environments. The system utilizes a **Hybrid Inference Architecture**, intelligently routing workloads between a local **Apple M4-powered Small Language Model (SLM)** for privacy-first tasks and **IBM Watsonx.ai** for complex reasoning.

The project demonstrates a complete end-to-end data engineering lifecycle: from ingestion and recursive character splitting to vectorization and persistent storage in a ChromaDB instance.

## 🚀 Key Features
* **Hybrid Inference Engine:** Implements a switchable LLM backbone using `Ollama` (Local Phi-4) and `Watsonx.ai` (Granite/Llama-3).
* **Local Embedding Pipeline:** Offloads heavy vectorization tasks to a local Mac Mini M4, ensuring data privacy and zero API costs during the ingestion phase.
* **Durable Document Processing:** Uses `RecursiveCharacterTextSplitter` with custom length functions to maintain semantic integrity across document chunks.
* **Stateful UI:** A Gradio-based web interface allowing users to upload documents dynamically and interact with the knowledge base in real-time.
* **Performance Engineering:** Optimized for low latency using Unified Memory Architecture (UMA) on Apple Silicon.

## 🛠️ Technical Stack
* **LLM Orchestration:** LangChain
* **Cloud LLM:** IBM Watsonx.ai
* **Local LLM/Embeddings:** Ollama (Phi-4 / Slate)
* **Vector Database:** ChromaDB
* **Frontend:** Gradio
* **Language:** Python

## 🏗️ Architecture
1.  **Ingestion:** PDFs are processed on a Windows-based development environment.
2.  **Embedding:** Text chunks are sent to a networked **Mac Mini M4** via a secure local API for vectorization.
3.  **Storage:** Vectors are persisted in a local ChromaDB instance.
4.  **Retrieval:** A similarity search is performed to find the top $k$ relevant context snippets.
5.  **Generation:** The context is "stuffed" into a prompt and sent to either the local SLM or Watsonx.ai for the final response.

## 📈 Impact & Use Cases
This architecture addresses the primary "Corporate AI" hurdles:
1.  **Data Sovereignty:** Sensitive documents are processed locally.
2.  **Cost Scaling:** Reduces token consumption by using local SLMs for summarization and routing.
3.  **Reliability:** Provides a fallback mechanism between local and cloud providers.
