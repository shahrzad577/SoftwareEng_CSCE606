from behave import *
from selenium import webdriver
import time
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@when('I click on \'Add Program\'')
def step_impl(context):
    context.selenium.find_element_by_xpath("//a[contains(text(),'Add Program')]").click()

@then('I should be on \'program_create.html\'')
def step_impl(context):
    onProgramCreate = context.selenium.find_element_by_xpath("//h1[contains(text(),'Program Create')]").is_displayed()
    assert onProgramCreate is True

@when('I input the program name and click \'Save\'')
def step_impl(context):

    programName = context.selenium.find_element_by_name("program_name")
    programName.send_keys("Django-Behave-Testing-Program")

    context.selenium.find_element_by_xpath("//button[contains(text(),'Save')]").click()

@then('I should be on the home page and should see the newly created program')
def step_impl(context):

    isHomeView = context.selenium.find_element_by_xpath("//h1[contains(text(),'Home Page')]").is_displayed()
    isProgramShowing = context.selenium.find_element_by_xpath("//a[contains(text(),'Django-Behave-Testing-Program')]").is_displayed()
    assert isHomeView and isProgramShowing is True

