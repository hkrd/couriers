from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

def test_earnings_endpoint():
    # Example activity log data

    with open("tests/test_payload.json", "r") as f:
        activity_log_data = json.loads(f.read())

    # Choose a rate card ID for testing
    rate_card_id = "platinum_tier"

    # Make a POST request to the endpoint
    response = client.post(f"api/v1/earnings/{rate_card_id}", json=activity_log_data)

    # Verify the status code
    assert response.status_code == 200

    # Verify part of the response
    with open("tests/expected_response.json", "r") as f:
        expected = json.loads(f.read())
        assert response.json() == expected
