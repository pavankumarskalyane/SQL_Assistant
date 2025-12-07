# backend/retriever.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_PATH = "./chroma_db"

class SQLRetriever:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"  # ✅ Fast + accurate
        )

        self.db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embeddings
        )

    def retrieve(self, query, top_k=3):
        results = self.db.similarity_search_with_score(query, k=top_k)

        formatted = []
        for doc, score in results:
            formatted.append({
                "content": doc.page_content,
                "similarity_score": float(score)
            })

        return formatted
