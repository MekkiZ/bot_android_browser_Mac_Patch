'''
Author : Yacine Hamida / Laurent Maréchal
task : auto follow twitter
contact : yacine.hamida@ynov.com

'''

"""
This module contain some modules from mymodules.py improved by other developpers
https://github.com/phonebotco/phonebot
"""
'''
Author : Yacine Hamida
Task : Auto follow twitter
Contact : yacine.hamida@ynov.com
'''

import logging
import os
import shutil
import time
import random
import threading
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
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
import pathlib
import platform
import psutil
import sqlite3
from modules import mymodulesteam


open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_auto_infollow_twitter__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ================================================================================
# ================= Send action to action table ==================================



def Browser_Twitter_Auto_Follow(p_browser, p_taskuser_id, follow_number):
    pass