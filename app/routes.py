import importlib
from app import openai_service
importlib.reload(openai_service)  # <- Force reload

from app.schemas import SummarizeRequest, SummarizeResponse

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    return await openai_service.summarize_text(request)
