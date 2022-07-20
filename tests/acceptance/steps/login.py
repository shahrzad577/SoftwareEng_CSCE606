from behave import *
from selenium import webdriver
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# use_step_matcher("re")
# from selenium.webdriver.chrome.options import Options 

# Feature: Test that program coordinator can login
#     Scenario: Program Coordinator can login
#     Given I am on the home screen 
#     When I click login
#     Then I am on the login page
#     When I enter my username and password and login
#     Then I should be on the coordinator page

@given('I am on the home screen')
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

    loggedIn = context.selenium.find_element_by_xpath("//body//p")
    assert loggedIn.text == 'You are not logged in'


@when('I click login')
def step_impl(context):
    context.selenium.find_element_by_link_text('Log In').click()

@then('I am on the login page')
def step_impl(context):
    status = context.selenium.find_element_by_xpath("//body/div[@id='loginForm']/form[1]/center[1]/div[1]/center[1]/img[1]").is_displayed()
    assert status is True 

@when('I enter my "{userN}" and "{passW}" and login')
def step_impl(context, userN, passW):
    username = context.selenium.find_element_by_name("username")
    username.send_keys(userN)

    password = context.selenium.find_element_by_name("password")
    password.send_keys(passW)

    context.selenium.find_element_by_xpath("//button[contains(text(),'Login')]").click()


@then('I should be on the authorized page')
def step_impl(context):

    isHomeView = context.selenium.find_element_by_xpath("//a[contains(text(),'HOME')]").is_displayed()
    assert isHomeView is True

@when('I click on the logout button')
def step_impl(context):

    context.selenium.find_element_by_xpath("//a[contains(text(),'LOGOUT')]").click() 


@then('I am on the home screen')
def step_impl(context):

    loggedIn = context.selenium.find_element_by_xpath("//body//p")
    assert loggedIn.text == 'You are not logged in'

@when('I go back') 
def step_impl(context):

    context.selenium.get(f'{context.test.live_server_url}/accounts/login/home')

@then('I should see an \'Error\'')
def step_impl(context):

    error = context.selenium.find_element_by_xpath("//body//p")
    assert error.text == 'Unauthorized User Detected. You can\'t view this page'
