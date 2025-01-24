Feature: Payment Processing
  As a user of the payment system
  I want to process a payment
  So that the payment is recorded in the system

  Scenario: Successful payment processing
    Given I have the following payment data:
      | field        | value            |
      | order_id     | 12345            |
      | total_amount | 100.00           |
    When I send a POST request to "/payments"
    Then the response status code should be 200
    And the response should contain:
      | field    | type   |
      | id       | string |
      | qr_code  | string |
