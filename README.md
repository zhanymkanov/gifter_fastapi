Backend API for the e-commerce built with FastAPI

## Installation
1. Create `.env` file in the project directory with
```
DATABASE_URL=postgresql://postgres:postgres@db/postgres
ALGORITHM=HS256
SECRET_KEY=SECRET
```
2. Install with Docker
```
docker-compose build
```
## Usage
1. `docker-compose up`
2. Go to localhost:8000/docs
3. Play with Swagger Docs


## Pytest with flake8 and coverage
```
docker-compose exec gifter pytest
```

## Format with Black
```
docker-compose exec gifter ./format
```
