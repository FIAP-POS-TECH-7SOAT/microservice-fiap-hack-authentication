Feature: Create User

  Scenario: Successful create user
    Given I have the following user data
    When I send a POST request to "/user/create"
    Then the response status code should be 200
    And the response should contain
