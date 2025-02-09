Feature: Password Reset

  Scenario: Successful change password
    Given I have the following token data
    When I send a POST request to "/password/reset"
    Then the response status code should be 200
    And the response should contain
