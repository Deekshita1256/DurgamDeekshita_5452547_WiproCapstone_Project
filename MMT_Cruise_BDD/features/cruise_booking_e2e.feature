@cruise @e2e
Feature: MakeMyTrip Cruise Booking Module
  As an online traveler looking for a vacation package
  I want to search, select, and process details for a cruise itinerary
  So that I can successfully progress through the reservation confirmation stage

  @happy_path
  Scenario: End-to-End Cruise Selection and Checkout Reservation Flow from Excel Data
    Given the user has navigated to the Cruise module tab
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user selects the first available cruise listing card from the search results
    And the user reviews cabin deals using traveler ages from data sheet "PassengerAges"
    And the user populates traveler registration forms using details from data sheet "SearchCriteria"
    And the user provides contact details from data sheet "SearchCriteria" to progress
    Then the user should view the final booking confirmation summary or payment gateway screen