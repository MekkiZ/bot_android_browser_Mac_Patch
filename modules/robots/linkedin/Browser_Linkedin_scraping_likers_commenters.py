# -*- coding: utf-8 -*-

"""
Author : Océane Gbamene
Email : oceane.gba.pro@gmail.com
"""


import selenium
import logging
from selenium import webdriver
from random import random
import re
import sqlite3
import threading
import time
import os

import random
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#from modules.robots.linkedin.Browser_Linkedin_send_message_Search_By_Keywords_City import Linkedin_Search_By_Keywords_And_City
#from modules.robots.linkedin.Linkedin_Browser_Bot import Browser_Linkedin_scraping_likers_commenters_61
from modules import mymodulesteam

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__NAME_OF_TASK__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)



# =============================== scrapping main ===============================
def ScrapPosts(p_browser, p_taskuser_id, Linkedin_username, p_quantity_actions, label_log, lock, p_driver):
    pass