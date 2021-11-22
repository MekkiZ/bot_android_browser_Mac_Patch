# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
sys.path.append(".")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam
from modules.robots.craigslist import Browser_Craigslist_scraping_ads
import logging



# ================================ LOGGER ====================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Craigslist_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)



def RunCraigslistBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):
    logger.info(f"================================================ RunCraigslistBrowser {p_taskuser_id} ===================================================")

    """
        This method will open browser and run the task for all the profiles found in cookies Browser
        It will have to check for the daily & hourly limit
        It will return True if it run some actions, or False if nothing
        :param p_function:
        :param p_taskuser_id:
        :return:
        """
    # ============================================================================
    # === 1 OPEN BROWSER =========================================================
    logger.info("=== [1] Open Browser =======================================")
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False
    # For craiglist we need to find the url of city craigslist website. Ex: lille.craigslist.org
    # We will use Google to find it.


    Craigslist_username = "Desktop"
    # Let's get the quantity of actions possible
    logger.info("=== [3] GetQuantityActions =======================================")
    quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Craigslist_username)
    if quantity_actions > 0:
        # ===================================================================================
        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
        # ===================================================================================
        result, counter =p_function(p_browser,p_taskuser_id, driver, Craigslist_username, quantity_actions)
        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
        logger.info(f"Profile {Craigslist_username} logout of Craigslist .")
        return result, counter
    else:
        logger.info(
            f"Profile {Craigslist_username} couldn't execute task because quantity_actions doesn't allow' => {quantity_actions}' .")

        return False,0






def Scraping_Craigslist_Ads_23(p_browser,p_taskuser_id,p_driver,Craigslist_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Scraping_Craigslist_Ads_23 {p_taskuser_id} - {Craigslist_username} - {p_quantity_actions} =======================")

    result, counter = Browser_Craigslist_scraping_ads.Scraping_Craigslist_Scrap_Craigslist_Ads_23(p_browser, p_taskuser_id, p_quantity_actions,Craigslist_username, label_log, lock)


    mymodulesteam.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Craigslist_Ads_23",
                                  "Black")
    return result, counter