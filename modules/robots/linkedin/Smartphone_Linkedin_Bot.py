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
        "deviceName": "Android Emulator",
        "platformName": "Android",
        #"deviceName": "sdk_gphone_x86_64",
        #"platformName": "Android",
        "appPackage": "com.linkedin.android",
        "appActivity": "com.linkedin.android.authenticator.LaunchActivity",
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


def AreWeInLKHomepage(p_udid, p_driver):
    #
    # first let's check if we are in Linkedin home page, otherwise it will close the app if we click on Android back button
    we_are_in_homepage = False
    while True or False:
        try:
            p_driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="My Profile and Communities"]')
            logger.info(f"PhoneBot found LK profil. So we are connected ")
            try:
                p_driver.find_element_by_id("com.linkedin.android:id/tab_feed").find_element_by_xpath('//*[@selected="true"]')
                logger.info(f"PhoneBot found Icon Home. So we are connected ")
                try:
                    p_driver.find_element_by_id("com.linkedin.android:id/home_drawer_frame").find_element_by_xpath(
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


def AreWeinLKProfilesPage(p_driver, p_udid):
    """
  This function will check if we are in the lk homepage where all the profiles are displayed
  """
    logger.info("=============================== AreWeinLKProfilesPage() =========================================")
    while True:
                try:
                    list_TW_profiles = []
                    buttons_account = WebDriverWait(p_driver, 15).until(
                        EC.presence_of_all_elements_located((By.ID, "com.google.android.gms:id/account_display_name")))
                    for button_account in buttons_account:
                        list_TW_profiles.append(button_account.text)
                        '''resultat = [x for x in list_TW_profiles if x.startswith('@')]
                        list_TW_profiles = resultat'''
                    logger.info(list_TW_profiles)
                    print(list_TW_profiles)
                    return True, list_TW_profiles
                except Exception as ex:
                    try:
                        login = p_driver.find_element_by_id("com.linkedin.android:id/growth_prereg_fragment_join_with_google_button")
                        login.click()
                        logger.info(f"PhoneBot found a login button.")
                        p_driver.implicitly_wait(10)
                        time.sleep(random.uniform(1, 2))
                        try:
                            list_TW_profiles = []
                            buttons_account = WebDriverWait(p_driver, 15).until(
                                EC.presence_of_all_elements_located(
                                    (By.ID, "com.google.android.gms:id/account_display_name")))
                            for button_account in buttons_account:
                                list_TW_profiles.append(button_account.text)
                                '''resultat = [x for x in list_TW_profiles if x.startswith('@')]
                                list_TW_profiles = resultat'''
                            logger.info(list_TW_profiles)
                            print(list_TW_profiles)
                            return True, list_TW_profiles
                        except:
                            logger.error(f"PhoneBot did found a list profiles.")
                            return False, None
                    except Exception as ex:
                        logger.error(f"PhoneBot did found a windows opened. So we are not in TW Homepage ")
                        return False, None





def TWLogin(p_driver, p_profile, p_udid, label_log,lock):
    """
    This method will login to Twitter with a specific profile
    """

    logger.info(f"=============================== FBLogin {p_profile} =========================================")

    while True:
        try:
            try:
                # Click on Account menu
                button_account = p_driver.find_element_by_xpath(f'//*[@text="{p_profile}"]')
                logger.info(f"PhoneBot found {p_profile}")
                button_account.click()
                time.sleep(random.uniform(4.3, 5.5))
                logger.info(f"PhoneBot changed accounts to this profile : {p_profile}")
            except Exception as ex:
                try:
                    sign_button = p_driver.find_element_by_id(
                        "com.linkedin.android:id/growth_prereg_fragment_login_button")
                    sign_button.click()
                    logger.info(f"|||The bot will sleep just a few seconds..............................")
                    time.sleep(random.uniform(0.9, 3.3))
                    p_driver.implicitly_wait(10)
                except Exception as ex:
                    logger.error(f"|||PhoneBot didn't find the sign button. Let's try again ! : {ex}")
                    print(type(ex).__name__, ':', str(ex))



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




label_log=''
lock = threading.Lock()
p_udid = 'EMULATOR30X8X4X0'
modele = 'sdk_gphone_x86'
p_os= 'Android'
p_os_version = '11'
p_taskuser_id = 250

def test(p_udid):
    driver = Initialisation_Driver_Emulator()
    AreWeinLKProfilesPage(driver, p_udid)



test(p_udid)