import json
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document


# ✅ CHROMA STORAGE PATH
CHROMA_PATH = "./chroma_db"

# ✅ DATASET PATH
JSONL_PATH = r"C:\Users\pavankumar.kalyane\Downloads\sql_assistant\backend\data\sql_corrections_advanced.jsonl"


# ✅ PREVENT RE-INGEST ON EVERY DEPLOY (IMPORTANT FOR RENDER)
if os.path.exists(CHROMA_PATH):
    print("✅ Chroma already exists. Skipping ingestion.")
    exit()


def ingest_data():
    print("🚀 Starting ingestion...")

    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    documents = []

    print("📂 Loading dataset...")
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

    print(f"📄 Total documents loaded: {len(documents)}")

    print("💾 Creating ChromaDB...")
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    db.persist()
    print("✅ ChromaDB successfully created using LOCAL embeddings!")


if __name__ == "__main__":
    ingest_data()
