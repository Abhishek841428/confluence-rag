from .retriever import retrieve
from .generator import generate


def build_context(chunks):
    sections = []
    for chunk in chunks:
        title = chunk.get("title", "Untitled")
        text = chunk.get("text", "")
        sections.append(f"{title}:\n{text}")
    return "\n\n".join(sections)


def ask(query, k=3):
    retrieved = retrieve(query, k=k)

    if not retrieved:
        return "No relevant documentation found.", []

    context = build_context(retrieved)
    answer = generate(context, query)

    return answer, retrieved