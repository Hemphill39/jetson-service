from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        assert self.driver.title == 'Jetson Service'

    def test_record_button(self):
        self.driver.get(self.baseURL)
        element = self.driver.find_element(By.ID, 'recordButton')
        assert element.text == 'Record'

if __name__ == '__main__':
    unittest.main()
