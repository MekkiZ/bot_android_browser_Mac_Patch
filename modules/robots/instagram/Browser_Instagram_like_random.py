# -*- coding: utf-8 -*-

"""
Author : Florian Riviere
task: Browser Instagram Like Random Posts
Email : florian.riviere@epitech.eu 
"""

import logging
import sqlite3
import threading
import time
import os
import shutil
import time

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
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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


def sleeping_bot():
    """
        Random time.sleep for being a stealth bot.
    """
    ts = random.uniform(1, 5)
    ts = round(ts, 2)
    time.sleep(ts)


def save_action_database(lock, post_url, id_task_user):
    # db.db needs to be on the folder to use this function
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        sqlite_cursor.execute(
            "INSERT INTO actions (platform,type_action,date,fb_group_url,id_task_user) VALUES (?,?,?,?,?)",
            ('instagram',
             'liking',
             str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
             post_url,
             id_task_user))
        sqlite_connection.commit()


def is_post_already_liked(lock, post_url):
    # db.db needs to be on the folder to use this function
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        count = sqlite_cursor.execute(
            "SELECT COUNT(*) FROM actions WHERE platform = ? AND type_action = ? AND fb_group_url = ?",
            ('instagram', 'liking', post_url))

    if count.fetchone()[0] == 0:
        return False
    else:
        return True


def Find_Element(p_driver):
    like = p_driver.find_element_by_xpath("//div[@role='presentation']//ul[@class='vi798']/li[2]//div[@role='button'][1]")
    if like is not None:
        print("Je peux clicker sur le like")
        return True
    else:
        print("c'est deja like")
        return False

def Browser_Instagram_Like_random_post(p_browser,p_taskuser_id,Instagram_username,p_driver, p_quantity_actions,label_log,lock):
    """
    :param p_browser: "firefox" or "chrome"
    :param p_taskuser_id: The Id N° in database of the user task (ex: 254 )
    :param p_quantity_actions: The quantity maximum of actions. Ex: 5 messages to 5 members
    :param label_log: This is the label of our GUI (PyQt5). It will display the message you want to the user interface. This is very useful for displaying important error.
    :param lock: This function will be executed inside a thread. The program PhoneBot use multithread to run different tasks at same times on different devices (browser desktop, smartphones).
    If several tasks save at same time some data in SQLITE3 database, there will be some error for multiple access at same time. We need to "Lock" the access.
    You simply create it with this line of code : lock = threading.Lock()
    :return: True if everything was fine or False if error
    """
    logger.info("=== [1] Open Browser =======================================")

    p_driver.implicitly_wait(10)
    p_driver.maximize_window()

    # RECUPERATION DES INFORMATIONS SUR LA TASK

    task_details_dict = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)

    if task_details_dict["enable"] == 0:
        logger.error("The task is not enabled, please check your dashboard to enable the task.")
        p_driver.quit()
        return False

    print("*******************************************************")
    print(str(task_details_dict))
    print("*******************************************************")
    print("=======================================================")
    print(str(p_quantity_actions))
    print("=======================================================")
    counter = 0
    set = 0
    nb_like_button = 1
    rdm_for_condition = randint(1, 2)


    while counter < p_quantity_actions:

        try:
            post = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//time/parent::a")))
        except:
            logger.error("You are not connected on your Instagram account, please allow your browser to save cookies "
                         "to make sure you do not have to type your username/password to log into your Instagram "
                         "account")
            return False, 0

        print("Debut boucle")
        rdm_for_condition = randint(1, 2)
        print(f"rmd := {rdm_for_condition}")
        like_buttons = p_driver.find_elements_by_xpath("//*[local-name()='svg' and @aria-label='Like' and @width='24'][1]")
        numbers_of_button = len(like_buttons)
        print(f"numbers_of_button =: {numbers_of_button}")
        print("For scrolling")
        post_url = post.get_attribute("href")

        """ J'initialise set == 0 car je veux qu'il like que le premier post """
        if set == 0:
            post = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//time/parent::a")))
            print("===================================")
            print("Like le premier post")
            print("===================================")
            print("je sroll de 450")
            p_driver.execute_script("window.scrollBy(0, 450);")
            sleeping_bot()
            print("ALl function for click")
            print("Like")
            """
            like_buttons[0].click()
            p_driver.execute_script("arguments[0].click();", like_buttons[0])
            p_driver.execute_script("arguments[0].click();", like_buttons[0])
            """
            print("et maintenant 150 de plus")
            p_driver.execute_script("window.scrollBy(0, 150);")
            sleeping_bot()
            counter += 1
            """
            print("je scroll de 700")
            p_driver.execute_script("window.scrollBy(0, 700);")
            sleeping_bot()
            """
            set += 1
        else:
            """SI rdm == 1 le like sinon je continue de scroll"""
            if rdm_for_condition == 1:
                print("JE LIKE CAR RDM == 1")
                print("===================================")
                print("Like les autres posts")
                print("===================================")
                print("Like")
                sleeping_bot()
                print(f"nb_button!= {nb_like_button}")
                print("click")
                """
                like_buttons[nb_like_button].click()
                p_driver.execute_script("arguments[0].click();", like_buttons[0 + counter])
                """
                print(f"On like {counter + 1} eme post")
                counter += 1
                nb_like_button += 1
                """
                save_action_database(lock, post_url, p_taskuser_id)
                """
            else:
                print("===================================")
                print("Like pas  les autres posts")
                print("===================================")
                print("JE NE LIKE PAS CAR RDM == 2")
                print(f"nb_button!= {nb_like_button}")
                nb_like_button += 1
                sleeping_bot()
                p_driver.execute_script("window.scrollBy(0, 700);")

    p_driver.quit()
    return True, counter


"""
lock = threading.Lock() #This is necessary to protect the access to the database in multithreading mode
p_browser = "Chrome"
p_taskuser_id = 4789 # This is the Task user id you get from the dashboard.phonebot.co
# OUVERTURE DU NAVIGATEUR
if p_browser == "Chrome":
    p_driver = mymodulesteam.ChromeDriverWithProfile()
elif p_browser == "Firefox":
    p_driver = mymodulesteam.FireFoxDriverWithProfile()
else:
    logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
p_driver.get("https://www.instagram.com/")
Instagram_username = "toto"
p_quantity_actions = 10 # This is the maximum of actions that can do your task
label_log = "" # This is an object of PyQt5 which will display some message on the UI
result, counter = Browser_Instagram_Like_random_post(p_browser, p_taskuser_id,Instagram_username, p_driver, p_quantity_actions, label_log, lock)
"""
