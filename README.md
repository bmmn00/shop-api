# Shop API — Хичээл 81 starter

Локал:
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env        # DATABASE_URL-ээ шалга
    fastapi dev main.py         # http://127.0.0.1:8000/docs

Prod шиг локал:
    uvicorn main:app --host 0.0.0.0 --port 8000

Deploy: lab guide-ийг үз (L81_Lab_Guide.md).
