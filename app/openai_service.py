from openai import OpenAI
from app.schemas import SummarizeRequest, SummarizeResponse
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

async def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a neutral and concise assistant. "
                    "Summarize the given text clearly and simply, avoiding phrases like 'the user said' or 'the customer is'. "
                    "Do not include introductions, assumptions, or commentary. Just return a brief, clear summary."
                )
            },
            {
                "role": "user",
                "content": request.text
            }
        ],
        temperature=0.5,
        max_tokens=150,
    )
    summary = response.choices[0].message.content.strip()
    print("💥 THIS IS THE FUNCTION BEING USED 💥", flush=True)
    return SummarizeResponse(summary=summary)

