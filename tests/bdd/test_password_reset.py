from itsdangerous import URLSafeTimedSerializer

import requests
import pytest
from pytest_bdd import scenario, given, when, then, parsers

from adapters.drivens.infra.settings.env import ENV

env = ENV()
API_BASE_URL = env.BASE_URL
serializer = URLSafeTimedSerializer(env.SALT_KEY)

@pytest.fixture
def token_data():
    """Storage data from token and response"""
    return {}

@scenario("features/password_reset.feature", "Successful change password")
def test_password_reset():
    """Execute scenario BDD"""
    pass

@given("I have the following token data", target_fixture="token_data")
def store_token_data():
    """Return json token with user data"""
    token = serializer.dumps("test@gmail.com", salt=env.SALT_KEY)
    return {
        "token": token,
        "new_password": "test123"
    }

@when(parsers.parse('I send a POST request to "{endpoint}"'))
def send_request(token_data, endpoint):
    """Send request to reset password"""
    url = f"{API_BASE_URL}{endpoint}/{token_data["token"]}"
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
    assert response_json["message"] == "Password reset successful"
