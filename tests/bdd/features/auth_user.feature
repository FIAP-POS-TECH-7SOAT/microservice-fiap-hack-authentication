Feature: Auth User

  Scenario: Successful auth user
    Given I have the following user data
    When I send a POST request to "/auth/check"
    Then the response status code should be 200
    And the response should contain
