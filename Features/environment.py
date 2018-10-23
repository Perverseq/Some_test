import behave
from selenium import webdriver

def before_all(context):
    context.driver = webdriver.Chrome(".//chromedriver.exe")
