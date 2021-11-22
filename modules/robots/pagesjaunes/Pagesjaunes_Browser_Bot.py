# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import Browser_PagesJaunes_Search_by_keywords_city
from modules import mymodulesteam
import logging

# ================================ LOGGER ====================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Pagesjaunes_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def RunPagesjaunesBrowser(p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(
        f"================================================ RunPagesjaunesBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://pagesjaunes.fr')
    driver.implicitly_wait(10)

    # ======================= We need to accept Cookies popup =================================
    try:
        button_Accepter_Fermer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='didomi-notice-agree-button']")))
        driver.execute_script("arguments[0].click();", button_Accepter_Fermer)
    except Exception as ex:
        logger.info("Phonebot didn't see any 'Cookies popup'! We carry on the job!")

    Pagesjaunes_username = "Desktop"
    # Let's get the quantity of actions possible
    logger.info("=== [3] GetQuantityActions =======================================")
    quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Pagesjaunes_username)
    if quantity_actions > 0:
        # ===================================================================================
        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
        # ===================================================================================
        result,counter=p_function(p_browser, p_taskuser_id, driver, Pagesjaunes_username, quantity_actions, label_log, lock)
        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
        logger.info(f"Profile {Pagesjaunes_username} logout of Pagesjaunes .")
        return result,counter
    else:
        logger.info(
            f"Profile {Pagesjaunes_username} couldn't execute task because quantity_actions doesn't allow' => {quantity_actions}' .")

        return False,0


def Scraping_Pages_Jaunes_Search_by_keywords_city_28(p_browser, p_taskuser_id, p_driver, Pagesjaunes_username,
                                                     p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Scraping_Pages_Jaunes_Search_by_keywords_city_28 {p_taskuser_id} - {Pagesjaunes_username} - {p_quantity_actions} =======================")

    result, counter = Browser_PagesJaunes_Search_by_keywords_city.Browser_PagesJaunes_Search_by_keywords_city(
        p_browser, p_taskuser_id,Pagesjaunes_username, p_driver, p_quantity_actions, label_log, lock)

    mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Pages_Jaunes_Search_by_keywords_city_28",
                                      "Black")
    return result,counter
