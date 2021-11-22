# -*- coding: utf-8 -*-
########################################################
#                   Jordy Naiya                        #
#               jordynabina@gmail.com                  #
########################################################


"""
This is a sample task for automation software Phonebot.co on Browser Firefox & Chrome
https://github.com/phonebotco/phonebot

"""

import logging
import sqlite3
import threading
from modules import mymodulesteam

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import pathlib
import platform
import psutil
import random
import time
import unidecode
if platform.system() == 'Windows':
    import winsound



# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Linkedin_Search_By_Keywords_And_City__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================




# ===================================================================================================================
# ============================ METHOD TO SCRAP LINKEDIN RESULTS =====================================================
# ===================================================================================================================
def Linkedin_Search_By_Keywords_And_City(label_log, p_browser,p_id_social_account,p_limit, p_taskuser_id, lock, keywords=str, city=str):

    pass