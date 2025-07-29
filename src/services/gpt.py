import logging
from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY,
)

async def generate_response(context: list[dict]) -> str | None:
    """Generates a response from the AI model."""
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