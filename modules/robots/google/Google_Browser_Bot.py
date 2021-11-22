import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules
import logging
from modules import mymodulesteam

# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Google_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)




def Cold_Messaging_Google_Group_Members_3(p_browser,p_taskuser_id,p_driver,Google_username, p_quantity_actions,label_log,lock):
    pass