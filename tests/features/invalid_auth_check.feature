Feature: Invalid Authentication
  As a user of some system
  I want to handle invalid authentication
  So that I receive meaningful error messages

  Scenario: Missing required fields
    Given I have the following user data:
      | field        | value            |
      | user_email   | test_mail.com    |
    When I send a POST request to "/auth/check"
    Then the response status code should be 404
    And the response should contain:
      | field        | type             |
      | error        | string           |
