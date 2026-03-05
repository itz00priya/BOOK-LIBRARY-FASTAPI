import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run():
    # First create a book
    resp_create = client.post(
        "/api/v1/books/",
        json={
            "title": "Initial Book",
            "author": "Initial Author",
            "isbn": "1111111111111",
            "total_copies": 1
        }
    )
    if resp_create.status_code != 201:
        print("Create failed", resp_create.text)
        return
        
    book_id = resp_create.json()["id"]
    print(f"Created book with ID {book_id}")

    # Create another book to cause an ISBN collision, or just do the PUT
    # We will just do the PUT first to see if it causes a 500 under normal conditions
    update_data = {
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
    }

    try:
        resp_put = client.put(f"/api/v1/books/{book_id}", json=update_data)
        print(f"Status: {resp_put.status_code}")
        print(f"Response: {resp_put.text}")
    except Exception as e:
        print(f"Client raised exception: {e}")

if __name__ == "__main__":
    run()
