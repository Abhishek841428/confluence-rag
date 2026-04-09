from dotenv import load_dotenv

load_dotenv()

from confluence_rag.pipeline import ask

if __name__ == "__main__":
    print("🔍 Confluence RAG query\n")
    question = input("Enter your question: ").strip()

    if not question:
        print("❌ Please ask a question.")
        exit(1)

    answer, sources = ask(question)

    print("\n🧠 Answer:")
    print(answer)

    print("\n📚 Sources:")
    for i, src in enumerate(sources, 1):
        print(f"{i}. {src['title']}")
