from fastapi import FastAPI
import threading
import time
from service_bus_listener import listen_to_queue

app = FastAPI(title="Feedback Service")


@app.get("/feedback")
def get_feedback():
    from sqlalchemy import text
    from db import engine

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM Volha_Platnitskaya_feedback.Feedback")
        )
        return [dict(row._mapping) for row in result]


def background_worker():
    while True:
        try:
            listen_to_queue()
        except Exception as e:
            print("Error in worker:", e)

        time.sleep(5)


@app.on_event("startup")
def start_worker():
    thread = threading.Thread(target=background_worker)
    thread.daemon = True
    thread.start()