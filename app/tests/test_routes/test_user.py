from fastapi import status

root_path = "/user"


def create_user(name, password, client):
    payload = {"username": f"{name}", "password": f"{password}"}
    response = client.post(f"{root_path}/create", json=payload)
    return response


def create_patient(id, name, surname, age, client):
    payload = {
        "name": f"{name}",
        "surname": f"{surname}",
        "age": age,
        "owner_id": id,
    }
    client.post(f"patient", json=payload)

# It's the same as get all users empty
# def test_user(client):
#     response = client.get(f"{root_path}/")
#     assert response.json() == []
#     assert response.status_code == 200


def test_get_all_user_empty(client):
    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_patient(client):
    response = create_user("0bartosz", "0górski", client)
    assert response.status_code == 201
    assert response.json()["success"] == True

# Again, nonsense as i don't have unique nicknames
# def test_create_existing_user(client):
#     create_user("0bartosz", "0górski", client)
#     response = create_user("0bartosz", "0górski", client)


def test_get_all_user_multiple_users(client):
    create_user("1bartosz", "1górski", client)
    create_user("2bartosz", "2górski", client)
    create_user("3bartosz", "3górski", client)

    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "patients": [], "username": "1bartosz"},
        {"id": 2, "patients": [], "username": "2bartosz"},
        {"id": 3, "patients": [], "username": "3bartosz"},
    ]


def test_get_user_by_id(client):
    create_user("1bartosz", "1górski", client)

    response = client.get(f"{root_path}/1")
    assert response.json() == {"username": "1bartosz", "id": 1, "patients": []}
    assert response.status_code == 200


def test_get_patient_by_id(client):
    create_user("1bartosz", "1górski", client)
    create_patient(1, "0marcin", "0górski", 30, client)
    response = client.get(f"{root_path}/1")
    assert response.json() == {
        "username": "1bartosz",
        "id": 1,
        "patients": [{"name": "0marcin", "surname": "0górski"}],
    }
    assert response.status_code == 200


def test_delete_user(client):
    create_user("0bartosz", "0górski", client)
    response = client.delete(f"{root_path}/delete/1")
    assert response.status_code == 204
