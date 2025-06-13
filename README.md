# Smart Summarizer API 📝

A FastAPI-powered text summarization tool using OpenAI's GPT-3.5 Turbo.

---

## 🔧 Setup Instructions

1. **Clone and Navigate:**
   ```bash
   git clone https://github.com/your-username/smart_summarizer_api.git
   cd smart_summarizer_api
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Your `.env` File:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

5. **Run the App:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌟 Features

- 🔗 FastAPI backend  
- 🎨 Simple frontend with HTML/CSS (Poppins font)  
- 💬 Uses OpenAI’s GPT-3.5 Turbo API for summarization  
- 🧹 Clean and neutral summaries  
- 🛡️ CORS enabled for frontend/backend separation  

---

## 📁 Project Structure

```
smart_summarizer_api/
├── app/
│   ├── main.py
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   └── templates/
│       └── summarizer.html
├── .env                # (ignored by Git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔐 .env Security

`.env` file is ignored by Git thanks to `.gitignore`:
```
.env
```

---

## 📄 License

MIT License

---
