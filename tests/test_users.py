def test_create_user(client):
    response = client.post(
        "/user/create", json={"name": "John", "email": "john@gmail.com"}
    )

    assert response.status_code == 200
    assert "id" in response.json()


def test_get_user(client):
    res = client.post(
        "/user/create", json={"name": "Alice", "email": "alice@gmail.com"}
    )

    user_id = res.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user(client):
    res = client.post("/user/create", json={"name": "Bob", "email": "bob@gmail.com"})

    user_id = res.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"name": "Bob Updated", "email": "bobupdated@gmail.com"},
    )

    assert response.status_code == 200


def test_delete_user(client):
    res = client.post(
        "/user/create", json={"name": "Delete Me", "email": "delete@gmail.com"}
    )

    user_id = res.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200


def test_user_not_found(client):
    response = client.get("/users/999999")
    assert response.status_code == 404
