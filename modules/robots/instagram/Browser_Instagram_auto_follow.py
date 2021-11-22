# ========================================== #
#       Author: Yann JOUBERT                 #
#           Not Finished                     #
#           In Progress                      #
# ========================================== #

import logging
import os, sys
import shutil
import time
import random
import threading
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver import ActionChains, DesiredCapabilities
import pathlib
import platform
import psutil
import sqlite3
from modules import mymodulesteam
from modules.mymodulesteam import LoadFile

# from importlib.machinery import SourceFileLoader
# mymodulesteam = SourceFileLoader("mymodulesteam", "C:\\Users\\Jyann\\OneDrive\\Bureau\\PycharmProjects\\phonebot_debug-main\\modules\\mymodulesteam.py").load_module()

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_auto_follow_instagram__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================
# ================= Send action to action table ==================================


def Inser_Value_To_action(date_created, id_contact, user_id, plateform = str("Instagram")):
    try:
        conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        cursor = conn.cursor()
        insert_query = """INSERT INTO actions(platform, type_action, date, id_contact, date_created,
                        id_task_user) VALUES(?, ?, ?, ?, ?, ?) """
        action_tuple = (
            plateform, "follow", date_created, id_contact,
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), user_id)
        cursor.execute(insert_query, action_tuple)
        conn.commit()
        conn.close()
    except Exception as ex:
        logger.error(f'sqlite execption (Inser_Value_To_action): {ex}')
        return False
    return True


def Sleeping_Bot(borne_inf=float, borne_sup=float):
    """
        Random time.sleep for being a stealth bot.
    """
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)
# ================================= send contacts to contacts table =========================


def Inser_Value_To_contact(user_id, name, plateform=str("Instagram")):
    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        cursor = conn.cursor()
        insert_query = """INSERT INTO contacts(platform, username, id_task_user, date_created) 
                            VALUES (?, ?, ?, ?) """
        contact_tuple = (plateform, name, user_id, date_created)
        cursor.execute(insert_query, contact_tuple)
        conn.commit()

        contact_id = cursor.execute("SELECT id FROM contacts WHERE username = ? AND date_created = ?",
                                    [name, date_created]).fetchone()[0]
        conn.close()
        return Inser_Value_To_action(date_created, contact_id, user_id)
    except Exception as ex:
        logger.error(f'Exception thrown (Inser_Value_To_contact): {ex} {ex.__cause__}')
        return False


def get_url_list(url):
    if url is None:
        logger.info(f'url spreadsheet not found')
        return False
    return mymodulesteam.GoogleSheetGetValues(mymodulesteam.extract_ss_id_regex(url))


def click_on_element(driver, element):
    driver.execute_script("arguments[0].click();", element)


def follow_button(driver, action_done, p_quantity_actions, p_taskuser_id):
    followButton = []
    action = True
    isEnd = False
    cpt_scroll = 6
    while action and not isEnd:
        try:
            # ===== RECUPERE LES BOUTTONS FOLLOW AVEC LEUR XPATH S’abonner ========

            driver.implicitly_wait(10)
            buttons = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, (
                "//button[(text()='Follow') or contains(text(),'abonner')]"))))

            # RECUPERE LES NOMS de FOLLOW AVEC LEUR XPATH

            # names = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
                # By.CSS_SELECTOR, "span.Jv7Aj>a.FPmhX")))

            # names = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
                # By.CSS_SELECTOR, "a[class='FPmhX notranslate MBL3Z']")))

            for button in buttons:
                if button not in followButton:
                    # ========== On clique sur le Bouton pour Follow ==============
                    followButton.append(button)
                    # click_on_element(driver, button)
                    logger.info("FOLLOW WORKING")
                    time.sleep(random.uniform(1, 1.2))
                    print("follow is confirmed")
                    cpt_scroll = cpt_scroll - 1
                    time.sleep(random.uniform(1, 2))

                    # ========== SCROLL PART =============

                    # On récupère le petit enfant du grand père dans le Xpath et on sélectionne le 2ième enfant
                    popup = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, (
                        "//div[@role='dialog']/div/child::div[2]"))))
                    if cpt_scroll == 0:
                        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)

                    time.sleep(random.uniform(1, 2))

                    # name = names[buttons.index(button)].text

                    # name = name[1:]
                    # Inser_Value_To_contact(p_taskuser_id, name)
                    action_done += 1

                if action_done == p_quantity_actions:
                    logger.info(f'the work for {p_quantity_actions} action is already done')
                    action = False
                    break

            # isEnd = scroll_down(driver)

        except TimeoutException:
            logger.info('not found any followers in the page scroll down')

        except Exception as ex:
            logger.error(f'Didn\'t not found any followers : {ex}')
            return False


def Browser_Instagram_Auto_Follow(p_browser, p_taskuser_id, Instagram_username, p_driver, p_quantity_actions, label_log, lock):
    logger.info("=== [1] PREPARE THE GOOGLESHEET =======================================")
    action_done = 0
    task = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    print(f"task : {task}")
    googlesheet = task["url_list"]
    googlesheet_id = str(googlesheet).split("/")[5]
    List_of_array = mymodulesteam.GoogleSheetGetValues(googlesheet_id)

    logger.info("=== [2] OPEN BROWSER =======================================")
    # OUVERTURE DU NAVIGATEUR

    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

    logger.info("=== [3] CONNECT TO GOOGLE PAGE URLS =======================================")
    try:
        driver.get('https://instagram.com')
        driver.implicitly_wait(10)
        for url in List_of_array:
            url = str(url[0])
            try:
                time.sleep(1)
                p_driver.get(url)
                # p_driver.maximize_window()
                p_driver.implicitly_wait(3)
            except Exception as ex:
                print("Error on the following url : " + url)
                return False

            # Go to "Followers"
            logger.info("=== [4] GO THE 'FOLLOWERS' =======================================")
            try:
                followersButton = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, ("//li/a[contains(@href,'/followers/')]"))))
                # $x("//li/a[contains(@href,'/followers/')]")
                time.sleep(random.uniform(1, 3))
                click_on_element(driver, followersButton)
            except Exception as ex:
                logger.error(f"Couldn't access to the followers page ")

            try:
                # listOfFollow = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, (
                    # "//button[contains(text(),'abonner')] | //button[contains(text(),'Follow')]"))))
                # Sleeping_Bot(2.0, 12.0)
                # driver.execute_script("arguments[0].click();", listOfFollow)
                driver.implicitly_wait(5)

                follow_button(driver, action_done, p_quantity_actions, p_taskuser_id)

            except Exception as ex:
                logger.error(f'url not defined {ex}')
                return False
    finally:
        driver.quit()
        logger.info("=== JOB DONE ==================")


# p_browser = "Firefox"
# p_taskuser_id = "4688"
# p_quantity_actions = 6
# label_log = ""
# lock = threading.Lock()
# p_quantity_actions = 6
# Instagram_username = "toto"
# if p_browser == "Chrome":
    # driver = mymodulesteam.ChromeDriverWithProfile()
# elif p_browser == "Firefox":
    # driver = mymodulesteam.FireFoxDriverWithProfile()
# else:
    # logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
# driver.get('https://instagram.com')
# p_driver = driver
# Browser_Instagram_Auto_Follow(p_browser, p_taskuser_id, Instagram_username, p_driver, p_quantity_actions, label_log, lock)
