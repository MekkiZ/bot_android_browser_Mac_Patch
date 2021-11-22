"""
Author : Lydia Berte
task: Browser Facebook Like Random Posts
Email : katyberte2@gmail.com

Remarque j'ai créé un champs url pour url de post
"""
import logging
import sqlite3
import threading
import time
import os
import shutil
import time
import random
from datetime import datetime

from modules import mymodulesteam
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
import random
from random import randint

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__NAME_OF_TASK__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================

"""
Random time.sleep for being a stealth bot.
"""


def Sleeping_Bot(borne_inf=float, borne_sup=float):
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)


def insert_To_Action_Table(p_browser, type_action, facebook_username, url, p_taskuser_id, lock):
    try:
        database = 'db.db'
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile(database))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO actions (platform,type_action,id_smartphone, id_social_account,source,date_created , id_task_user) VALUES (?,?,?,?,?,?,?)",
                ("Facebook", type_action, p_browser, facebook_username, url, str(datetime.now()), p_taskuser_id))
            sqlite_connection.commit()
            sqlite_connection.close()

    except Exception as ex:
        logger.error(f'sqlite execption (store_action): {ex}')
        return False
    return True


# fonction qui permet de scroller et d'aimer les post
def scrollPost(counter, p_browser, p_driver, p_quantity_actions, FB_username, p_taskuser_id, lock):
    SCROLL_PAUSE_TIME = 10

    nom_utilisateur = ""
    platform = "Facebook"
    type_action = "Like_random"
    date = ""
    message = ""
    id_social = ""

    # get name

    # Get scroll height
    last_height = p_driver.execute_script("return document.body.scrollHeight")
    # trouver les boutons de like by Xpath

    # Search for all Like Buttons

    buttons = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, (
        "//div[contains(@aria-label,'J’aime') or contains(@aria-label,'Like') and contains(@role,'button')]//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v lrazzd5p m9osqain']"))))


    while True and counter <= p_quantity_actions:
        try:
            # Scroll down to bottom
            buttons = buttons[randint(0, len(buttons) - 1)]
            p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            # p_driver.implicitly_wait(SCROLL_PAUSE_TIME)
        except Exception as ex:
            return False, counter
        time.sleep(SCROLL_PAUSE_TIME)

        try:
            # buttons = random.choices(buttons,k=len(buttons)-1 )
            # pointer sur le bouton like
            p_driver.execute_script("arguments[0].scrollIntoView(true);", buttons)
            time.sleep(3)
            # remonter vers le bouton Like
            p_driver.execute_script("window.scrollBy(0,200);")
            time.sleep(3)

            p_driver.execute_script("arguments[0].click();", buttons)
            time.sleep(3)
            # button.click()


            URL_Post = WebDriverWait(p_driver, 4).until(EC.presence_of_element_located((By.XPATH, (
                "//div[@class='qzhwtbm6 knvmm38d']//span[contains(@class,'tojvnm2t')]//a[contains(@class,'oajrlxb2 g5ia77u1') and contains(@role,'link')]"))))
            result = URL_Post.get_attribute("href")
            print("le lien du post est : ", str(result))
            nom_utilisateur = WebDriverWait(p_driver, 4).until(EC.presence_of_element_located((By.XPATH, (
                "//div[@class='qzhwtbm6 knvmm38d']//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v ekzkrbhg oo9gr5id hzawbc8m']//span[@class='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7']"))))
            nom_utilisateur = nom_utilisateur.text
            print("likerPost", str(nom_utilisateur))

            insert_To_Action_Table(p_browser, type_action, nom_utilisateur, result, p_taskuser_id, lock)

        except Exception as ex:
            logger.error(f"Error when trying to like a post: {ex}")

        # Calculate new scroll height and compare with last scroll height

        new_height = p_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        counter += 1
        print("j'aime")
    return True, counter


"""
def likeRandom(p_driver):
    compte = 0
    finish_like = False
    likesButtons = []
    while (compte<20):
        try:

            # trouver les boutons de like
            buttons = WebDriverWait(p_driver, 3).until(EC.presence_of_element_located((By.XPATH, (
                "//div[contains(@class,'QBdPU')]//svg[contains(@aria-label,'J'aime') ]"))))
            Sleeping_Bot(2.5, 4.5)

            for button in buttons:
                button.click()
                compte+=1
        except Exception as ex:
            logger.error(f"Error when trying to get the followers profiles : {ex}")"

"""


def Browser_Facebook_Like_random_post(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log,
                                      lock):
    # logger.info("=== [1] Open Browser =======================================")
    result = False
    # Page loading
    # Try 5 times before print an error message (Connexion's problemes ?)
    counter = 0
    errorCounter = 0
    while errorCounter < 5:
        try:
            # # agrandir le navigateur
            # p_driver.maximize_window()
            # # chargement de la page facebook
            # p_driver.get('https://www.facebook.com/')
            # # fonction de defilement et like
            result, counter = scrollPost(counter, p_browser, p_driver, p_quantity_actions, FB_username, p_taskuser_id, lock)

            time.sleep(3)
            # errorCounter += 1
            # check p_quantity_actions
            if counter == p_quantity_actions:
                result = True
                break
        except Exception as ex:
            errorCounter += 1
            time.sleep(3)
            # if errorCounter >= 5:
            #     errorCounter = -1
            #     logger.error(f"Error when getting access to the website : {ex}")

    return result, counter


"""
p_browser = "Chrome"
p_taskuser_id = "254"
p_driver = ""
Linkedin_username = ""
p_quantity_actions = 5

lock = threading.Lock()

Browser_Facebook_Like_random_post(p_browser,p_taskuser_id, p_quantity_actions,lock)
"""