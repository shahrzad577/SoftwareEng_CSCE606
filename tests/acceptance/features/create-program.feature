Feature: Creating a program

    Scenario: Program Coordinator can create a program from the home view  
        Given I am logged in as the program coordinator
        When I click on 'Add Program'
        Then I should be on 'program_create.html'
        When I input the program name and click 'Save'
        Then I should be on the home page and should see the newly created program
        