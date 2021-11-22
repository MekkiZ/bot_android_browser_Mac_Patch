# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
sys.path.append(".")
from modules import mymodules, mymodulesteam
import logging

from . import Browser_YellowPages_scraping_search_result

# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Yellowpages_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def RunYellowpagesBrowser(p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(
        f"================================================ RunYellowpagesBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://yellowpages.com')
    driver.implicitly_wait(10)

    Yellowpages_username = "Desktop"
    # Let's get the quantity of actions possible
    logger.info("=== [3] GetQuantityActions =======================================")
    quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Yellowpages_username)
    if quantity_actions > 0:
        # ===================================================================================
        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
        # ===================================================================================
        result, counter = p_function(p_browser, p_taskuser_id, driver, Yellowpages_username,
                                     quantity_actions, label_log, lock)
        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE

        return result, counter
    else:
        logger.info(
            f"Profile {Yellowpages_username} couldn't execute task because quantity_actions doesn't allow' => {quantity_actions}' .")
        return False, 0


def Scraping_YellowPages_Search_by_keywords_city_29(p_browser, p_taskuser_id, Yellowpages_username, p_driver,
                                                    p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Scraping_YellowPages_Search_by_keywords_city_29 {p_taskuser_id} - {Yellowpages_username} - {p_quantity_actions} =======================")
    # mymodules.PopupMessage("ACTIONS", f"Yellowpages user {Yellowpages_username} can make {p_quantity_actions} actions now of Scraping_YellowPages_Search_by_keywords_city_29!")

    result, counter = Browser_YellowPages_scraping_search_result.Browser_YellowPage_Search_by_keywords_city(
        p_browser, p_taskuser_id,
        Yellowpages_username, p_driver,
        p_quantity_actions,
        label_log, lock)
    mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Browser_YellowPage_Search_by_keywords_city",
                                      "Black")
    return result, counter
