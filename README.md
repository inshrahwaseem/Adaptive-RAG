# Adaptive RAG 🤖
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-red?logo=streamlit&logoColor=white)

## 📌 What is this project?
Adaptive RAG is an advanced, self-correcting question-answering system that dynamically routes user queries to the most appropriate data source. Instead of blindly querying a vector database, it decides whether to retrieve internal documents, perform an external web search, or answer from general knowledge, ensuring highly accurate and context-aware responses.

## 🏗️ Architecture
![Adaptive RAG Architecture](./adaptive_RAG.png)

The system utilizes a directed graph workflow to handle queries intelligently:
**Router → Retriever → Grader → Generator → Hallucination Check → Answer**

```text
       [User Query]
            |
            v
     (Query Classifier) ----- [General Knowledge] ---> [Answer]
            |
   [Needs Retrieval] 
            |
            v
       (Retriever) <-----------+
            |                  |
            v                  |
         (Grader) ---[Poor]--> (Rewrite Query)
            |
          [Good]
            |
            v
       (Generator)
            |
            v
         [Answer]
```
*(Note: If the query cannot be answered by internal documents, it routes to Web Search before generating the final answer).*

## 🛠️ Tech Stack
- Python 3.11+
- LangChain
- LangGraph
- OpenAI GPT (gpt-4o-mini)
- Groq (optional alternative LLM provider)
- Qdrant Vector DB (with FAISS fallback support)
- Tavily Web Search API

## 📁 Project Structure
```text
Adaptive-RAG/
├── docs/                # Additional documentation files
│   ├── CODE_STYLE_GUIDE.md
│   ├── DOCUMENTATION_INDEX.md
│   ├── DOCUMENT_FLOW_VISUAL.md
│   ├── DOCUMENT_UPLOAD_FLOW.md
│   ├── QDRANT_SETUP_GUIDE.md
│   └── QUICK_REFERENCE.md
├── src/
│   ├── api/             # FastAPI routes and endpoints
│   ├── config/          # Configuration and prompt templates
│   ├── core/            # Core settings and logger setup
│   ├── db/              # MongoDB client setup (for memory)
│   ├── llms/            # LLM initialization (OpenAI)
│   ├── memory/          # Chat history management (In-memory & MongoDB)
│   ├── models/          # Pydantic schemas for state, routing, and grading
│   ├── rag/             # LangGraph nodes, retriever setup, and agent logic
│   ├── tools/           # Common helper tools and graph routing logic
│   ├── main.py          # Main entry point for the FastAPI application
├── streamlit_app/
│   ├── pages/           # Streamlit UI pages (e.g., chat interface)
│   ├── utils/           # Helper functions for the Streamlit frontend
│   └── home.py          # Streamlit main landing page
├── requirements.txt     # Pinned Python dependencies
├── .env.example         # Template for environment variables
├── LICENSE              # MIT License
└── README.md            # Project documentation (You are here)
```

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- OpenAI API Key
- Tavily API Key

### Steps

Open your terminal or PowerShell and follow these exact Windows commands:

1. **Clone the repo**
   ```powershell
   git clone https://github.com/inshrahwaseem/Adaptive-RAG.git
   cd Adaptive-RAG
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   ```powershell
   copy .env.example .env
   ```
   *Open the `.env` file in your editor and add your actual API keys.*

5. **Run the Application**
   You can either run the FastAPI backend or the Streamlit UI.
   
   **To run the backend:**
   ```powershell
   uvicorn src.main:app --reload
   ```
   
   **To run the frontend UI:**
   ```powershell
   streamlit run streamlit_app/home.py
   ```

## 🔑 API Keys — How to Get Them
- **OpenAI**: https://platform.openai.com/
- **Tavily**: https://tavily.com/

## 🔄 How It Works (Step by Step)
1. **Query Routing**: The system receives a user question and classifies it. It decides if the question requires internal documents, general knowledge, or a web search.
2. **Retrieval**: If internal knowledge is needed, it fetches the most relevant document chunks from the Qdrant / FAISS Vector Database.
3. **Grading**: An LLM grades the retrieved documents to check if they are actually relevant to the user's question.
4. **Self-Correction (Rewriting)**: If the retrieved documents are not useful, the system rewrites the query to be more effective and tries retrieving again.
5. **Web Search Fallback**: If internal documents still fail or if the query requires external data, it searches the web using Tavily.
6. **Generation**: Finally, the generator compiles the relevant context and creates a concise, accurate answer for the user.

## 📊 Example Output

**Input Question:**
> "What is the architecture of the Adaptive RAG system?"

**Process Flow:**
> *Router → Retriever → Grader → Generator*

**Output Answer:**
> "The Adaptive RAG system uses a directed graph workflow built with LangGraph. User queries are first classified by a router, then relevant documents are retrieved from the vector store. A grader evaluates document relevance — if the documents are not useful, the query is rewritten and retrieval is retried. If internal documents fail, a Tavily web search is used as a fallback before generating the final answer."

## ⚠️ Common Issues & Fixes

| Error / Issue | Cause | Solution |
|--------------|--------|----------|
| `ModuleNotFoundError: No module named 'src'` | Running scripts from the wrong directory. | Ensure you are in the root `Adaptive-RAG` folder before running `python` or `uvicorn`. |
| `openai.AuthenticationError` | Missing or invalid OpenAI key. | Check your `.env` file and make sure `OPENAI_API_KEY` is set correctly without quotes. |
| `Tavily HTTP 401 Unauthorized` | Invalid Tavily API key. | Ensure `TAVILY_API_KEY` in `.env` is correct. |
| `Streamlit: Command not found` | Virtual environment not activated. | Run `.\venv\Scripts\activate` before starting Streamlit. |

## 📚 Additional Documentation
- [Code Style Guide](docs/CODE_STYLE_GUIDE.md)
- [Qdrant Setup Guide](docs/QDRANT_SETUP_GUIDE.md)
- [Quick Reference](docs/QUICK_REFERENCE.md)
- [Document Flow Visual](docs/DOCUMENT_FLOW_VISUAL.md)

## 🤝 Credits
Inspired by LangGraph's Adaptive RAG tutorial.
