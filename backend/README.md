Backend for Lonq Frontend

FastAPI + SQLite backend that serves travel places and tracks user actions.

Quick start (from project root):

```bash
cd backend
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python run.py  # seed the DB with travel places and start the server

If you prefer package-style startup with uvicorn directly (advanced):

```bash
# from backend folder
uvicorn src.main:app --reload --port 8000
```
```

API endpoints:
- `GET /places?limit=<n>` - list places (optional `limit`)
- `GET /places/{place_id}` - get single place
- `POST /users/track` - track user action (body: `user_id`, optional `action`, `place_id`)

Cors is enabled for common frontend dev hosts (Vite on localhost:5173).
