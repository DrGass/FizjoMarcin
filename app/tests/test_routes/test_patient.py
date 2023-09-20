from fastapi import status

root_path = "/patient"

def create_user(name, password, client):
    payload = {"username": f"{name}", "password": f"{password}"}
    response = client.post(f"{root_path}", json=payload)
    return response


def create_patient(id, name, surname, age, client):
    payload = {
        "name": f"{name}",
        "surname": f"{surname}",
        "age": age,
        "owner_id": id,
    }
    response = client.post(f"patient", json=payload)
    return response

def test_create_patient(client):
    create_user("bartosz", "górski", client)
    response = create_patient(1,"marcin", "górski",30, client)
    assert response.status_code == 201
    assert response.json()["success"] == True


def test_get_all_patient_empty(client):
    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_patients_multiple_patients(client):
    create_user("bartosz", "górski", client)
    create_patient(1,"1marcin", "1górski",10, client)
    create_patient(1,"2marcin", "2górski",20, client)
    create_patient(1,"3marcin", "3górski",30, client)

    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "1marcin", "surname": "1górski"},
        {"name": "2marcin", "surname": "2górski"},
        {"name": "3marcin", "surname": "3górski"}
    ]


def test_get_patient_by_id(client):
    create_user("1bartosz", "1górski", client)
    create_patient(1,"1marcin", "1górski",10, client)

    response = client.get(f"{root_path}/1")
    assert response.json() == {"name": "1marcin", "surname": "1górski"}
    assert response.status_code == 200


# Can't do it as database gives numbers by itself
# def test_get_not_existing_user_by_id(client):
#     response = client.get(f"{root_path}/0")
#     assert response.json() == {"detail": "User with number 0 is not avaiable"}
#     assert response.status_code == 404

def test_delete_user(client):
    create_user("1bartosz", "1górski", client)
    response = client.delete(f"{root_path}/1")
    assert response.status_code == 204
