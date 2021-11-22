# -*- coding: utf-8 -*-

"""
Authors : Ilker Soyturk / Clément Nonnet
Emails : ilkerstrk33@gmail.com / cl.nonnet@laposte.net
"""

import threading

from selenium.common.exceptions import TimeoutException

from modules import mymodulesteam
import logging
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__AUTHORITY_FACEBOOK_COMMENT_RANDOM_POSTS_FROM_GROUPS__')
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


# def connexion_to_facebook(p_driver):
#     p_driver.get('https://www.facebook.com/')
#
#     # Cliquer sur le pop-up des cookies
#
#     cookies_acceptation_button = WebDriverWait(p_driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//button[@title='Tout accepter']")))
#     p_driver.execute_script("arguments[0].click();", cookies_acceptation_button)
#
#     sleeping_bot()
#
#     # Connexion au compte Facebook
#
#     username_input = WebDriverWait(p_driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
#     username_input.send_keys("testitesto37@laposte.net")
#
#     sleeping_bot()
#
#     password_input = WebDriverWait(p_driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#pass")))
#     password_input.send_keys("TestTest37")
#
#     sleeping_bot()
#
#     connection_button = WebDriverWait(p_driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//button[@name='login']")))
#     p_driver.execute_script("arguments[0].click();", connection_button)
#
#     sleeping_bot()


def save_action_database(lock, message, post_url, id_task_user):
    # db.db needs to be on the folder to use this function
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        sqlite_cursor.execute(
            "INSERT INTO actions (platform,type_action,date,message,fb_group_url,id_task_user) VALUES (?,?,?,?,?,?)",
            ('facebook',
             'comment_posts',
             str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
             message,
             post_url,
             id_task_user))
        sqlite_connection.commit()
        sqlite_connection.close()


def is_post_already_commented(lock, post_url, id_task_user):
    # db.db needs to be on the folder to use this function
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        count = sqlite_cursor.execute(
            "SELECT COUNT(*) FROM actions WHERE platform = 'facebook' AND type_action = 'comment_posts' AND "
            "fb_group_url = ? AND id_task_user = ?", (post_url, id_task_user))
        sqlite_connection.commit()

    if count.fetchone()[0] == 0:
        return False
    else:
        return True


def comment_facebook_posts_by_keyword(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log,
                                      lock):
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

    # p_driver.maximize_window()

    # TO DO : Gérer le cas d'un user non connecté (pas de cookies)

    # RECUPERATION DES INFORMATIONS SUR LA GOOGLESHEET
    posts_list_urls = []
    number_commented_posts = 0

    result = False
    task_details_dico = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    googlesheet = task_details_dico["url_keywords"]
    googlesheet_id = str(googlesheet).split("/")[5]
    comments_list = mymodulesteam.GoogleSheetGetValues(googlesheet_id)
    daily_limit = task_details_dico["daily_limit"]

    # Changes ------------------------------------------

    # create list of keyword & msg
    # comment_data_list[0] -> keyword
    # comment_data_list[1] -> message

    comment_data_list = []
    for comment in comments_list:
        posts_urls = []
        post_msg = comment[1]
        keywords = comment[0]
        if keywords.__contains__(";"):
            keywords = keywords.split(";")
        elif keywords.__contains__(","):
            keywords = keywords.split(",")
        for word in keywords:
            comment_data_list.append((word, post_msg, posts_urls))

    """get posts to comment"""
    for keyword, msg, posts_urls in comment_data_list:
        keyword_url = "https://www.facebook.com/search/posts/?q=" + keyword
        p_driver.get(keyword_url)

        sleeping_bot()

        publication_choice_button = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//span[contains(text(), 'Publications de') or contains(text(), 'Posts from')]")))
        # By.XPATH, "//span[contains(text()='Publications de') or contains(text()='Posts From')]")))
        p_driver.execute_script("arguments[0].click();", publication_choice_button)

        sleeping_bot()

        public_publications_button = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[text()='Publications Publiques' or text()='Publications publiques' or text()='Public "
                "posts' or text()='Public Posts']"))
        )
        # By.XPATH, "//span[text()='Publications publiques' or text()='Public Posts']")))
        p_driver.execute_script("arguments[0].click();", public_publications_button)

        sleeping_bot()

        mymodulesteam.ScrollToTheEnd(p_driver)

        sleeping_bot()

        try:
            posts = WebDriverWait(p_driver, 10).until(
                EC.presence_of_all_elements_located((
                    By.XPATH, "//a[contains(@href,'/posts/') and starts-with(@href,'https://www.facebook.com/') "
                              "and not(contains(@href,'/groups/'))]")))

            for post in posts:
                posts_urls.append(post.get_attribute("href"))

        except TimeoutException as toe:
            mymodulesteam.logger.error(f'No posts found matching Keyword - Error: {toe}')

    """Write Comments"""
    for i in range(0, len(comment_data_list)):
        # Unpack line of comment_data_list[]
        keyword = comment_data_list[i][0]
        message = comment_data_list[i][1]
        urls = comment_data_list[i][2]
        logger.info(f'Write comment to posts containing keyword: {keyword}')
        # Get one url corresponding to the keyword, not yet commented
        post_to_comment = ""
        allow_comment = False
        capped = 0

        try:
            while not allow_comment and capped <= len(urls):
                post_to_comment = urls[random.randint(1, len(urls))-1]
                if not is_post_already_commented(lock, post_to_comment, p_taskuser_id):
                    allow_comment = True
                capped += 1
        except Exception as e:
            logger.info(f'All the post were commented previously, proceed to the next keyword - {e}')

        # Proceed to comment
        if allow_comment:
            p_driver.get(post_to_comment)

            sleeping_bot()

            comment_input = WebDriverWait(p_driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@aria-label='Écrire un commentaire' or @aria-label='Write a comment']")))
            p_driver.execute_script("arguments[0].scrollIntoView(true);", comment_input)

            sleeping_bot()

            p_driver.execute_script("window.scrollBy(0, -250);")

            sleeping_bot()

            comment_input.send_keys('')
            for j in message:
                if j == 0:
                    comment_input.send_keys('')
                else:
                    comment_input.send_keys(j)
                time.sleep(0.25)

            sleeping_bot()

            comment_input.send_keys(Keys.ENTER)

            sleeping_bot()

            save_action_database(lock, message, p_driver.current_url, p_taskuser_id)

            number_commented_posts += 1

            # Break loop when number_commented_posts == to p_quantity_actions
        if number_commented_posts >= p_quantity_actions:
            logger.info(f'Quantity of actions achieived: {number_commented_posts} of {p_quantity_actions}')
            break

    # p_driver.quit()
    result = True
    return result, number_commented_posts


    # --------------------------------------------------
#     """ Original code
#     # CALCUL DU NB DE COMMENTAIRES A ECRIRE POUR CHAQUE TOPIC
#
#     number_posts_to_comment = daily_limit // len(comment_data_list)
#     additionnal_nb_posts_to_comment = daily_limit % len(comment_data_list)
#
#     nb_comments_to_do = {keyword: number_posts_to_comment for keyword, message in comment_data_list}
#
#     i = 0
#     # try:
#     for keyword, value in nb_comments_to_do.items():
#         if i < additionnal_nb_posts_to_comment:
#             nb_comments_to_do[keyword] = value + 1
#         i += 1
#
#         for key, message, posts_urls in comment_data_list:
#
#              # RECUPERATION DES URLS DES POSTS A COMMENTER
#
#              keyword_url = "https://www.facebook.com/search/posts/?q=" + key
#              p_driver.get(keyword_url)
#
#              sleeping_bot()
#
#              publication_choice_button = WebDriverWait(p_driver, 10).until(
#                  EC.presence_of_element_located((
#                      By.XPATH, "//span[contains(text(), 'Publications de') or contains(text(), 'Posts from')]")))
#              # By.XPATH, "//span[contains(text()='Publications de') or contains(text()='Posts From')]")))
#              p_driver.execute_script("arguments[0].click();", publication_choice_button)
#
#              sleeping_bot()
#
#              public_publications_button = WebDriverWait(p_driver, 10).until(
#                  EC.presence_of_element_located((
#                      By.XPATH,
#                      "//span[text()='Publications Publiques' or text()='Publications publiques' or text()='Public "
#                      "posts' or text()='Public Posts']"))
#             )
#             # By.XPATH, "//span[text()='Publications publiques' or text()='Public Posts']")))
#             p_driver.execute_script("arguments[0].click();", public_publications_button)
#
#             sleeping_bot()
#
#             mymodulesteam.ScrollToTheEnd(p_driver)
#
#             sleeping_bot()
#
#             try:
#                 posts = WebDriverWait(p_driver, 10).until(
#                     EC.presence_of_all_elements_located((
#                         By.XPATH, "//a[contains(@href,'/posts/') and starts-with(@href,'https://www.facebook.com/') "
#                                   "and not(contains(@href,'/groups/'))]")))
#
#                 for post in posts:
#                     posts_list_urls.append(post.get_attribute("href"))
#
#             except TimeoutException as toe:
#                 mymodulesteam.logger.error(f'No posts found matching Keyword - Error: {toe}')
#             """
#
#         # ECRITURE DES COMMENTAIRES
# """
#         for url in posts_list_urls:
#
#             if number_commented_posts < nb_comments_to_do[keyword] and not is_post_already_commented(lock, url,
#                                                                                                      p_taskuser_id):
#                 p_driver.get(url)
#
#                 sleeping_bot()
#
#                 comment_input = WebDriverWait(p_driver, 10).until(
#                     EC.presence_of_element_located(
#                         (By.XPATH, "//div[@aria-label='Écrire un commentaire' or @aria-label='Write a comment']")))
#                 p_driver.execute_script("arguments[0].scrollIntoView(true);", comment_input)
#
#                 sleeping_bot()
#
#                 p_driver.execute_script("window.scrollBy(0, -250);")
#
#                 sleeping_bot()
#
#                 comment_input.send_keys('')
#                 for j in message:
#                     if j == 0:
#                         comment_input.send_keys('')
#                     else:
#                         comment_input.send_keys(j)
#                     time.sleep(0.25)
#
#                 sleeping_bot()
#
#                 comment_input.send_keys(Keys.ENTER)
#
#                 sleeping_bot()
#
#                 save_action_database(lock, message, p_driver.current_url, p_taskuser_id)
#
#                 number_commented_posts += 1
#
#                 # Break loop when number_commented_posts == to p_quantity_actions
#                 if number_commented_posts > p_quantity_actions:
#                     break
#
#     result = True
#     # except Exception as ex:
#     #     mymodulesteam.logger.error(f'Something went wrong while trying to comment post - Error: {ex}')
#     #     result = False
#     # p_driver.quit()
#
#     return result, number_commented_posts"""


# lock = threading.Lock()  # This is necessary to protect the access to the database in multithreading mode
# p_browser = "Firefox"  # This is the name of the browser
# p_taskuser_id = 3264  # This is the Task user id you get from the dashboard.phonebot.co
# p_quantity_actions = 5.0  # This is the maximum of actions that can do your task
# label_log = ""  # This is an object of PyQt5 which will display some message on the UI
# # comment_facebook_posts_by_keyword(p_browser, p_taskuser_id, p_quantity_actions, label_log, lock)
# p_driver = mymodulesteam.FireFoxDriverWithProfile()
# FB_username = ""
# p_driver.get("https://www.facebook.com")
#
# comment_facebook_posts_by_keyword(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock)
