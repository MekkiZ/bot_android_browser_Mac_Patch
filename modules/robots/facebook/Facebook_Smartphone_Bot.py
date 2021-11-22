# -*- coding: utf-8 -*-
import pdb
import subprocess
import threading
import random
import sqlite3
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging
from modules import mymodulesteam, mymodules

from modules.robots.facebook.Smartphone_Scraping_Facebook_Group_members \
    import Smartphone_Scraping_Facebook_Group_members
# from . import Smartphone_Scraping_Facebook_Group_members

open (mymodulesteam.LoadFile ('log.log'), 'w').close()
logger = logging.getLogger('__Facebook_Smartphone_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ==========================================================================================================
# ==============================     FUNCTION INITIALISATION OF DRIVER     =================================
# ==========================================================================================================
def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os,p_label_log,lock):
    # ======================== INITIALISATION OF DRIVER ================================
    logger.info(
        f"{p_udid}|||============== INITIALISATION OF DRIVER for Smartphone {p_udid} for action FACEBOOK ==========")
    logger.info(f"{p_udid}|||p_udid : {p_udid}")
    logger.info(f"{p_udid}|||p_systemPort : {p_systemPort}")
    logger.info(f"{p_udid}|||p_deviceName : {p_deviceName}")
    logger.info(f"{p_udid}|||p_version : {p_version}")
    logger.info(f"{p_udid}|||p_os : {p_os}")
    logger.info(
        f"{p_udid}|||===============================================================================================")

    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'

    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['appWaitDuration'] = 100000
    desired_caps['newCommandTimeout'] = 0
    desired_caps['wdaStartupRetries'] = 4
    desired_caps['wdaStartupRetryInterval'] = 20000
    desired_caps['uiautomator2ServerLaunchTimeout'] = 100000
    desired_caps['uiautomator2ServerInstallTimeout'] = 100000
    desired_caps['remoteAppsCacheLimit'] = 0
    desired_caps['waitForQuiescence'] = 'false'
    # desired_caps['appWaitPackage'] = 'com.facebook.android'
    # desired_caps['appWaitActivity'] = '.StartActivity'
    desired_caps['appPackage'] = 'com.facebook.katana'
    desired_caps['appActivity'] = 'com.facebook.katana.LoginActivity'
    cpt_appium_start=0
    while True:
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            print(f"desired_caps['appPackage'] : {desired_caps['appPackage']}")
            print(f"desired_caps['appActivity'] : {desired_caps['appActivity']}")
            # driver.update_settings({"normalizeTagNames": True})
            time.sleep(random.uniform(3.5, 5.3))
            return driver

        except Exception as ex:
            cpt_appium_start+=1
            logger.critical(f"{p_udid}|||Something went wrong when initializing driver : {ex}")
            logger.critical(
                f"{p_udid}|||We can't open Facebook. Please check if device is connected. Let's try again!")
            if str(ex).find('hang up')!=-1:
                logger.error("PhoneBot caught the issue exception 'hang up' when initializing Driver!")
                proc = subprocess.Popen(
                    f'adb -s {p_udid} uninstall io.appium.uiautomator2.server',
                    shell=True,
                    stdin=None, stdout=None, stderr=None, close_fds=True)

                proc2 = subprocess.Popen(
                    f'adb -s {p_udid} uninstall io.appium.uiautomator2.server.test',
                    shell=True,
                    stdin=None, stdout=None, stderr=None, close_fds=True)
                proc3 = subprocess.Popen(
                    f'adb -s {p_udid} uninstall io.appium.settings',
                    shell=True,
                    stdin=None, stdout=None, stderr=None, close_fds=True)

            elif str(ex).find('Failed to establish a new connection')!=-1:
                logger.critical(f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")
                logger.critical(
                    f"{p_udid}|||We can't open Facebook. Please check if device is connected. Let's try again!")
                mymodulesteam.DisplayMessageLogUI(p_label_log,
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")

            if cpt_appium_start > 3:
                mymodulesteam.PopupMessage("Error","PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                mymodulesteam.DisplayMessageLogUI(p_label_log,
                                       "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                return None

            time.sleep(random.uniform(2.5, 3.3))
def AreWeInFBHomepage(p_udid, p_driver):
    #
    # first let's check if we are in Facebook home page, otherwise it will close the app if we click on Android back button
    we_are_in_homepage = False
    try:
        logo_facebook = p_driver.find_elements_by_xpath(
            "*//android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ImageView")
        logo_facebook_string = str(mymodulesteam.GetTextfromScreenshot(p_driver, p_udid, logo_facebook[0])).lower()
        logo_facebook_string=logo_facebook_string.strip()
        logo_facebook_string = logo_facebook_string.replace('\n','').replace('\\n','')

        logger.info(f"{p_udid}||| logo_facebook_string : {logo_facebook_string}")
        if logo_facebook_string == 'facebook':
            logger.info(
                f"{p_udid}||| PhoneBot found the logo 'Facebook'. That means we are in homepage. PhoneBot will not go back!")
            we_are_in_homepage = True
        else:
            logger.info(
                f"{p_udid}||| PhoneBot didn't find the logo 'Facebook'. That means we are not in homepage. PhoneBot will go back!")
            we_are_in_homepage = False
    except Exception as ex:
        logger.info(f"PhoneBot didn't found FB logo. So we are not in FB page : {ex}")
        we_are_in_homepage = False

    return we_are_in_homepage


def GoBackButtonFacebook(p_driver, p_udid):
    # first let's check if we are in Facebook home page, otherwise it will close the app if we click on Android back button
    if not AreWeInFBHomepage(p_udid, p_driver):
        cpt = 0
        while True:

            try:
                back_buttons = p_driver.find_elements_by_xpath(
                    "//*[@class='android.widget.ImageView' and contains(@content-desc, 'Retour')]")
                back_buttons[0].click()
                logger.info(f"{p_udid}|||PhoneBot found the French Back button.")
                break
            except:
                logger.info(f"{p_udid}|||PhoneBot didn't find the French Back button.")

                try:
                    back_buttons = p_driver.find_elements_by_xpath(
                        "//*[@class='android.widget.ImageView' and contains(@content-desc, 'Back')]")
                    back_buttons[0].click()
                    logger.info(f"{p_udid}|||PhoneBot found the English Back button.")

                    break
                except:
                    logger.info(f"{p_udid}|||PhoneBot didn't find the English Back button.")

                    logger.info(
                        f"{p_udid}|||PhoneBot didn't find the English & French 'back' button. Let's try the Android back button.")
                    # === ANDROID BACK BUTTON ============================================
                    p_driver.press_keycode(keycode=4)
                    break

    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    time.sleep(random.uniform(0.9, 3.3))



def AreWeFBLoggedIn(p_driver,p_udid):
    """
    This function check if browser is connected to facebook or not and return True with FB username
    or False with None
    """

    logger.info("=============================== AreWeFBLoggedIn() =========================================")

    # INITIALISATION
    fb_username = None
    # ======================= TRY TO GET USERNAME TO SEE IF WE ARE LOGGED IN ====================================
    try:
        profile = p_driver.find_element_by_xpath("//android.view.ViewGroup[contains(@content-desc,'profil')]")
        logger.info(f"{p_udid}|||PhoneBot found your 'See profile' menu.")
        profile.click()
        # logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
        # time.sleep(random.uniform(1.9, 3.3))
        # p_driver.implicitly_wait(10)
        # # === Let's scroll up a bit in case there is a popup
        # mymodulesteam.Scroll_Down(p_driver, p_udid)
        # mymodulesteam.Scroll_Up(p_driver, p_udid)
        # logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
        # time.sleep(random.uniform(0.9, 3.3))
        # p_driver.implicitly_wait(10)
    except Exception as ex:
        logger.info(f"{p_udid}|||PhoneBot didn't find the username. Let's try again! : {ex}")
        return False, None

    try:
        my_username_element = p_driver.find_elements_by_xpath(
            "//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/"
            "android.view.ViewGroup")

        logger.info(f"{p_udid}|||PhoneBot found your profile username.")
        myprofile_username = mymodulesteam.GetTextfromScreenshot(p_driver, p_udid, my_username_element[0])
        myprofile_username = str(myprofile_username).strip()
        print(f"myprofile_username : {myprofile_username}")

        WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//android.widget.ImageView[contains(@content-desc, "Retour") or '
                       'contains(@content-desc, "Return") or contains(@content-desc, "Back")]')
            )).click()
        return True,myprofile_username

    except Exception as ex:
        logger.error(f"||||SMARTPHONE|||{p_udid}|||PhoneBot didn't find username : {ex}")

def AreWeinFBProfilesPage(p_driver,p_udid):
    """
    This function will check if we are in the fb homepage where all the profiles are displayed
    """
    logger.info("=============================== AreWeinFBProfilesPage() =========================================")

    result = False
    profiles = None
    profiles_list = None

    try:
        profiles_list = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//android.widget.ScrollView//android.widget.TextView')
        ))

    except:
        logger.info(f'Fail to find Facebook app profile, phonebot will try to find profile on the Google Vault')
        try:
            profiles_list = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located(
                (By.ID, "com.google.android.gms:id/credential_primary_label")
            ))

        except Exception as e:
            try:
                logger.info(f'Error: {e}')
                WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, '//android.widget.Button[contains(@text, "connect")]')
                )).click()
                p_driver.implicitly_wait(1.5)

                profiles_list = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located(
                    (By.ID, "com.google.android.gms:id/credential_primary_label")
                ))
            except:
                logger.info(f"Couldn't find profiles")

    if profiles_list is not None:
        profiles = []
        for profile in profiles_list:
            profiles.append(profile.text)
        result = True

    return result, profiles

    # try:
    #     list_FB_profiles = []
    #     buttons_account = WebDriverWait(p_driver, 15).until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//android.widget.ScrollView//android.widget.TextView")))
    #     for button_account in buttons_account:
    #         list_FB_profiles.append(button_account.text)
    #     return True, list_FB_profiles
    #
    # except Exception as ex:
    #     logger.error(f"ERROR when clicking on Logout : {ex}")
    #     return False, None

def RunMultiAccountsTask(p_driver,p_udid, p_function, p_taskuser_id,label_log,lock):
    # We need now to execute the task with other FB accounts
    logger.info(f"PhoneBot is NOT logged in Facebook")
    are_we_profiles_FB_pages, list_FB_profiles = AreWeinFBProfilesPage(p_driver,p_udid)

    if are_we_profiles_FB_pages:
        mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Facebook|| PhoneBot found multi accounts page.",
                                      "Black")
        logger.info(f"PhoneBot is in Facebook page list of profiles {list_FB_profiles}")
        # WE WILL RUN THE TASK FOR EACH PROFILE EXCEPT THE ONE WE JUST DID
        for FB_profile in list_FB_profiles:
            logger.info(f"We will start automation on Facebook with profile {FB_profile}.")
            FBLogin(p_driver, FB_profile, p_udid, label_log,lock)
            # === TEST IF WE SUCCESSFULLY LOGGED IN
            are_we_connected_FB, FB_username = AreWeFBLoggedIn(p_driver,p_udid)
            if not are_we_connected_FB:
                logger.error(f"SMARTPHONE|||{p_udid}||Facebook|| PhoneBot couldn't login with profile {FB_profile}!")
                mymodulesteam.DisplayMessageLogUI(label_log,
                                              f"SMARTPHONE|||{p_udid}||Facebook||{FB_profile}| PhoneBot couldn't login with profile {FB_profile}!",
                                              "Red")
            else:
                # ===================================================================================
                # Let's get the quantity of actions possible
                quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, FB_username)
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================

                    result, counter = p_function(p_udid, p_taskuser_id, p_driver, FB_username,
                                                 quantity_actions,label_log, lock)

                    FBLogout(p_driver,p_udid)
                    logger.info(f"Profile {FB_profile} logout of Facebook .")
                    mymodulesteam.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Facebook||{FB_profile}| Profile {FB_profile} logout of Facebook.",
                                                  "Black")
                else:
                    FBLogout(p_driver,p_udid)
                    logger.info(
                        f"Profile {FB_profile} logout of Facebook because he/she did too many actions.")
                    mymodulesteam.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Facebook||{FB_profile}| Profile {FB_profile} logout of Facebook because he/she did too many actions.",
                                                  "Black")

    else:
        logger.info(f"SMARTPHONE|||{p_udid}||Facebook|| PhoneBot didn't found multi accounts page.")
        mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Facebook|| PhoneBot didn't found multi accounts page.",
                                      "Red")


def FBLogout(p_driver,p_udid):
    """
    This method will logout of Facebook
    """
    logger.info("=============================== FBLogout() =========================================")
    while True:
        try:
            # Click on Account menu
            button_menu = p_driver.find_element_by_xpath("//android.view.View[contains(@content-desc,'Menu')]")
            #button_menu.click()
            button_menu.click()
            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            # WE NEED TO SCROLL DOWN AT THE BOTTOM
            mymodules.Scroll_Down(p_driver,p_udid,2)
            # Click on Logout
            try:
                # TRY WITH ENGLISH LABEL
                button_logout = p_driver.find_element_by_xpath("//android.view.ViewGroup[contains(@content-desc,'Log Out') or "
                                                               "contains(@content-desc,'Déconnexion')]")
                button_logout.click()
                time.sleep(random.uniform(2.3, 4.5))
                break
            except Exception as ex:
                logger.error(f"ERROR when clicking on Logout Link in English : {ex}. Let's try in French")
                try:
                    # TRY WITH FRENCH LABEL
                    button_logout = p_driver.find_element_by_xpath(
                        "//android.view.ViewGroup[contains(@content-desc,'Déconnexion')]")
                    button_logout.click()
                    time.sleep(random.uniform(2.4, 4.6))
                    break
                except Exception as ex:
                    logger.error(f"ERROR when clicking on Logout Link in French : {ex}. Let's try to come back to home page")
                    GoBackButtonFacebook(p_driver, p_udid)

        except Exception as ex:
            logger.error(f"ERROR clicking on top right menu : {ex}")
            GoBackButtonFacebook(p_driver, p_udid)


def FBLogin(p_driver, p_profile,p_udid,label_log,lock):
    """
    This method will login to Facebook with a specific profile
    """
    logger.info(f"=============================== FBLogin {p_profile} =========================================")
    try:
        # button_account = WebDriverWait(p_driver, 5).until(
        #     EC.element_to_be_clickable((By.XPATH, f"//android.widget.LinearLayout[@content-desc='{p_profile}']")))
        button_account = WebDriverWait(p_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f'//android.widget.TextView[contains(@text, "{p_profile}")]')))

        logger.info(f"PhoneBot found {p_profile}")
        button_account.click()
        time.sleep(random.uniform(4.3, 5.5))

        try:
            button_account = WebDriverWait(p_driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, f'//android.widget.Button[contains(@text, "OK")]')))

            button_account.click()
        except:
            pass
    except Exception as ex:
        #print(ex.__class__.__name + ': ' + (str(ex)))
        print(type(ex).__name__, ':', str(ex))
        logger.error(f"Error FB_login : {ex}")



def RunFaceBookApp(p_udid, p_function, p_taskuser_id, label_log, lock):

    """
    This method will open Facebook app in smartphone and run the task for all the profiles found in cookies Browser
    It will have to check for the daily & hourly limit
    It will return True if it run some actions, or False if nothing
    :param p_function:
    :param p_taskuser_id:
    :return:
    """
    logger.info(f"""
        p_udid : {p_udid}
        p_function : {p_function}
        p_taskuser_id : {p_taskuser_id}
        label_log : {label_log}
        lock : {lock}
    """)
    # ========================= WE NEED TO GET DETAILS OF SMARTPHONE FOR OPENING DRIVER ==============================
    # ============================== devicename, platformversion, systemPort, OS_device ==============================
    # ===================================== CREATE SQLITE3 CONNECTION ==============================================
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    parameters_smartphone = sqlite_cursor.execute(
        "SELECT devicename, platformversion, systemPort, OS_device FROM smartphones WHERE udid=?",
        (p_udid,)).fetchone()
    logger.info(f"{p_udid}|||parameters_smartphone = {parameters_smartphone}")

    logger.info(f"str(p_udid) : {str(p_udid)}")
    logger.info(f"systemPort : {parameters_smartphone[2]}")
    logger.info(f"devicename : {str(parameters_smartphone[0])}")
    logger.info(f"platformversion : {str(parameters_smartphone[1])}")
    logger.info(f"OS_device : {str(parameters_smartphone[3])}")

    systemPort = parameters_smartphone[2]
    devicename = str(parameters_smartphone[0])
    platformversion = str(parameters_smartphone[1])
    OS_device = str(parameters_smartphone[3])
    driver= ""
    """
    WE NEED HERE TO WRITE THE CODE FOR MULTI ACCOUNT LOGGING AND GET QUANTITY OF TASK
    # ===================================================================================
    # Let's get the quantity of actions possible
    quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, FB_username)
    """

    logger.info(
        f"{p_udid}|||# ======================== [1] INITIALISATION OF DRIVER ================================")
    driver = Initialisation_Driver(p_udid, systemPort, devicename, platformversion, OS_device,label_log,lock)
    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    print(f"driver : {driver}")


    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_FB, FB_username = AreWeFBLoggedIn(driver, p_udid)



    # === IF WE ARE LOGGED IN , WE EXECUTE THE TASK
    if are_we_connected_FB:
        logger.info(f"PhoneBot is logged in Facebook with profile {FB_username}.")
        mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Facebook||{FB_username}| PhoneBot is logged in Facebook with profile {FB_username}.",
                                      "Black")
        # ===================================================================================
        # Let's get the quantity of actions possible
        quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, FB_username)
        cpt=0
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter = p_function(p_udid, p_taskuser_id, driver, FB_username, quantity_actions,label_log,lock)

            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {FB_username} logout of Facebook .")
            mymodulesteam.DisplayMessageLogUI(label_log,
                                          f"SMARTPHONE|||{p_udid}||Facebook||{FB_username}| Profile {FB_username} logout of Facebook.",
                                          "Black")
            FBLogout(driver,p_udid)
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
        else:
            # THis user already reach the limit, We need to logout and loop all the profiles
            logger.info(f"Profile {FB_username} logout of Facebook .")
            FBLogout(driver,p_udid)
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)




    # === ELSE , WE GET LIST OF ACCOUNTS
    else:
        RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)

    return True


def Smartphone_Cold_Messaging_Facebook_Group_Members_3(p_udid,p_taskuser_id,p_driver,FB_username,p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Facebook_Group_Members_3 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    #mymodulesteam.PopupMessage("ACTIONS", f"Facebook user {FB_username} can make {p_quantity_actions} actions now of Cold_Messaging_Facebook_Group_Members_3!")
    mymodulesteam.GoogleSheetAddValues('11jJvq12zM5q0VhkZS3RjttqhlQ61mtBmavkox0symZQ',
                                   [p_udid, p_taskuser_id, 'Smartphone_Cold_Messaging_Facebook_Group_Members_3',
                                    FB_username, p_quantity_actions])
    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    mymodulesteam.DisplayMessageLogUI(label_log,
                                  f"SMARTPHONE|||{p_udid}||{FB_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Facebook_Group_Members_3",
                                  "Black")
    mymodulesteam.PopupMessage("Done", f"SMARTPHONE|||{p_udid}||{FB_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Facebook_Group_Members_3")

"""
label_log=''
lock = threading.Lock()
RunFaceBookApp('A60ProEEA0112572', 'A60Pro_EEA', 250,label_log,lock)
"""