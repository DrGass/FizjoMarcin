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
   # {'creaśted_id:': 0, 'success': True}
   assert response.json()['success'] == True
   # assert response.json()['created_id'] == 0
    
def test_get_all_user_empty(client):
    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() == []

def create_user(id,name,password,client):
    payload = {
               "id": id,
               "username": f"{name}",
               "password": f"{password}"
               }
    client.post(f"{root_path}/create", json=payload)

def test_get_all_user_multiple_users(client):
    create_user(0,"0bartosz","0górski",client)
    create_user(1,"1bartosz","1górski",client)
    create_user(2,"2bartosz","2górski",client)

    response = client.get(f"{root_path}/")
    assert response.status_code == 200
    assert response.json() ==  [             
          
           {'id': 0,
            'patients': [],
            'username': '0bartosz'},
           {'id': 1,
            'patients': [],
            'username': '1bartosz'},
           {'id': 2,
            'patients': [],
            'username': '2bartosz'},
           ]