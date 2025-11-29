# Retail Data Sync Pipeline

Tech Used: Python, FastAPI, MySQL, Docker

This service simulates terminal → backend → database communication for retail POS:
- Terminals send sales events (JSON) to FastAPI.
- FastAPI stores events in MySQL with batched inserts.
- Background worker marks events as processed and exposes simple monitoring endpoints.
