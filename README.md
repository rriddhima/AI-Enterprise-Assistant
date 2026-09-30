## 🚀 Live Demo

👉 [AI Enterprise Knowledge Assistant](https://ai-enterprise-assistant.streamlit.app/)

# AI Enterprise Knowledge Assistant

A multi-agent RAG (Retrieval-Augmented Generation) application built with
**LangGraph**, **Groq**, **FAISS**, **Sentence Transformers**, and
**Streamlit**. Employees can ask natural-language questions about internal
company documents (HR policy, technical docs, project docs) and get
grounded, source-cited answers.

## How it works

1. A **Manager Agent** classifies each question as `HR`, `TECHNICAL`,
   `PROJECT`, or `GENERAL`.
2. The **Document Retriever** runs a semantic vector search (FAISS +
   Sentence Transformers) scoped to the relevant department.
3. A **specialist agent** (via Groq's `llama-3.3-70b-versatile`) generates
   an answer using only the retrieved context — reducing hallucination.
4. The UI shows the answer along with its **source document and page**.

```
USER -> Streamlit Chat UI -> Manager Agent -> [HR | Technical | Project] Agent
     -> Document Retriever -> Groq LLM -> Grounded Answer + Source Citation
```

## Project structure

```
AI_Enterprise_Assistant/
├── app.py              # Streamlit UI
├── config.py            # Env / model config
├── rag.py                # PDF loading, chunking, embeddings, FAISS, retrieval
├── agents.py             # Manager agent + answer generation
├── graph.py              # LangGraph workflow
├── requirements.txt
├── .env.example
├── .gitignore
└── documents/
    ├── hr/
    │   ├── leave_policy.pdf
    │   └── attendance_policy.pdf
    ├── technical/
    │   ├── python_guidelines.pdf
    │   └── deployment_guide.pdf
    └── projects/
        ├── project_alpha.pdf
        └── project_beta.pdf
```

Six sample PDFs are already included under `documents/` so the app works
out of the box — swap them for your own company PDFs any time.

## Setup

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Groq API key**

   Copy `.env.example` to `.env` and fill in your key (get one from the
   [Groq Console](https://console.groq.com/)):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Then open http://localhost:8501

## Try it

- **HR:** "How many casual leaves do employees receive?"
  → *Employees receive 12 casual leaves per year.* (`leave_policy.pdf — Page 1`)
- **Technical:** "How is the application deployed?"
  → *The application is deployed using Docker...* (`deployment_guide.pdf — Page 1`)
- **Project:** "What technology does Project Alpha use?"
  → *Project Alpha uses Python and FastAPI for its backend and MySQL for its database.*
- **Unknown info:** "What is the company's international travel allowance?"
  → *I could not find this information in the available company documents.*
  (hallucination-control check)

## Next upgrades

- Split the single manager→answer graph into explicit HR / Technical /
  Project / General agent nodes with a dedicated response-aggregation node.
- Add persistent conversation history (e.g. MySQL) across sessions.
- Add an admin interface for uploading and re-indexing documents.
