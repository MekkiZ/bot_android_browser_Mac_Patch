'''
    Author: Yadé COULIBALY
    Contact: devcoulby@gmail.com
    Task: Like Twitter Tweets Random
'''

import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import logging
import sqlite3
import threading
from datetime import datetime
from modules import mymodulesteam as myModTeam


open(myModTeam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_YellowPages_Search_by_keywords_city__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(myModTeam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class Browser_Like_Twitter_Tweets_Random:

    pass