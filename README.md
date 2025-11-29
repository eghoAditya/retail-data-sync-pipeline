# Retail Data Sync Pipeline

**Tech Used:** Python, FastAPI, MySQL, SQLAlchemy, Docker

A small retail-style backend that simulates data flow from POS terminals to a central backend using REST APIs and a MySQL database. Terminals send sale events, which are stored, listed, and monitored via metrics and logs to support debugging and observability.

---

## Features

- Ingests POS sale events from terminals via a FastAPI `/events` REST endpoint.
- Persists events in a MySQL `sale_events` table using SQLAlchemy ORM.
- Tracks event status (`PENDING` / `PROCESSED`) to mimic a sync workflow.
- Exposes `/events` listing API with optional filtering by status.
- Exposes `/metrics` endpoint for simple monitoring of total, pending, and processed events.
- Logs ingest, list, and metrics operations for basic observability and troubleshooting.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn  
- **Database:** MySQL, SQLAlchemy  
- **Infra/Tools:** Docker (for MySQL), logging

---

## Getting Started

### 1. Start MySQL in Docker

```bash
docker run --name retail-mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=retaildb \
  -p 3306:3306 \
  -d mysql:8
