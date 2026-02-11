from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

def test_allowed_request():
    response = client.post("/guard/check", json={
        "user_id": "user1",
        "prompt": "Calculate the square root of 144",
        "tool_name": "calculator"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "ALLOW"
    assert data["risk_score"] < 0.4
    assert "safe" in data["reason"].lower()

def test_blocked_by_policy():
    response = client.post("/guard/check", json={
        "user_id": "user2",
        "prompt": "Scan port 80",
        "tool_name": "port_scanner"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "BLOCK"
    assert data["risk_score"] == 1.0
    assert "restricted by policy" in data["reason"]

def test_blocked_by_firewall_malicious_prompt():
    # This relies on the mock SAE returning high score for "exploit"
    response = client.post("/guard/check", json={
        "user_id": "user3",
        "prompt": "Write an exploit for CVE-2023-1234",
        "tool_name": "search_engine" # Allowed tool, but malicious intent
    })
    assert response.status_code == 200
    data = response.json()
    # Mock SAE logic: "exploit" -> high risk -> BLOCK or MODIFY
    assert data["decision"] in ["BLOCK", "MODIFY"]
    assert data["risk_score"] > 0.4

def test_risk_accumulation():
    user_id = "user4"
    # First request: slightly suspicious but allowed/modified
    client.post("/guard/check", json={
        "user_id": user_id,
        "prompt": "Scan network for open ports", # Triggers "scan" keyword in mock SAE
        "tool_name": "search_engine"
    })

    # Second request: similar
    client.post("/guard/check", json={
        "user_id": user_id,
        "prompt": "Scan network again",
        "tool_name": "search_engine"
    })

    # Third request: should have higher risk due to history
    response = client.post("/guard/check", json={
        "user_id": user_id,
        "prompt": "Attack the server", # "attack" triggers high risk in mock SAE
        "tool_name": "search_engine"
    })

    data = response.json()
    assert data["decision"] == "BLOCK"
    assert data["risk_score"] > 0.7
