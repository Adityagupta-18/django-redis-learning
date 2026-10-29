# Django Redis Learning

A hands-on project exploring Redis integration with Django, including caching, cache invalidation, data structures, and API rate limiting.

## Overview

This project demonstrates how Redis can improve a Django backend by caching frequently accessed data, storing temporary counters, and controlling API request rates.

The project focuses on learning Redis through practical backend implementations, Django REST Framework APIs, Django signals, and Postman testing.

## Tech Stack

- **Language:** Python
- **Backend:** Django, Django REST Framework
- **In-memory data store:** Redis
- **Database:** SQLite
- **Python Redis client:** `redis`
- **Environment configuration:** `python-dotenv`
- **API testing:** Postman
- **Redis inspection:** RedisInsight

## Features Implemented

### 1. Redis Integration

- Connected Django to Redis using a configurable Redis URL.
- Tested direct Redis operations through Python.
- Used Django's cache framework with Redis as the configured backend.
- Kept environment-specific configuration in a `.env` file.

### 2. API Response Caching

- Created a Product model with name, price, and stock fields.
- Implemented a product-list API endpoint.
- Cached database query results in Redis for 60 seconds.
- Implemented cache-hit and cache-miss behavior.
- Tested API responses using Postman.

**Endpoint:** `GET /api/products/`

### 3. Automatic Cache Invalidation

- Used Django `post_save` and `post_delete` signals to invalidate the cached product list.
- Ensured product updates and deletions do not leave the cached list stale until its original expiry.
- Tested cache invalidation by modifying product records and requesting the API again.

### 4. Direct Redis Operations

Practised Redis commands through the Python Redis client, including:

- **Strings:** Store and retrieve values.
- **Counters:** Increment request counts with `INCR`.
- **Expiry:** Set key expiration with `EXPIRE` and inspect remaining time with `TTL`.
- **Hashes:** Store related fields under one key.
- **Lists:** Store and retrieve ordered collections of events.
- **Sets:** Store unique values and count set members.

Also practised Redis data structures through the Redis CLI.

### 5. Custom Redis-Based Rate Limiting

Implemented a custom rate-limited Django endpoint using a Redis counter.

- Identifies requests using the client's IP address.
- Allows five requests per 60-second fixed window.
- Increments the counter using Redis `INCR`.
- Sets an expiry for the counter.
- Uses a Lua script to execute the increment-and-expiry logic atomically.
- Returns HTTP `429 Too Many Requests` when the limit is exceeded.
- Includes a `Retry-After` response header.

**Endpoint:** `GET /api/rate-limit-test/`

### 6. Django REST Framework Throttling

Implemented a separate endpoint using DRF's built-in `ScopedRateThrottle`.

- Configured a named throttle scope in Django settings.
- Set the `test` scope to five requests per minute.
- Used Django's configured Redis cache backend for throttle data.
- Tested allowed and throttled requests using Postman.

**Endpoint:** `GET /api/drf-throttle-test/`

The project demonstrates the difference between custom Redis rate limiting and DRF's built-in throttling.

## How Redis Is Used

This project demonstrates two integration approaches:

**Django cache framework**

Used for caching database query results and invalidating cached data when the underlying model changes.

**Direct Redis client**

Used for counters, expiry, hashes, lists, sets, and the custom rate-limiting implementation.

Both approaches connect to the configured Redis server, but the direct client provides access to Redis commands beyond the basic cache interface.

## Project Setup

### Prerequisites

- Python and pip
- Redis server
- Git

Docker can be used to run Redis locally.

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/django-redis-learning.git
cd django-redis-learning
```

Replace `<your-username>` with your GitHub username.

### 2. Create and Activate the Virtual Environment

On Linux or WSL Ubuntu:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis

If using Docker for a new Redis Stack container:

```bash
docker run -d \
  --name redis-stack \
  -p 6379:6379 \
  -p 8001:8001 \
  redis/redis-stack:latest
```

If the `redis-stack` container already exists but is stopped:

```bash
docker start redis-stack
```

RedisInsight is available at `http://localhost:8001` when the container is running and the port is accessible.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=replace-with-your-secret-key
REDIS_URL=redis://localhost:6379/0
```

Use a private Django secret key. Do not commit `.env` or real secrets to GitHub.

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

The application runs at `http://127.0.0.1:8000/`.

## Testing with Postman

Use the following endpoints to explore the implemented features:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products/` | Test API caching and cache hits/misses |
| GET | `/api/rate-limit-test/` | Test custom Redis rate limiting |
| GET | `/api/drf-throttle-test/` | Test DRF scoped throttling |

For both rate-limiting endpoints, send repeated requests within the configured window and verify that the limit eventually produces a `429 Too Many Requests` response.

For cache testing, compare repeated product-list requests and modify a product record to observe cache invalidation.

## Security and Production Considerations

- Keep secret keys and environment-specific settings out of version control.
- Use a shared Redis-backed cache when running multiple Django application instances.
- Treat IP-based limiting carefully when applications run behind proxies or load balancers.
- DRF's built-in throttling is useful for application-level usage policies, but its standard implementation may allow extra requests under concurrency.
- Use appropriately designed atomic rate-limiting logic when strict limits are required.
- Login, password-reset, and OTP endpoints require additional security controls beyond ordinary API throttling.
- Configure Redis access controls, networking, and production credentials appropriately.

This project is a learning implementation, not a complete production security solution.

## Learning Outcomes

Through this project, I practised:

- Connecting Redis to a Django application.
- Caching database query results and invalidating stale cache entries.
- Using Django signals for cache invalidation.
- Working with Redis strings, counters, hashes, lists, and sets.
- Understanding TTL and automatic key expiration.
- Implementing custom rate limiting with Redis and Lua.
- Configuring and testing Django REST Framework throttling.
- Comparing custom Redis operations with Django's higher-level cache and API abstractions.

## Future Learning

- Celery with Redis as a message broker.
- Background task processing in Django.
- Further exploration of caching strategies and backend performance.
