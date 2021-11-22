            # ============================================================================== #
            #                                                                                #
            #                    Developer : Imad RAFAI                                      #
            #       Contact :                                                                #
            #                   WTSP : +33 7 53 16 48 12                                     #
            #                   Mail : imad.rafai@yahoo.com                                  #
            #                   FB.com/iimadrafaii                                           #
            #                   LINKEDIN.com/in/rafaiimad                                    #
            # ============================================================================== #

from datetime import datetime
import logging
import threading
import time
import sqlite3
import random
from mymodulesteam import LoadFile
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


open(LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Smartphone_Scrap_Craigslist_Ads__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
)
file_handler = logging.FileHandler(LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

            # ==============================================================================#
            #                                                                               #
            #                   Initializing Appium and launching driver                    #
            #                                                                               #
            # ==============================================================================#
def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock):
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
    desired_caps['appActivity'] = 'com.instagram.mainactivity.LauncherActivity'
    cpt_appium_start = 0
    while True:
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            time.sleep(random.uniform(3.5, 5.3))
            return driver

        except Exception as ex:
            cpt_appium_start += 1
            logger.critical(f"{p_udid}|||Something went wrong when initializing driver : {ex}")
            logger.critical(
                f"{p_udid}|||We can't open Instagram. Please check if device is connected. Let's try again!")
            if str(ex).find('hang up') != -1:
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

            elif str(ex).find('Failed to establish a new connection') != -1:
                logger.critical(
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")
                logger.critical(
                    f"{p_udid}|||We can't open Facebook. Please check if device is connected. Let's try again!")
                mymodules.DisplayMessageLogUI(p_label_log,
                                              f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")

            if cpt_appium_start > 3:
                mymodules.PopupMessage("Error",
                                       "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                mymodules.DisplayMessageLogUI(p_label_log,
                                              "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                return None

            time.sleep(random.uniform(2.5, 3.3))

            # ==============================================================================#
            #                                                                               #
            #                    Shortcut to find an element via XPATH                      #
            #                                                                               #
            # ==============================================================================#

def findOneByXPath(xpath,time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, (xpath))))

            # ==============================================================================#
            #                                                                               #
            #                    Shortcut to find all elements via XPATH                    #
            #                                                                               #
            # ==============================================================================#

def findAllByXPath(xpath,time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, (xpath))))
    # ==============================================================================#
    #                                                                               #
    #                    Shortcut to find an element via ID                         #
    #                                                                               #
    # ==============================================================================#

def checkExistsByXpath(xpath):
    try:
        element = findOneByXPath(xpath)
    except Exception:
        return False
    return element

def checkAllExistByXpath(xpath):
    try:
        elements = findAllByXPath(xpath)
    except Exception:
        return False
    return elements

def checkExistsById(id):
    try:
        element = findOneById(id)
    except Exception:
        return False
    return element

def findOneById(id, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, (id))))

def Sleeping_Bot(borne_inf=float, borne_sup=float):
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)

def storeInBD(instagram_username,url):
    try:
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO actions (platform,type_action,id_smartphone, id_social_account,source , date_created, id_task_user) VALUES (?,?,?,?,?,?,?)",
                ('Instagram','Like_Random', p_udid,instagram_username,url, str(datetime.now()),p_taskuser_id))
            sqlite_connection.commit()
    except Exception as ex:
        logger.error(f'sqlite execption (store_action): {ex}')

def getPostUsername():
    usernameInScreen = checkExistsByXpath(
        '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[1]')
    userFound = usernameInScreen != False

    bools = True

    while not usernameInScreen:
        if bools:
            logger.info(f"First while == Username not found in screen")
            bools = False
        userFound = False
        driver.swipe(width / 2, height * 0.2, width / 2, height * 0.5, 2000)
        usernameInScreen = checkExistsByXpath(
            '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[1]')

    if userFound:
        logger.info(f"Username found on screen")
        post = checkExistsByXpath('//android.widget.ImageView[@content-desc="Liked"]')
        buttonX, buttonY = post.location.values()
        usernameX, usernameY = usernameInScreen.location.values()
        if buttonY < usernameY:
            logger.info(f"Username found au dessous du like button")
            driver.swipe(width / 2, height * 0.2, width / 2, height * 0.8, 2000)

        usernameInScreen = checkExistsByXpath(
            '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[1]')

        while not usernameInScreen:
            driver.swipe(width / 2, height * 0.2, width / 2, height * 0.5, 2000)
            usernameInScreen = checkExistsByXpath(
                '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[1]')

    if usernameInScreen:
        logger.info(f"Username : {usernameInScreen.text}")
        return usernameInScreen.text
    return ''

def getPostLink():
    secondTitle = checkExistsByXpath('//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[2]')
    if secondTitle and 'sponsored' in secondTitle.text.lower():
        return ''

    moreButton = checkExistsById('com.instagram.android:id/feed_more_button_stub')
    try:
        moreButton.click()
        linkButton = checkExistsById('com.instagram.android:id/link')
        linkButton.click()
        Sleeping_Bot(2,3)
        link = driver.get_clipboard_text().split('?')[0]
        logger.info(f'Liked post url : {link}')
        return link

    except Exception:
        logger.info("Url cannot be detected")
        return ''

def Smartphone_Authority_Instagram_Like_Rand_Post(p_taskuser_id, p_udid, p_systemPort, p_deviceName,
                                                        p_version, p_os, p_label_log, lock,
                                                        limit_of_liked_post):
    logger.info("=== Open Smartphone =======================================")
    global driver
    global sqlite_cursor
    global sqlite_connection
    global database
    global width
    global height

    database = 'db.db'
    sqlite_connection = sqlite3.connect(LoadFile(database))
    sqlite_cursor = sqlite_connection.cursor()

    # ==============================================================================#
    #                                                                               #
    #                       Opening Instagram On SMARTPHONE                         #
    #                                                                               #
    # ==============================================================================#

    try:
        driver = Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock)
        size = driver.get_window_size()

        width = size['width']
        height = size['height']

        likesCounter = 0

        nonEffectiveSwipes = 0

        while nonEffectiveSwipes < 10 and likesCounter < limit_of_liked_post:
            randomPostScrolls = random.randint(0,3)

            for _ in[0]*randomPostScrolls:
                driver.swipe(width / 2, height * 0.8, width / 2, height * 0.2, 2000)

            post = checkExistsByXpath('//android.widget.ImageView[@content-desc="Like"]')
            while nonEffectiveSwipes < 10 and not post:
                driver.swipe(width / 2, height * 0.8, width / 2, height * 0.2, 2000)
                nonEffectiveSwipes += 1
                post = checkExistsByXpath('//android.widget.ImageView[@content-desc="Like"]')

            if nonEffectiveSwipes >= 10:
                logger.info(f"Phone BOT couldn't find new posts to be liked.")
                logger.info(f"Here are some possible reasons for this issue : ")
                logger.info(f"    A problem while loading the feed (connexion problem ... )")
                logger.info(f"    Maybe the user have launched PHONEBOT on this task many time in a short period, so that the same liked posts reappear")
                logger.info(f"    The limit number of likes to be performed is very big !")
                break
            else:
                nonEffectiveSwipes = 0
                logger.info("Like Button found.")
                post.click()
                logger.info("Like performed correctly.")

                storeInBD(getPostUsername(), getPostLink())
                logger.info("Operation details have been saved locally.")
                Sleeping_Bot(1,2)
                logger.info("#"*40)
                likesCounter += 1

        if nonEffectiveSwipes < 10:
            logger.info(f"We have reached the limit of {limit_of_liked_post} liked post")

    except Exception as ex:
        logger.error(f'ERROR :  {ex}')
        return False

    finally:
        sqlite_connection.close()
        time.sleep(1000)
        driver.quit()

# Numero de task user arbitraire
"""
p_taskuser_id = 254
limit_of_liked_post = 20  # Maximum number of posts to be liked
p_deviceName = "Honor 8X"
p_udid = "9YHNW18C28002110"
p_os = "Android"
p_version = "10.0"
p_systemPort = ""
p_label_log = ""
lock = threading.Lock()

Smartphone_Authority_Instagram_Like_Rand_Post(p_taskuser_id, p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock, limit_of_liked_post)
"""
