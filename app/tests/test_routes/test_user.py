from fastapi import status

root_path = "/user"


def test_user(client):
    response = client.get(f"{root_path}/")
    assert response.json() == []
    assert response.status_code == 200


def test_create_user(client):
   payload = {
               "id": 0,
               "username": "bartosz",
               "password": "gorski"
               }
   response = client.post(f"{root_path}/create", json=payload)
   assert response.status_code == 201
   # {'created_id:': 0, 'success': True}
   assert response.json()['success'] == True
   # assert response.json()['created_id'] == 0
    
