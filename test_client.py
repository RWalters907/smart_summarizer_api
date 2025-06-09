import asyncio
import httpx

async def test_summarize():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        payload = {"text": "FastAPI is a modern web framework for building APIs with Python."}
        response = await client.post("/summarize", json=payload)
        print("Status code:", response.status_code)
        print("Response JSON:", response.json())

if __name__ == "__main__":
    asyncio.run(test_summarize())
