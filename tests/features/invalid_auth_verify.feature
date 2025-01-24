Feature: Invalid Authentication Verification
  As a user of some system
  I want to handle invalid token authentication
  So that I receive meaningful error messages

  Scenario: Not valid data
    Given I have the following token:
      | field   | value                                  |
      | token   | jvhdfhgoidjfogjdoifhjijhdfjgpdfjpog    |
    When I send a POST request to "/auth/verify"
    Then the response status code should be 401
    And the response should contain:
      | field      | value                     |
      | message    | Something went wrong      |
