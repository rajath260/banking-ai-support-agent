"""Hugging Face LLM connection for the Banking AI Support Agent.

This module only sends a prompt to a hosted model. It does not execute banking
tools or make the LangGraph workflow an LLM-powered agent yet.
"""

import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load local environment variables from the repository's .env file.
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("HF_MODEL", "openai/gpt-oss-120b")

if not HF_TOKEN:
    raise RuntimeError(
        "HF_TOKEN is not set. Create a .env file in the repository root "
        "and add HF_TOKEN=your_huggingface_token."
    )

# Hugging Face routes the request to an available inference provider.
client = InferenceClient(token=HF_TOKEN, provider="auto")


def ask_llm(question: str) -> str:
    """Send one question to the configured Hugging Face chat model."""
    if not question or not question.strip():
        raise ValueError("question must not be empty")

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful banking customer support assistant. "
                    "Explain general banking concepts clearly. Never invent "
                    "customer account details, balances, or transactions. "
                    "If account-specific information is requested, explain "
                    "that you need to retrieve it from an approved banking tool."
                ),
            },
            {"role": "user", "content": question.strip()},
        ],
        max_tokens=250,
        temperature=0.2,
    )

    content = response.choices[0].message.content
    return content or ""


if __name__ == "__main__":
    prompt = "Explain the difference between a savings account and a current account."
    print(f"Model: {MODEL_ID}")
    print("\nUser:", prompt)
    print("\nAssistant:", ask_llm(prompt))
