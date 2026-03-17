# 🛡️ Insurance Policy Chatbot

> AI-powered chatbot for a Chilean insurance management company. Customers can query their policy details in natural language and get real-time insurance news — all through a conversational interface backed by a multi-agent LLM system.

---

## 📌 The Problem

Insurance customers frequently need to look up information about their policies — coverage details, expiry dates, claim procedures — but navigating dense policy documents is frustrating. This chatbot makes policy information instantly accessible through natural conversation, while also surfacing relevant industry news when needed.

**Real client:** Chilean insurance management company.

---

## 🏗️ Architecture

```
Customer message
        │
        ▼
Main LLM Agent (Gemini)
        │
        ├──► RAG retrieval ──► ChromaDB (policy documents)
        │
        └──► Web Search Agent ──► You.com API (real-time news)
```

**Multi-agent design:** The main agent decides autonomously whether to answer from the policy database (RAG) or fetch current news from the web — without the user needing to specify.

---

## ✨ Features

- **Policy Q&A** — customers ask questions about their policies in plain language; the chatbot retrieves and explains the relevant information
- **Real-time news** — integrated web search agent surfaces recent insurance industry news on demand
- **Multi-agent routing** — the system automatically chooses between internal knowledge (ChromaDB) and live web search depending on the query
- **Prompt-engineered responses** — structured prompts ensure consistent, professional tone appropriate for insurance communication

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Google Gemini API |
| Orchestration | LangChain |
| Vector DB | ChromaDB |
| Web Search | You.com API |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- Google Gemini API Key
- You.com API Key

### Installation

```bash
git clone https://github.com/LautaroSantos8/insurance-chatbot
cd insurance-chatbot

pip install -r requirements.txt

cp .env.example .env
# Set GEMINI_API_KEY and YOU_API_KEY in .env
```

### Ingest policy documents

```bash
python ingest.py  # Loads policy documents into ChromaDB
```

### Run

```bash
python app.py
```

---

## 💡 My Contribution

This was a team project. My responsibilities:

- **Backend architecture** — designed the overall agent structure and tool routing logic
- **Prompt engineering** — wrote and iterated all prompt templates for the main agent and sub-agents
- **Query handling module** — implemented the core query processing pipeline: input → intent classification → RAG or web search → response formatting
- **LangChain integration** — connected Gemini, ChromaDB retrieval, and the You.com search agent into a single coherent chain

---

## 👤 Author

**Lautaro Santos Da Silveira**
[LinkedIn](https://www.linkedin.com/in/lautaro-santos-da-silveira-2a0852201/) · [GitHub](https://github.com/LautaroSantos8)
