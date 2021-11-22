# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules, mymodulesteam
import logging

import pdb
from . import Browser_Leboncoin_scraping_ads

# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Leboncoin_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# =========================================================================================
# =================================== FACEBOOK DESKTOP METHODS ============================
# =========================================================================================

def AreWeLeboncoinLoggedIn(p_driver):
    """
    This function check if browser is connected to facebook or not and return True with Leboncoin username
    or False with None
    """
    
    logger.info("=============================== AreWeLeboncoinLoggedIn() =========================================")

    # INITIALISATION
    fb_username = None
    # ======================= ACCEPT TERMS POPUP ==============================================
    try:
        # Click on cookie popup is exists
        button_Accept_popup = p_driver.find_element_by_xpath(
            "//button[contains(@id,'agree-button')]//span[contains(text(),'Accept')]")
        # button_Accept_popup.click()
        p_driver.execute_script("arguments[0].click();", button_Accept_popup)
    except Exception as ex:
        logger.error(f"ERROR clicking on cookie popup : {ex}")

    # Now let's check if there is the button "Se connecter"
    try:
        button_se_connecter = WebDriverWait(p_driver, 15).until(EC.presence_of_element_located((By.XPATH,"//span[@data-text='Se connecter']")))
        if button_se_connecter :
            logger.error("PhoneBot is NOT logged in Leboncoin. You must log in in Leboncoin from your browser and never log out. Your browser will keep the session open with Leboncoin and PhoneBot will be able to do the automation task!")
            return False,None
    except Exception as ex:
        logger.error(f"{ex} - PhoneBot didn't find the button 'Se connecter'!")

    # Let's get the username
    spans_username = WebDriverWait(p_driver, 15).until(EC.presence_of_all_elements_located((By.XPATH,"(//a[@title='Messages' and @href='/messages'])[1]/following-sibling::div//button//span")))
    print(f"spans_username : {spans_username}")
    pdb.set_trace()
    for i in range(0,len(spans_username)):
        try:
            Leboncoin_username = spans_username[i].get_attribute('data-text')
            print(Leboncoin_username)
            if Leboncoin_username is not None:
                return True, Leboncoin_username
        except Exception as ex:
            logger.error(f"{ex} - No span username found")
    return False,None




def RunLeboncoinBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):

    """
    This method will open browser and run the task for all the profiles found in cookies Browser
    It will have to check for the daily & hourly limit
    It will return True if it run some actions, or False if nothing
    :param p_function:
    :param p_taskuser_id:
    :return:
    """
    # === 1 OPEN BROWSER
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False
    driver.get('https://leboncoin.fr')
    driver.implicitly_wait(10)

    # Let's "Accept" the cookie popup if necessary
    
    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_Leboncoin, Leboncoin_username = AreWeLeboncoinLoggedIn(driver)
    print(f"are_we_connected_Leboncoin : {are_we_connected_Leboncoin}")
    print(f"Leboncoin_username : {Leboncoin_username}")
    if Leboncoin_username == "":
        print(f"ERROR Leboncoin_username is empty!!!")
    if are_we_connected_Leboncoin:
        logger.info(f"PhoneBot is logged in Leboncoin with profile {Leboncoin_username}")
        # ===================================================================================
        # Let's get the quantity of actions possible
        quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Leboncoin_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter = p_function(p_browser,p_taskuser_id, driver, Leboncoin_username, quantity_actions)
            return result, counter
        else:
            # THis user already reach the limit, We need to logout and loop all the profiles
            logger.error(f"Profile {Leboncoin_username} already reach his daily limits on Leboncoin")
            return False,0

    else:
        logger.info(f"PhoneBot is NOT logged in Leboncoin. You must log in in Leboncoin from your browser '{p_browser}' and never log out. Your browser will keep the session open with Leboncoin and PhoneBot will be able to do the automation task!")
        return False,0



def Scraping_Leboncoin_Ads_27(p_browser,p_taskuser_id,p_driver,Leboncoin_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Scraping_Leboncoin_Ads_27 {p_taskuser_id} - {Leboncoin_username} - {p_quantity_actions} =======================")


    result, counter = Browser_Leboncoin_scraping_ads.Browser_leboncoin_ADS(p_browser, p_taskuser_id, Leboncoin_username, p_quantity_actions, label_log, lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Leboncoin_Ads_27",
                                  "Black")
    return result, counter