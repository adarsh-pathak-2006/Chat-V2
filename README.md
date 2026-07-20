# Chat-V2 Backend

A production-ready, full-stack real-time chat application backend built with Django REST Framework and Django Channels (WebSockets).

## Features

- **Real-Time WebSockets:** Instant messaging powered by Django Channels and Redis.
- **Custom JWT Authentication:** Secure WebSocket and HTTP endpoints using `rest_framework_simplejwt`.
- **Throttling & Rate Limiting:** Protection against API abuse and brute-force attacks.
- **Automated Testing:** Comprehensive `APITestCase` suite for core chat and registration logic.
- **Production Ready:** Pre-configured for deployment (WhiteNoise for static files, CORS headers, environment variables).

## Tech Stack

- **Framework:** Django & Django REST Framework (DRF)
- **WebSockets:** Django Channels & Redis
- **Auth:** JWT (JSON Web Tokens)
- **Database:** SQLite (Local) / PostgreSQL (Production)
- **ASGI Server:** Uvicorn

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/adarsh-pathak-2006/Chat-V2.git
cd Chat-V2
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Leave the defaults as-is for local development.

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
uvicorn chat.asgi:application --reload
```
*Note: You must have a local Redis server running on port `6379` for WebSockets to function.*

## API Documentation

Interactive API documentation is automatically generated using `drf-spectacular`. When the server is running, visit:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`

## Deployment (Render / Railway)

This project is fully configured for deployment on platforms like Render.

1. **Build Command:** `./build.sh`
2. **Start Command:** `uvicorn chat.asgi:application --host 0.0.0.0 --port $PORT`
3. **Environment Variables:**
   - `SECRET_KEY`: Your secure secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your deployment URL (e.g., `your-app.onrender.com`)
   - `CORS_ALLOW_ALL_ORIGINS`: `False`
   - `CORS_ALLOWED_ORIGINS`: Your frontend URL
   - `REDIS_URL`: Your production Redis connection string
   - `DATABASE_URL`: Your PostgreSQL connection string (Optional)
