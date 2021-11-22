import subprocess
import random
import sqlite3
import threading
import time

from modules import mymodules
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging



open (mymodules.LoadFile ('log.log'), 'w').close()
logger = logging.getLogger('__Twitter_Smartphone_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)


# ==========================================================================================================
# ==============================     FUNCTION INITIALISATION OF DRIVER     =================================
# ==========================================================================================================

def Initialisation_Driver_Emulator():
    desired_cap = {
        "automationName": 'UiAutomator2',
        #"deviceName": "Android Emulator",
        #"platformName": "Android",
        "deviceName": "sdk_gphone_x86",
        "platformName": "Android",
        "appPackage": "com.twitter.android",
        "appActivity": "com.twitter.android.StartActivity",
        "appWaitDuration": 100000,
        "newCommandTimeout": 0,
        "wdaStartupRetries": 4,
        "wdaStartupRetryInterval": 20000,
        "uiautomator2ServerLaunchTimeout": 100000,
        "uiautomator2ServerInstallTimeout": 100000,
        "remoteAppsCacheLimit": 0,
        "noReset": 'true',
        "waitForQuiescence": 'false',

        # "app": "C:\\Users\\ackaw\\OneDrive\\Documents\\Stage\\stage BSc1\\twitter-9-9-0.apk"
    }
    while True:
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cap)
            print(f"desired_caps['appPackage'] : {desired_cap['appPackage']}")
            print(f"desired_caps['appActivity'] : {desired_cap['appActivity']}")
            # driver.update_settings({"normalizeTagNames": True})
            time.sleep(random.uniform(3.5, 5.3))
            return driver
        except Exception as ex:
            print("driver is return :  None")
            time.sleep(random.uniform(2.5, 3.3))
            return None







def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os,p_label_log,lock):
    # ======================== INITIALISATION OF DRIVER ================================
    logger.info(
        f"{p_udid}|||============== INITIALISATION OF DRIVER for Smartphone {p_udid} for action TWITTER ==========")
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
    # desired_caps['appWaitPackage'] = 'com.facebook.katana'
    # desired_caps['appWaitActivity'] = 'com.facebook.katana.LoginActivity'
    desired_caps['appPackage'] = 'com.twitter.android'
    desired_caps['appActivity'] = 'com.twitter.app.main.MainActivity'
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
                f"{p_udid}|||We can't open Twitter. Please check if device is connected. Let's try again!")
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
                    f"{p_udid}|||We can't open Twitter. Please check if device is connected. Let's try again!")
                mymodules.DisplayMessageLogUI(p_label_log,
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")

            if cpt_appium_start > 3:
                mymodules.PopupMessage("Error", "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                mymodules.DisplayMessageLogUI(p_label_log,
                                       "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                return None

            time.sleep(random.uniform(2.5, 3.3))




def AreWeTWLoggedIn(p_driver, p_udid):
    """
  This function check if browser is connected to facebook or not and return True with TW username
  or False with None
  """
    logger.info("=============================== AreWeTWLoggedIn() =========================================")
    # INITIALISATION
    fb_username = None
    # ======================= TRY TO GET USERNAME TO SEE IF WE ARE LOGGED IN ====================================
    while True or False:
        try:
            try:
                # Click on Account menu
                menu_buttons = p_driver.find_element_by_xpath(
                    "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
                # button_menu.click()
                menu_buttons.click()
                logger.info(f"|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 3.3))
                p_driver.implicitly_wait(10)
            except Exception as ex:
                button_register = p_driver.find_element_by_xpath('//*[@text="CREATE ACCOUNT"]')
                time.sleep(random.uniform(2.3, 4.5))
                logger.error(f"|||PhoneBot didn't find a connected account. Let's try again! : {ex}")
                return False, None
            try:
                myprofile_username = p_driver.find_element_by_id("com.twitter.android:id/username").text
                # myprofile_username = p_driver.find_element_by_xpath('//*[@text]').text
                logger.info(f"myprofile_username : {myprofile_username}")
                GoBackButtonTwitter(p_driver, p_udid)
                return True, myprofile_username
            except Exception as ex:
                logger.error(f"||||SMARTPHONE||||||PhoneBot didn't find username : {ex}")
                return False, None
        except Exception as ex:
            logger.error(f"|||PhoneBot didn't find the profil menu. Let's try again! : {ex}")
            GoBackButtonTwitter(p_driver, p_udid)



def AreWeinTWProfilesPage(p_driver, p_udid):
    """
  This function will check if we are in the fb homepage where all the profiles are displayed
  """
    logger.info("=============================== AreWeinTWProfilesPage() =========================================")
    while True:
        try:
            try:
                # Click on Account menu
                p_driver.find_element_by_id("com.twitter.android:id/drawer").find_element_by_xpath('//*[@displayed="true"]')
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(1, 2))
            except Exception as ex:
                # Click on Account menu
                menu_buttons = p_driver.find_element_by_xpath(
                    "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
                menu_buttons.click()
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(1, 2))
            try:
                # Click on Account menu
                switch_accounts = p_driver.find_element_by_xpath(
                    "//android.widget.ImageView[@content-desc='Switch accounts']")
                switch_accounts.click()
                logger.info(f"|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 3.3))
                p_driver.implicitly_wait(10)
                try:
                    list_TW_profiles = []
                    buttons_account = WebDriverWait(p_driver, 15).until(
                        EC.presence_of_all_elements_located((By.ID, "com.twitter.android:id/username")))
                    for button_account in buttons_account:
                        list_TW_profiles.append(button_account.text)
                        '''resultat = [x for x in list_TW_profiles if x.startswith('@')]
                        list_TW_profiles = resultat'''
                    logger.info(list_TW_profiles)
                    GoBackButtonTwitter(p_driver, p_udid)
                    return True, list_TW_profiles
                except Exception as ex:
                    logger.error(f"ERROR when clicking on Profil list : {ex}")
                    return False, None
            except Exception as ex:
                logger.error(f"|||PhoneBot didn't find the list of accounts. Let's try again ! : {ex}")
                return False, None
        except Exception as ex:
            logger.error(f"ERROR clicking on top left menu : {ex}")
            GoBackButtonTwitter(p_driver, p_udid)


def AreWeInTWHomepage(p_udid, p_driver):
    #
    # first let's check if we are in Twitter home page, otherwise it will close the app if we click on Android back button
    we_are_in_homepage = False
    while True or False:
        try:
            p_driver.find_element_by_xpath(
                "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
            logger.info(f"PhoneBot found TW profil. So we are connected ")
            try:
                p_driver.find_element_by_id("com.twitter.android:id/channels").find_element_by_xpath('//*[@selected="true"]')
                logger.info(f"PhoneBot found Icon Home. So we are connected ")
                try:
                    p_driver.find_element_by_id("com.twitter.android:id/drawer").find_element_by_xpath(
                        '//*[@displayed="false"]')
                    we_are_in_homepage = True
                except Exception as ex:
                    logger.error(f"PhoneBot did found a windows opened. So we are not in TW Homepage ")
                    we_are_in_homepage = False
                    return we_are_in_homepage
            except Exception as ex:
                logger.error(f"PhoneBot didn't Icon Home. So we are not in TW Homepage : {ex}")
                we_are_in_homepage = False
                return we_are_in_homepage
        except Exception as ex:
            logger.error(f"PhoneBot didn't found TW profil. So we are not in TW Homepage : {ex}")
            we_are_in_homepage = False
        return we_are_in_homepage



def TWLogin(p_driver, p_profile, p_udid, label_log,lock):
    """
    This method will login to Twitter with a specific profile
    """

    logger.info(f"=============================== FBLogin {p_profile} =========================================")

    while True:
        try:
            try:
                # Click on Account menu
                p_driver.find_element_by_xpath(
                    "//android.widget.ImageView[@content-desc='Switch accounts']")
                logger.info(f"|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 3.3))
                p_driver.implicitly_wait(10)
            except Exception as ex:
                # Click on Account menu
                menu_buttons = p_driver.find_element_by_xpath(
                    "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
                # button_menu.click()
                menu_buttons.click()
                logger.info(f"|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 3.3))
                p_driver.implicitly_wait(10)
            try:
                # Click on Account menu
                switch_accounts = p_driver.find_element_by_xpath(
                    "//android.widget.ImageView[@content-desc='Switch accounts']")
                switch_accounts.click()
                logger.info(f"|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 3.3))
                p_driver.implicitly_wait(10)
                try:
                    '''button_account = WebDriverWait(p_driver, 15).until(
                      EC.element_to_be_clickable(
                        (By.ID, f"com.twitter.android:id/username[@text='{p_profile}']")))'''
                    myprofile_username = p_driver.find_element_by_id("com.twitter.android:id/username").text
                    if (myprofile_username != p_profile):
                        button_account = p_driver.find_element_by_xpath(f'//*[@text="{p_profile}"]')
                        logger.info(f"PhoneBot found {p_profile}")
                        button_account.click()
                        time.sleep(random.uniform(4.3, 5.5))
                        logger.info(f"PhoneBot changed accounts to this profile : {p_profile}")
                        return True
                    else:
                        logger.info(f"this profile : {p_profile} is already logged in")
                        print(f"this profile : {p_profile} is already logged in")
                        time.sleep(random.uniform(1.1, 2.2))
                        GoBackButtonTwitter(p_driver, p_udid)
                        time.sleep(random.uniform(1.5, 2.5))
                        break
                except Exception as ex:
                    # print(ex.__class__.__name + ': ' + (str(ex)))
                    print(type(ex).__name__, ':', str(ex))
                    logger.error(f"|||PhoneBot didn't find a account. Let's try again ! : {ex}")
            except Exception as ex:
                logger.error(f"|||PhoneBot didn't find the list of accounts. Let's try again ! : {ex}")
                print(type(ex).__name__, ':', str(ex))
        except Exception as ex:
            logger.error(f"|||PhoneBot didn't find the profil menu. Let's try again! : {ex}")
            print(type(ex).__name__, ':', str(ex))
            GoBackButtonTwitter(p_driver, p_udid)


def GoBackButtonTwitter(p_driver, p_udid):
    # first let's check if we are in Twitter home page
    if not AreWeInTWHomepage(p_udid, p_driver):
        cpt = 0
        while True:
            try:
                #back_button = p_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up')
                #back_button = p_driver.find_elements_by_xpath('//*[@content-desc="Navigate up]')
                back_button = p_driver.find_elements_by_accessibility_id("Navigate up")
                back_button[0].click()
                print(f"{p_udid}|||PhoneBot found the Back button.")
                logger.info(f"{p_udid}|||PhoneBot found the Back button.")
                break
            except:
                try:
                    close_windows = p_driver.find_element_by_xpath(
                        '//android.widget.ImageButton[@content-desc="New Tweet"]')
                    close_windows.click()
                    logger.info(f"{p_udid}|||PhoneBot found the Close Windows button.")
                    break
                except:
                    logger.info(f"{p_udid}|||PhoneBot didn't find the Back button. Let's try the Android back button.")
                    # === ANDROID BACK BUTTON ============================================
                    #p_driver.press_keycode(keycode=4)
                    break
    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    time.sleep(random.uniform(0.9, 3.3))



def RunMultiAccountsTask(p_driver,p_udid, p_function, p_taskuser_id,label_log,lock):
    # We need now to execute the task with other TW accounts
    logger.info(f"PhoneBot is NOT logged in Twitter")
    are_we_profiles_TW_pages, list_TW_profiles = AreWeinTWProfilesPage(p_driver,p_udid)

    if are_we_profiles_TW_pages:
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Twitter|| PhoneBot found multi accounts page.",
                                      "Black")
        print(f"PhoneBot is in Twitter page list of profiles {list_TW_profiles}")
        logger.info(f"PhoneBot is in Twitter page list of profiles {list_TW_profiles}")
        # WE WILL RUN THE TASK FOR EACH PROFILE EXCEPT THE ONE WE JUST DID
        for TW_profile in list_TW_profiles:
            logger.info(f"We will start automation on Twitter with profile {TW_profile}.")
            TWLogin(p_driver, TW_profile, p_udid, label_log,lock)
            # === TEST IF WE SUCCESSFULLY LOGGED IN
            are_we_connected_TW, TW_username = AreWeTWLoggedIn(p_driver,p_udid)
            if not are_we_connected_TW:
                logger.error(f"SMARTPHONE|||{p_udid}||Twitter|| PhoneBot couldn't login with profile {TW_profile}!")
                mymodules.DisplayMessageLogUI(label_log,
                                              f"SMARTPHONE|||{p_udid}||Twitter||{TW_profile}| PhoneBot couldn't login with profile {TW_profile}!",
                                              "Red")
            else:
                # ===================================================================================
                # Let's get the quantity of actions possible
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, TW_username)
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================

                    #p_function(p_udid, p_taskuser_id, p_driver, TW_username, quantity_actions,label_log,lock)
                    p_function()

                    #TWLogout(p_driver,p_udid)
                    logger.info(f"Profile {TW_profile} logout of Twitter .")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Twitter||{TW_profile}| Profile {TW_profile} logout of Twitter.",
                                                  "Black")
                else:
                    TWLogout(p_driver,p_udid)
                    logger.info(f"Profile {TW_profile} logout of Twitter because he/she did too many actions.")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Twitter||{TW_profile}| Profile {TW_profile} logout of Twitter because he/she did too many actions.",
                                                  "Black")

    else:
        logger.info(f"SMARTPHONE|||{p_udid}||Twitter|| PhoneBot didn't found multi accounts page.")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Twitter|| PhoneBot didn't found multi accounts page.",
                                      "Red")







def RunTwitterApp(p_udid, modele, os, os_version, p_function, p_taskuser_id,label_log,lock):
    """
    This method will open Twitter app in smartphone and run the task for all the profiles found in cookies Browser
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
    sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    parameters_smartphone = sqlite_cursor.execute(
        "SELECT devicename, platformversion, systemPort, OS_device FROM smartphones WHERE udid=?",
        (p_udid,)).fetchone()
    '''logger.info(f"{p_udid}|||parameters_smartphone = {parameters_smartphone}")

    logger.info(f"str(p_udid) : {str(p_udid)}")
    logger.info(f"systemPort : {parameters_smartphone[2]}")
    logger.info(f"devicename : {str(parameters_smartphone[0])}")
    logger.info(f"platformversion : {str(parameters_smartphone[1])}")
    logger.info(f"OS_device : {str(parameters_smartphone[3])}")

    systemPort = parameters_smartphone[2]
    devicename = str(parameters_smartphone[0])
    platformversion = str(parameters_smartphone[1])
    OS_device = str(parameters_smartphone[3])'''
    driver = ""
    """
    WE NEED HERE TO WRITE THE CODE FOR MULTI ACCOUNT LOGGING AND GET QUANTITY OF TASK
    # ===================================================================================
    # Let's get the quantity of actions possible
    quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, FB_username)
    """

    logger.info(
        f"{p_udid}|||# ======================== [1] INITIALISATION OF DRIVER ================================")
    #driver = Initialisation_Driver(p_udid, systemPort, devicename, platformversion, OS_device, label_log, lock)
    driver = Initialisation_Driver_Emulator()
    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    print(f"driver : {driver}")

    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_TW, TW_username = AreWeTWLoggedIn(driver, p_udid)

    # === IF WE ARE LOGGED IN , WE EXECUTE THE TASK
    if are_we_connected_TW:
        logger.info(f"PhoneBot is logged in Twitter with profile {TW_username}.")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Twitter||{TW_username}| PhoneBot is logged in Twitter with profile {TW_username}.",
                                      "Black")
        # ===================================================================================
        # Let's get the quantity of actions possible
        quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, TW_username)
        cpt = 0
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            #p_function(p_udid, p_taskuser_id, driver, TW_username, quantity_actions, label_log, lock)
            p_function()

            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {TW_username} logout of Twitter .")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"SMARTPHONE|||{p_udid}||Twitter||{TW_username}| Profile {TW_username} logout of Twitter.",
                                          "Black")
            #TWLogout(driver, p_udid)
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
        else:
            # THis user already reach the limit, We need to logout and loop all the profiles
            logger.info(f"Profile {TW_username} logout of Twitter .")
            TWLogout(driver, p_udid)
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
    # === ELSE , WE GET LIST OF ACCOUNTS
    else:
        RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
    return True



def TWLogout(p_driver, p_udid):
        """
        This method will logout of Twitter
        """
        logger.info("=============================== TWLogout() =========================================")
        while True:
            try:
                try:
                    button_setting = p_driver.find_element_by_xpath('//*[@text="Settings and privacy"]')
                    time.sleep(random.uniform(2.3, 4.5))
                except Exception as ex:
                    logger.error(f"ERROR when clicking on setting Link : {ex}")
                    # Click on Account menu
                    menu_buttons = p_driver.find_elements_by_xpath(
                        "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
                    # button_menu.click()
                    menu_buttons[0].click()
                    p_driver.implicitly_wait(10)
                    time.sleep(random.uniform(1, 2))
                    # WE NEED TO SCROLL DOWN AT THE BOTTOM
                    # mymodules.Scroll_Down(p_driver, p_udid, 2)
                try:
                    button_setting = p_driver.find_element_by_xpath('//*[@text="Settings and privacy"]')
                    button_setting.click()
                    time.sleep(random.uniform(2.3, 4.5))
                    try:
                        button_account = p_driver.find_element_by_xpath('//*[@text="Account"]')
                        button_account.click()
                        time.sleep(random.uniform(2.3, 4.5))
                        try:
                            # WE NEED TO SCROLL DOWN AT THE BOTTOM
                            mymodules.Scroll_Down(p_driver, p_udid, 1)
                            # Click on Logout
                            button_logout = p_driver.find_element_by_xpath('//*[@text="Log out"]')
                            button_logout.click()
                            time.sleep(random.uniform(2.3, 4.5))
                            try:
                                # Click on Logout
                                button_conf_logout = p_driver.find_element_by_xpath('//*[@text="OK"]')
                                button_conf_logout.click()
                                time.sleep(random.uniform(2.3, 4.5))
                                break
                            except Exception as ex:
                                logger.error(f"ERROR when clicking for confirm logout : {ex}")
                        except Exception as ex:
                            logger.error(f"ERROR when clicking on logout Link : {ex}")
                    except Exception as ex:
                        logger.error(f"ERROR when clicking on account Link : {ex}")
                except Exception as ex:
                    logger.error(f"ERROR when clicking on setting Link : {ex}")

            except Exception as ex:
                logger.error(f"ERROR clicking on top right menu : {ex}")
                GoBackButtonTwitter(p_driver, p_udid)


def Smartphone_Cold_Messaging_Twitter_Group_Members_3(p_udid,p_taskuser_id,p_driver,TW_username,p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Twitter_Group_Members_3 {p_taskuser_id} - {TW_username} - {p_quantity_actions} =======================")
    #mymodules.PopupMessage("ACTIONS", f"Twitter user {TW_username} can make {p_quantity_actions} actions now of Cold_Messaging_Twitter_Group_Members_3!")
    mymodules.GoogleSheetAddValues('11jJvq12zM5q0VhkZS3RjttqhlQ61mtBmavkox0symZQ',
                                   [p_udid, p_taskuser_id, 'Smartphone_Cold_Messaging_Twitter_Group_Members_3',
                                    TW_username, p_quantity_actions])
    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodules.GetDetailsTaskUser(p_taskuser_id)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"SMARTPHONE|||{p_udid}||{TW_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Twitter_Group_Members_3",
                                  "Black")
    mymodules.PopupMessage("Done", f"SMARTPHONE|||{p_udid}||{TW_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Twitter_Group_Members_3")





label_log=''
lock = threading.Lock()
p_udid = 'EMULATOR30X8X4X0'
modele = 'sdk_gphone_x86'
p_os= 'Android'
p_os_version = '11'
p_taskuser_id = 250

def afficheMessage ():
    print("executer p_function")

def test(p_driver):
    button_tout = p_driver.find_element_by_xpath('//android.widget.LinearLayout[@content-desc="Search and Explore"]')
    button_tout.click()
    p_driver.implicitly_wait(10)
    '''menu_buttons = p_driver.find_elements_by_xpath(
        "//android.widget.ImageButton[@content-desc='Show navigation drawer']")
    # button_menu.click()
    menu_buttons[0].click()
    p_driver.implicitly_wait(10)
    button_setting = p_driver.find_element_by_xpath('//*[@text="Settings and privacy"]')
    button_setting.click()
    time.sleep(random.uniform(2.3, 4.5))'''
    #button_tout = p_driver.find_element_by_xpath('//android.widget.LinearLayout[@content-desc="Search and Explore"]' )
    """button_account = p_driver.find_element_by_xpath('//*[@text="Account"]')
    button_account.click()
    time.sleep(random.uniform(2.3, 4.5))"""

def test2(p_udid):
    driver = Initialisation_Driver_Emulator()
    test(driver)
    AreWeInTWHomepage(p_udid, driver)




RunTwitterApp(p_udid, modele, p_os, p_os_version, afficheMessage, p_taskuser_id,label_log,lock)
"RunMultiAccountsTask(Initialisation_Driver_Emulator(), p_udid, afficheMessage, p_taskuser_id, label_log, lock)"


