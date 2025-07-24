import logging
from openai import AsyncOpenAI

# It's better to move the API key to a config file or environment variables
# For this refactoring, I'll leave it here but add a note.
API_KEY = "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"

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

async def generate_response(context: list[dict]) -> str | None:
    """Generates a response from the AI model asynchronously."""
    try:
        response = await client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "TG BOT",
            },
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=context,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        return None