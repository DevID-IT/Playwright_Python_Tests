Feature: Register User
    As a new user
    I want to register an account
    So that I can access member-only features
    
    Scenario Outline: Successful user registration
        Given I am on the Parabank home page
        And I navigate to the registration page
        When I fill in the registration form with valid details for user <username>, <password>
        Then I should see a confirmation message indicating successful registration
    Examples:
            | username       | password        |
            | Grosz12      | Dawid12341      |

    Scenario: Invalid user registration form - username
        Given I am on the Parabank home page
        And I navigate to the registration page
        When I fill in the registration form with invalid data
        Then Verify error message

    Scenario: Invalid user registration form - obligatory fields
        Given I am on the Parabank home page
        And I navigate to the registration page
        When Save form with empty obligatory fields
        Then Verify error message
        Then Verify error message

    Scenario: Invalid user registration form - password mismatch
        Given I am on the Parabank home page
        And I navigate to the registration page
        When Fill in the registration form with password mismatch
        Then Verify error message