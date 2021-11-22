# -*- coding: utf-8 -*-

"""
Author : YEO EDITH
Email : gnidanhanatia-edith.yeo@etudiant.univ-rennes1.fr
"""
import logging
import random
import re
import sqlite3
import threading
import time
import os

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
from random import randint
import datetime

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Linkedin_like_Random__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================


def sleeping_bot(min, max):
    """
        Random time.sleep for being a stealth bot.
    """
    try:
        ts = random.uniform(min, max)

        #ts = round(ts, 2)
        time.sleep(ts)
        print(f"Sleeping {ts} seconds....")
    except Exception as ex:
        logger.error(f"Error during sleeping : {ex}")

def save_action_database(lock, post_url, p_task_user_id, Linkedin_username):
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO actions(platform,type_action, id_social_account, date, source, id_task_user) VALUES(?,?,?,?,?,?)",
                ('linkedin',
                 'random_like',
                 Linkedin_username,
                 str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                 post_url,
                 p_task_user_id))
            sqlite_connection.commit()
            sqlite_connection.close()
    except Exception as ex:
        logger.info(f"Query Failed in save_action_database, Error: {str(ex)}")
        return False
    else:
        logger.info(f"Comment saved to the database successfully!")
        return True

def is_already_liked(lock, post_url):
    # db.db needs to be on the folder to use this function
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        count = sqlite_cursor.execute(
            "SELECT COUNT(*) FROM actions WHERE platform = ? AND type_action = ? AND fb_group_url = ?",
            ('linkedin', 'like', post_url))

    if count.fetchone()[0] == 0:
        return False
    else:
        return True


def like_posts(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions, label_log, lock):
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

    posts_urls = []
    random_for_condition = randint(1, 2)
    counter = 0
    counter_scroll = 0
    print(f"p_quantity_actions : {p_quantity_actions}")

    while counter < p_quantity_actions:

        print("Debut boucle de Likes")
        # On recupere quelques boutons like qui n'ont pas été likés
        button_likes = p_driver.find_elements_by_xpath("//li-icon[@type='like-icon']/ancestor::button[@aria-pressed='false'][1]")

        how_much_buttons = len(button_likes)
        print(f"nombre de boutons a liker : {how_much_buttons}")
        number_post_to_like_after_scroll = 0

        if how_much_buttons > 5:
            number_post_to_like_after_scroll = round(how_much_buttons/2)
            print(f"number_post_to_like_after_scroll : {number_post_to_like_after_scroll}")

        print(f"how_much_buttons Likes found : {how_much_buttons}")
        if counter_scroll == 0:
            print("On like un 1er post")
            p_driver.execute_script("window.scrollBy(0, 500);")
            p_driver.execute_script("arguments[0].click()", button_likes[0])
            # On recupere l'ID du post
            post_id = button_likes[0].get_attribute('id')
            print(f"test pour l'id {post_id}")
            # button_likes[0].click()
            counter_scroll += 1
        else:
            if random_for_condition == 1:
                print(f"On like un {counter + 1} ème post")
                # button_likes[0 + how_much_buttons].click()
                p_driver.execute_script("arguments[0].click()", button_likes[0+number_post_to_like_after_scroll])
                post_id = button_likes[0+number_post_to_like_after_scroll].get_attribute('id')
                print(f"test pour l'id {post_id}")

                post_id = button_likes[0 + number_post_to_like_after_scroll].get_attribute('id')
                # Sauvegarde dans la base de données
            save_action_database(lock, post_id, p_taskuser_id, Linkedin_username)
            counter += 1

            sleeping_bot(1.2, 2.5)
            p_driver.execute_script("window.scrollBy(0, 1500);")
            sleeping_bot(2.2, 4.5)

            print(f"Fin de boucle. counter = {counter}")
    p_driver.quit()
    return True, counter

    # if test == 0:
    #     p_driver.execute_script("window.scrollBy(0, 500);")
    #     where_to_click = p_driver.find_element_by_xpath(
    #         "// button[@ aria-pressed='false'][contains(., 'J’aime')]")
    #     where_to_click.click()
    #     # p_driver.execute_script("arguments[0].click;", where_to_click)
    #     test = 1
    # else:
    #     p_driver.execute_script("window.scrollBy(0, 650);")
    #     sleeping_bot()

    #     p_driver.execute_script("window.scrollBy(0, 3000);")
    #     like_button = p_driver.find_element_by_xpath(
    #         "//span[contains(@class, 'artdeco-button__text react-button__text')]")
    #     p_driver.execute_script("arguments[0].click;", like_button)
    #     try:
    #         posts = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,
    #     "//span[contains(@class, 'artdeco-button__text react-button__text')]")))
    #     except:
    #         logger.error("You are not connected on your Linkedin account, please allow your browser to save cookies "
    #                      "to make sure you do not have to type your username/password to log into your Instagram "
    #                      "account")
    #         return False, 0
    #     post_url = posts.get_attribute("href")
    #     if not is_already_liked(lock, post_url) and post_url not in posts_urls:
    #         posts_urls.append(post_url)
    #     p_driver.execute_script("window.scrollBy(0, 3000);")
    #     like_button = p_driver.find_element_by_xpath("//span[contains(@class, 'artdeco-button__text react-button__text')]")
    #     p_driver.execute_script("arguments[0].click;", like_button)
    #     # like_button.click()
    #     print("click ok")
    #     sleeping_bot()
    #
    # counter = 1
    # for post_url in posts_urls:
    #     p_driver.get(post_url)
    #     sleeping_bot()
    #     like_button = WebDriverWait(p_driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, "//span[contains(@class, 'artdeco-button__text react-button__text')]")))
    #     print("---------------------------------------------------------------")
    #     p_driver.execute_script("arguments[0].click;", like_button)
    #     print("CLick on Button")
    #     # like_button.click()
    #     print("---------------------------------------------------------------")
    #     sleeping_bot()
    #     save_action_database(lock, post_url, p_taskuser_id)
    #     if counter < p_quantity_actions:
    #         counter += 1
    #     else:
    #         p_driver.quit()
    #         return True, counter
    # p_driver.quit()
    # return True, counter











        # if counter == 0:
        #     p_driver.execute_script("window.scrollBy(0, 500);")
        #     counter = 1
        # else:
        #     p_driver.execute_script("window.scrollBy(0, 500);")
        #     liked = p_driver.find_element_by_xpath("// button[@ aria-pressed='false'][contains(., 'J’aime')]")
        #     liked.click()
        #     sleeping_bot()
        #
        # if find_an_element(p_driver):
        #     print("test script")
        #     liked = p_driver.find_element_by_xpath("// button[@ aria-pressed='false'][contains(., 'J’aime')]")
        #     liked.click()
        #     counter += 1


    #     try:
    #         post = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Aimer le post']")))
    #
    #     except:
    #         logger.error("You are not connected on your Linkedin account, please allow your browser to save cookies "
    #                      "to make sure you do not have to type your username/password to log into your Linkedin "
    #                      "account")
    #     post_url = post.get_attribute("href")
    #     if not is_already_liked(lock, post_url) and post_url not in posts_urls:
    #         posts_urls.append(post_url)
    #     p_driver.execute_script("window.scrollBy(0, 3000);")
    #     sleeping_bot()
    #
    # counter = 1
    # for post_url in posts_urls:
    #     p_driver.get(post_url)
    #     sleeping_bot()
    #     like_button = WebDriverWait(p_driver, 10).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, "//button[@aria-label='Aimer le post de LinkedIn Actualités']")))
    #     like_button.click()
    #     sleeping_bot()
    #     save_action_database(lock, post_url, p_taskuser_id)
    #     if counter < p_quantity_actions:
    #         counter += 1
    #     else:
    #         p_driver.quit()
    #         return True, counter



"""
lock = threading.Lock()
p_browser = "Chrome"
p_taskuser_id = 4884 # Task user id from the dashboard
p_driver = mymodulesteam.ChromeDriverWithProfile()
p_driver.get("https://www.linkedin.com/")
Linkedin_username = "yass"
p_quantity_actions = 10
label_log = ""
result, counter = like_posts(p_browser, p_taskuser_id, Linkedin_username, p_driver, p_quantity_actions, label_log, lock)
"""
