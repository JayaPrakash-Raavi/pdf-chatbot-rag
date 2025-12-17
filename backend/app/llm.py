import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama3-8b-8192"


def generate_answer(question: str, context: str) -> str:
    """
    Generate a grounded answer using Groq LLM.
    Context = retrieved PDF chunks
    """
    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the information in the context.
If the answer is not in the context, say "The document does not contain that information."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content.strip()
