from pytest import raises
from fastapi import status, HTTPException

# from fastapi.testclient import TestClient

from modules.auth.token import verify_token, create_access_token

from env import get_env

env = get_env()

def test_validate_token_not_dev_env():
    env.environment = "some_env"
    validated_token = verify_token("fake token")
    assert validated_token.get("email") == "test@test.com"
