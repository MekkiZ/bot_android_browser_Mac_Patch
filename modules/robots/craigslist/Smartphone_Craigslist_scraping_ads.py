# ==============================================================================#
#                                                                               #
#                    Developer : Imad RAFAI                                     #
#       Contact :                                                               #
#                   WTSP : +33 7 53 16 48 12                                    #
#                   Mail : imad.rafai@yahoo.com                                 #
#                   FB.com/iimadrafaii                                          #
#                   LINKEDIN.com/in/rafaiimad                                   #
# ==============================================================================#

from selenium import webdriver
import threading
import sqlite3
import mymodulesteam
from mymodulesteam import LoadFile
import logging
import time
import random
from datetime import datetime
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Smartphone_Scrap_Craigslist_Ads__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
)
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
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
    desired_caps['webkitResponseTimeout'] = 40000
    desired_caps['uiautomator2ServerLaunchTimeout'] = 100000
    desired_caps['uiautomator2ServerInstallTimeout'] = 100000
    desired_caps['remoteAppsCacheLimit'] = 0
    desired_caps['waitForQuiescence'] = 'false'
    desired_caps['appPackage'] = 'ru.yandex.searchplugin'
    desired_caps['appActivity'] = 'ru.yandex.searchplugin.MainActivity'
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
                f"{p_udid}|||We can't open Twitter. Please check if device is connected. Let's try again!")
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


def findOneByXPath(driver, xpath, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, (xpath))))

    # ==============================================================================#
    #                                                                               #
    #                    Shortcut to find an element via ID                         #
    #                                                                               #
    # ==============================================================================#


def findOneById(driver, id, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, (id))))

    # ==============================================================================#
    #                                                                               #
    #                    Shortcut to find all elements via XPATH                    #
    #                                                                               #
    # ==============================================================================#


def findAllByXPath(driver, xpath, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, (xpath))))


def get_keyword_city(keywords_list):
    """Returns a key and a list of cities."""
    if keywords_list is None:
        logger.info(f"Keyword / City spreadsheet not found.")
        return False
    return mymodulesteam.GoogleSheetGetValues(
        mymodulesteam.extract_ss_id_regex(keywords_list)
    )


def Smartphone_Craigslist_Scraping_Ads(p_taskuser_id, p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log,
                                       lock):
    logger.info("=== Open Smartphone =======================================")
    task = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)

    # ==============================================================================#
    #                                                                               #
    #                          Opening Twitter On SMARTPHONE                        #
    #                                                                               #
    # ==============================================================================#

    driver = Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock)

    searchBox = findOneById(driver, "ru.yandex.searchplugin:id/bender_omnibox_hint")
    searchBox.click()
    logger.info("On vient de cliquer sur le search box")

    searchBox = findOneById(driver, "ru.yandex.searchplugin:id/suggest_view_query")
    logger.info("Search box 2 trouvé ")
    searchBox.clear()
    logger.info("Box vidé")

    searchBox.send_keys("New york Craigslist")
    logger.info("Send keys")

    driver.press_keycode(66)
    logger.info("Key Code")

    logger.info("Open craigslist")
    logger.info(f"contexts : {driver.contexts}")
    searchedElement = findOneByXPath(driver,
                                     "//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]")
    searchedElement.click()
    logger.info("clicked on element on search results")

    keywords_list = get_keyword_city(task["url_keywords"])
    logger.info(f"list of keywords : {keywords_list}")

    if keywords_list is None:
        logger.error("Empty list!")
        return False

    # Switch to browser mode :
    menuList = findOneById(driver, "ru.yandex.searchplugin:id/bro_omnibar_address_button_menu")
    menuList.click()
    versionSwitchButton = findOneByXPath(driver,
                                         "//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[8]")

    if "Desktop" in versionSwitchButton.text:
        versionSwitchButton.click()
        logger.info("Switched to desktop version")
    else:
        driver.swipe(411, 290, 411, 900, 2000)
        logger.info("Swiped")
    try:
        for ad in keywords_list:
            pass
            logger.info(f"ad :  {ad} ")

            # Search on craigslist:
            searchBox = findOneById(driver, "query")
            searchBox.clear()
            searchBox.send_keys(ad[2])
            # select_list = findAllByXPath(driver, "//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.webkit.WebView/android.view.View/android.widget.ListView/android.view.View")

            # try:
            #     for web_elem in select_list:
            #         if (ad[1].lower()) in web_elem.text:
            #             web_elem.click()
            #             break
            # except Exception as e:
            #     logger.info(
            #         f"Not results were found with key word {ad[2]} and category {ad[1].lower()}"
            #     )



    except Exception as e:
        logger.error(
            f"Error while executing Smartphone_Scraping_Craigslist_Ads(): {e}"
        )

    time.sleep(3)
    try:

        while True:
            time.sleep(100)


    except Exception as ex:
        logger.error(f'ERROR :  {ex}')
        return False

    finally:
        driver.quit()


# Numero de task user arbitraire
"""
p_taskuser_id = "269"
p_deviceName = "Honor 8X"
p_udid = "9YHNW18C28002110"
p_os = "Android"
p_version = "10.0"
p_systemPort = ""
p_label_log = ""
lock = threading.Lock()

Smartphone_Craigslist_Scraping_Ads(p_taskuser_id, p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log,
                                   lock)
"""
