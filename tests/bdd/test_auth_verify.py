import base64, uuid
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

import requests
import pytest
from jose import jwt
from pytest_bdd import scenario, given, when, then, parsers

from adapters.drivens.infra.settings.env import ENV

env = ENV()
API_BASE_URL = env.BASE_URL
serializer = URLSafeTimedSerializer(env.SALT_KEY)

@pytest.fixture
def token_data():
    """Storage data from token and response"""
    return {}

@scenario("features/auth_verify.feature", "Successful verification of auth user")
def test_verify_auth():
    """Execute scenario BDD"""
    pass

@given("I have the following token data", target_fixture="token_data")
def store_token_data():
    """Return json token with user data"""
    private_key = base64.b64decode(env.PRIVATE_KEY).decode('utf-8')
    token = jwt.encode(
                    {
                        "sub": str(uuid.uuid4()),
                        "user_email": "test@gmail.com",
                        "phone": "+5511912347896",
                        "exp": datetime.now() + timedelta(days=int(env.EXP_DATE)),
                        "iat": datetime.now(),
                    },
                    private_key,
                    algorithm="RS256",
                )
    return {
        "token": token
    }

@when(parsers.parse('I send a POST request to "{endpoint}"'))
def send_request(token_data, endpoint):
    """Send request to verify auth of user"""
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.post(url, json=token_data)
    token_data["response"] = response

@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(token_data, status_code):
    """Check return code"""
    assert token_data["response"].status_code == status_code

@then("the response should contain")
def check_response_message(token_data):
    """Check if response contains correct message"""
    response_json = token_data["response"].json()
    assert response_json["payload"]["user_email"] == "test@gmail.com"
    assert response_json["payload"]["phone"] == "+5511912347896"
