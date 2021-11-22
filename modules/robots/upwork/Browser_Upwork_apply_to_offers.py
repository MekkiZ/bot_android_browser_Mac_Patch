import logging
import random
import threading
import time

from selenium.common.exceptions import TimeoutException, InvalidElementStateException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam as MMTeam


# ======================================== Custom Exceptions ===========================================================
class InvalidTaskUserException(Exception):
    """Thronw when the task_user is None or not valid"""

    def __init__(self):
        self.msg = 'No valid task was received!'


# ======================================================================================================================

# ========================================= Logger =====================================================================
open(MMTeam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_Upwork_Apply_To_Offers_found_from_keywords_search_result__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(MMTeam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)



# ======================================================================================================================
def Browser_Upwork_Apply_To_Offers_found_from_keywords_search_result(browser, task_user, lock):
    pass