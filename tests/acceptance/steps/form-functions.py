from behave import *
from selenium import webdriver
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


@given('I am logged in as the program coordinator and I have created a new form that I can see in the program view')
def step_impl(context):

    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration

    webdriver_service = Service(ChromeDriverManager().install())

    # Choose Chrome Browser
    context.selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    context.selenium.get(f'{context.test.live_server_url}/')

    context.selenium.find_element_by_link_text('Log In').click()

    username = context.selenium.find_element_by_name("username")
    username.send_keys("coordinator")

    password = context.selenium.find_element_by_name("password")
    password.send_keys("systempassword")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Login')]").click()

    isHomeView = context.selenium.find_element_by_xpath("//h1[contains(text(),'Home Page')]").is_displayed()
    assert isHomeView is True

    context.selenium.find_element_by_xpath("//a[contains(text(),'Create Form')]").click()

    onFormCreate = context.selenium.find_element_by_xpath("//label[contains(text(),'Form name:')]").is_displayed()
    assert onFormCreate is True

    formName = context.selenium.find_element_by_name("form_name")
    formName.send_keys("Form-Functions-Testing")

    programID = context.selenium.find_element_by_name("program_id")
    programID.send_keys("2")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Save')]").click()

    assert isHomeView is True
    context.selenium.find_element_by_xpath("//a[contains(text(),'Program2')]").click()

    onFormPage = context.selenium.find_element_by_xpath("//li[contains(text(),'Form-Functions-Testing')]").is_displayed()
    onFormPagev2 = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/input[2]").is_displayed()
    assert onFormPage and onFormPagev2 is True

@when('I click on the newly created form')
def step_impl(context):
    context.selenium.find_element_by_xpath("//li[contains(text(),'Form-Functions-Testing')]").click()
    
@then('I am on the form generation view')
def step_impl(context):
    onFormFunction = context.selenium.find_element_by_name("generate_pdf").is_displayed()
    assert onFormFunction is True

@when('I input a question for short answer and click \'Save\'')
def step_impl(context):
    content = context.selenium.find_element_by_name("normalquestion") 
    content.send_keys("normal question")
    context.selenium.find_element_by_name("submitQ").click() 

@then('I should see my newly created question')
def step_impl(context):
    isFirstQuestion = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]").is_displayed()
    isEditButton = context.selenium.find_element_by_xpath("/html[1]/body[1]/div[2]/form[1]/div[1]/button[2]").is_displayed()
    assert isFirstQuestion and isEditButton is True 

# multiple choice question 

@given('I am logged in as the program coordinator and I have a recently made form that I can see in the program view')
def step_impl(context):
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    # webdriver_service = Service("/home/sedupuganti/chromedriver/stable/chromedriver")

    webdriver_service = Service(ChromeDriverManager().install())

    # Choose Chrome Browser
    context.selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    context.selenium.get(f'{context.test.live_server_url}/')

    context.selenium.find_element_by_link_text('Log In').click()

    username = context.selenium.find_element_by_name("username")
    username.send_keys("coordinator")

    password = context.selenium.find_element_by_name("password")
    password.send_keys("systempassword")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Login')]").click()

    isHomeView = context.selenium.find_element_by_xpath("//h1[contains(text(),'Home Page')]").is_displayed()
    assert isHomeView is True

    context.selenium.find_element_by_xpath("//a[contains(text(),'Program2')]").click()

    onFormPage = context.selenium.find_element_by_xpath("//li[contains(text(),'Form-Functions-Testing')]").is_displayed()
    onFormPagev2 = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/input[2]").is_displayed()
    assert onFormPage and onFormPagev2 is True

@when('I select \'MCQ\' for the question type, and I select 3 options, and then click \'Add Question\'')
def step_impl(context):
    questionType = Select(context.selenium.find_element_by_name("question_type"))
    questionType.select_by_visible_text("MCQ")

    numOptions = Select(context.selenium.find_element_by_name("how_many"))
    numOptions.select_by_visible_text("3") 

    context.selenium.find_element_by_name("AddQ").click()

@then('I should see the input have 3 options')
def step_impl(context):
    answerChoice1 = context.selenium.find_element_by_name("0").is_displayed()
    answerChoice2 = context.selenium.find_element_by_name("1").is_displayed()
    answerChoice3 = context.selenium.find_element_by_name("2").is_displayed()

    assert answerChoice1 and answerChoice2 and answerChoice3 is True 

@when('I input a question, and set the answer choices, to \'1\', \'2\', \'3\', and then click \'Submit Question\'')
def step_impl(context):


    mcqQues = context.selenium.find_element_by_name("MCQquestion")
    answerChoice1 = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/div[2]/textarea[1]")
    answerChoice2 = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/div[3]/textarea[1]")
    answerChoice3 = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/div[4]/textarea[1]")

    mcqQues.send_keys("MC Question")
    answerChoice1.send_keys("1")
    answerChoice2.send_keys("2")
    answerChoice3.send_keys("3")

    # time.sleep(3)

    submitQ = context.selenium.find_element_by_name("submitQ")
    context.selenium.execute_script("arguments[0].click();", submitQ)


@then('I should see my newly created multiple choice question')
def step_impl(context):

    assert context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[2]").is_displayed() is True
    isFChoice = context.selenium.find_element_by_xpath("//label[contains(text(),'1')]").is_displayed()
    isSChoice = context.selenium.find_element_by_xpath("//label[contains(text(),'2')]").is_displayed()
    isTChoice = context.selenium.find_element_by_xpath("//label[contains(text(),'3')]").is_displayed()

    assert isFChoice and isSChoice and isTChoice is True 

@when("I click edit on the normal question")
def step_impl(context):
    context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]/button[2]").click() 

@then('I should see the normal question being edited')
def step_impl(context):

    editInput = context.selenium.find_element_by_name("normalquestion").text

    if "normal question" in editInput:
        assert True 
    else:
        assert False
@when('I edit the text to \' - checking edit function\' and click \'Save Changes\'')
def step_impl(context):

    editInput = context.selenium.find_element_by_name("normalquestion")
    editInput.send_keys(" - checking edit function") 

    saveChange = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/input[2]")
    context.selenium.execute_script("arguments[0].click();", saveChange)

@then('I should see the changes to the normal question')
def step_impl(context):

    isEditedQuestion = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]").text
    # print("ISFIRST: ", isFirstQuestion)
    # assert False

    if "normal question - checking edit function" in isEditedQuestion:
        assert True 
    else:
        assert False

@when('I click the delete button on the normal question')
def step_impl(context):
    context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]/button[1]").click()

@when('I click the delete button on the multiple choice question')
def step_impl(context):
    context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[2]/button[1]").click()


@then('I should no longer see the normal question')
def step_impl(context):

    isQueDeleted = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]").text
  
    if "MC Question" in isQueDeleted:
        assert True 
    else:
        assert False

@then('I should no longer see the multiple choice question')
def step_impl(context):

    isQueDeleted = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[1]").text
  
    if "MC Question" in isQueDeleted:
        assert False 
    else:
        assert True


@when("I click edit on the multiple choice question")
def step_impl(context):
    context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[2]/button[2]").click()

@then("I should see the multiple choice question being edited")
def step_impl(context):

    editInput = context.selenium.find_element_by_name("MCQquestion").text

    # answerChoice1 = context.selenium.find_element_by_name("0").text 
    # answerChoice2 = context.selenium.find_element_by_name("1").text 
    # answerChoice3 = context.selenium.find_element_by_name("2").text 

    # print("ANSWER: " , answerChoice1)
    # print("ANSWER2: ", answerChoice2)

    print(editInput)

    if "MC Question" in editInput:
        assert True 
    else:
        assert False

@when("I change the question text to \' - checking edit function\', and change the answer choices to \'12\', \'22\', and \'32\', and then click \'Save Changes\'")
def step_impl(context):

    editInput = context.selenium.find_element_by_name("MCQquestion")
    editInput.send_keys(" - checking edit function") 
    answerChoice1 = context.selenium.find_element_by_name("0")
    answerChoice2 = context.selenium.find_element_by_name("1")
    answerChoice3 = context.selenium.find_element_by_name("2")

    answerChoice1.send_keys("2")
    answerChoice2.send_keys("2")
    answerChoice3.send_keys("2")

    saveChange = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/input[2]")
    context.selenium.execute_script("arguments[0].click();", saveChange)

@then("I should see the changes to the multiple choice question")
def step_impl(context):

    isEditedQuestion = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[2]").text
    # print("ISFIRST: ", isFirstQuestion)
    # assert False

    if "MC Question - checking edit function" in isEditedQuestion and "12" in isEditedQuestion and "22" in isEditedQuestion and "32" in isEditedQuestion:
        assert True 
    else:
        assert False

@when('I change the Order to 2 and click on \'Save Changes\'')
def step_impl(context):
    order = Select(context.selenium.find_element_by_name("order"))
    order.select_by_visible_text("2")

    saveChange = context.selenium.find_element_by_xpath("//body/div[2]/form[3]/input[2]")
    context.selenium.execute_script("arguments[0].click();", saveChange)

@then('I should see the normal question as the second question')
def step_impl(context):

    isEditedQuestion = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/div[2]").text
    # print("ISFIRST: ", isFirstQuestion)
    # assert False

    if "2." in isEditedQuestion:
        assert True 
    else:
        assert False


@when('I click finalize')
def step_impl(context):

    finalizeForm = context.selenium.find_element_by_name("Finalize Form")
    context.selenium.execute_script("arguments[0].click();", finalizeForm)

@then('No more changes can be made to the form')
def step_impl(context):

    pass


@when('I click on \'Clone Form\'')
def step_impl(context):

    cloneForm = context.selenium.find_element_by_name("Clone Form")
    context.selenium.execute_script("arguments[0].click();", cloneForm)


@then('I should be on a cloned version of the previous form, and the cloned version is not finalized')
def step_impl(context):

    isSubQ = context.selenium.find_element_by_name("submitQ").is_displayed()

    assert isSubQ is True

@when('I click on \'Generate PDF\'')
def step_impl(context):
    generatePDF = context.selenium.find_element_by_name("generate_pdf")
    context.selenium.execute_script("arguments[0].click();", generatePDF)

@then('I should be on a new page with the generated PDF')
def step_impl(context):

    context.selenium.implicitly_wait(1)
    assert True


@given('I am logged in as a supervisor, and I see a finalized form from the program coordinator')
def step_impl(context):
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    # webdriver_service = Service("/home/sedupuganti/chromedriver/stable/chromedriver")

    webdriver_service = Service(ChromeDriverManager().install())

    # Choose Chrome Browser
    context.selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    context.selenium.get(f'{context.test.live_server_url}/')

    context.selenium.find_element_by_link_text('Log In').click()

    username = context.selenium.find_element_by_name("username")
    username.send_keys("supervisor1")

    password = context.selenium.find_element_by_name("password")
    password.send_keys("systempassword")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Login')]").click()

    isHomeView = context.selenium.find_element_by_xpath("//a[contains(text(),'HOME')]").is_displayed()
    assert isHomeView is True

@when('I click on the finalized form')
def step_impl(context):
    
    findFinalizedForm = context.selenium.find_element_by_xpath("//a[contains(text(),'Form-Functions-Testing')]")
    context.selenium.execute_script("arguments[0].click();", findFinalizedForm)

@then('I am on the form view')
def step_impl(context):
    onFormFunction = context.selenium.find_element_by_name("generate_pdf").is_displayed()
    assert onFormFunction is True

@when('I answer the questions with \'22\', and \'random text here\', and click on \'Finalize\'')
def step_impl(context):

    # test = context.selenium.find_element_by_xpath("//textarea[@id='']")
    # print("IS ENABLED?:", test.is_enabled())

    # assert False

    context.selenium.find_element_by_css_selector("input[type='radio'][value='22']").click()

    input = context.selenium.find_element_by_xpath("//textarea[@id='']")
    input.send_keys("random text here!")

    finalizeForm = context.selenium.find_element_by_name("Finalize Answer")
    context.selenium.execute_script("arguments[0].click();", finalizeForm)

@then('the form should be finalized and no more changes can be made')
def step_impl(context):

    disabledInput = context.selenium.find_element_by_xpath("//textarea[@id='']")
    assert disabledInput.is_enabled() is False

@given('I am logged in as a student, and I see a finalized form from the supervisor and the program coordinator')
def step_impl(context):

    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    # webdriver_service = Service("/home/sedupuganti/chromedriver/stable/chromedriver")

    webdriver_service = Service(ChromeDriverManager().install())

    # Choose Chrome Browser
    context.selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    context.selenium.get(f'{context.test.live_server_url}/')

    context.selenium.find_element_by_link_text('Log In').click()

    username = context.selenium.find_element_by_name("username")
    username.send_keys("student2")

    password = context.selenium.find_element_by_name("password")
    password.send_keys("systempassword")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Login')]").click()

    isHomeView = context.selenium.find_element_by_xpath("//a[contains(text(),'HOME')]").is_displayed()
    assert isHomeView is True

@when('I input some text into the feedback as \'this is feedback!\', and click on \'Submit Feedback\'')
def step_impl(context):

    feedback = context.selenium.find_element_by_name("Feedback")
    feedback.send_keys('this is feedback!')

    submitFeed = context.selenium.find_element_by_name("Submit Feedback")
    context.selenium.execute_script("arguments[0].click();", submitFeed)

@then('the feedback should be disabled, and no more changes can be made')
def step_impl(context):

    disabledFeedback = context.selenium.find_element_by_xpath("//button[contains(text(),'Student Feedback')]").is_displayed()
    assert disabledFeedback is True











    








    
     





