# Expense Tracker Backend API

A backend API for tracking personal expenses. I built this project to understand how backend systems handle authentication, database integration, and protected CRUD operations in a more practical way.

This was my first backend project, and it helped me move beyond basic CRUD by working with authentication and persistent data.

Users can register, log in, add expenses, view them, update them, and delete them through API endpoints.

Interactive API docs are available at `/docs` when the server is running.

## Live Demo

- API Base URL: `https://expense-tracker-api-4tzg.onrender.com`
- Swagger Docs: `https://expense-tracker-api-4tzg.onrender.com/docs`

## Features

- User registration and login
- JWT-based authentication
- Protected expense CRUD operations
- PostgreSQL integration using SQLAlchemy
- Health check endpoint
- Pytest-based API testing
- Docker support for local setup

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Pytest
- Docker

## Project Structure

    app/
    ├── api/
    │   ├── routes/
    │   └── dependencies/
    ├── core/
    │   ├── config.py
    │   └── security.py
    ├── db/
    │   ├── models.py
    │   ├── session.py
    │   └── base.py
    ├── schemas/
    ├── services/
    └── main.py

    tests/
    docker/
    .env

## API Endpoints

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Expenses

- `POST /expenses`
- `GET /expenses`
- `PUT /expenses/{id}`
- `DELETE /expenses/{id}`

### Health

- `GET /health`

## Local Setup

    git clone https://github.com/jayanthjinka/expense-tracker-api.git
    cd expense-tracker-api
    python -m venv venv
    ./venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

## Docker Setup

    docker-compose up --build

## Environment Variables

    DATABASE_URL=postgresql://user:password@db:5432/expenses
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

## Testing

    pytest

## Security

- Password hashing with bcrypt
- JWT-based authentication
- Protected routes
- Environment variables for secrets

## What I Learned

This project helped me understand:

- how JWT authentication works in APIs
- how FastAPI works with PostgreSQL using SQLAlchemy
- how to separate routes, schemas, and database logic
- how protected routes and request validation work together

## Author

**Jayanth Jinka**

## License

MIT License
