"""
    Author : Julio Morais
    Email : jjlmorais@gmail.com
"""
import logging
import random
import sqlite3
import threading
import time
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam


# ==================== LOG FILE ==================================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_PagesJaunes_Search_by_keywords_city__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)





def Browse_PagesJaunes_Search_by_Keyword_City(p_browser, p_taskuser_id,Pagesjaunes_username, p_driver, p_quantity_actions, label_log, lock):

    pass