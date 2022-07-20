from behave import *
from selenium import webdriver
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from behave_django.decorators import fixtures



# @fixtures('tests/fixtures/initial-fixture.json')
@given('I am logged in as the program coordinator')
def step_impl(context):

    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

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

@when('I click on \'Create Form\'')
def step_impl(context):
    context.selenium.find_element_by_xpath("//a[contains(text(),'Create Form')]").click()


@then('I should be on \'form_create.html\'')
def step_impl(context):
    onFormCreate = context.selenium.find_element_by_xpath("//label[contains(text(),'Form name:')]").is_displayed()
    assert onFormCreate is True


@when('I input the form name, and designated program id (1) and click on \'Save\'')
def step_impl(context):

    formName = context.selenium.find_element_by_name("form_name")
    formName.send_keys("Django-Behave-Testing")

    programID = context.selenium.find_element_by_name("program_id")
    programID.send_keys("1")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Save')]").click()
    

@then('I should be on the home page')
def step_impl(context):

    isHomeView = context.selenium.find_element_by_xpath("//h1[contains(text(),'Home Page')]").is_displayed()
    assert isHomeView is True

@when('I click on Program1')
def step_impl(context):
    context.selenium.find_element_by_xpath("//a[contains(text(),'Program1')]").click()

@then('I should see my newly created form')
def step_impl(context):
    isFormShowing = context.selenium.find_element_by_xpath("//li[contains(text(),'Django-Behave-Testing')]").is_displayed()
    assert isFormShowing is True

@then('I should be in the program view')
def step_impl(context):
    onFormPage = context.selenium.find_element_by_xpath("/html[1]/body[1]/div[2]/form[1]/ul[1]/a[1]/li[1]").is_displayed()
    onFormPagev2 = context.selenium.find_element_by_xpath("//body/div[2]/form[1]/input[2]").is_displayed()
    assert onFormPage and onFormPagev2 is True

@when('I input the form name and click on \'Save\'')
def step_impl(context):

    formName = context.selenium.find_element_by_name("form_name")
    formName.send_keys("Django-Behave-Testingv2")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Save')]").click()

@then('I should see my newly created form with v2')
def step_impl(context):
    isFormShowing = context.selenium.find_element_by_xpath("//li[contains(text(),'Django-Behave-Testingv2')]").is_displayed()
    assert isFormShowing is True

@when('I click on \'Create Form\' in the program view')
def step_impl(context):
    context.selenium.find_element_by_xpath("//body/div[2]/form[1]/input[2]").click()

    

    # Scenario: Program Coordinator can create a form from form view 
    #     Given I am logged in as the program coordinator
    #     When I click on Program1
    #     Then I should be in the forms view 
    #     When I click on 'Create Form'
    #     Then I should be on 'form_create.html'
    #     When I input the form name and click on 'Save'
    #     Then I should be on the home page
    #     When I click on Program1
    #     Then I should see my newly created form