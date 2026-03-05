from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_put_book_validations():
    # 1. Create two books
    client.post("/api/v1/books/", json={"title": "Book 1", "author": "Auth 1", "isbn": "2222222222222", "total_copies": 5})
    
    resp_create2 = client.post("/api/v1/books/", json={"title": "Book 2", "author": "Auth 2", "isbn": "3333333333333", "total_copies": 2})
    book_id_2 = resp_create2.json()["id"]

    # 2. Test 422 Unprocessable Entity - available_copies > total_copies
    resp_422 = client.put(f"/api/v1/books/{book_id_2}", json={"available_copies": 4, "total_copies": 3})
    assert resp_422.status_code == 422, f"Expected 422, got {resp_422.status_code}: {resp_422.text}"
    print("422 Validation Passed!")

    # 3. Test 400 Bad Request - ISBN collision
    resp_400 = client.put(f"/api/v1/books/{book_id_2}", json={"isbn": "2222222222222"})
    assert resp_400.status_code == 400, f"Expected 400, got {resp_400.status_code}: {resp_400.text}"
    print("400 ISBN Validation Passed!")

if __name__ == "__main__":
    test_put_book_validations()
