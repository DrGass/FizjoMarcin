from fastapi import status

root_path = "/patient"


def test_user(client):
    response = client.get(f"{root_path}/")
    assert response.json() == []
    assert response.status_code == 200


# def test_create_user(client):
#    response = client.get(f"{root_path}/")
