# Book Library FastAPI

A modern, asynchronous RESTful API for a Book Library Management System built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: Secure signup and login using JWT (JSON Web Tokens) and bcrypt password hashing.
- **Book Management**: Full CRUD operations for books, including tracking total and available copies.
- **Borrowing System**: Borrow and return books with automated availability tracking.
- **Fine Management**: Integrated payment system using Stripe to handle fines for overdue books.
- **Asynchronous Database Access**: Uses `asyncpg` and SQLAlchemy 2.0 for high-performance database interactions.
- **Database Migrations**: Managed by Alembic for version-controlled schema updates.
- **API Documentation**: Interactive Swagger (OpenAPI) and ReDoc documentation.

## Tech Stack

- **Framework**: [FastAPI]
- **Database**: [PostgreSQL]
- **ORM**: [SQLAlchemy 2.0]
- **Migrations**: [Alembic]
- **Payments**: [Stripe]
- **Validation**: [Pydantic v2]

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Stripe Account (for payment features)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd book-library-fastapi
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   ```

5. **Run Migrations**:
   ```bash
   alembic upgrade head
   ```

### Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## API Endpoints

- `POST /api/v1/users/register`: Register a new user.
- `POST /api/v1/users/login`: Login to get an access token.
- `GET /api/v1/books`: List all books.
- `POST /api/v1/borrowings`: Borrow a book.
- `POST /api/v1/payments/create-checkout-session`: Create a Stripe checkout session for fines.

## License

This project is licensed under the MIT License.
