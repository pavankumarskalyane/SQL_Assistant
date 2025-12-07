# backend/ingest.py

import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document


CHROMA_PATH = "./chroma_db"
JSONL_PATH = r"C:\Users\pavankumar.kalyane\Downloads\sql_assistant\backend\data\sql_corrections_advanced.jsonl"

def ingest_data():
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    documents = []

    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            wrong = row["wrong_query"]
            corrected = row["correct_query"]

            doc = Document(
                page_content=corrected,
                metadata={"wrong_query": wrong}
            )
            documents.append(doc)

    db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=CHROMA_PATH
    )

    db.persist()
    print("✅ ChromaDB successfully created using LOCAL embeddings!")

if __name__ == "__main__":
    ingest_data()
