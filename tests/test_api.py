from unittest.mock import patch, MagicMock


def test_get_feedback(client):
    response = client.get("/feedback")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.db.engine.connect")
def test_feedback_db_mock(mock_connect, client):

    mock_conn = MagicMock()
    mock_result = MagicMock()

    mock_result.__iter__.return_value = [
        MagicMock(_mapping={
            "feedbackId": 1,
            "submissionId": 10,
            "score": 5,
            "comment": "Great",
            "createdAt": "2026-01-01"
        })
    ]

    mock_conn.execute.return_value = mock_result
    mock_connect.return_value.__enter__.return_value = mock_conn

    response = client.get("/feedback")

    assert response.status_code == 200
    assert response.json()[0]["feedbackId"] == 1