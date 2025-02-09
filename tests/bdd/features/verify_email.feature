Feature: Verify Email

  Scenario: Successful verify email
    Given I have the following token data
    When I send a GET request to "/user/verify"
    Then the response status code should be 200
    And the response should contain
