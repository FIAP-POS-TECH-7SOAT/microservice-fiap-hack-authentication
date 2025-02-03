Feature: Auth User
  As a registered user
  I want to authenticate a user
  So that I can access protected resources

  Scenario: Successful authenticate user
    Given I have the following credentials:
      | field      | value            |
      | user_email | teste@gmail.com  |
      | password   | dev123           |
    When I send a POST request to "/auth/check"
    Then the response status code should be 200
    And the response should contain token:
      | field    | result     |
      | token    | fake_token |
