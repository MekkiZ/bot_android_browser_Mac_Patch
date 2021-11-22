import subprocess
import random
import sqlite3
import time
from appium.webdriver.common.touch_action import TouchAction
from modules import mymodules
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import logging


open (mymodules.LoadFile ('log.log'), 'w').close()
logger = logging.getLogger('__Instagram_Smartphone_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)


# ==========================================================================================================
# ==============================     FUNCTION INITIALISATION OF DRIVER     =================================
# ==========================================================================================================

def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os,p_label_log,lock):
    # ======================== INITIALISATION OF DRIVER ================================
    logger.info(
        f"{p_udid}|||============== INITIALISATION OF DRIVER for Smartphone {p_udid} for action INSTAGRAM ==========")
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
    desired_caps['appPackage'] = 'com.instagram.android'
    desired_caps['appActivity'] = 'com.instagram.android.activity.MainTabActivity'
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
                f"{p_udid}|||We can't open Instagram. Please check if device is connected. Let's try again!")
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
                    f"{p_udid}|||We can't open Instagram. Please check if device is connected. Let's try again!")
                mymodules.DisplayMessageLogUI(p_label_log,
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")

            if cpt_appium_start > 3:
                mymodules.PopupMessage("Error","PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                mymodules.DisplayMessageLogUI(p_label_log,
                                       "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                return None

            time.sleep(random.uniform(2.5, 3.3))



def AreWeInIGHomepage(p_udid, p_driver):
    #
    # first let's check if we are in instagram home page, otherwise it will close the app if we click on Android back button
    we_are_in_homepage = False
    while True or False:
        try:
            p_driver.find_element_by_id("com.instagram.android:id/tab_avatar")
            print(f"PhoneBot found IG profil. So we are connected ")
            try:
                p_driver.find_elements_by_accessibility_id("Faire défiler vers le haut")
                print(f"PhoneBot found IG logo. So we are in IG Homepage ")
                we_are_in_homepage = True
            except Exception as ex:
                print(f"PhoneBot didn't found IG logo. So we are not in IG Homepage : {ex}")
                we_are_in_homepage = False
            try:
                p_driver.find_elements_by_accessibility_id("Scroll Up")
                print(f"PhoneBot found IG logo. So we are in IG Homepage ")
                we_are_in_homepage = True
            except Exception as ex:
                print(f"PhoneBot didn't found IG logo. So we are not in IG Homepage : {ex}")
                we_are_in_homepage = False
        except Exception as ex:
            print(f"PhoneBot didn't found IG profil. So we are not in IG Homepage : {ex}")
            we_are_in_homepage = False
        return we_are_in_homepage




def GoBackButtonInstagram(p_driver, p_udid):
    # first let's check if we are in Instagram home page, otherwise it will close the app if we click on Android back button
    if not AreWeInIGHomepage(p_udid, p_driver):
        cpt = 0
        while True:
            try:
                back_button = p_driver.find_elements_by_accessibility_id("Faire défiler vers le haut")
                back_button[0].click()
                print(f"{p_udid}|||PhoneBot found the French Back button.")
                logger.info(f"{p_udid}|||PhoneBot found the French Back button.")
                break
            except:
                logger.info(f"{p_udid}|||PhoneBot didn't find the French Back button.")
            try:
                back_button = p_driver.find_elements_by_accessibility_id("Scroll Up")
                back_button.click()
                print(f"{p_udid}|||PhoneBot found the English Back button.")
                logger.info(f"{p_udid}|||PhoneBot found the English Back button.")
                break
            except:
                logger.info(f"{p_udid}|||PhoneBot didn't find the Back button.")
                break

    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    time.sleep(random.uniform(0.9, 3.3))





def AreWeIGLoggedIn(p_driver, p_udid):
    """
    This function check if browser is connected to facebook or not and return True with TW username
    or False with None
    """

    logger.info("=============================== AreWeTWLoggedIn() =========================================")

    # INITIALISATION
    ig_username = None
    # ======================= TRY TO GET USERNAME TO SEE IF WE ARE LOGGED IN ====================================
    try:
        # Click on Account menu
        menu_buttons = p_driver.find_element_by_id("com.instagram.android:id/tab_avatar")
        menu_buttons.click()
        logger.info(f" {p_udid} |||The bot will sleep just a few seconds..............................")
        time.sleep(random.uniform(0.9, 3.3))
        p_driver.implicitly_wait(10)
        try:
            myprofile_username = p_driver.find_element_by_id("com.instagram.android:id/action_bar_large_title_auto_size").text
            logger.info(f" {p_udid} myprofile_username : {myprofile_username}")
            return True, myprofile_username

        except Exception as ex:
            logger.error(f" {p_udid} ||||SMARTPHONE||||||PhoneBot didn't find username : {ex}")
            return False, None

    except Exception as ex:
        logger.error(f" {p_udid} |||PhoneBot didn't find the profil menu. Let's try again! : {ex}")
        return False, None



def AreWeinIGProfilesPage(p_driver, p_udid):
    """
    This function will check if we are in the ig homepage where all the profiles are displayed
    """
    logger.info("=============================== AreWeinIGProfilesPage() =========================================")
    while True:
        try:
            accounts = p_driver.find_element_by_id("com.instagram.android:id/tab_avatar")
            actions = TouchAction(p_driver)
            actions.long_press(accounts)
            actions.perform()
            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            try:
                list_IG_profiles = []
                buttons_account = WebDriverWait(p_driver, 15).until(
                    EC.presence_of_all_elements_located((By.ID, "com.instagram.android:id/row_user_textview")))
                for account_name in buttons_account:
                    list_IG_profiles.append(account_name.text)
                    print(list_IG_profiles)
                    return True, list_IG_profiles
            except Exception as ex:
                logger.error(f"ERROR when clicking on Profil list : {ex}")
                return False, None
        except Exception as ex:
            logger.error(f"|||PhoneBot didn't find the list of accounts. Let's try again ! : {ex}")
            return False, None






def IGLogin(p_driver, p_profile,p_udid,label_log,lock):
    """
    This method will login to Instagram with a specific profile
    """
    logger.info(f"=============================== IGLogin {p_profile} =========================================")
    try:
        accounts = p_driver.find_element_by_id("com.instagram.android:id/tab_avatar")
        actions = TouchAction(p_driver)
        actions.long_press(accounts)
        actions.perform()
        p_driver.implicitly_wait(10)
        time.sleep(random.uniform(1, 2))
        button_account = p_driver.find_element_by_xpath(f'//*[@text="{p_profile}"]')
        print((f"PhoneBot found {p_profile}"))
        button_account.click()
        time.sleep(random.uniform(4.3, 5.5))
    except Exception as ex:
        logger.error(f"|||PhoneBot didn't find an account. Let's try again ! : {ex}")
        return False, None


def RunMultiAccountsTask(p_driver,p_udid, p_function, p_taskuser_id,label_log,lock):
    # We need now to execute the task with other IG accounts
    logger.info(f"PhoneBot is NOT logged in Instagram")
    are_we_profiles_IG_pages, list_IG_profiles = AreWeinIGProfilesPage(p_driver,p_udid)

    if are_we_profiles_IG_pages:
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Instagram|| PhoneBot found multi accounts page.",
                                      "Black")
        logger.info(f"PhoneBot is in Instagram page list of profiles {list_IG_profiles}")
        # WE WILL RUN THE TASK FOR EACH PROFILE EXCEPT THE ONE WE JUST DID
        for IG_profile in list_IG_profiles:
            logger.info(f"We will start automation on Instagram with profile {IG_profile}.")
            IGLogin(p_driver, IG_profile, p_udid, label_log,lock)
            # === TEST IF WE SUCCESSFULLY LOGGED IN
            are_we_connected_IG, IG_username = AreWeIGLoggedIn(p_driver,p_udid)
            if not are_we_connected_IG:
                logger.error(f"SMARTPHONE|||{p_udid}||Instagram|| PhoneBot couldn't login with profile {IG_profile}!")
                mymodules.DisplayMessageLogUI(label_log,
                                              f"SMARTPHONE|||{p_udid}||Instagram||{IG_profile}| PhoneBot couldn't login with profile {IG_profile}!",
                                              "Red")
            else:
                # ===================================================================================
                # Let's get the quantity of actions possible
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, IG_username)
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================


                    result, counter = p_function(p_udid, p_taskuser_id, p_driver, IG_username, quantity_actions,label_log,lock)

                    logger.info(f"Profile {IG_profile} is done.")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Instagram||{IG_profile}| Profile {IG_profile} is done.",
                                                  "Black")
                else:
                    logger.info(
                        f"Profile {IG_profile} you must wait, he/she did too many actions.")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"SMARTPHONE|||{p_udid}||Instagram||{IG_profile}| Profile {IG_profile} you must wait, he/she did too many actions.",
                                                  "Black")

    else:
        logger.info(f"SMARTPHONE|||{p_udid}||Instagram|| PhoneBot didn't found multi accounts page.")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Instagram|| PhoneBot didn't found multi accounts page.",
                                      "Red")
    return result, counter


def RunInstagramApp(p_udid, p_function, p_taskuser_id, label_log, lock):
    """
    This method will open Instagram app in smartphone and run the task for all the profiles found in cookies Browser
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
    driver = ""
    """
    WE NEED HERE TO WRITE THE CODE FOR MULTI ACCOUNT LOGGING AND GET QUANTITY OF TASK
    # ===================================================================================
    # Let's get the quantity of actions possible
    quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, FB_username)
    """

    logger.info(
        f"{p_udid}|||# ======================== [1] INITIALISATION OF DRIVER ================================")
    driver = Initialisation_Driver(p_udid, systemPort, devicename, platformversion, OS_device, label_log, lock)
    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
    print(f"driver : {driver}")

    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_IG, IG_username = AreWeIGLoggedIn(driver, p_udid)

    # === IF WE ARE LOGGED IN , WE EXECUTE THE TASK
    if are_we_connected_IG:
        logger.info(f"PhoneBot is logged in Facebook with profile {IG_username}.")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE|||{p_udid}||Facebook||{IG_username}| PhoneBot is logged in Instagram with profile {IG_username}.",
                                      "Black")
        # ===================================================================================
        # Let's get the quantity of actions possible
        quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, IG_username)
        cpt = 0
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            p_function(p_udid, p_taskuser_id, driver, IG_username, quantity_actions, label_log, lock)

            # AT THE END OF THE TASK, TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {IG_username} already reach the limit, let's try with an other account.")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"SMARTPHONE|||{p_udid}||Facebook||{IG_username}| Profile {IG_username} logout of Facebook.",
                                          "Black")
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
        else:
            # THis user already reach the limit.
            logger.info(f"Profile {IG_username} already reach the limit .")
            RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)
    # === ELSE , WE GET LIST OF ACCOUNTS
    else:
        RunMultiAccountsTask(driver, p_udid, p_function, p_taskuser_id, label_log, lock)

    return True



def Smartphone_Cold_Messaging_Instagram_Group_Members_3(p_udid,p_taskuser_id,p_driver,IG_username,p_quantity_actions,label_log,lock):
    logger.info(f"=================== Cold_Messaging_Twitter_Group_Members_3 {p_taskuser_id} - {IG_username} - {p_quantity_actions} =======================")
    #mymodules.PopupMessage("ACTIONS", f"Twitter user {TW_username} can make {p_quantity_actions} actions now of Cold_Messaging_Twitter_Group_Members_3!")
    mymodules.GoogleSheetAddValues('11jJvq12zM5q0VhkZS3RjttqhlQ61mtBmavkox0symZQ',
                                   [p_udid, p_taskuser_id, 'Smartphone_Cold_Messaging_Instagram_Group_Members_3',
                                    IG_username, p_quantity_actions])
    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodules.GetDetailsTaskUser(p_taskuser_id)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"SMARTPHONE|||{p_udid}||{IG_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Instagram_Group_Members_3",
                                  "Black")
    mymodules.PopupMessage("Done", f"SMARTPHONE|||{p_udid}||{IG_username}| PhoneBot finished the automation Smartphone_Cold_Messaging_Instagram_Group_Members_3")
