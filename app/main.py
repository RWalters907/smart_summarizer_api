print("🟢 RUNNING: app/main.py ✅")
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
import traceback
import openai  # For version logging

# ✅ Confirm that main.py is executing at runtime
print("🚀 MAIN.PY IS RUNNING")

# ✅ Log OpenAI package version at app start (will show in Render logs)
print(f"✅ OpenAI version: {openai.__version__}")

# ✅ Configure server logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ✅ Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not found in environment variables.")

# ✅ Create OpenAI client (for openai>=1.3.7)
client = OpenAI(api_key=api_key)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS for all origins (safe for public frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount static assets and template engine
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ✅ Request input model
class TextInput(BaseModel):
    text: str

# ✅ Confirm that /summarize endpoint is active
print("📣 /summarize endpoint is defined and active")

# ✅ Frontend HTML route
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("summarizer.html", {"request": request})

# ✅ POST /summarize with full logging
@app.post("/summarize")
async def summarize_text(input: TextInput):
    try:
        print(f"📝 Received input: {input.text[:100]}")  # 👈 TRACE incoming input
        logging.info(f"📩 Received text to summarize: {input.text[:100]}...")

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
        print(f"🧾 Summary returned: {summary}")  # 👈 DEBUG: Show summary in logs
        logging.info("✅ Summary generated successfully.")
        return {"summary": summary}

        # 🧪 TEST MODE: Uncomment below to hardcode a working summary
        # return {"summary": "This is a test summary."}

    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/ping")
async def ping():
    return {"message": "pong"}
