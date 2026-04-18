def test_chat_validation_errors_include_legal_information_boundary(client):
    response = client.post("/api/v1/chat/query", json={"question": "hi"})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error_code"] == "request_validation_failed"
    assert "legal information" in payload["boundary_note"].lower()
    assert "clearer legal-information question" in payload["detail"].lower()
