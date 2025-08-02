from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from app.models import QueryRequest, QueryResponse
from app.document_loader import load_document
from app.embeddings import split_chunks, embed_and_store
from app.llm import get_llm
from app.logic import semantic_search, answer_question

app = FastAPI()

load_dotenv()
llm = get_llm()

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_submission(request: QueryRequest):
    try:
        docs = load_document(request.documents)
        full_text = "\n".join(doc.page_content for doc in docs)
        chunks = split_chunks(full_text)
        vstore = embed_and_store(chunks)
        answers = []
        for question in request.questions:
            clauses = semantic_search(vstore, question, k=4)
            explanation = answer_question(llm, question, clauses)
            answers.append(explanation)
        return QueryResponse(answers=answers)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
