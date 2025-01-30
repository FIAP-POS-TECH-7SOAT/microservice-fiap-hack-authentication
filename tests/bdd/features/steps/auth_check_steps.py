import requests
from behave import given, when, then
from hamcrest import assert_that, equal_to

API_BASE_URL = "http://localhost:8000"

@given("I have the following credentials")
def step_given_valid_user_credentials(context):
    context.data = {"user_email": "teste@gmail.com", "password": "dev123"}

@then('the response should contain token')
def step_then_response_contains_token(context):
    response_json = context.response.json()
    assert 'token' in response_json, "Token not found in response"
