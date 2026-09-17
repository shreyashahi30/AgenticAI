import os
from groq import Groq


# =========================================================
# GROQ CLIENT
# =========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY environment variable is not set"
    )

client = Groq(api_key=api_key)


# =========================================================
# LLM CALL
# =========================================================

def call_llm(prompt: str) -> str:
    """
    Send a prompt to Groq and return the model response.

    GPT-OSS 20B is used as the current Groq model.
    JSON Object Mode ensures that the model returns JSON.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        response_format={
            "type": "json_object"
        },

        temperature=0.2,

        max_tokens=1600
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "Groq returned an empty response"
        )

    return content.strip()
