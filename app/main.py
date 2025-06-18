import os
import uuid
import logging
import traceback
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import openai  # for logging version

# 🔒 Constants
MAX_LENGTH = 10000
SUMMARY_DIR = "summaries"

# ✅ Runtime Logs
print("🟢 RUNNING: app/main.py ✅")
print("🚀 MAIN.PY IS RUNNING")
print(f"✅ OpenAI version: {openai.__version__}")

# ✅ Logging Config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ✅ Load Environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)

# ✅ FastAPI App Init
app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Static + Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ✅ Ensure summaries/ exists
os.makedirs(SUMMARY_DIR, exist_ok=True)

# ✅ Request Model
class TextInput(BaseModel):
    text: str

# ✅ Home Page Route
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("summarizer.html", {"request": request})

# ✅ Summarize Route
@app.post("/summarize")
async def summarize_text(input: TextInput):
    try:
        if len(input.text) > MAX_LENGTH:
            error_msg = f"Maximum characters allowed is {MAX_LENGTH}, please try again."
            logging.warning(f"⚠️ Input too long: {len(input.text)} characters")
            raise HTTPException(status_code=400, detail=error_msg)

        logging.info(f"📩 Received text to summarize: {input.text[:100]}...")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a neutral and concise assistant. "
                        "Summarize the given text clearly and simply, avoiding phrases like 'the user said'. "
                        "Do not include introductions or commentary. Just return a brief, clear summary."
                    )
                },
                {"role": "user", "content": input.text},
            ],
            temperature=0.5,
            max_tokens=300
        )

        summary = completion.choices[0].message.content.strip()
        logging.info("✅ Summary generated successfully.")

        # ✅ Save summary to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}_{uuid.uuid4().hex[:6]}.txt"
        filepath = os.path.join(SUMMARY_DIR, filename)

        with open(filepath, "w") as f:
            f.write(summary)

        logging.info(f"💾 Summary saved to {filepath}")
        return {"summary": summary, "filename": filename}

    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"❌ Exception occurred: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

# ✅ Download Summary Route
@app.get("/download/{filename}")
async def download_summary(filename: str):
    filepath = os.path.join(SUMMARY_DIR, filename)
    if not os.path.exists(filepath):
        logging.warning(f"❌ Download failed — file not found: {filename}")
        raise HTTPException(status_code=404, detail="Summary file not found")

    logging.info(f"📤 Downloading file: {filename}")
    return FileResponse(
        filepath,
        media_type="text/plain",
        filename=filename
    )
