from pytest import raises
from fastapi import status, HTTPException
# from fastapi.testclient import TestClient

from modules.auth.token import verify_token, create_access_token

from env import get_env


env = get_env()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def test_validate_token_not_dev_env():
    env.environment = "some_env"
    validated_token = verify_token("fake token",credentials_exception)
    assert validated_token.get('email') == "test@test.com"

# def test_read_main():
#     env.environment = 'some_env'
#     assert response.status_code == status.HTTP_200_OK
#     # assert response.json() == 


fake_db = {
    "foo": {"id": "1", "username": "Foo","password": "PP"},
    "bar": {"id": "2", "username": "Bar","password": "PP" },
}





# def test_validate_token():
#     token = create_access_token(data={"sub": fake_db[user.id]})
#     print(verify_token(token,credentials_exception))
    
