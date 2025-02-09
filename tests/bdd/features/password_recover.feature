Feature: Password Recover

  Scenario: Successful recover password
    Given I have the following user data
    When I send a POST request to "/password/recover"
    Then the response status code should be 200
    And the response should contain
