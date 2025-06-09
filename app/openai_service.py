from openai import OpenAI
from app.schemas import SummarizeRequest, SummarizeResponse
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

async def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who summarizes text briefly and clearly."},
            {"role": "user", "content": request.text},
        ],
        max_tokens=150,
        temperature=0.5,
    )
    summary = response.choices[0].message.content.strip()
    return SummarizeResponse(summary=summary)
