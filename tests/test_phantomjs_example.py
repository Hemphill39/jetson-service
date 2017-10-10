from flask import Flask
from selenium import webdriver
import welcome
import unittest

class ExampleTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.baseURL = "http://localhost:5000/"

    def tearDown(self):
        self.driver.quit

    def test_home(self):
        self.driver.get(self.baseURL)
        assert "Jetson Service" == self.driver.title