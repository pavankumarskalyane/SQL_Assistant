from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.llm import get_gemini_llm
from backend.retriever import SQLRetriever
from backend.rag import rag_with_fallback


# ✅ CREATE APP FIRST
app = FastAPI(
    title="SQL Assistant API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ✅ ADD CORS AFTER APP IS CREATED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ LOAD COMPONENTS
retriever = SQLRetriever()
llm = get_gemini_llm()


# ✅ REQUEST SCHEMA
class SQLRequest(BaseModel):
    query: str


# ✅ MAIN API ROUTE
@app.post("/correct-sql")
def correct_sql(req: SQLRequest):
    result = rag_with_fallback(req.query, retriever, llm)
    return result


# ✅ HEALTH CHECK
@app.get("/")
def root():
    return {"status": "✅ SQL Assistant Backend is running"}
