from flask import Flask
from selenium import webdriver
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
        print self.baseURL
        assert 'Jetson Service' == self.driver.title
