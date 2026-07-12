from fastapi.testclient import TestClient


def test_login_and_profile(client: TestClient) -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin@shakar.ir", "password": "Admin@123456"},
    )
    assert login_response.status_code == 200
    token_payload = login_response.json()
    assert token_payload["access_token"]
    assert token_payload["refresh_token"]

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer " + token_payload["access_token"]},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@shakar.ir"
