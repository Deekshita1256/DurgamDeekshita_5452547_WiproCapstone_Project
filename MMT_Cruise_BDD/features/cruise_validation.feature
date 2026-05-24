@cruise @validation
Feature: Cruise Booking Module - Input Guardrails & Results Filtering
  As a quality engineer validating front-end validation limits
  I want to verify that field inputs block faulty data, check form validations, and evaluate page sorting layouts
  So that the application prevents bad reservation payloads from being processed

  Background:
    Given the user has navigated to the Cruise module tab

  # =========================================================================
  # ❌ NEGATIVE TEST CASE 1: INVALID PAN CARD NUMBER
  # =========================================================================
  @negative @invalid_pan
  Scenario: Negative Test - Invalid Short PAN Input Restriction Check
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user selects the first available cruise listing card from the search results
    And the user reviews cabin deals using traveler ages from data sheet "PassengerAges"
    And the user populates traveler registration forms using details from data sheet "SearchCriteria"
    And the user provides contact details from data sheet "SearchCriteria" to progress
    Then the system should ensure the final booking proceed button remains disabled

  # =========================================================================
  # ❌ NEGATIVE TEST CASE 2: MISSING MANDATORY FIELD
  # =========================================================================
  @negative @missing_field
  Scenario: Negative Test - Missing Mandatory Field Guardrail Check
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user selects the first available cruise listing card from the search results
    And the user reviews cabin deals using traveler ages from data sheet "PassengerAges"
    And the user completes a default cabin selection stage but leaves the passenger first name blank from data sheet "SearchCriteria"
    And the user attempts to submit the passenger details form
    Then the system should display a validation error containing invalid first name

  # =========================================================================
  # 🟢 POSITIVE TEST CASE 1: LOWERCASE PAN CARD ENTRY AUTOMATION
  # =========================================================================
  @positive @lowercase_pan
  Scenario: Positive Test 1 - Lowercase PAN Alphanumeric Input Handling
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user selects the first available cruise listing card from the search results
    And the user reviews cabin deals using traveler ages from data sheet "PassengerAges"
    And the user populates traveler registration forms using details from data sheet "SearchCriteria"
    And the user provides contact details from data sheet "SearchCriteria" to progress
    Then the user enters a lowercase PAN id "ffvpd1234h" and the system should accept the input and proceeds

  # =========================================================================
  # 🟢 POSITIVE TEST CASE 2: LAYOUT RESILIENCY WINDOW RESCALE
  # =========================================================================
  @positive @responsive_rescale
  Scenario: Positive Test 2 - UI Layout Resiliency Check on Window Rescale
    When the user rescales the browser viewport resolution to a narrower "1024x768" boundary view
    And the user searches for cruises using criteria from data sheet "SearchCriteria"
    Then the user should see that the cruise package listings grid is displayed and stable under the scaled layout

  # =========================================================================
  # 🟢 POSITIVE TEST CASE 3: FINANCIAL MATCH TOTAL FARE SUMMARY SYNC
  # =========================================================================
  @positive @price_sync
  Scenario: Positive Test 3 - Dynamic Sidebar Total Fare Handoff Sync
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user selects the first available cruise listing card from the search results
    And the user reviews cabin deals using traveler ages from data sheet "PassengerAges"
    And the user populates traveler registration forms using details from data sheet "SearchCriteria"
    And the user provides contact details from data sheet "SearchCriteria" to progress
    And the user submits a valid PAN card to advance past the review context onto the payment gateway screen
    Then the final gateway payment price should exactly match the baseline review stage total price string

  # =========================================================================
  # 🟢 POSITIVE TEST CASE 4: SORT BY DEPARTURE DATE AND GRID CONTENT ASSERTION
  # =========================================================================
  @positive @sort_by_date
  Scenario: Positive Test 4 - Sort by Departure Date and Assert List Sorting Change
    When the user searches for cruises using criteria from data sheet "SearchCriteria"
    And the user notes the title of the top cruise result under default price sorting
    And the user changes the active sorting dropdown option selection to "Departure Date"
    Then the cruise listing grid positions should update, showing a different top cruise item