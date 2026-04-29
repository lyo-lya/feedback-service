import os
import json
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient
from sqlalchemy import text
from db import engine
from datetime import datetime

load_dotenv()

CONNECTION_STR = os.getenv("SERVICE_BUS_CONNECTION_LISTEN")
QUEUE_NAME = "volhaplatnitskaya"


def listen_to_queue():
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        receiver = client.get_queue_receiver(queue_name=QUEUE_NAME)

        with receiver:
            messages = receiver.receive_messages(
                max_message_count=5,
                max_wait_time=5
            )

            for msg in messages:
                body = b"".join(msg.body).decode("utf-8")
                data = json.loads(body)

                print("Received:", data)

                with engine.connect() as conn:
                    conn.execute(
                        text("""
                             INSERT INTO Volha_Platnitskaya_feedback.Feedback
                                 (submissionId, score, comment, createdAt)
                             VALUES (:subId, :score, :comment, :createdAt)
                             """),
                        {
                            "subId": data["submissionId"],
                            "score": 5,
                            "comment": "Auto feedback",
                            "createdAt": datetime.utcnow()
                        }
                    )
                    conn.commit()

                receiver.complete_message(msg)