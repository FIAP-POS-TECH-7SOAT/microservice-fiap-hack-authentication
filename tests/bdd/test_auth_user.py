import requests
import pytest
from pytest_bdd import scenario, given, when, then, parsers

from adapters.drivens.infra.settings.env import ENV

env = ENV()
API_BASE_URL = env.BASE_URL

@pytest.fixture
def user_data():
    """Storage data from user and response"""
    return {}

@scenario("features/auth_user.feature", "Successful auth user")
def test_auth_user():
    """Execute scenario BDD"""
    pass

@given("I have the following user data", target_fixture="user_data")
def store_user_data():
    """Return data user"""
    return {
        "user_email": "test@gmail.com",
        "password": "dev123"
    }

@when(parsers.parse('I send a POST request to "{endpoint}"'))
def send_request(user_data, endpoint):
    """Send request to auth a user"""
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.post(url, json=user_data)
    user_data["response"] = response

@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(user_data, status_code):
    """Check return code"""
    assert user_data["response"].status_code == status_code

@then("the response should contain", target_fixture="user_data")
def check_response_message(user_data):
    """Check if is correct message"""
    response_json = user_data["response"].json()
    assert "token" in response_json
