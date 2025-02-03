import requests
from behave import given, when, then
from hamcrest import assert_that, equal_to

API_BASE_URL = "http://localhost:8000"

@given("I have the following token")
def step_given_valid_token(context):
    context.data = {"token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwNThmNTYwMC0wNTBhLTRiMjItOWRiYy1iOGJkMjA4MjkzZmIiLCJ1c2VyX2VtYWlsIjoidGVzdGVAZ21haWwuY29tIiwicGhvbmUiOiIrNTUxMTk2NzM1OTcwNyIsImV4cCI6MTczODg0MjE5OCwiaWF0IjoxNzM4MjM3Mzk4fQ.KjDxlIJouEOBv9AJcK3dnHmWgFoo_XUBF6yuvf6ToCZq2mS5NfvwDtdTeq3aaz1RBstYgAy1kopGFhXpDqyY0Vlu4ESVtSD1fd37Ea13car4JXFmilvDZpiUhIZHG_M-nPf5saUjI88txhwZpZ_p6JxBfI60LF8LlQ5465VMwpll2wsl5kgKjq4YK5qZ6gZcGHT8mtV-maKOkwmqJykDw6D4OfT6YOiZPqNMNmij0yRmzKJf23KWTxK7hnHFCLD77SjWPX62AxYn4FAOX6UzJ6Umlfl8RtNzyt-962fO_ZjaKluVGjnh5JKXkCZWe1JwRdySy8S4BAMDCdBVINIoww"}

@then('the response should contain payload')
def step_then_response_contains_payload(context):
    response_json = context.response.json()
    assert 'payload' in response_json, "Payload not found in response"
