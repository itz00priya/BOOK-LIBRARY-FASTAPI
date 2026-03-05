import asyncio
import sys
import traceback
from fastapi.testclient import TestClient
from app.main import app
from app.config.database import engine
from app.config.base import Base

def run():
    client = TestClient(app)
    # Create a book
    resp = client.post("/api/v1/books/", json={
        "title": "The Hitchhiker's Guide",
        "author": "Douglas Adams",
        "isbn": "0330258648",
        "total_copies": 3
    })
    
    if resp.status_code != 201:
        print("Failed to create book:", resp.text)
        book_id = 3 # Just guessing or fallback
    else:
        book_id = resp.json()["id"]
        print(f"Created book {book_id}")

    # Now do the exact PUT request that caused 500
    try:
        put_resp = client.put(f"/api/v1/books/{book_id}", json={
          "author": "Douglas Adams",
          "available_copies": 4,
          "description": "Don't panic! Now with extra panic.",
          "genre": "Science Fiction",
          "isbn": "0330258648",
          "language": "English",
          "pages": 224,
          "price": 24.99,
          "publication_year": 1979,
          "publisher": "Pan Books",
          "title": "The Hitchhiker's Guide to the Galaxy (Special Edition)",
          "total_copies": 3
        })
        print("Status Code:", put_resp.status_code)
        print("Response:", put_resp.text)
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    run()
