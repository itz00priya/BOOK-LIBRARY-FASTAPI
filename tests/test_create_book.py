from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book_copies():
    response = client.post(
        "/api/v1/books/",
        json={
            "title": "A Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "genre": "Fiction",
            "total_copies": 15
        }
    )
    
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    assert data["total_copies"] == 15
    assert data["available_copies"] == 15, "Available copies should match total copies"
    print("Test passed! available_copies correctly matches total_copies.")

if __name__ == "__main__":
    test_create_book_copies()
