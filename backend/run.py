"""Run script to seed DB and start the FastAPI server in one command.

Usage: run this from the `backend` folder:

    python run.py

This will ensure the SQLite DB and tables exist (and seed places), then start uvicorn.
"""
import importlib
import os
import sys
import uvicorn

HERE = os.path.abspath(os.path.dirname(__file__))
# Ensure backend folder is on path so `src` package imports work
if HERE not in sys.path:
    sys.path.insert(0, HERE)

def main():
    # Seed database (idempotent)
    try:
        seed_mod = importlib.import_module("src.seed")
    except Exception:
        print("Failed to import src.seed. Make sure you're running from the backend folder.")
        raise

    print("Seeding database (if needed)...")
    seed_mod.seed()

    # Start uvicorn programmatically
    print("Starting FastAPI (uvicorn) on http://0.0.0.0:8000 ...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
