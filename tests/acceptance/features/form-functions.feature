Feature: Tests that Program Coordinator can edit, add, order, and finalize questions to a form 

    Scenario: Program Coordinator can add a short answer question 
        Given I am logged in as the program coordinator and I have created a new form that I can see in the program view 
        When I click on the newly created form 
        Then I am on the form generation view 
        When I input a question for short answer and click 'Save'
        Then I should see my newly created question 
    
    Scenario: Program Coordinator can add a multiple choice question 
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view 
        When I click on the newly created form 
        Then I am on the form generation view 
        When I select 'MCQ' for the question type, and I select 3 options, and then click 'Add Question'
        Then I should see the input have 3 options
        When I input a question, and set the answer choices, to '1', '2', '3', and then click 'Submit Question'
        Then I should see my newly created multiple choice question 
    
    Scenario: Program Coordinator can edit a normal question
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view 
        When I click edit on the normal question 
        Then I should see the normal question being edited 
        When I edit the text to ' - checking edit function' and click 'Save Changes'
        Then I should see the changes to the normal question

    Scenario: Program Coordinator can edit a multiple choice question 
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view 
        When I click edit on the multiple choice question 
        Then I should see the multiple choice question being edited 
        When I change the question text to ' - checking edit function', and change the answer choices to '12', '22', and '32', and then click 'Save Changes'
        Then I should see the changes to the multiple choice question
    
    Scenario: Program Coordinator can delete a normal question
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view
        When I click the delete button on the normal question 
        Then I should no longer see the normal question

    Scenario: Program Coordinator can delete a multiple choice question
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view
        When I click the delete button on the multiple choice question 
        Then I should no longer see the multiple choice question


    Scenario: Program Coordinator can change the order of any question 
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view 
        When I click edit on the normal question 
        Then I should see the normal question being edited 
        When I change the Order to 2 and click on 'Save Changes'
        Then I should see the normal question as the second question 

    Scenario: Program Coordinator can finalize the form 
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view
        When I click finalize
        Then No more changes can be made to the form

    Scenario: Program Coordinator can clone the form
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view
        When I click on 'Clone Form'
        Then I should be on a cloned version of the previous form, and the cloned version is not finalized

    Scenario: Program Coordinator can generate a PDF of the form
        Given I am logged in as the program coordinator and I have a recently made form that I can see in the program view
        When I click on the newly created form 
        Then I am on the form generation view
        When I click on 'Generate PDF' 
        Then I should be on a new page with the generated PDF 


    Scenario: Supervisor can answer questions to a form that program coordinator has finalized 
        Given I am logged in as a supervisor, and I see a finalized form from the program coordinator 
        When I click on the finalized form 
        Then I am on the form view 
        When I answer the questions with '22', and 'random text here', and click on 'Finalize' 
        Then the form should be finalized and no more changes can be made

    Scenario: Student can submit feedback to form that supervisor and coordinator has finalized   
        Given I am logged in as a student, and I see a finalized form from the supervisor and the program coordinator 
        When I click on the finalized form 
        Then I am on the form view
        When I input some text into the feedback as 'this is feedback!', and click on 'Submit Feedback' 
        Then the feedback should be disabled, and no more changes can be made 

        
        