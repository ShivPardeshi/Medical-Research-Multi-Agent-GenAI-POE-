"""Tools for Medical Researcher Agno Agents.

Provides access to the curated medical clinical guidelines and pharmacology knowledge base
with keyword, domain, and clinical concept scoring, allowing the Medical Evidence Researcher
and Clinical Reviewer to inspect and cite authentic peer-reviewed materials.
"""

from typing import List, Set
from app.data.sample_documents import SAMPLE_MEDICAL_DOCUMENTS

# Thread-local / query-level source tracking container
_last_consulted_sources: Set[str] = set()


def get_last_consulted_sources() -> List[str]:
    """Retrieve the document titles consulted during the most recent research session."""
    return sorted(list(_last_consulted_sources))


def clear_consulted_sources() -> None:
    """Reset the consulted sources tracker before starting a new clinical inquiry."""
    _last_consulted_sources.clear()


def search_medical_library(query: str) -> str:
    """Search the medical and clinical guidelines knowledge base for relevant guidelines, drug mechanisms, and safety alerts.

    Args:
        query: The clinical keywords, medical condition, drug name, or clinical scenario.

    Returns:
        A formatted string containing relevant clinical excerpts and guideline recommendations.
    """
    if not query or not query.strip():
        return "No clinical query provided. Please specify medical topics, drug names, or clinical scenarios."

    query_tokens = [w.lower().strip("?,.;:\"'()") for w in query.split() if len(w) > 2]
    matched_docs = []

    for doc in SAMPLE_MEDICAL_DOCUMENTS:
        score = 0
        doc_keywords = [k.lower() for k in doc.get("keywords", [])]
        title_lower = doc.get("title", "").lower()
        content_lower = doc.get("content", "").lower()
        category_lower = doc.get("category", "").lower()

        for token in query_tokens:
            if token in doc_keywords:
                score += 3
            if token in title_lower:
                score += 4
            if token in category_lower:
                score += 2
            if token in content_lower:
                score += 1

        if score > 0:
            matched_docs.append((score, doc))

    if not matched_docs:
        available_titles = ", ".join(f"'{d['title']}'" for d in SAMPLE_MEDICAL_DOCUMENTS)
        return (
            f"No direct matches found in medical library for '{query}'. "
            f"Available clinical guideline modules include: {available_titles}."
        )

    # Sort descending by relevance score
    matched_docs.sort(key=lambda item: item[0], reverse=True)

    results: List[str] = []
    for _, doc in matched_docs[:2]:  # Top 2 most relevant clinical guidelines
        _last_consulted_sources.add(doc["title"])
        # Keep preview concise to balance depth with token efficiency
        content_preview = doc["content"][:400] + ("..." if len(doc["content"]) > 400 else "")
        results.append(
            f"[{doc['title']}]\nClinical Area: {doc['category']}\nGuideline Summary: {doc['summary']}\nKey Principles:\n{content_preview}\n"
        )

    return "\n".join(results)


# Backward compatibility alias for any lingering legal references
search_legal_library = search_medical_library
