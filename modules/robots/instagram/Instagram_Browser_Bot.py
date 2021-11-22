# -*- coding: utf-8 -*-
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules, mymodulesteam
import logging
import pdb
from . import Browser_Instagram_send_message_followers,Browser_Instagram_scraping_followers,  \
    Browser_Instagram_send_message_likers_commenters,Browser_Instagram_send_message_influencers,  \
    Browser_Instagram_like_random,Browser_Instagram_auto_follow,Browser_Instagram_auto_unfollow

# ================================ LOGGER ====================================
from modules.robots.instagram import Browser_Instagram_send_message_followers

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Instagram_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =========================================================================================
# =================================== Instagram DESKTOP METHODS ============================
# =========================================================================================

def AreWeInstagramLoggedIn(p_driver):
    """
    This function check if browser is connected to Instagram or not and return True with Instagram username
    or False with None
    """
    logger.info("=============================== AreWeInstagramLoggedIn() =========================================")

    # === CLick on Popup =================================================================
    try:
        buttons_accept = p_driver.find_elements_by_xpath("//div[@role='dialog']//button")
        for button_accept in buttons_accept:
            if str(button_accept).find('accept') != -1:
                #button_accept.click()
                p_driver.execute_script("arguments[0].click();", button_accept)
    except Exception as ex:
        logger.error(f"ERROR AreWeInstagramLoggedIn => profile icon menu in top right corner {ex}")

    # === Get username text ===================================================
    # INITIALISATION
    Instagram_username = None
    cpt=0
    while True:
        try:
            Instagram_username_element = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@aria-labelledby,*)]//div[contains(@style,'left:')]//div[@style='width: 100%;']//a[contains(@href,'/')]")))
            Instagram_username_brut = Instagram_username_element[1].text
            print(f"Instagram_username_brut : {Instagram_username_brut}")
            # We need to make some transformation because Instagram_username_brut is returning "Name\nYour profile"
            Instagram_username = Instagram_username_brut
            return True, Instagram_username
        except Exception as ex:
            cpt += 1

            if cpt > 2:
                logger.error(f"ERROR Instagram getting username : {ex}")
                return False, Instagram_username
    return False,None


def AreWeinInstagramProfilesPage(p_driver):

    """
    This function will check if we are in the Instagram homepage where all the profiles are displayed
    """
    logger.info("=============================== AreWeinInstagramProfilesPage() =========================================")

    try:
        list_Instagram_profiles = []

        buttons_account = WebDriverWait(p_driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button']//div")))
        p=1
        for button_account in buttons_account:
            if p%2!=0:
                list_Instagram_profiles.append(button_account.text)
            p+=1
            print(list_Instagram_profiles)
        return True, list_Instagram_profiles

    except Exception as ex:
        logger.error(f"ERROR Instagram when clicking on Logout : {ex}")

        #logger.info("Let's try another button 'Change account'")
        #buttons_account = WebDriverWait(p_driver, 15).until(
        #    EC.presence_of_element_located((By.XPATH,  "//button[@type='button' and contains(text(),'Change')]")))
        return False, None


def InstagramLogout(p_driver):
    """
    This method will logout of Instagram
    """
    logger.info("=============================== InstagramLogout() =========================================")

    while True:
        try:
            # Click on profile icon menu in top right corner
            try:
                button_menu = WebDriverWait(p_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//nav//span[@role='link']")))
                #button_menu.click()
                p_driver.execute_script("arguments[0].click();", button_menu)



            except Exception as ex:
                logger.error(f"ERROR profile icon menu in top right corner {ex}")

            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            # Click on Logout
            try:

                button_logout = WebDriverWait(p_driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Déconnexion') or contains(text(),'Logout' )]")))
                #button_logout.click()
                p_driver.execute_script("arguments[0].click();", button_logout)
                break

            except Exception as ex:
                logger.error(f"ERROR Instagram when clicking on Logout Link in top right menu : {ex}")



        except Exception as ex:
            logger.error(f"ERROR Instagram clicking on top right menu : {ex}")


def InstagramLogin(p_driver, p_profile=""):
    """
    This method will login to Instagram with a specific profile
    """
    logger.info(f"=============================== InstagramLogin =========================================")

    # ======================= ACCEPT TERMS POPUP ==============================================
    try:
        # Click on cookie popup is exists
        button_accept_cookies = p_driver.find_elements_by_xpath("//div[@role='dialog']//button")
        #button_accept_cookies[0].click()
        p_driver.execute_script("arguments[0].click();", button_accept_cookies[0])
    except Exception as ex:
        logger.error(f"ERROR clicking on cookie popup : {ex}")

    # =============================================================================
    # There are 3 scenarios:
    #       - A : Only one user with the button "continue as ..."  //button[@role='button']
    #       - B : several users with the button "continue as ..." //div[@role='button']
    #       - C : NO USER AT ALL, WE SIMPLY CLICK ON LOGIN BUTTON


    if p_profile=="":
        # A : Only ONE user with the button "continue as ..."  //button[@role='button']
        try:
            buttons_account = WebDriverWait(p_driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@type='button' and contains(text(),'continu')]")))
            #buttons_account[0].click()
            p_driver.execute_script("arguments[0].click();", buttons_account[0])

        except Exception as ex:
            logger.error(f"ERROR Instagram Login Scenario A clicking on button   : {ex}")
            logger.error(f"Let's try to simply click on login button if fields username and passwords are filled.")
            field_username = WebDriverWait(p_driver, 15).until(
                EC.presence_of_element_located((By.XPATH,"//input[@name='username']")))
            txt_username = field_username.text
            field_password = WebDriverWait(p_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH,"//input[@type='password']")))
            txt_password = field_password.text
            if txt_password !="" and txt_username!="":
                button_connexion = WebDriverWait(p_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
                p_driver.execute_script("arguments[0].click();", button_connexion)
                time.sleep(random.uniform(4, 6))


    else:
        # B : SEVERAL users with the button "continue as ..." //div[@role='button']
        try:
            button_account = WebDriverWait(p_driver, 15).until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='button']//div[contains(string(), '{p_profile}')]")))
            #button_account.click()
            p_driver.execute_script("arguments[0].click();", button_account)

        except Exception as ex:
            logger.error(f"ERROR Instagram clicking on profile  {p_profile} : {ex}")

    # ======================= refuse notification ==============================================
    try:
        # Click on cookie popup is exists
        popup_title = p_driver.find_element_by_xpath("//div[@role='dialog']//h2")
        popup_title_text=popup_title.text
        if str(popup_title_text).find('notification')!=-1:
            button_refuse_notification = p_driver.find_elements_by_xpath("//div[@role='dialog']//button")
            #button_refuse_notification[1].click()
            p_driver.execute_script("arguments[0].click();", button_refuse_notification[1])

    except Exception as ex:
        logger.error(f"ERROR clicking on cookie popup : {ex}")




def RunInstagramBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):

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
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False
    driver.get('https://instagram.com')

    time.sleep(random.uniform(3, 5))
    # ============================================================================
    # === 2 TEST IF WE ARE ALREADY LOGGED IN

    are_we_connected_Instagram, Instagram_username = AreWeInstagramLoggedIn(driver)
    print(f"are_we_connected_Instagram : {are_we_connected_Instagram}")
    print(f"Instagram_username : {Instagram_username}")
    if Instagram_username == "":
        print(f"ERROR Instagram_username is empty!!!")

    if are_we_connected_Instagram:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Instagram with profile {Instagram_username}")


        # Let's get the quantity of actions possible
        quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Instagram_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter = p_function(p_browser,p_taskuser_id, driver, Instagram_username, quantity_actions)

            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {Instagram_username} logout of Instagram .")
            InstagramLogout(driver)
            are_we_profiles_Instagram_pages, list_Instagram_profiles = AreWeinInstagramProfilesPage(driver)
            print(f"""
                are_we_profiles_Instagram_pages = {are_we_profiles_Instagram_pages}, 
                list_Instagram_profiles = {list_Instagram_profiles}
            """)
            if are_we_profiles_Instagram_pages:
                logger.info(f"PhoneBot is in Instagram page list of profiles {list_Instagram_profiles}")
                # WE WILL RUN THE TASK FOR EACH PROFILE EXCEPT THE ONE WE JUST DID
                for Instagram_profile in list_Instagram_profiles:
                    if str(Instagram_username).find(Instagram_profile) != -1:
                        logger.info(f"We just automated Instagram with {Instagram_profile}!")
                    else:
                        logger.info(f"We will start automation on Instagram with profile {Instagram_profile}.")
                        InstagramLogin(driver, Instagram_profile)
                        # === TEST IF WE SUCCESSFULLY LOGGED IN
                        are_we_connected_Instagram, Instagram_username = AreWeInstagramLoggedIn(driver)
                        if not are_we_connected_Instagram:
                            logger.error(f"PhoneBot couldn't login to Instagram with profile {Instagram_profile}!")
                        else:
                            # ===================================================================================
                            # Let's get the quantity of actions possible
                            quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Instagram_username)
                            if quantity_actions > 0:
                                # ===================================================================================
                                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                                # ===================================================================================

                                result, counter = p_function(p_browser,p_taskuser_id, driver, Instagram_username, quantity_actions)
                                logger.info(f"Profile {Instagram_profile} logout of Instagram .")
                                InstagramLogout(driver)
                            else:
                                InstagramLogout(driver)

        else:
            # THis user already reach the limit, We need to logout and loop all the profiles
            logger.info(f"Profile {Instagram_username} already reach the limit, We need to logout and loop all the profiles .")
            InstagramLogout(driver)

    else:
        # ============================================================================
        # ===== B - WE ARE NOT CONNECTED

        logger.info(f"PhoneBot is NOT logged in Instagram")
        # === TEST IF WE ARE IN THE LIST OF PROFILES PAGE
        logger.info(f"PhoneBot will login to Instagram with profile.")
        

        are_we_profiles_Instagram_pages, list_Instagram_profiles = AreWeinInstagramProfilesPage(driver)
        print(f"""
                        are_we_profiles_Instagram_pages = {are_we_profiles_Instagram_pages}, 
                        list_Instagram_profiles = {list_Instagram_profiles}
                    """)
        if are_we_profiles_Instagram_pages:
            logger.info(f"PhoneBot is in Instagram page list of profiles {list_Instagram_profiles}")
            # WE WILL RUN THE TASK FOR EACH PROFILE
            for Instagram_profile in list_Instagram_profiles:
                logger.info(f"PhoneBot login to Instagram with profile {Instagram_profile}.")
                InstagramLogin(driver, Instagram_profile)
                # === TEST IF WE SUCCESSFULLY LOGGED IN
                are_we_connected_Instagram, Instagram_username = AreWeInstagramLoggedIn(driver)
                if not are_we_connected_Instagram:
                    logger.error(f"PhoneBot couldn't login with profile {Instagram_profile}!")
                    # Sometimes an activation code will be sent by sms
                    # PhoneBot can't fill this code. So we need to skip this acccount.
                    # For the moment, the solution is to reload homepage, check if we are login, chec kon several profiles, login
                    # Which means we need to loop again from begining. So let's create a counter CPT_LOOP
                    # We need to come back to home page with the list of users
                    driver.get('https://instagram.com')
                    driver.implicitly_wait(10)
                    time.sleep(random.uniform(3, 5))

                else:

                    # ===================================================================================
                    # Let's get the quantity of actions possible
                    quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Instagram_username)
                    if quantity_actions > 0:
                        # ===================================================================================
                        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                        # ===================================================================================
                        result, counter = p_function(p_browser,p_taskuser_id, driver, Instagram_username, quantity_actions)
                        logger.info(f"Profile {Instagram_profile} logout of Instagram .")
                        InstagramLogout(driver)
                    else:
                        InstagramLogout(driver)
        else:
            logger.info(
                f"PhoneBot is not in multiple Account Login Instagram page")
            InstagramLogin(driver)


    return result, counter


def Scraping_Instagram_Followers_of_accounts_25(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Scraping_Instagram_Followers_of_accounts_25 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_scraping_followers.Scraping_Instagram_Followers(
        p_browser,
        p_taskuser_id,
        Instagram_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Instagram_Followers_of_accounts_25",
                                  "Black")

    return result, counter

def Authority_Instagram_Auto_Follow_34(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Authority_Instagram_Auto_Follow_34 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_auto_follow.Browser_Instagram_Auto_Follow(
        p_browser,
        p_taskuser_id,
        Instagram_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Instagram_Auto_Follow_34",
                                  "Black")

    return result, counter

def Cold_Messaging_Instagram_Followers_of_accounts_4(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Instagram_Followers_of_accounts_4 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_send_message_followers.Cold_Messaging_Instagram_Followers_Of_Accounts(
                                                                                    p_browser,
                                                                                    p_taskuser_id,
                                                                                    Instagram_username,
                                                                                    p_driver,
                                                                                    p_quantity_actions,
                                                                                    label_log,
                                                                                    lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Instagram_Followers_of_accounts_4",
                                  "Black")

    return result, counter

def Cold_Messaging_Instagram_Likes_Commenters_58(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Instagram_Likes_Commenters_58 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_send_message_likers_commenters.Browser_Cold_Messaging_Instagram_Likers_and_commenters_of_Instagram_post(
                                                                                    p_browser,
                                                                                    p_taskuser_id,
                                                                                    Instagram_username,
                                                                                    p_driver,
                                                                                    p_quantity_actions,
                                                                                    label_log,
                                                                                    lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Instagram_Likes_Commenters_58",
                                  "Black")

    return result, counter



def Instagram_Influencers_21(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Instagram_Influencers_21 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_send_message_influencers.Instagram_Influencers_21(
                                                                                    p_browser,
                                                                                    p_taskuser_id,
                                                                                    Instagram_username,
                                                                                    p_driver,
                                                                                    p_quantity_actions,
                                                                                    label_log,
                                                                                    lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Instagram_Influencers_21",
                                  "Black")

    return result, counter



def Authority_Instagram_Random_Like_48(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Authority_Instagram_Random_Like_48 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_like_random.Browser_Instagram_Like_random_post(
                                                                                    p_browser,
                                                                                    p_taskuser_id,
                                                                                    Instagram_username,
                                                                                    p_driver,
                                                                                    p_quantity_actions,
                                                                                    label_log,
                                                                                    lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Instagram_Random_Like_48",
                                  "Black")

    return result, counter



def Authority_Instagram_Unfollow_50(p_browser,p_taskuser_id,p_driver,Instagram_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Authority_Instagram_Unfollow_50 {p_taskuser_id} - {Instagram_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Instagram_auto_unfollow.Instagram_Unfollow(
                                                                                    p_browser,
                                                                                    p_taskuser_id,
                                                                                    Instagram_username,
                                                                                    p_driver,
                                                                                    p_quantity_actions,
                                                                                    label_log,
                                                                                    lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Instagram_Unfollow_50",
                                  "Black")

    return result, counter

