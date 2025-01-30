Feature: Create User
  As a user of the auth system
  I want to create a user
  So that the user is recorded in the system

  Scenario: Successful create user
    Given I have the following user data:
      | field      | value            |
      | user_email | test@gmail.com   |
      | password   | dev123           |
      | phone      | +5511912347896   |
    When I send a POST request to "/user/create"
    Then the response status code should be 200
    And the response should contain:
      | field    | result       |
      | message  | User created |
