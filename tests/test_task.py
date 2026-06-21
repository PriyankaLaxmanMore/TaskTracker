def test_create_task(client):
    user = client.post(
        "/user/create", json={"name": "Task User", "email": "taskuser@gmail.com"}
    ).json()

    response = client.post(
        "/tasks/create",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "user_id": user["id"],
        },
    )

    assert response.status_code == 200
    assert "id" in response.json()


def test_get_task(client):
    user = client.post(
        "/user/create", json={"name": "John Task", "email": "john.task@gmail.com"}
    ).json()

    task = client.post(
        "/tasks/create",
        json={"title": "Task 1", "description": "Desc", "user_id": user["id"]},
    ).json()

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == task["id"]


def test_update_task(client):
    user = client.post(
        "/user/create",
        json={"name": "Update Task User", "email": "update.task@gmail.com"},
    ).json()

    task = client.post(
        "/tasks/create",
        json={"title": "Old Task", "description": "Old Desc", "user_id": user["id"]},
    ).json()

    response = client.put(
        f"/tasks/{task['id']}", json={"title": "Updated Task", "completed": True}
    )

    assert response.status_code == 200


def test_delete_task(client):
    user = client.post(
        "/user/create",
        json={"name": "Delete Task User", "email": "delete.task@gmail.com"},
    ).json()

    task = client.post(
        "/tasks/create",
        json={"title": "Task to Delete", "description": "Desc", "user_id": user["id"]},
    ).json()

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 200


def test_task_not_found(client):
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999999", json={"title": "Does not exist", "completed": True}
    )

    assert response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999999")
    assert response.status_code == 404


def test_list_tasks(client):
    user = client.post(
        "/user/create", json={"name": "List Task User", "email": "list.task@gmail.com"}
    ).json()

    client.post(
        "/tasks/create",
        json={"title": "Task A", "description": "A", "user_id": user["id"]},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_tasks_with_filters(client):
    user = client.post(
        "/user/create",
        json={"name": "Filter Task User", "email": "filter.task@gmail.com"},
    ).json()

    client.post(
        "/tasks/create",
        json={
            "title": "Task Filter",
            "description": "Filter Desc",
            "user_id": user["id"],
            "completed": False,
        },
    )

    response = client.get(f"/tasks?user_id={user['id']}&completed=false")

    assert response.status_code == 200
