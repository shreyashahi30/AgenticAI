import os
from groq import Groq


# ---------------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------------

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=api_key)


# ---------------------------------------------------------
# LLM CALL
# ---------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Send a prompt to Groq and return a valid JSON response.

    GPT-OSS 20B is used because the previous
    llama-3.1-8b-instant model is no longer available.

    JSON Object Mode ensures the model returns valid JSON.
    Pydantic validation is performed by the individual agents.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        # Ask Groq to produce valid JSON
        response_format={
            "type": "json_object"
        },

        # Keep responses reasonably deterministic
        temperature=0.2,

        # GPT-OSS reasoning configuration
        reasoning_effort="low",
        reasoning_format="hidden",

        # Enough space for the 30/60/90 day roadmap
        max_completion_tokens=1600
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response")

    return content.strip()
