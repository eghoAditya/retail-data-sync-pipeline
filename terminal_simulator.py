import requests
import uuid
import random
import time

API_BASE = "http://127.0.0.1:8000"


def send_event(terminal_id: str):
    payload = {
        "terminal_id": terminal_id,
        "receipt_id": str(uuid.uuid4()),
        "amount": round(random.uniform(100, 2000), 2),
        "currency": "INR",
    }

    try:
        resp = requests.post(f"{API_BASE}/events", json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(
            f"[OK] Sent event: terminal={data['terminal_id']} "
            f"receipt={data['receipt_id']} amount={data['amount']} status={data['status']}"
        )
    except Exception as e:
        print(f"[ERROR] Failed to send event: {e}")


if __name__ == "__main__":
    # Simulate a terminal sending 5 events
    terminal_id = "T-DELHI-001"
    for i in range(5):
        send_event(terminal_id)
        time.sleep(1)  # small delay between events
