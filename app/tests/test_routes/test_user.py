root_path = "/user/"

def test_create_new_user(client):
   response = client.get(f"{root_path}/create/")




