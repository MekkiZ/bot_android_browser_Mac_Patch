# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
sys.path.append(".")
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam
import logging
import pdb
from . import Browser_Twitter_auto_follow
from . import Browser_Twitter_auto_unfollow
from . import Browser_Twitter_like_random



# ================================ LOGGER ====================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Twitter_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =========================================================================================
# =================================== Twitter DESKTOP METHODS ============================
# =========================================================================================


def AreWeTwitterLoggedIn(p_driver):
    """
    This function check if browser is connected to Twitter or not and return True with Twitter username
    or False with None
    """
    logger.info("=== [2] AreWeTwitterLoggedIn() ====================================")

    # INITIALISATION
    Twitter_username = None

    cpt=0
    while True:
        try:
            Twitter_username_element = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and contains(@data-testid,'Account')]//span[starts-with(text(),'@')]")))
            Twitter_username_brut = Twitter_username_element.text
            logger.info(f"Twitter_username_brut : {Twitter_username_brut}")
            # We need to make some transformation because Twitter_username_brut is returning "Name\nYour profile"

            Twitter_username = Twitter_username_brut
            return True, Twitter_username
        except Exception as ex:
            p_driver.switch_to.default_content()
            print("Switch to default content")
            cpt += 1
            if cpt > 2:
                logger.error(f"ERROR Twitter getting username : {ex}")
                return False, Twitter_username









def RunTwitterBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):
    logger.info(f"================================================ RunTwitterBrowser {p_browser} - {p_taskuser_id} ===================================================")

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

    if str(p_browser).lower() == "chrome":
        print("Open Chrome")
        p_driver = mymodulesteam.ChromeDriverWithProfile()
    elif str(p_browser).lower() == "firefox":
        print("Open Firefox")
        p_driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False
    print(p_driver.name)
    p_driver.get("https://twitter.com/login")
    #p_driver.implicitly_wait(10)
    print("Twitter page open")
    # ============================================================================
    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_Twitter, Twitter_username = AreWeTwitterLoggedIn(p_driver)
    logger.info(f"are_we_connected_Twitter : {are_we_connected_Twitter}")
    logger.info(f"Twitter_username : {Twitter_username}")
    if Twitter_username == "":
        logger.info(f"ERROR Twitter_username is empty!!!")

    if are_we_connected_Twitter:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Twitter with profile {Twitter_username}")

        # Let's get the quantity of actions possible
        logger.info("=== [3] GetQuantityActions =======================================")
        quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Twitter_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter =p_function(p_browser,p_taskuser_id,p_driver,Twitter_username, quantity_actions,label_log,lock)
    else:
        logger.info("No Twitter user is connected!")
        # Let's login:
        button_login = WebDriverWait(p_driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@role,'button') and contains(@data-testid,'Login')]")))
        button_login[0].click()
        print("Click on login link!")

        p_driver.implicitly_wait(10)
        time.sleep(random.uniform(3, 5))
        # === 2 TEST IF WE ARE ALREADY LOGGED IN
        are_we_connected_Twitter, Twitter_username = AreWeTwitterLoggedIn(p_driver)
        if are_we_connected_Twitter:
            # Let's get the quantity of actions possible
            logger.info("=== [3] GetQuantityActions =======================================")
            quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Twitter_username)
            if quantity_actions > 0:
                # ===================================================================================
                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                # ===================================================================================
                result, counter =p_function(p_taskuser_id, p_driver, Twitter_username, quantity_actions)
        else:
            logger.error("PhoneBot tried to login but it didn't succeed!")
    return result, counter

def Authority_Twitter_Auto_Follow_35(p_browser,p_taskuser_id,p_driver,Twitter_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Authority_Twitter_Auto_Follow_35 {p_taskuser_id} - {Twitter_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Twitter_auto_follow.Browser_Twitter_Auto_Follow(p_browser,
                                                                      p_taskuser_id,
                                                                      Twitter_username,
                                                                      p_driver,
                                                                      p_quantity_actions,
                                                                      label_log,
                                                                      lock)
    mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Twitter_Auto_Follow_35",
                                      "Black")
    return result, counter


def Authority_Twitter_Unfollow_51(p_browser,p_taskuser_id,p_driver,Twitter_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Authority_Twitter_Auto_Follow_35 {p_taskuser_id} - {Twitter_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Twitter_auto_unfollow.Browser_Twitter_Auto_unFollow(p_browser,
                                                                      p_taskuser_id,
                                                                      Twitter_username,
                                                                      p_driver,
                                                                      p_quantity_actions,
                                                                      label_log,
                                                                      lock)
    mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Twitter_Unfollow_51",
                                      "Black")
    return result, counter


def Influencers_Twitter_Influencers_5(p_browser,p_taskuser_id,p_driver,Twitter_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Influencers_Twitter_Influencers_5 {p_taskuser_id} - {Twitter_username} - {p_quantity_actions} =======================")
    # THIS TASK WAS NOT DONE !!!!
    mymodulesteam.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Twitter_Influencers_5",
                                  "Black")


def Cold_Messaging_Twitter_Followers_of_accounts_20(p_browser,p_taskuser_id,p_driver,Twitter_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Twitter_Followers_of_accounts_20 {p_taskuser_id} - {Twitter_username} - {p_quantity_actions} =======================")

    # THIS TASK WAS NOT DONE !!!!
    mymodulesteam.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Twitter_Followers_of_accounts_20",
                                  "Black")
