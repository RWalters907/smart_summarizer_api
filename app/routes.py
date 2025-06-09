from fastapi import APIRouter
from app.schemas import SummarizeRequest, SummarizeResponse
from app.openai_service import summarize_text

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    return await summarize_text(request)
