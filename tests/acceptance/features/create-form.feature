Feature: Creating a form 

    Scenario: Program Coordinator can create a form from home view  
        Given I am logged in as the program coordinator
        When I click on 'Create Form'
        Then I should be on 'form_create.html'
        When I input the form name, and designated program id (1) and click on 'Save'
        Then I should be on the home page
        When I click on Program1
        Then I should see my newly created form

    Scenario: Program Coordinator can create a form from form view 
        Given I am logged in as the program coordinator
        When I click on Program1
        Then I should be in the program view 
        When I click on 'Create Form' in the program view
        Then I should be on 'form_create.html'
        When I input the form name and click on 'Save'
        Then I should be on the home page
        When I click on Program1
        Then I should see my newly created form with v2
        


