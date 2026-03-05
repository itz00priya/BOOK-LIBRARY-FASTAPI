import asyncio
from fastapi.testclient import TestClient
from app.main import app

def reproduce_error():
    client = TestClient(app)
    # Attempt to register a student
    user_data = {
        "username": "testuser_" + str(asyncio.get_event_loop().time()),
        "email": f"test_{asyncio.get_event_loop().time()}@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    print(f"Attempting to register user: {user_data['username']}")
    resp = client.post("/api/v1/users/register", json=user_data)
    
    print("Status Code:", resp.status_code)
    print("Response:", resp.text)
    
    if resp.status_code == 500:
        print("Reproduced 500 Internal Server Error")
    elif resp.status_code == 201:
        print("Registration successful (did not reproduce error)")
    else:
        print(f"Unexpected status code: {resp.status_code}")

if __name__ == "__main__":
    reproduce_error()
