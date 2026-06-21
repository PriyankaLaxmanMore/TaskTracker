def test_healthz(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz(client):
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "status" in response.json()
