from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# ✅ Configure logging so errors and info appear in Render logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client using the latest library format
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 template engine
templates = Jinja2Templates(directory="app/templates")

# Define request model
class TextInput(BaseModel):
    text: str

# Serve frontend HTML page at root
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("summarizer.html", {"request": request})

# Summarization API endpoint
@app.post("/summarize")
async def summarize_text(input: TextInput):
    logging.info(f"📩 Received text to summarize: {input.text[:100]}...")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a neutral and concise assistant. "
                        "Summarize the given text clearly and simply, avoiding phrases like 'the user said' or 'the customer is'. "
                        "Do not include introductions, assumptions, or commentary. Just return a brief, clear summary."
                    )
                },
                {"role": "user", "content": input.text},
            ],
            temperature=0.5,
            max_tokens=300
        )

        summary = completion.choices[0].message.content.strip()
        logging.info(f"✅ Summary generated successfully.")
        return {"summary": summary}

    except Exception as e:
        logging.error(f"❌ Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
