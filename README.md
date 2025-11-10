# Book Shop API

A FastAPI-based REST API for managing a book shop inventory system with PostgreSQL database integration.

## Features

- **Book Management**: Create, read, update, and delete books
- **Inventory Tracking**: Track book inventory with counts and pricing
- **RESTful API**: Clean REST endpoints for all operations
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Auto Documentation**: Interactive API docs with Swagger UI

## Architecture

### Layered Architecture
- **Route Layer (HTTP)**: FastAPI routes handling HTTP requests and responses
- **Repository Layer**: Business logic and database interactions
- **Model Layer**: SQLAlchemy ORM models for database entities
- **Schema Layer**: Pydantic models for request/response validation

### Project Structure
```
app/
├── api/
│   ├── models/          # SQLAlchemy database models
│   ├── repositories/    # Data access layer
│   ├── routes/          # FastAPI route handlers
│   ├── schemas/         # Pydantic schemas
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection setup
│   ├── dependencies.py  # Dependency injection
│   └── main.py          # Application entry point
└── test/                # Test files
```

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL database
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Configure environment variables**
   Create `.env` file in `app/` directory:
   ```env
   POSTGRES_DB=your_database_name
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

5. **Starting the Server**
```bash
python app/api/main.py
```
The API will be available at `http://localhost:8000`

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`


## Development

### Database Migrations
The application automatically creates database tables on startup using SQLAlchemy's `create_all_tables()` function.

### Adding New Features
1. Create model in `models/`
2. Add repository in `repositories/`
3. Define schemas in `schemas/`
4. Implement routes in `routes/`
5. Update dependencies if needed

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation

## License

This project is licensed under the MIT License.