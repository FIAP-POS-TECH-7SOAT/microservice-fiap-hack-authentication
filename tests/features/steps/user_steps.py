import requests
from behave import given, when, then
from hamcrest import assert_that, equal_to

API_BASE_URL = "http://localhost:5000"

@given("I have the following payment data")
def step_given_payment_data(context):
    context.payment_data = {row['field']: row['value'] for row in context.table}
    if context.payment_data.get("total_amount"):
        context.payment_data["total_amount"] = float(context.payment_data["total_amount"])

@when('I send a POST request to "{endpoint}"')
def step_when_send_post_request(context, endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    context.response = requests.post(url, json=context.payment_data)

@then("the response status code should be {status_code}")
def step_then_response_status_code(context, status_code):
    assert_that(context.response.status_code, equal_to(int(status_code)))

@then(u'the response should contain')
def step_then_response_contains(context):
    response_json = context.response.json()
    for row in context.table:
        expected_type = row['type']
        field_value = response_json[row['field']]
        type_map = {
            "string": str,
            "null": type(None),
            "error":str
        }
        assert_that(isinstance(field_value, type_map[expected_type]), 
                    f"Field '{row['field']}' expected to be of type '{expected_type}', but got '{type(field_value).__name__}'")