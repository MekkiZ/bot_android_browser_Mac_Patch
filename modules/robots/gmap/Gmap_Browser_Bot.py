# -*- coding: utf-8 -*-
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules
import logging
import pdb
from . import Browser_Google_Map_scraping_search_results
# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Gmap_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# =========================================================================================
# =================================== Gmap DESKTOP METHODS ============================
# =========================================================================================

def AreWeGmapLoggedIn(p_driver):
    """
        This function check if browser is connected to Gmap or not and return True with Gmap username
        or False with None
        """
    logger.info("=== [2] AreWeGmapLoggedIn() ====================================")
    Gmap_username = None
    # Is there the "Accept Agreement Popup"
    try:
        button_accept = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.ID, "introAgreeButton")))
        button_accept.click()
        time.sleep(random.uniform(3, 5))

    except Exception as ex:
        logger.error(f"No button Accept Agreement {ex}")

    # Is there the button "connexion" ?
    try:
        button_connection = p_driver.find_element_by_xpath(
            "//a[contains(text(),'onnexion') or contains(text(),'login') or contains(text(),'onnection')]")
        if button_connection:
            logger.error("No Google Account Founds")
            return False, Gmap_username
    except:
        logger.error("No 'connexion' button")

    # CLick on Top right corner User Account picture
    try:
        button_google_account = WebDriverWait(p_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@guidedhelpid and contains(@title,'@')]")))
        # button_google_account.click()
        p_driver.execute_script("arguments[0].click();", button_google_account)
        time.sleep(random.uniform(1, 2))
    except:
        logger.error("ERROR : No top right corner Google Account button found!")

    # INITIALISATION

    cpt = 0
    while True:
        try:

            # We extract all the string with '@'
            Gmap_usernames_elements = WebDriverWait(p_driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(text(),'@')]")))
            list_gmap_username = []
            for gmap_user in Gmap_usernames_elements:
                if gmap_user.text != "" and gmap_user.text is not None:
                    list_gmap_username.append(gmap_user.text)
                    logger.info(f"Gmap username : {Gmap_username}")
            return True, list_gmap_username
        except Exception as ex:
            cpt += 1
            if cpt > 2:
                logger.error(f"ERROR AreWeGmapLoggedIn No Google Account Found  {ex}")
                return False, Gmap_username


def RunGmapBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):
    logger.info(
        f"================================================ RunGmapBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://google.com/maps')
    driver.implicitly_wait(10)

    # ============================================================================
    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_Gmap, Gmap_username = AreWeGmapLoggedIn(driver)
    logger.info(f"are_we_connected_Gmap : {are_we_connected_Gmap}")
    logger.info(f"Gmap_username : {Gmap_username}")

    if Gmap_username == "" or Gmap_username is None:
        logger.info(f"ERROR Gmap_username is empty!!!")

    if are_we_connected_Gmap:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Gmap with profile {Gmap_username}")

        # ARE THERE SEVERAL GMAP ACCOUNTS OR 1
        if isinstance(Gmap_username, list):
            # As we need to skip the first Gmap user who just executed the task
            for i in range(0,len(Gmap_username)):
                print(f"""
                {Gmap_username}
                Start the loop for i in range(0,{len(Gmap_username)}):
                {Gmap_username[i]}
                """)
                Gmap_user = Gmap_username[i]
                # Let's get the quantity of actions possible
                logger.info(f"=== [3] GetQuantityActions {Gmap_user} =======================================")
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Gmap_user)
                if quantity_actions > 0:
                    # We want to execute the function now because everything is ready for. But we need
                    # to prepare the loop of the other accounts
                    # So here is the plan:
                    #      1 - We execute immediately task,
                    #          Then we need to login in next account and come back to loop for executing this task
                    #      2 - We CLick on top right corner account button
                    #      3 - We match the Gmap_user in the list of accounts displayed

                    # 1 - We execute immediately task
                    try:
                        p_function(p_browser,p_taskuser_id, driver, Gmap_user, quantity_actions)
                        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                        logger.info(f"FINISHED Task {p_taskuser_id} - {Gmap_user} - {quantity_actions} actions.")
                    except Exception as ex:
                        logger.error(f"ERROR excuting {p_function} - {ex}")
                    cpt_i=0
                    while True:
                        try:
                            # 2 - We CLick on top right corner account button
                            # CLick on Top right corner User Account picture
                            button_google_account = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, "//a[@guidedhelpid and contains(@title,'@')]")))
                            driver.execute_script("arguments[0].click();", button_google_account)
                            # 3 - We match the Gmap_user in the list of accounts displayed
                            Gmap_user = Gmap_username[i+1]
                            logger.info(f"Try to click on next account {Gmap_user}")
                            Gmap_user_element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(),'{Gmap_user}')]/ancestor::a")))
                            driver.execute_script("arguments[0].click();", Gmap_user_element)
                            time.sleep(random.uniform(3,5))
                            break
                        except Exception as ex:
                            cpt_i+=1
                            if cpt_i>2:
                                break
                            else:
                                logger.error(f"ERROR CLick on next GMap Account : {ex}")
            return True
        else:

            # Let's get the quantity of actions possible
            logger.info("=== [3] GetQuantityActions =======================================")
            quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Gmap_username)
            if quantity_actions > 0:
                # ===================================================================================
                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                # ===================================================================================
                p_function(p_browser,p_taskuser_id, driver, Gmap_username, quantity_actions)
                logger.info(f"FINISHED Task {p_taskuser_id} - {Gmap_username} - {quantity_actions} actions.")
                return True


def Scraping_Google_Map_Search_by_keywords_city_26(p_browser,p_taskuser_id, p_driver, Gmap_username, p_quantity_actions,label_log,lock):
    logger.info(
        f"=================== Scraping_Gmap_Group_Members_32 {p_taskuser_id} - {Gmap_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS", f"Gmap user {Gmap_username} can make {p_quantity_actions} actions now of Scraping_Google_Map_Search_by_keywords_city_26!")
    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodules.GetDetailsTaskUser(p_taskuser_id)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Google_Map_Search_by_keywords_city_26",
                                  "Black")



def Cold_Messaging_Google_Map_Search_by_keyword_city_9(p_browser,p_taskuser_id, p_driver, Gmap_username, p_quantity_actions,label_log,lock):
    logger.info(
        f"=================== Cold_Messaging_Google_Map_Search_by_keyword_city_9 {p_taskuser_id} - {Gmap_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Google_Map_scraping_search_results(p_browser, p_taskuser_id, p_driver, Gmap_username,
                                               p_quantity_actions, label_log,
                                               lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Google_Map_Search_by_keyword_city_9",
                                  "Black")
    return result, counter
