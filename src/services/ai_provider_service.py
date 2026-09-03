import os

from google import genai


DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=api_key)


def generate_ai_response(
    prompt: str,
    model: str | None = None,
) -> str:
    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt must not be empty."
        )

    client = get_gemini_client()

    selected_model = (
        model
        or os.getenv(
            "GEMINI_MODEL",
            DEFAULT_GEMINI_MODEL,
        )
    )

    response = client.models.generate_content(
        model=selected_model,
        contents=prompt,
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text.strip()
