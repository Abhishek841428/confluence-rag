import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set. Add it to your environment or .env file.")
    return Groq(api_key=api_key)


def generate(context, query):
    client = _get_client()

    prompt = f"""
You are an assistant answering questions based on internal company documentation.

Context:
{context}

Question:
{query}

Instructions:
- Answer only from the context
- If the answer is not found, reply with \"Not found in documentation.\"
- Keep the answer concise.
"""

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()