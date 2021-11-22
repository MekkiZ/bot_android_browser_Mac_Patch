# ==============================================================================#
#                                                                               #
#                    Developer : mohammed haddoudi                              #
#       Contact :                                                               #
#                   WTSP : +33 6 98 47 11 68                                    #
#                  Mail : haddoudimo@cy-tech.fr                                 #
#                                                                     #

import subprocess
import threading
import logging
import time
import sqlite3
import mymodulesteam
from datetime import datetime
import random
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

platform=str('instagram')
#the followers number we choose to scrap
followers_to_scrap = 30
p_taskuser_id = "2953"
id_task_user = str(p_taskuser_id)
p_systemPort = ""
p_deviceName = "Galaxy A02s"
p_udid = "R9JNC0B7N3J"
p_os = "Android"
p_version = "10.0"
p_label_log = ""
lock = threading.Lock()
# ==============================================================================#
#                                                                               #
#            Launching LOGGER To save notes about the script's issues           #
#                                                                               #
# ==============================================================================#

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__smartphone_scrapping_followers_instagram__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
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
                print(
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")
                print(
                    f"{p_udid}|||We can't open Facebook. Please check if device is connected. Let's try again!")

            if cpt_appium_start > 3:
                print("Error", "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")

                return None

            time.sleep(random.uniform(2.5, 3.3))

            # ==============================================================================#
            #                                                                               #
            #                    Shortcut to find an element via XPATH or ID                #
            #                                                                               #
            # ==============================================================================#


def findOneByXPath(driver, xpath, time=10):
    try:
        elmt = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, (xpath))))
        return elmt
    except:
        return(None)

def findOneByID(driver, id, time=10):
    try:
        elmt = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, (id))))
        return elmt
    except:
        return(None)
    # ==============================================================================#
    #                                                                               #
    #                    Shortcut to find all elements via XPATH or ID              #
    #                                                                               #
    # ==============================================================================#


def findAllByXPath(driver, xpath, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, (xpath))))

def findAllByID(driver, id, time=10):
    elmts = WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.ID, (id))))
    return elmts
# ==============================================================================#
#                                                                               #
#                     functions to add elements to database                     #
#                                                                               #
# ==============================================================================#

def store_contact(id_task_user, username, insta_header_full_name, platform):

    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        with lock:
            conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            cursor = conn.cursor()

            insert_query = """INSERT INTO contacts(platform, username, id_task_user, date_created, insta_header_full_name)
                            VALUES (?, ?, ?, ?, ?) """
            contact_tuple = (platform, username, id_task_user, date_created, insta_header_full_name )

            cursor.execute(insert_query, contact_tuple)
            conn.commit()

    except Exception as ex:
        mymodulesteam.logger.error(f'Exception thrown (store_contact): {ex} {ex.__cause__}')
        return False
type_action = str("scrap")
id_smartphone = str(p_udid)

def store_action(id_task_user, id_social_account, type_action, id_smartphone, platform):

    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        with lock:
            conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            cursor = conn.cursor()

            insert_query = """INSERT INTO actions(platform, id_social_account, id_task_user, date_created, id_smartphone, type_action)
                            VALUES (?, ?, ?, ?, ?, ?) """
            contact_tuple = (platform, id_social_account, id_task_user, date_created, id_smartphone, type_action)

            cursor.execute(insert_query, contact_tuple)
            conn.commit()

    except Exception as ex:
        mymodulesteam.logger.error(f'Exception thrown (store_contact): {ex} {ex.__cause__}')
        return False

def is_in_db(platform, username, id_task_user):

    try:
        with lock:
            conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            cursor = conn.cursor()
            profile = cursor.execute("SELECT * FROM contacts WHERE platform = ? AND username = ? AND id_task_user = ?",
                                        [platform, username, id_task_user]).fetchone()
            if profile is None:
                return False
            conn.close()
            return True

    except Exception as e:
        mymodulesteam.logger.error(f'Error is_in_db : error msg: {e}')
#                                                   #
#                                                   #
#  Main function of scrapping instagram followers   #
#                                                   #
#                                                   #



def Smartphone_instagram_scrapping_followers(p_udid, p_systemPort, p_deviceName, p_version,
                                       p_os, p_label_log, lock):
    # get keywords randomly from the google sheet
    a = random.randrange(3)
    task_details_dico = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    googlesheet = task_details_dico['url_keywords']
    googlesheet_id = str(googlesheet).split("/")[5]
    keywords_list = mymodulesteam.GoogleSheetGetValues(googlesheet_id)
    word_search = keywords_list[a]

    # ==============================================================================#
    #                                                                               #
    #                          Opening instagram On SMARTPHONE                      #
    #                                                                               #
    # ==============================================================================#

    driver = Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock)
    #function to scroll the window
    def scroll(x, y):
        screen_size = driver.get_window_size()
        start_x = round(0.5 * screen_size['width'])
        start_y = round(0.7 * screen_size['height'])
        end_x = round((0.5 + x) * screen_size['width'])
        end_y = round((0.9 + y) * screen_size['height'])
        driver.swipe(start_x, start_y, end_x, end_y, 1000)

    def getUserFollowers(driver, word_search):
        search_button = findOneByXPath(driver, "//android.widget.FrameLayout[@content-desc='Search and Explore' or @content-desc='Rechercher et explorer' ]/android.widget.ImageView")
        if search_button is not None:
            search_button.click()
        search_text = findOneByXPath(driver, "//android.widget.FrameLayout/android.widget.EditText")
        if search_text is not None:
            search_text.click()
            search_text.send_keys(word_search)
        driver.execute_script('mobile: performEditorAction', {"action": "search"})
        time.sleep(2)
        profile = findOneByXPath(driver, "//android.widget.LinearLayout/android.widget.TextView")
        if profile is not None:
            profile.click()
        #check if the account is private
        private = findOneByID(driver, "com.instagram.android:id/igds_headline_emphasized_headline")
        if (private != None):
            print("the scrapping is interrupted, the account is private, please tryagain")
            exit(-1)
        list_followers = findOneByID(driver, "com.instagram.android:id/row_profile_header_textview_followers_title")
        if list_followers is not None:
            list_followers.click()
        time.sleep(2)
        followers_username = []

        while (len(followers_username)<followers_to_scrap):
            try:
                followersList = findAllByID(driver, "com.instagram.android:id/follow_list_container")
                for user in followersList:
                    if len(followers_username) == followers_to_scrap:
                        break
                    username = user.find_element_by_id('com.instagram.android:id/follow_list_username').get_attribute('text')
                    if (is_in_db(platform, username, id_task_user) == False):
                        print("contact ready to  be added")
                        followers_username.append(username)
                        insta_header_full_name = user.find_element_by_id('com.instagram.android:id/follow_list_subtitle').get_attribute('text')
                        driver.implicitly_wait(10)
                        store_contact(id_task_user, username, insta_header_full_name, platform)
                        store_action(id_task_user, username, type_action, id_smartphone, platform)
                    else:
                        print("contact is already in the db")
                scroll(0, -0.85)
            except:
                scroll(0, -0.85)
    getUserFollowers(driver, word_search)



"""
Smartphone_instagram_scrapping_followers(p_udid, p_systemPort, p_deviceName, p_version, p_os,
                                   p_label_log, lock)
"""
