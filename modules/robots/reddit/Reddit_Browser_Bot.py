# -*- coding: utf-8 -*-
import random
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
from modules import mymodules,mymodulesteam
import logging
import pdb
from random import randint
from random import uniform
import requests
from . import Browser_Reddit_send_message_group_members, Browser_Reddit_send_message_group_admins

# ================================ LOGGER ====================================
open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Reddit_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# =========================================================================================
# =================================== Reddit DESKTOP METHODS ============================
# =========================================================================================
def CheckAndChangeProfileString(profile):
    # profile must be between 3 and 20 characters
    if len(profile) > 20:
        print(f"'{profile}' is too long!")
        # We need to make it shorter
        profile = profile[:20]
        print(f"New profile is '{profile}'")
    if len(profile) < 3:
        # We need to make it longer
        print(f"'{profile}' is too short!")
        profile = profile + str(randint(10000, 99999))
        print(f"New profile is '{profile}'")
    return profile

def AreWeRedditLoggedIn(p_driver, profile=''):
    """
    This function check if browser is connected to Reddit or not and return True with Reddit username
    or False with None
    """
    logger.info("=== [2] AreWeRedditLoggedIn() ====================================")
    # =====================================================================
    # Let's check if there is a popup inviting us to join communities,
    # In this case, we click on button 'Finish'
    try:
        button_finish = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(),'Finish')]")))
        button_finish.click()
        time.sleep(random.uniform(3, 5))
    except Exception as ex:
        logger.info(f"No button 'Finish'! : {ex}")
    # ======================================================================
    # INITIALISATION
    Reddit_username = None

    try:
        Reddit_username_element = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[@id='email-collection-tooltip-id']/span/span[1]")))
        Reddit_username_brut = Reddit_username_element.text
        logger.info(f"Reddit_username_brut : {Reddit_username_brut}")
        # We need to make some transformation because Reddit_username_brut is returning "Name\nYour profile"
        Reddit_username = Reddit_username_brut
        time.sleep(uniform(2, 5))
        return True, Reddit_username
        logger.info(f"We are connected")
    except Exception as ex:
        logger.error(f"ERROR Reddit getting username : {ex}")
        return False, Reddit_username
        logger.info(f"We are not connected")
    
    time.sleep(uniform(4.5, 8))
    #button_menu.click()
    logger.info(f"AreWeRedditLoggedIn finished")

    Reddit_username = p_username

def CheckAndChangeProfile(p_driver):
    #    This method will disconnect of Reddit, open the popup 'Login' and change automatically profiles
    #    :param p_driver:
    #    :return:
    try:
        button_Log_In = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='SHORTCUT_FOCUSABLE_DIV']//a[contains(@href,'https://www.reddit.com/login')]")))
        logger.info("Obviously, there is the Login popup!")
        p_driver.get("https://www.reddit.com/settings")
        time.sleep(random.uniform(4.5, 6.8))
        # Get the email
        reddit_email_element = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'@')]")))
        reddit_email = reddit_email_element.text
        profile = reddit_email[:reddit_email.find('@')]
        domain = reddit_email[reddit_email.find('@') + 1:]
        print(f"{profile} @ {domain}")

        with open(mymodules.LoadFile('free_email_provider_domains.txt')) as freeemailprovider_file:
            if str(domain).lower() in freeemailprovider_file.read():
                print(f'Domain {domain} is a free email provider')
            else:
                profile = domain.replace(".", "")

        print(f"PhoneBot found the email {reddit_email} and build a new username {profile}")
        # IF THE POPUP 'CHANGE USERNAME' IS SHOWN, WE CHANGE IT. IT MEANS WE JUST IN FACT CREATED A NEW REDDIT USER
        try:
            pdb.set_trace()
            button_Log_In = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='SHORTCUT_FOCUSABLE_DIV']//a[contains(@href,'https://www.reddit.com/login')]")))
            # button_Log_In.click()
            p_driver.execute_script("arguments[0].click();", button_Log_In)
            time.sleep(random.uniform(3, 5))
            profile = CheckAndChangeProfileString(profile)
            New_Reddit_Username = str(profile).replace(' ', '_')
            input_new_username_field = WebDriverWait(p_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@spellcheck='false']")))

            while True:
                print(f"New_Reddit_Username : {New_Reddit_Username}")
                input_new_username_field.click()
                input_new_username_field.clear()
                input_new_username_field.send_keys(New_Reddit_Username)
                # LET'S CHECK IS USERNAME ALREADY EXISTS OR NOT
                try:
                    alert_username_already_exists = p_driver.find_element_by_xpath(
                        "//p[contains(text(),'Sorry, this username is taken. Try another.')]")
                    New_Reddit_Username = New_Reddit_Username + str(randint(10000, 99999))
                    profile = CheckAndChangeProfileString(New_Reddit_Username)

                except:
                    logger.info("There is no alert message 'User already exists'!")
                    continue_button = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Continue')]")))
                    # continue_button.click()
                    p_driver.execute_script("arguments[0].click();", continue_button)
                    time.sleep(random.uniform(3, 6))
                    # CLick on Save username  ==> NOT FOUND
                    button_save_username = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Save Username')]")))
                    # button_save_username.click()
                    p_driver.execute_script("arguments[0].click();", button_save_username)
                    time.sleep(random.uniform(3, 7))
                    return New_Reddit_Username
        except Exception as ex:
            logger.error(f"ERROR There wasn't 'Change Username' button!")
            return None

    except Exception as ex:
        logger.error(f"ERROR Failed to click on 'Change Username' button!")
        return None

def IsMultipleAccounts(p_driver):

    logger.info("==== IsMultipleAccounts =====")
    #______Open the Loggin Pop up________#
    #______Click on "Connect" if there is a registered profile______#
    try:
        button_Log_In = p_driver.find_element_by_xpath("//div[@id='SHORTCUT_FOCUSABLE_DIV']//a[contains(@href,'https://www.reddit.com/login')]")
        p_driver.execute_script("arguments[0].click();", button_Log_In)
        # button_Log_In.click()
        time.sleep(random.uniform(3, 6))
    except:
        logger.error("No Reddit Link button_Log_In found!")
    #______Click on "Continue with google______#
    try:
        # OPen Google Accounts Window
        cpt_result_google=0
        while True:
            result_google=RedditLogin(p_driver)
            if result_google:
                break
            else:
                cpt_result_google+=1
                if cpt_result_google>2:
                    return None
        button_Google_accounts = p_driver.find_elements_by_xpath("//div[contains(@data-identifier,'@')]")
        List_Reddit_username = []
        for button_Google_account in button_Google_accounts:
            button_account_text_brut = button_Google_account.text
            list_button_account_text_brut = button_account_text_brut.split("\n")
            Reddit_username = list_button_account_text_brut[0]
            email = list_button_account_text_brut[1]

            logger.info(f"email : {email}")
            logger.info(f"Reddit_username : {Reddit_username}")

            List_Reddit_username.append(Reddit_username)
        return List_Reddit_username

    except Exception as ex:
        logger.info(f"ERROR IsMultipleAccounts : {ex}")
        return None

def LoopAllAccounts(p_driver,p_browser,p_function, p_username,p_taskuser_id,label_log,lock):

    logger.info(f"=== [5] LoopAllAccounts {p_taskuser_id} =======================================")
    #------------------------------Disconnect--------------------#
    RedditLogout(p_driver)
    #--------------------Begin LoopAllAccount---------------------#
    list_profiles = IsMultipleAccounts(p_driver)
    logger.info(f"list_profiles : {list_profiles}")

    if list_profiles is not None:

        for profile in list_profiles:
            logger.info(f"Loop list_profiles profile : {profile}")

            # We need to login to pickup username and check quantity of actions
            try:
                result = p_driver.window_handles
                # IF THERE IS NOT THE 2ND WINDOW GOOGLE LOGIN ACCOUNTS, WE OPEN IT
                if len(result) == 1:
                    cpt_result_google=0
                    while True:
                        result_google = RedditLogin(p_driver)
                        if result_google:
                            break
                        else:
                            cpt_result_google += 1
                            if cpt_result_google > 2:
                                return None
                    result = p_driver.window_handles
                p_driver.switch_to.window(result[1])
                # WE CLICK ON THE PROFILE GOOGLE ACCOUNT TO LOGIN
                button_Google_account = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f"//div[contains(@data-identifier,'@')]//div[contains(string(), '{profile}')]")))
                button_Google_account[0].click()
                time.sleep(random.uniform(5, 8))
                p_driver.switch_to.window(result[0])
                logger.info("PhoneBot returned back to main Window")

            except Exception as ex:
                logger.error(f"ERROR Reddit when button_Google_account.click() : {ex}")
            are_we_connected_Reddit, Reddit_username = AreWeRedditLoggedIn(p_driver, profile)
            # WE NEED TO CHECK IF THERE IS THE POPUP 'CHANGE USERNAME' IN CASE IT IS A NEW REGISTRATION
            New_Reddit_Username = CheckAndChangeProfile(p_driver)
            if New_Reddit_Username is not None:
                Reddit_username = New_Reddit_Username

            logger.info(f"are_we_connected_Reddit : {are_we_connected_Reddit}")
            if are_we_connected_Reddit:
                # Let's get the quantity of actions possible
                p_quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, p_username)
                logger.info(f"quantity_actions : {p_quantity_actions} *****")
                if p_quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    p_function(p_browser,p_driver,p_taskuser_id, p_username, p_quantity_actions,label_log,lock)
                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {profile} logout of Reddit .")
                    RedditLogout(p_driver)
                    # ==============================================
                    # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                    # WE NEED TO MAKE A BREAK
                    time.sleep(random.uniform(6, 9))
                    logger.info("PAUSE....")

                else:
                    p_driver.get('https://reddit.com')
                    time.sleep(random.uniform(3, 6))

    else:
        logger.info(f"Try to click on simple 'Sign in' button ")
        # A : Only ONE user with the button "Sign in / S'identifier ..."  class=sign-in-form__submit-button
        try:
            # We open Reddit log in window
            button_Log_In = p_driver.find_element_by_xpath("//div[@id='SHORTCUT_FOCUSABLE_DIV']//a[contains(@href,'https://www.reddit.com/login')]")
            button_Log_In.click()
            time.sleep(random.uniform(4, 7))

        except Exception as ex:
            logger.error(f"ERROR Reddit Sign in Scenario A clicking on button   : {ex}")

        try:
            # We click on sign in button
            button_Log_In_submit = p_driver.find_element_by_xpath("//button[@type='submit' and contains(text(),'Log In')]")
            button_Log_In_submit.click()
            time.sleep(random.uniform(2, 6))
            are_we_connected_Reddit, Reddit_username = AreWeRedditLoggedIn(p_driver)
            logger.info(f"are_we_connected_Reddit : {are_we_connected_Reddit}")
            # WE NEED TO CHECK IF THERE IS THE POPUP 'CHANGE USERNAME' IN CASE IT IS A NEW REGISTRATION
            New_Reddit_Username = CheckAndChangeProfile(p_driver)
            if New_Reddit_Username is not None:
                Reddit_username = New_Reddit_Username
                p_username = Reddit_username
            if are_we_connected_Reddit:
                # Let's get the quantity of actions possible
                p_quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, p_username)
                logger.info(f"quantity_actions : {p_quantity_actions} *****")
                if p_quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    p_function(p_browser,p_driver,p_taskuser_id, p_username, p_quantity_actions,label_log,lock)
                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {Reddit_username} logout of Reddit .")
                    RedditLogout(p_driver)
                    # ==============================================
                    # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                    # WE NEED TO MAKE A BREAK
                    time.sleep(random.uniform(2, 6))
                    logger.info("PAUSE....")

                else:
                    p_driver.get('https://reddit.com')
                    time.sleep(random.uniform(3, 8))


        except:
            logger.error("PhoneBot failed to click on 'LOGIN' button!")
            return False
        # login simple

def RedditChangeUser(p_driver):
# Define objects usefull for this method
    button_Log_In = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//button[@role='button' and contains(text(),'Login' or 'Se connecter')]")))
# Check if we are disconnected:
    if AreWeRedditLoggedIn:
        try:
            RedditLogout(p_driver)
            logger.info(f"We are disconnected.")
        except:
            logger.info(f"We were already disconnected")
    else:
            logger.info(f"We are already disconnected.")
# Open Login Popup and connect to profiles:
    try:
        RedditLogin(p_driver)

    except:
        logger.info(f"Reddit is not able to connect to a profile")

def RedditLogin(p_driver):
    """
    This method will:
         - click on Reddit Log In button which will open Reddit login popup
         - click on Reddit Log In button in the Reddit login popup
         - click on Google Sign In popup which will open Google Account Window
    :param p_driver:
    :return:
    """
    # =======================================================================
    # BUTTON 'Log In'
    try:
        button_Log_In = p_driver.find_element_by_xpath("//div[@id='SHORTCUT_FOCUSABLE_DIV']//a[contains(@href,'https://www.reddit.com/login')]")
        p_driver.execute_script("arguments[0].click();", button_Log_In)
        # button_Log_In.click()
        time.sleep(random.uniform(2, 6))
    except:
        logger.error("No Reddit Link button_Log_In found!")

    try:
        # Find the iframe of login popup
        iframe = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ("//iframe[contains(@src,'https://www.reddit.com/login')]"))))
        p_driver.switch_to.frame(iframe)

        print("PhoneBot switch to iframe login")
    except:
        logger.error("No Iframe_Log_In found!")

    try:
        button_Google_login = p_driver.find_element_by_xpath("//div[@id='google-sso']")
        p_driver.execute_script("arguments[0].click();", button_Google_login)
        # button_Google_login.click()
        time.sleep(random.uniform(4, 7))
        print("PhoneBot click on Google Login button")
        result = p_driver.window_handles
        logger.info(result)
        p_driver.switch_to.window(result[1])
        return True
    except:
        logger.error("No googleIdButton found!")
        return False

def RedditLogout(p_driver):
    """
    This method will logout of Reddit
    """
    logger.info("=== [4] RedditLogout() ===================")

    while True:
        try:
            #___________________Click on Account menu___________________________
            button_menu_username = WebDriverWait(p_driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@id='email-collection-tooltip-id']/span/span[1]")))
            #button_menu_username.click()
            p_driver.execute_script("arguments[0].click();", button_menu_username)

            print("Click on username menu top right corner")

            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(3, 7))
            #____________________Click on Logout_________________________

            try:
                button_logout = WebDriverWait(p_driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@role='menu']/a[@href='/']/div[contains(text(),'Se déconnecter') or contains(text(),'Log Out')]")))
                button_logout.click()
                #p_driver.execute_script("arguments[0].click();", button_logout)
                time.sleep(random.uniform(2, 6))
                logger.info(f"We are disconnected now.")
                break

            except Exception as ex:
                logger.error(f"ERROR Reddit didn't find Logout button' : {ex}")


        except Exception as ex:
            logger.error(f"ERROR Reddit clicking on top right menu : {ex}")
            logger.info(f"We are already not connected")
            time.sleep(random.uniform(3, 7))
            break

def RunRedditBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):
    logger.info(f"================================================ RunRedditBrowser {p_taskuser_id} ===================================================")

    """
        This method will open browser and run the task for all the profiles found in cookies Browser
        It will have to check for the daily & hourly limit
        It will return True if it run some actions, or False if nothing
        :param p_function:
        :param p_taskuser_id:
        :return:
        """

    logger.info("=== [1] Open Browser =======================================")
    if p_browser == "Chrome":
        p_driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        p_driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False

    p_driver.get('https://reddit.com')
    p_driver.maximize_window()
    p_driver.implicitly_wait(10)

    # ============================================================================
    AreWeRedditLoggedIn(p_driver, profile='')

    are_we_connected_Reddit, Reddit_username = AreWeRedditLoggedIn(p_driver)
    logger.info(f"are_we_connected_Reddit : {are_we_connected_Reddit}")
    logger.info(f"Reddit_username : {Reddit_username}")
    Reddit_username=CheckAndChangeProfile(p_driver)
    if Reddit_username == None:
        logger.info(f"ERROR Reddit_username is empty!!!")
        p_username = Reddit_username
        LoopAllAccounts(p_driver,p_browser,p_function, p_username, p_taskuser_id,label_log,lock)

    else:
        if are_we_connected_Reddit:
            # ============================================================================
            # ===== A - WE ARE CONNECTED
            logger.info(f"PhoneBot is logged in Reddit with profile {Reddit_username}")
            p_username = Reddit_username

            # Let's get the quantity of actions possible
            logger.info("=== [3] GetQuantityActions =======================================")
            p_quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, p_username)
            if p_quantity_actions > 0:
                # ===================================================================================
                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                # ===================================================================================
                p_function(p_browser,p_driver,p_taskuser_id, p_username, p_quantity_actions,label_log,lock)
                # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                logger.info(f"Profile {Reddit_username} logout of Reddit .")
                RedditLogout(p_driver)
                LoopAllAccounts(p_driver,p_browser,p_function,p_username,p_taskuser_id,label_log,lock)
            else:
                logger.info("No Reddit user is connected!")

        return True



def Influencers_Reddit_Group_Admins_15(p_browser,p_taskuser_id,p_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Influencers_Reddit_Group_Admins_15 {p_taskuser_id} - {p_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Reddit_send_message_group_admins.Browser_Influencers_Reddit_Group_Admins(p_browser, p_taskuser_id, p_username,
                                                                           p_quantity_actions, label_log, lock)

    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Reddit_Group_Admins_15",
                                  "Black")
    return result, counter


def Cold_Messaging_Reddit_Group_Members_55(p_browser,p_taskuser_id,p_driver,p_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Influencers_Reddit_Group_Admins_15 {p_taskuser_id} - {p_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Reddit_send_message_group_members.Cold_Messaging_Reddit_Members_of_groups(p_browser, p_taskuser_id, p_driver, p_username,
                                                                           p_quantity_actions, label_log, lock)

    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Reddit_Group_Admins_15",
                                  "Black")
    return result, counter

#============================Test==================================#
#=====En cas de test sans PhoneBot Remplacer ligne 12 :
# from . import Browser_Reddit_send_message_group_members,Browser_Reddit_send_message_group_admins
# par:
# import Browser_Reddit_send_message_group_members,Browser_Reddit_send_message_group_admins
#==================================================================#
'''
p_browser = "Chrome"
p_function = Cold_Messaging_Reddit_Group_Members_55
p_taskuser_id = "3548"
p_quantity_actions = 5
label_log = ""
lock = threading.Lock()
RunRedditBrowser(p_browser, p_function, p_taskuser_id,label_log,lock)
'''