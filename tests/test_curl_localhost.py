import requests

url = "http://localhost:8000/api/v1/books/3"
payload = {
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
    response = requests.put(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
