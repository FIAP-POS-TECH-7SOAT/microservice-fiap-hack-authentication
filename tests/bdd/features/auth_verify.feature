Feature: Auth verify

  Scenario: Successful verification of auth user
    Given I have the following token data
    When I send a POST request to "/auth/verify"
    Then the response status code should be 200
    And the response should contain
