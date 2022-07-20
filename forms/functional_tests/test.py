# install selenium
# put chromedriver.exe in your testing file (check your version of chrome to be compatible)

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
from django.test import Client
from student.models import Student
from django.contrib.auth.models import User
from django.test import Client



class TestForms(StaticLiveServerTestCase):
    # will be run for each test when a url is fired up
    def setUp(self):
        self.browser = webdriver.Chrome('forms/functional_tests/chromedriver.exe')

    # will be run at the end of each test to close the url
    def tearDown(self):
        self.browser.close()

    # the user requests the page for the first time
    def test_user_not_logged_in(self):
        self.browser.get(self.live_server_url)
        #time.sleep(20)

        self.assertEquals(
            self.browser.find_element_by_tag_name('p').text,
            'You are not logged in'
        )

    def test_login_click(self):
        self.browser.get(self.live_server_url)
        #time.sleep(20)

        # the user requests the page for the first time
        add_url = self.live_server_url + reverse('login')
        self.browser.find_element_by_tag_name('a').click()
        self.assertEquals(
            self.browser.current_url,
            add_url
        )


    def test_user_click_login(self):
        self.browser.get(self.live_server_url)

        user = User.objects.create(username='coordinator')
        user.set_password('systempassword')
        user.save()

        c = Client()
        logged_in = c.login(username='coordinator', password='systempassword')
        self.assertTrue(logged_in)








