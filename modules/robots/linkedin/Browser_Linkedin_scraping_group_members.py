# Ilic Nikola
# Email : nikolapadjan@gmail.com
# discord Nikola.I#6349
# last push on branch 07/05/2021 00:45
# pour les ajouts dans la bd le readme fourni avec explique tout
import logging
import datetime
import threading
import sqlite3
from math import e
import os
import time
from modules import mymodulesteam
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.common.exceptions import InvalidSelectorException as notAnElement
from webdriver_manager.firefox import GeckoDriverManager
from random import uniform


# ================================ LOGGER ====================================
import pathlib
import platform
import psutil


open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Linkedin_Browser_Bot__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)




# =============================   main scraping ================================
def Browser_Scraping_Linkedin_Group_Members_32(p_browser, p_taskuser_id,Linkedin_username, p_quantity_actions, label_log, lock):

    pass