from flask import Flask
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import welcome
import unittest

class ExampleTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.baseURL = "http://127.0.0.1:5000/"

    def tearDown(self):
        self.driver.quit

    def test_home(self):
        self.driver.get(self.baseURL)
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.url_contains('127'))
            assert 'Jetson Service' == self.driver.title
        except:
            print 'timeout exception'
