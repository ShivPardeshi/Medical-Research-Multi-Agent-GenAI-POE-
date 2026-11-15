"""Tests for Input Validation and Error Handling in MediResearch AI."""

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_empty_payload():
    """Verify empty POST payload returns 422 Unprocessable Entity."""
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_short_question():
    """Verify question below 5 characters is rejected with 422."""
    response = client.post("/ask", json={"question": "med?"})
    assert response.status_code == 422


def test_ask_whitespace_only():
    """Verify question containing only whitespace is rejected with 422."""
    response = client.post("/ask", json={"question": "          "})
    assert response.status_code == 422


def test_ask_missing_api_key(monkeypatch):
    """Verify 503 Service Unavailable when API key is unconfigured."""
    monkeypatch.setattr("app.config.GROQ_API_KEY", "")
    monkeypatch.setattr("app.config.GEMINI_API_KEY", "")
    response = client.post(
        "/ask",
        json={"question": "What are the first-line therapies for Type 2 Diabetes with CKD?"}
    )
    assert response.status_code == 503
    data = response.json()
    assert "API key is not configured" in data["detail"]


def test_ask_success_with_mocked_workflow(monkeypatch):
    """Verify successful response formatting when LLM and workflow return an answer."""
    monkeypatch.setattr("app.config.GROQ_API_KEY", "mock_valid_key_123")

    mock_result = {
        "answer": "SGLT2 inhibitors and Metformin are recommended first-line agents in T2D with CKD.",
        "sources": ["Type 2 Diabetes Mellitus: ADA Standards of Care & Cardiorenal Protection"],
    }

    with patch("app.main.run_medical_workflow", return_value=mock_result):
        response = client.post(
            "/ask",
            json={"question": "What is recommended for Type 2 Diabetes with eGFR 44?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "SGLT2 inhibitors" in data["answer"]
        assert "Type 2 Diabetes Mellitus: ADA Standards of Care & Cardiorenal Protection" in data["sources"]
        assert "Medical Disclaimer:" in data["disclaimer"]
