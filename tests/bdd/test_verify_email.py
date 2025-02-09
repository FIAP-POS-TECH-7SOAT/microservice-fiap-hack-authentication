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

@scenario("features/verify_email.feature", "Successful verify email")
def test_verify_email():
    """Execute scenario BDD"""
    pass

@given("I have the following token data", target_fixture="token_data")
def store_token_data():
    """Return json token serialized"""
    token = serializer.dumps("test@gmail.com", salt=env.SALT_KEY)
    return {
        "token": token
    }

@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_request(token_data, endpoint):
    """Send request to verify email"""
    url = f"{API_BASE_URL}{endpoint}/{token_data['token']}"
    response = requests.get(url)
    token_data["response"] = response

@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(token_data, status_code):
    """Check return code"""
    assert token_data["response"].status_code == status_code

@then("the response should contain")
def check_response_message(token_data):
    """Check if response contains correct message"""
    response_json = token_data["response"].json()
    assert response_json["message"] == "Email verified successfully!"
