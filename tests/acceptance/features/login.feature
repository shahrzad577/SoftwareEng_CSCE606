Feature: Test that users can login

    Scenario Outline: Authorized Users Can Login
        Given I am on the home screen 
        When I click login
        Then I am on the login page
        When I enter my "<userN>" and "<passW>" and login
        Examples:
            | userN       | passW          |
            | coordinator | systempassword |
            | supervisor1 | systempassword |
            | student1    | systempassword |
        Then I should be on the authorized page

    Scenario Outline: Unauthorized users cannot view content from login 
        Given I am on the home screen 
        When I click login
        Then I am on the login page
        When I enter my "<userN>" and "<passW>" and login
        Examples:
            | userN       | passW          |
            | coordinator | systempassword |
            | supervisor1 | systempassword |
            | student1    | systempassword |
        Then I should be on the authorized page
        When I click on the logout button
        Then I am on the home screen 
        When I go back
        Then I should see an 'Error' 

        