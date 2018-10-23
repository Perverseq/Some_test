import behave
from selenium import webdriver
import os

def before_all(context):
    context.driver = webdriver.Chrome(".//chromedriver.exe")
    dirs = os.listdir()
    create = True
    for index in range(len(dirs)):
        if dirs[index] == "Screens":
            create == False
            return
    if create == True:
        os.makedirs(".\\Screens\\")