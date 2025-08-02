# bajaj-hack1
🚀 LLM-Powered Intelligent Query–Retrieval System
An enterprise-ready API backend for context-aware retrieval from large insurance/legal/HR/compliance documents, using FastAPI, Pinecone, LangChain, and Groq Llama3.

📄 Overview
This project implements an LLM-powered document retrieval system that:
Processes large documents (PDF/DOCX)
Answers natural language queries using semantic clause search (via Pinecone) and an LLM (Groq/Llama3)
Returns structured, explainable JSON answers
Designed for insurance, legal, HR, and compliance domains

🏗️ Architecture
Tech Stack:
Backend: FastAPI
Vector Search: Pinecone (semantic search & retrieval)
LLM: Groq Llama3 (via LangChain)
Doc Processing: LangChain loaders
Structure: Modular Python (embeddings, document loaders, logic)
API Docs: Automatic Swagger UI via FastAPI
High-Level Flow:
User provides a document (PDF/DOCX public URL) and questions via API
Document is chunked & embedded, embeddings stored/searched in Pinecone
Top-matched clauses retrieved for each question
LLM (Groq Llama3) reasons using only these context clauses
Returns answers in structured JSON

🚦 Features
Accepts PDF/DOCX URLs (easily extensible to email/web)
Semantic clause/paragraph search (retrieval augmented generation)
Explainable answers, referencing policy/contract clauses
Structured JSON output as per sample and scoring requirements
FastAPI /docs auto-generated UI for testing
Modular codebase designed for production and extensibility

🏁 Quickstart
1. Clone the Repo
bash
git clone <your-repo-url>
cd <your-project-directory>
2. Install Dependencies
bash
pip install -r requirements.txt
pip install python-dotenv
3. Set Up Environment Variables
Copy .env.example to .env and fill in:

text
GROQ_API_KEY=sk-...           # get from Groq dashboard
PINECONE_API_KEY=pcsk-...     # get from Pinecone dashboard
PINECONE_ENV=us-west1-gcp-free # or as shown in your Pinecone project
4. Start the Backend Server
bash
uvicorn app.main:app --reload
API runs at http://127.0.0.1:8000
Interactive docs: http://127.0.0.1:8000/docs

🧪 Usage & Testing
Interactive API Docs
Visit /docs (Swagger UI):
Expand the POST /api/v1/hackrx/run endpoint
Click Try it out
Paste a request in this format:

json
{
    "documents": "https://yourdomain.com/policy.pdf",
    "questions": [
        "What is the grace period for premium payment under this policy?",
        "Does the policy cover maternity expenses, and what are the conditions?"
    ]
}
Click Execute, view answer(s) belo
Sample cURL Request
bash
curl -X POST "http://127.0.0.1:8000/api/v1/hackrx/run" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{"documents": "https://yourdomain.com/policy.pdf", "questions": ["What is the grace period?"]}'

🧰 Project Structure
text
project-root/
├── app/
│   ├── main.py               # FastAPI app and endpoints
│   ├── document_loader.py    # PDF/DOCX loaders
│   ├── embeddings.py         # Chunking and Pinecone operations
│   ├── llm.py                # Groq Llama3 wrapper
│   ├── logic.py              # Clause matching and answer logic
│   ├── models.py             # Pydantic data models
├── requirements.txt
├── .env.example              # Example for secrets (never share your real .env)
├── README.md

🧠 How This System Satisfies the Requirements
Input: Processes PDFs/DOCX (email/web easily added), parses NLQs
Semantic Search: Uses Pinecone embeddings for clause retrieval
Contextual Decisions: LLM answers are constrained by relevant context
Explainability: Prompts ask for clause-based, justified explanations
Output: API returns strict JSON as per provided schema
Latency & Token Efficiency: Top-k clause retrieval minimizes LLM cost and speeds up response
Reusability: Modular files for each component enable easy extension and production deployment

🔒 Security Note
Add auth middleware (Bearer token) for production if exposing the API publicly.

🚀 Deploying to Cloud
Free cloud (for demo): Use Render, Railway, or Deta
Heroku:
Add a Procfile:
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
Set all env variables via UI/CLI before deploy.
Containerize (for GCP/AWS/Azure):
Add a Dockerfile if deploying as a container.

🛡 Extending or Customizing
Add file upload endpoints if required (see FastAPI docs)
Add PostgreSQL integration for conversation/session logging
Plug in OpenAI GPT-4 LLM if your submission specifically requires it

💬 Support
If you get an SSL or doc download error, make sure you use a public HTTPS PDF/DOCX URL with a valid certificate.
For local testing with private PDFs, ask about the file upload variant.

👨💻 Vatsal chauhan & pratik kumar singh
Designed by: [Vatsal chauhan & pratik kumar singh], HackRX 2025 Solution

Technologies: FastAPI, Pinecone, LangChain, Groq
