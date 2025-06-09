from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

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
    allow_origins=["*"],  # You can tighten this to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class TextInput(BaseModel):
    text: str

# POST endpoint to summarize text
@app.post("/summarize")
async def summarize_text(input: TextInput):
    logging.info(f"📩 Received text to summarize: {input.text[:100]}...")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional assistant that summarizes customer emails."},
                {"role": "user", "content": input.text},
            ],
            temperature=0.7,
            max_tokens=300
        )

        summary = completion.choices[0].message.content.strip()
        return {"summary": summary}

    except Exception as e:
        logging.error(f"❌ Error calling OpenAI API: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
