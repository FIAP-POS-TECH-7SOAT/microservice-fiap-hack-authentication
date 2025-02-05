from behave import given, when, then
from hamcrest import assert_that, equal_to

API_BASE_URL = "http://localhost:8000"

@given("I have the following user data")
def step_given_user_data(context):
    context.data = {row['field']: row['value'] for row in context.table}

@then(u'the response should contain')
def step_then_response_contains(context):
    response_json = context.response.json()
    assert_that(response_json['message'], equal_to("User created"))