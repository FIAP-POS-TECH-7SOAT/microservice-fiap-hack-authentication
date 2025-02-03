import requests
from behave import given, when, then
from hamcrest import assert_that, equal_to

API_BASE_URL = "http://localhost:8000"

@when('I send a POST request to "{endpoint}"')
def step_when_send_post_request(context, endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    context.response = requests.post(url, json=context.data)

@then("the response status code should be {status_code}")
def step_then_response_status_code(context, status_code):
    assert_that(context.response.status_code, equal_to(int(status_code)))