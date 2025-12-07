# backend/rag.py

def rag_with_fallback(query, retriever, llm, top_k=3, min_score=1.2):
    query_clean = query.strip().lower()

    results = retriever.retrieve(query, top_k=top_k)

    if results:
        best_doc = results[0]

        content = best_doc.get("content", "").strip()
        score = best_doc.get("similarity_score", 0)

        content_clean = content.lower()

        print("✅ Retrieved content:", content_clean)
        print("✅ Raw similarity score:", score)

        # ✅ CASE 1: HIGH CONFIDENCE VECTOR MATCH → USE RAG
        if isinstance(score, (int, float)) and score >= min_score:
            return {
                "source": "RAG",
                "answer": content,
                "confidence": float(score)
            }

        # ✅ CASE 2: TEXT MATCH FALLBACK → STILL RAG
        if query_clean in content_clean or content_clean in query_clean:
            return {
                "source": "RAG",
                "answer": content,
                "confidence": 0.85
            }

    # ✅ ✅ ✅ CASE 3: TRUE LLM FALLBACK (FIXED)
    prompt = f"""
You are a SQL error-correction system.

Format strictly as:
<Short mistake explanation>. Correct: <Correct SQL>;

Wrong SQL:
{query}
"""

    response = llm.invoke(prompt)   # ✅ NOW RETURNS STRING

    return {
        "source": "LLM",
        "answer": response.strip(),   # ✅ FIXED (.content REMOVED)
        "confidence": 0.2
    }
