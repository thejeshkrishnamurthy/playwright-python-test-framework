Feature: Product checkout

  As a registered customer
  I want to purchase a product
  So that I can complete an online order

  @smoke
  Scenario: Customer completes checkout successfully
    Given the customer is logged in
    When the customer adds "Sauce Labs Backpack" to the cart
    And the customer completes checkout
    Then an order confirmation should be displayed