# -*- coding: utf-8 -*-
#############################################################################################################
# Dimitri Détré                                                                                             #
# Finished task (21/05/2021)                                                                                #
#############################################################################################################
# Chris Techer                                                                                              #
# Work In Progress (08/10/2021) :                                                                           #
#                                                                                                           #
#     à ajouter à la Méthode:                                                                               #
#     - Parcours en boucle de la liste des influenceurs (visiter le site de l'influenceur et s'y abonner    #
#     - L'ajout de nouveaux contacts en followant (7500/day, 60 follow/hour)                                #
#     - Gestion des messages (entre 30 à 50 DM/jour pour un compte récent et 100 à 150 DM/jour)             #
#############################################################################################################

"""
This is a sample task for automation software Phonebot.co on Browser Firefox & Chrome
https://github.com/phonebotco/phonebot

"""

import logging
import sqlite3
import threading
from modules import mymodulesteam

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
from time import sleep
from datetime import datetime
import pathlib
import platform
import psutil
import random


"""
import by hand modules lib

##from importlib.machinery import SourceFileLoader
##mymodulesteam = SourceFileLoader("mymodulesteam","C:\\Users\\chris\\Downloads\\phonebot_debug\\modules\\mymodulesteam.py").load_module()
"""

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Cold_Messaging_Instagram__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================

"""
Send Message
"""


def Cold_Messaging_Platform_id(p_browser, p_taskuser_id, p_username, p_quantity_actions, label_log, lock):
    """
    Cette méthode va préparer et envoyer des messages
    :param p_browser: "Chrome" ou "Firefox"
    :param p_taskuser_id: "Ex: 254"
    :param p_username: "Ex: Gauthier Buttez"
    :param p_quantity_actions: "Ex:8"
    :param label_log: Pour afficher des messages sur l'UI
    :param lock: Pour pouvoir modifier la base de donner en mode multi-threads
    :return:
    """

    """
    Spreadsheet download & parsing
    
    testone = details_task["url_list"]
    testone_id = str(testone).split("/")[5]
    array_url_group = mymodulesteam.GoogleSheetGetValues(testone_id)
    print(f"array elements : {array_url_group}")
    """
    
    # We get details task
    details_task = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    print(f"details_task : {details_task}")

    # A --- See who reply ---------------------------------------------------------
    # A.1 get usernames who received a message with last message date
    # --- Get list of id_contacts
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    print("# =========================== AVANT CHECKING AWNSERS =================================")

    # Get the last date
    with lock:
        list_contacts_who_received_message = sqlite_cursor.execute(
            "SELECT actions.id_contact, contacts.username,actions.id_message, actions.date_created,actions.replied FROM actions INNER JOIN contacts ON actions.id_contact=contacts.id WHERE actions.id_task_user=? AND actions.id_social_account=? GROUP BY actions.id_contact ORDER BY actions.date_created",
            (int(p_taskuser_id), p_username)).fetchall()
    print(f"list_contacts_who_received_message : {list_contacts_who_received_message}")
    for contact in list_contacts_who_received_message:
        print(f"contact : {contact}")

    print("          ")
    print("# =========================== SELENIUM CHECKING INBOX WHO AWNSERED =================================")

    # A.2 Open the page with selenium and check who replied

    # try:
    #    btn_inbox_msg = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,("//nav//a[@href='/direct/inbox/']"))))
    #    p_driver.execute_script("arguments[0].click();", btn_inbox_msg)
    # except Exception as ex:
    #    logger.error(f"can't find messaging box {ex} .")

    reply = bool

    contactList = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, (
        "/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]"))))
    lastPosition = p_driver.execute_script('return arguments[0].scrollHeight', contactList)
    listEnd = False

    # first scroll to get a specific class name on all items in the list
    p_driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollHeight;', contactList)
    p_driver.execute_script(
        'arguments[0].scrollTop = 0;', contactList)

    # first date checking
    stop_scrolling = dateCheck()

    # scroll and check
    list_result = [listEnd, lastPosition, stop_scrolling]
    while (list_result[2] == False) and (list_result[0] != True):
        list_result = scrollDown(list_result[0], p_driver, contactList, list_result[1], list_result[2])

    # verify if someone replied
    try:
        reply_verif = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH, (
            "//div[contains(@class,'oNO81')]//a//div[contains(@class,'rBNOH')]//div[contains(@class,'Sapc9')]/parent::div/preceding-sibling::div[contains(@class,'vwCYk')]//div[contains(@class,'ui_ht')]//div[contains(@class,'fDxYl')]"))))
        reply = True
        logger.info(f"There is {len(reply_verif)} reply(ies).")
    except:
        reply = False

    if reply:

        # A.3 Update the data base
        for i in range(0, len(reply_verif)):
            username = str(reply_verif[i])
            with lock:
                sqlite_cursor.execute(
                    "INSERT INTO contact (replied = ?, date_update = ?) WHERE platform = ? AND username = ? AND id_task_user = ?",
                    (1, datetime.today(), "instagram", username, p_taskuser_id))
                contacts_who_replied = sqlite_cursor.execute(
                    "SELECT id_contact FROM contact WHERE platform = ? AND username = ? AND id_task_user = ? AND replied = ?",
                    ("instagram", username, p_taskuser_id, 1))
                sqlite_cursor.execute(
                    "INSERT INTO actions (replied = ?, date_update = ?) WHERE platform = ? AND id_contact = ? AND id_task_user = ?",
                    (1, datetime.today(), "instagram", contacts_who_replied, p_taskuser_id))

    print("          ")
    print("# =========================== APRES CHECKING REPONSES =================================")

    # B Planify list of messages to send
    # 2 choices:
    # - until_reply
    # - no_stop

    # B.1 serie_type == 'until_reply'
    if details_task['serie_type'] == 'until_reply':

        print("          ")
        print("# =========================== until_reply =================================")

        # delete all contact in messaging_queue who replied
        list_contacts_who_replied = sqlite_cursor.execute(
            "SELECT actions.id_contact, contacts.username,actions.id_message, actions.date_created,actions.replied FROM actions INNER JOIN contacts ON actions.id_contact=contacts.id WHERE actions.id_task_user=? AND actions.id_social_account=? AND actions.replied=? GROUP BY actions.id_contact ORDER BY actions.date_created DESC",
            (int(p_taskuser_id), p_username, 1)).fetchall()
        print(f"list_contacts_who_received_message : {list_contacts_who_received_message}")
        for contact in list_contacts_who_replied:
            print(f"contact : {contact}")
            with lock:
                sqlite_cursor.execute(
                    "DELETE FROM messaging_queue WHERE id_contact=? AND id_task_user=? AND id_social_account=?",
                    (contact[0], p_taskuser_id, p_username))
                sqlite_connection.commit()

        # =========================================================
        list_contacts_who_didnt_replied = sqlite_cursor.execute(
            "SELECT actions.id_contact, contacts.username,actions.id_message, actions.date_created,actions.replied FROM actions INNER JOIN contacts ON actions.id_contact=contacts.id WHERE actions.id_task_user=? AND actions.id_social_account=? AND (actions.replied<>? OR actions.replied IS ?)  GROUP BY actions.id_contact ORDER BY actions.date_created DESC",
            (int(p_taskuser_id), p_username, 1, None)).fetchall()
        print(f"list_contacts_who_didnt_replied : {list_contacts_who_didnt_replied}")
        for contact in list_contacts_who_didnt_replied:
            print("--------------------------------------------")
            print(f"contact who didn't reply: {contact}")
            # get last message without reply
            if contact[4] != 1:

                str_id_message = str(contact[2])
                print(f"str_id_message : {str_id_message}")
                last_two_characters = str_id_message[len(str_id_message) - 2:]
                print(f"last_two_characters : {last_two_characters}")

                if last_two_characters == '1A':
                    last_two_characters_next_message = '2A'
                    # When send
                    delay_type = details_task['time_delay_1A_type']
                    delay = details_task['time_delay_1A']

                    # What message send
                    if details_task['message_txt_2A'] != '':
                        id_prochain_message = 'message_txt_2A'
                    elif details_task['message_voice_2A'] != '':
                        id_prochain_message = 'message_voice_2A'

                elif last_two_characters == '2A':
                    last_two_characters_next_message = '3A'
                    # When send
                    delay_type = details_task['time_delay_2A_type']
                    delay = details_task['time_delay_2A']

                    # What message send
                    if details_task['message_txt_3A'] != '':
                        id_prochain_message = 'message_txt_3A'
                    elif details_task['message_voice_3A'] != '':
                        id_prochain_message = 'message_voice_3A'
                elif last_two_characters == '3A':
                    last_two_characters_next_message = '4A'
                    # When send
                    delay_type = details_task['time_delay_3A_type']
                    delay = details_task['time_delay_3A']

                    # What message send
                    if details_task['message_txt_4A'] != '':
                        id_prochain_message = 'message_txt_4A'
                    elif details_task['message_voice_4A'] != '':
                        id_prochain_message = 'message_voice_4A'

                elif last_two_characters == '1B':
                    last_two_characters_next_message = '2B'

                    # When send
                    delay_type = details_task['time_delay_1B_type']
                    delay = details_task['time_delay_1B']

                    # What message send
                    if details_task['message_txt_2B'] != '':
                        id_prochain_message = 'message_txt_2B'
                    elif details_task['message_voice_2B'] != '':
                        id_prochain_message = 'message_voice_2B'


                elif last_two_characters == '2B':
                    last_two_characters_next_message = '3B'
                    # When send
                    delay_type = details_task['time_delay_2B_type']
                    delay = details_task['time_delay_2B']

                    # What message send
                    if details_task['message_txt_3B'] != '':
                        id_prochain_message = 'message_txt_3B'
                    elif details_task['message_voice_3B'] != '':
                        id_prochain_message = 'message_voice_3B'


                elif last_two_characters == '3B':
                    last_two_characters_next_message = '4B'
                    # When send
                    delay_type = details_task['time_delay_3B_type']
                    delay = details_task['time_delay_3B']

                    # What message send
                    if details_task['message_txt_4B'] != '':
                        id_prochain_message = 'message_txt_4B'

                    elif details_task['message_voice_4B'] != '':
                        id_prochain_message = 'message_voice_4B'
                else:
                    last_two_characters_next_message = ''
                    id_prochain_message = ''

            print(f"last_two_characters_next_message: {last_two_characters_next_message}")
            print(f"id_prochain_message: {id_prochain_message}")
            print(f"delay: {delay} {delay_type}")

            # Search time delay
            print(f"contact[3] : {type(contact[3])} - {contact[3]}")
            # calculate time delay
            if delay_type == 'days':

                date_scheduled = datetime.strptime(contact[3], '%y/%m/%d %H:%M:%S') + datetime.timedelta(days=delay)
            elif delay_type == 'months':
                date_scheduled = contact[3] + datetime.timedelta(months=delay)
            elif delay_type == 'hours':
                date_scheduled = contact[3] + datetime.timedelta(hours=delay)
            elif delay_type == 'weeks':
                date_scheduled = contact[3] + datetime.timedelta(weeks=delay)

            print(f"date_scheduled : {date_scheduled}")

            # Add line in messaging_queue. But test if this line is already in this.
            with lock:
                if not sqlite_cursor.execute(
                        "SELECT * FROM messaging_queue WHERE id_message=? AND id_contact =? AND social_account=? AND id_task_user=?",
                        (id_prochain_message, contact[0], p_username, p_taskuser_id)).fetchone():
                    sqlite_cursor.execute(
                        "INSERT INTO messaging_queue (id_message,id_contact,social_account,schedule_date,id_task_user) VALUES(?, ?, ?, ?, ?)",
                        (id_prochain_message, contact[0], p_username, date_scheduled, p_taskuser_id))
                    sqlite_connection.commit()

            #  ---
            cpt = 0

            with lock:
                sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                sqlite_cursor = sqlite_connection.cursor()
                contact_to_contact = sqlite_cursor.execute(
                    "SELECT contacts.username, messaging_queue.id_message, messaging_queue.schedule_date, contacts.id FROM messaging_queue INNER JOIN contacts ON messaging_queue.id_contact = contacts.id WHERE social_account=? AND id_task_user=?",
                    (p_username, p_taskuser_id))

                for to_contact in contact_to_contact:
                    if to_contact[2] <= datetime.today():
                        if (cpt < p_quantity_actions):

                            # the time delay is passed, so we prepare the message
                            msg = str(details_task[to_contact[1]])
                            formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(to_contact[0]))

                            # We send the message
                            try:
                                messaging_profil = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, (f"//div[contains(text(),'{to_contact[0]}')]"))))
                                Sleeping_Bot(4.5, 5.5)
                                p_driver.execute_script("arguments[0].click();", messaging_profil)
                            except Exception as ex:
                                logger.error(f"can't find messaging profil {ex} .")

                            try:
                                message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                                Sleeping_Bot(2.5, 4.5)
                                p_driver.execute_script("arguments[0].click();", message_bar)
                            except:
                                try:
                                    message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                        (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                                    Sleeping_Bot(2.5, 4.5)
                                    p_driver.execute_script("arguments[0].click();", message_bar)
                                except Exception as ex:
                                    logger.error(f"can't find message_bar {ex} .")

                            try:
                                message_bar.send_key(formated_msg)
                                Sleeping_Bot(7.5, 9.5)
                                message_bar.sendKeys(Keys.ENTER)
                                Sleeping_Bot(10.5, 12.5)
                                cpt += 1
                            except Exception as ex:
                                logger.error(f"can't write and send the message {ex} .")

                            # We update the data base
                            try:
                                with lock:
                                    sqlite_cursor.execute(
                                        "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        ("instagram", "sent_message", formated_msg, p_username, contact[3],
                                         datetime.today(), id_prochain_message, p_taskuser_id, "texte"))
                                    sqlite_connection.commit()
                            except Exception as ex:
                                logger.error(f"can't commit the udate in the database {ex} .")


        # D --- Send the message n°1 to the new contacts
        with lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            new_contacts = sqlite_cursor.execute(
                "SELECT contacts.username, contacts.id FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact WHERE actions.id_social_account=? AND actions.id_task_user=? AND actions.message IS ? AND actions.id_message IS ?",
                (p_username, p_taskuser_id, None, None))

        # D.1 With or not AB_test
        cpt_AB = 1

        for new_contact in new_contacts:
            if ((cpt < p_quantity_actions) and (details_task['AB_testing_enable'] == '1')):
                if (cpt_AB % 2 == 0):

                    if details_task['message_txt_1A'] != '':
                        id_message = 'message_txt_1A'
                    elif details_task['message_voice_1A'] != '':
                        id_message = 'message_voice_1A'

                    msg = str(details_task[id_message])
                    formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                    # We send the message
                    try:
                        messaging_profil = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                        Sleeping_Bot(4.5, 5.5)
                        p_driver.execute_script("arguments[0].click();", messaging_profil)
                    except Exception as ex:
                        logger.error(f"can't find messaging profil {ex} .")

                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except:
                        try:
                            message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                            Sleeping_Bot(2.5, 4.5)
                            p_driver.execute_script("arguments[0].click();", message_bar)
                        except Exception as ex:
                            logger.error(f"can't find message_bar {ex} .")

                    try:
                        message_bar.send_key(formated_msg)
                        Sleeping_Bot(7.5, 9.5)
                        message_bar.sendKeys(Keys.ENTER)
                        Sleeping_Bot(10.5, 12.5)
                        cpt += 1
                    except Exception as ex:
                        logger.error(f"can't write and send the message {ex} .")

                    cpt += 1
                    cpt_AB += 1

                    # We update the database
                    with lock:
                        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                        sqlite_cursor = sqlite_connection.cursor()
                        sqlite_cursor.execute(
                            "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                             id_message, p_taskuser_id, "texte"))

                else:

                    if details_task['message_txt_1B'] != '':
                        id_message = 'message_txt_1B'
                    elif details_task['message_voice_1B'] != '':
                        id_message = 'message_voice_1B'

                    msg = str(details_task[id_message])
                    formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                    # We send the message
                    try:
                        messaging_profil = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                        Sleeping_Bot(4.5, 5.5)
                        p_driver.execute_script("arguments[0].click();", messaging_profil)
                    except Exception as ex:
                        logger.error(f"can't find messaging profil {ex} .")

                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except:
                        try:
                            message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                            Sleeping_Bot(2.5, 4.5)
                            p_driver.execute_script("arguments[0].click();", message_bar)
                        except Exception as ex:
                            logger.error(f"can't find message_bar {ex} .")

                    try:
                        message_bar.send_key(formated_msg)
                        Sleeping_Bot(7.5, 9.5)
                        message_bar.sendKeys(Keys.ENTER)
                        Sleeping_Bot(10.5, 12.5)
                        cpt += 1
                    except Exception as ex:
                        logger.error(f"can't write and send the message {ex} .")

                    cpt += 1
                    cpt_AB += 1

                    # We update the database
                    with lock:
                        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                        sqlite_cursor = sqlite_connection.cursor()
                        sqlite_cursor.execute(
                            "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                             id_message, p_taskuser_id, "texte"))

            elif ((cpt < p_quantity_actions) and (
                    (details_task['AB_testing_enable'] == '0') or (details_task['AB_testing_enable'] == ''))):
                if details_task['message_txt_1A'] != '':
                    id_message = 'message_txt_1A'
                elif details_task['message_voice_1A'] != '':
                    id_message = 'message_voice_1A'

                if details_task['message_txt_1B'] != '':
                    id_message = 'message_txt_1B'
                elif details_task['message_voice_1B'] != '':
                    id_message = 'message_voice_1B'

                msg = str(details_task[id_message])
                formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                # We send the message
                try:
                    messaging_profil = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                    Sleeping_Bot(4.5, 5.5)
                    p_driver.execute_script("arguments[0].click();", messaging_profil)
                except Exception as ex:
                    logger.error(f"can't find messaging profil {ex} .")

                try:
                    message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                    Sleeping_Bot(2.5, 4.5)
                    p_driver.execute_script("arguments[0].click();", message_bar)
                except:
                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except Exception as ex:
                        logger.error(f"can't find message_bar {ex} .")

                try:
                    message_bar.send_key(formated_msg)
                    Sleeping_Bot(7.5, 9.5)
                    message_bar.sendKeys(Keys.ENTER)
                    Sleeping_Bot(10.5, 12.5)
                    cpt += 1
                except Exception as ex:
                    logger.error(f"can't write and send the message {ex} .")

                cpt += 1

                # We update the database
                with lock:
                    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                    sqlite_cursor = sqlite_connection.cursor()
                    sqlite_cursor.execute(
                        "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                         id_message, p_taskuser_id, "texte"))

    else:
        print("          ")
        print("# =========================== no_stop =================================")

        # =========================================================
        complete_list_of_contacts = sqlite_cursor.execute(
            "SELECT actions.id_contact, contacts.username, actions.id_message, actions.date_created, FROM actions INNER JOIN contacts ON actions.id_contact=contacts.id WHERE actions.id_task_user=? AND actions.id_social_account=? GROUP BY actions.id_contact ORDER BY actions.date_created DESC",
            (int(p_taskuser_id), p_username, 1, None)).fetchall()
        print(f"complete_list_of_contacts : {complete_list_of_contacts}")
        for contact in complete_list_of_contacts:

            str_id_message = str(contact[2])
            print(f"str_id_message : {str_id_message}")
            last_two_characters = str_id_message[len(str_id_message) - 2:]
            print(f"last_two_characters : {last_two_characters}")

            if last_two_characters == '1A':
                last_two_characters_next_message = '2A'
                # When send
                delay_type = details_task['time_delay_1A_type']
                delay = details_task['time_delay_1A']

                # What message send
                if details_task['message_txt_2A'] != '':
                    id_prochain_message = 'message_txt_2A'
                elif details_task['message_voice_2A'] != '':
                    id_prochain_message = 'message_voice_2A'

            elif last_two_characters == '2A':
                last_two_characters_next_message = '3A'
                # When send
                delay_type = details_task['time_delay_2A_type']
                delay = details_task['time_delay_2A']

                # What message send
                if details_task['message_txt_3A'] != '':
                    id_prochain_message = 'message_txt_3A'
                elif details_task['message_voice_3A'] != '':
                    id_prochain_message = 'message_voice_3A'
            elif last_two_characters == '3A':
                last_two_characters_next_message = '4A'
                # When send
                delay_type = details_task['time_delay_3A_type']
                delay = details_task['time_delay_3A']

                # What message send
                if details_task['message_txt_4A'] != '':
                    id_prochain_message = 'message_txt_4A'
                elif details_task['message_voice_4A'] != '':
                    id_prochain_message = 'message_voice_4A'

            elif last_two_characters == '1B':
                last_two_characters_next_message = '2B'

                # When send
                delay_type = details_task['time_delay_1B_type']
                delay = details_task['time_delay_1B']

                # What message send
                if details_task['message_txt_2B'] != '':
                    id_prochain_message = 'message_txt_2B'
                elif details_task['message_voice_2B'] != '':
                    id_prochain_message = 'message_voice_2B'


            elif last_two_characters == '2B':
                last_two_characters_next_message = '3B'
                # When send
                delay_type = details_task['time_delay_2B_type']
                delay = details_task['time_delay_2B']

                # What message send
                if details_task['message_txt_3B'] != '':
                    id_prochain_message = 'message_txt_3B'
                elif details_task['message_voice_3B'] != '':
                    id_prochain_message = 'message_voice_3B'


            elif last_two_characters == '3B':
                last_two_characters_next_message = '4B'
                # When send
                delay_type = details_task['time_delay_3B_type']
                delay = details_task['time_delay_3B']

                # What message send
                if details_task['message_txt_4B'] != '':
                    id_prochain_message = 'message_txt_4B'

                elif details_task['message_voice_4B'] != '':
                    id_prochain_message = 'message_voice_4B'
            else:
                last_two_characters_next_message = ''
                id_prochain_message = ''

            print(f"last_two_characters_next_message: {last_two_characters_next_message}")
            print(f"id_prochain_message: {id_prochain_message}")
            print(f"delay: {delay} {delay_type}")

            # Search time delay
            print(f"contact[3] : {type(contact[3])} - {contact[3]}")
            # calculate time delay
            if delay_type == 'days':

                date_scheduled = datetime.strptime(contact[3], '%y/%m/%d %H:%M:%S') + datetime.timedelta(days=delay)
            elif delay_type == 'months':
                date_scheduled = contact[3] + datetime.timedelta(months=delay)
            elif delay_type == 'hours':
                date_scheduled = contact[3] + datetime.timedelta(hours=delay)
            elif delay_type == 'weeks':
                date_scheduled = contact[3] + datetime.timedelta(weeks=delay)

            print(f"date_scheduled : {date_scheduled}")

            # Add line in messaging_queue. but test if this line is already in this.
            with lock:
                if not sqlite_cursor.execute(
                        "SELECT * FROM messaging_queue WHERE id_message=? AND id_contact =? AND social_account=? AND id_task_user=?",
                        (id_prochain_message, contact[0], p_username, p_taskuser_id)).fetchone():
                    sqlite_cursor.execute(
                        "INSERT INTO messaging_queue (id_message,id_contact,social_account,schedule_date,id_task_user) VALUES(?, ?, ?, ?, ?)",
                        (id_prochain_message, contact[0], p_username, date_scheduled, p_taskuser_id))
                    sqlite_connection.commit()

            # C --- Send planificated messages
            cpt = 0

            with lock:
                sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                sqlite_cursor = sqlite_connection.cursor()
                contact_to_contact = sqlite_cursor.execute(
                    "SELECT contacts.username, messaging_queue.id_message, messaging_queue.schedule_date, contacts.id FROM messaging_queue INNER JOIN contacts ON messaging_queue.id_contact = contacts.id WHERE social_account=? AND id_task_user=?",
                    (p_username, p_taskuser_id))

                for to_contact in contact_to_contact:
                    if to_contact[2] <= datetime.today():
                        if (cpt < p_quantity_actions):

                            # the time delay is passed, so we prepare the message
                            msg = str(details_task[to_contact[1]])
                            formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(to_contact[0]))

                            # We send the message
                            try:
                                messaging_profil = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, (f"//div[contains(text(),'{to_contact[0]}')]"))))
                                Sleeping_Bot(4.5, 5.5)
                                p_driver.execute_script("arguments[0].click();", messaging_profil)
                            except Exception as ex:
                                logger.error(f"can't find messaging profil {ex} .")

                            try:
                                message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                                Sleeping_Bot(2.5, 4.5)
                                p_driver.execute_script("arguments[0].click();", message_bar)
                            except:
                                try:
                                    message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                        (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                                    Sleeping_Bot(2.5, 4.5)
                                    p_driver.execute_script("arguments[0].click();", message_bar)
                                except Exception as ex:
                                    logger.error(f"can't find message_bar {ex} .")

                            try:
                                message_bar.send_key(formated_msg)
                                Sleeping_Bot(7.5, 9.5)
                                message_bar.sendKeys(Keys.ENTER)
                                Sleeping_Bot(10.5, 12.5)
                                cpt += 1
                            except Exception as ex:
                                logger.error(f"can't write and send the message {ex} .")

                            # We update the data base
                            try:
                                with lock:
                                    sqlite_cursor.execute(
                                        "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        ("instagram", "sent_message", formated_msg, p_username, contact[3],
                                         datetime.today(), id_prochain_message, p_taskuser_id, "texte"))
                                    sqlite_connection.commit()
                            except Exception as ex:
                                logger.error(f"can't commit the udate in the database {ex} .")


        # D --- Send the message n°1 to the new contacts
        with lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            new_contacts = sqlite_cursor.execute(
                "SELECT contacts.username, contacts.id FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact WHERE social_account=? AND id_task_user=? AND actions.message IS ? AND actions.id_message IS ?",
                (p_username, p_taskuser_id, None, None))

        # D.1 With or not AB_test
        cpt_AB = 1

        for new_contact in new_contacts:
            if ((cpt < p_quantity_actions) and (details_task['AB_testing_enable'] == '1')):
                if (cpt_AB % 2 == 0):

                    if details_task['message_txt_1A'] != '':
                        id_message = 'message_txt_1A'
                    elif details_task['message_voice_1A'] != '':
                        id_message = 'message_voice_1A'

                    msg = str(details_task[id_message])
                    formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                    # We send the message
                    try:
                        messaging_profil = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                        Sleeping_Bot(4.5, 5.5)
                        p_driver.execute_script("arguments[0].click();", messaging_profil)
                    except Exception as ex:
                        logger.error(f"can't find messaging profil {ex} .")

                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except:
                        try:
                            message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                            Sleeping_Bot(2.5, 4.5)
                            p_driver.execute_script("arguments[0].click();", message_bar)
                        except Exception as ex:
                            logger.error(f"can't find message_bar {ex} .")

                    try:
                        message_bar.send_key(formated_msg)
                        Sleeping_Bot(7.5, 9.5)
                        message_bar.sendKeys(Keys.ENTER)
                        Sleeping_Bot(10.5, 12.5)
                        cpt += 1
                    except Exception as ex:
                        logger.error(f"can't write and send the message {ex} .")

                    cpt += 1
                    cpt_AB += 1

                    # We update the database
                    with lock:
                        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                        sqlite_cursor = sqlite_connection.cursor()
                        sqlite_cursor.execute(
                            "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                             id_message, p_taskuser_id, "texte"))

                else:

                    if details_task['message_txt_1B'] != '':
                        id_message = 'message_txt_1B'
                    elif details_task['message_voice_1B'] != '':
                        id_message = 'message_voice_1B'

                    msg = str(details_task[id_message])
                    formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                    # We send the message
                    try:
                        messaging_profil = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                        Sleeping_Bot(4.5, 5.5)
                        p_driver.execute_script("arguments[0].click();", messaging_profil)
                    except Exception as ex:
                        logger.error(f"can't find messaging profil {ex} .")

                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except:
                        try:
                            message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                                (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                            Sleeping_Bot(2.5, 4.5)
                            p_driver.execute_script("arguments[0].click();", message_bar)
                        except Exception as ex:
                            logger.error(f"can't find message_bar {ex} .")

                    try:
                        message_bar.send_key(formated_msg)
                        Sleeping_Bot(7.5, 9.5)
                        message_bar.sendKeys(Keys.ENTER)
                        Sleeping_Bot(10.5, 12.5)
                        cpt += 1
                    except Exception as ex:
                        logger.error(f"can't write and send the message {ex} .")

                    cpt += 1
                    cpt_AB += 1

                    # We update the database
                    with lock:
                        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                        sqlite_cursor = sqlite_connection.cursor()
                        sqlite_cursor.execute(
                            "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                             id_message, p_taskuser_id, "texte"))

            elif ((cpt < p_quantity_actions) and (
                    (details_task['AB_testing_enable'] == '0') or (details_task['AB_testing_enable'] == ''))):
                if details_task['message_txt_1A'] != '':
                    id_message = 'message_txt_1A'
                elif details_task['message_voice_1A'] != '':
                    id_message = 'message_voice_1A'

                if details_task['message_txt_1B'] != '':
                    id_message = 'message_txt_1B'
                elif details_task['message_voice_1B'] != '':
                    id_message = 'message_voice_1B'

                msg = str(details_task[id_message])
                formated_msg = mymodulesteam.TransformMessage(msg, firstname=str(new_contact[0]))

                # We send the message
                try:
                    messaging_profil = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, (f"//div[contains(text(),'{new_contact[0]}')]"))))
                    Sleeping_Bot(4.5, 5.5)
                    p_driver.execute_script("arguments[0].click();", messaging_profil)
                except Exception as ex:
                    logger.error(f"can't find messaging profil {ex} .")

                try:
                    message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, ("//textarea[contains(@placeholder,'Votre message')]"))))
                    Sleeping_Bot(2.5, 4.5)
                    p_driver.execute_script("arguments[0].click();", message_bar)
                except:
                    try:
                        message_bar = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, ("//textarea[contains(@placeholder,'Message')]"))))
                        Sleeping_Bot(2.5, 4.5)
                        p_driver.execute_script("arguments[0].click();", message_bar)
                    except Exception as ex:
                        logger.error(f"can't find message_bar {ex} .")

                try:
                    message_bar.send_key(formated_msg)
                    Sleeping_Bot(7.5, 9.5)
                    message_bar.sendKeys(Keys.ENTER)
                    Sleeping_Bot(10.5, 12.5)
                    cpt += 1
                except Exception as ex:
                    logger.error(f"can't write and send the message {ex} .")

                cpt += 1

                # We update the database
                with lock:
                    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                    sqlite_cursor = sqlite_connection.cursor()
                    sqlite_cursor.execute(
                        "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        ("instagram", "sent_message", formated_msg, p_username, new_contact[1], datetime.today(),
                         id_message, p_taskuser_id, "texte"))


def dateCheck():
    dates = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//time[@datetime]"))))
    with lock:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        last_date = sqlite_cursor.execute(
            "SELECT min(date_created) FROM actions WHERE platform = ? AND message IS NOT ?", ("instagram", None))

        last_date = str(last_date)
        new_last_date = last_date[:len(last_date) - 9]

    for date in dates:
        date = str(date)
        new_date = date[:len(date) - 14]

        if new_date <= new_last_date:
            stop_scrolling = True
        else:
            stop_scrolling = False

    return stop_scrolling


def scrollDown(listEnd, driver, contactList, lastPosition, stop_scrolling):
    """
        scroll down the list of contacts and return a list with the new last position and if we are at the end
        of the list of contact
    """
    if not listEnd and stop_scrolling:
        list_result[listEnd, lastPosition, stop_scrolling]
        p_driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight', contactList)
        Sleeping_Bot(0.5, 5.0)
        newPosition = driver.execute_script(
            'return arguments[0].scrollHeight', contactList)
        if newPosition == lastPosition:
            listEnd = True
            stop_scrolling = dateCheck()
        lastPosition = newPosition

        list_result[0] = listEnd
        list_result[1] = lastPosition
        list_result[2] = stop_scrolling

    return list_result


'''
Random time.sleep to avoid being detected as a bot.
'''


def Sleeping_Bot(borne_inf=float, borne_sup=float):
    sleep_time = random.uniform(borne_inf, borne_sup)
    sleep_time = round(sleep_time, 2)
    sleep(sleep_time)


'''

'''


def Cold_Messaging_Instagram_Followers_Of_Accounts(p_browser, p_taskuser_id, Instagram_username, p_driver,
                                                   p_quantity_actions, label_log, lock):
    logger.info("=== [1] Open Browser =======================================")

    # Page loading
    # Try 5 times before print an error message (Network issue ?)
    count = 0
    while (count != (-1)):
        try:
            p_driver.get("https://www.instagram.com/direct/inbox/")
            Sleeping_Bot(7.5, 10.5)
            count = -1
        except Exception as ex:
            count += 1
            Sleeping_Bot(7.5, 10.5)
            if (count >= 5):
                count = -1
                logger.error(f"Error : Can't access the website : {ex}")

    Cold_Messaging_Platform_id(p_browser, p_taskuser_id, Instagram_username, p_quantity_actions, label_log, lock)


########################################################################################################################
"""

p_browser = "Firefox"

if p_browser == "Chrome":
    p_driver = mymodulesteam.ChromeDriverWithProfile()
elif p_browser == "Firefox":
    p_driver = mymodulesteam.FireFoxDriverWithProfile()
else:
    logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

p_taskuser_id = "3412"
p_quantity_actions = "20"
label_log = ""
lock = threading.Lock()
p_username = ""

start = datetime.today()
Instagram_username = "toto"
Cold_Messaging_Instagram_Followers_Of_Accounts(p_browser, p_taskuser_id, Instagram_username, p_driver, p_quantity_actions, label_log, lock)

end = datetime.today()
print(f"\\\\\ RUN DURATION : |{start}|---|{end}| /// ")

"""
'''
example spreadsheet:

https://docs.google.com/spreadsheets/d/11rkELpW8_1p-s9-uvYym0hC-SB0dT3T0DLJYpsvpu0g/edit?usp=sharing
'''
