import behave
from selenium import webdriver
import os

def before_all(context):
    context.driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
    context.driver.maximize_window()
    if os.path.exists("Screens"):
        print("Папка уже создана\n")
    else:
        os.makedirs(os.path.abspath("Screens"))
    #with open(os.path.abspath("Email.txt"),"r") as maildata:
        #context.logpass = maildata.read().split()
    #with open(os.path.abspath("Subj.txt"), "r") as subjdata:
        #context.subj = subjdata.read().split()
