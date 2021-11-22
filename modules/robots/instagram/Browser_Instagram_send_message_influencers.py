# -*- coding: utf-8 -*-
"""
Author : Thi Phan
Email : thiphan94@gmail.com
"""

import logging
import threading
import time
import sys
import sqlite3
import pathlib
import platform
import psutil
import random
import datetime
from datetime import timedelta
import re

sys.path.append("..")
sys.path.append(".")
from modules import mymodulesteam
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Scrap_Craigslist_accounts__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
)
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def Sleeping_Bot(borne_inf=float, borne_sup=float):
    """Random time.sleep for being a stealth bot."""
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)


def get_keyword_city(keywords_list):
    """Returns a key and a list of cities."""
    if keywords_list is None:
        logger.info(f"Keyword / City spreadsheet not found")
        return False
    return mymodulesteam.GoogleSheetGetValues(
        mymodulesteam.extract_ss_id_regex(keywords_list)
    )


def scraping_accounts(driver,lock):
    """Elements for scraping."""
    try:
        # username of account
        username = driver.find_element_by_css_selector(".fDxYl").text
        # header_full_name of account
        try:
            insta_header_full_name = driver.find_element_by_css_selector(".rhpdm").text
        except Exception:
            insta_header_full_name = None
        # header_biz_category of account
        try:
            insta_header_biz_category = driver.find_element_by_css_selector("._8FvLi").text
        except Exception:
            insta_header_biz_category = None
        # insta_bio of account
        try:
            insta_bio = driver.find_element_by_css_selector(".-vDIg>span").text
        except Exception:
            insta_bio = None
        # insta_website of account
        try:
            insta_website = driver.find_element_by_css_selector(".yLUwa").text
        except Exception:
            insta_website = None
        # current day time
        date_n_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        platform_name = "instagram"
        # type_action
        action = "scrap"
        followed = 1
        ### Scraping for contacts and actions tables ###
        id_contact = scraping_contacts_table(
            platform_name, username, followed, insta_header_full_name, insta_header_biz_category, insta_bio, insta_website, date_n_time,lock
        )
        # call function to scrape data to actions table
        scraping_actions_table(
            platform_name,
            action,
            date_n_time,
            username,
            id_contact,lock
        )
        return True
    except Exception as e:
        logger.info(f"Error while scraping data to tables '{e}' ")
        return False


def search_in_instagram(driver,keywords_list,index):
    """Search on Instagram with keywords."""
    # search bar
    input_search = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    # enter keyword in search bar
    keyword = keywords_list[index][0]
    # s = keywords_list[index][0]
    input_search.send_keys(keyword)


def check(title,lock):
    """Check if data existed in DataBase."""
    with lock:
        try:
            connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM contacts WHERE username LIKE ?", (title,)
            )
            data = cursor.fetchone()[0]
            if data == 0:
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"Error when trying to get the title in the dataBase {e}")

def follow_account(driver):
    """Check if account is influencer"""
    try:
        follow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._6VtSN")))
        follow_button.click()
    except Exception as e:
        logger.info(f"error follow {e}")

def check_follow(username,lock):
    """Check if followed."""
    with lock:
        try:
            connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM contacts WHERE username LIKE ?", (username,)
            )
            data = cursor.fetchone()[0]
            if data == 0:
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"Error when trying to get the username in the dataBase {e}")


def send_message(driver, msg):
    """Send message to new influencer."""

    msg_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Message']")))
    msg_btn.click()

    msg_bar = driver.find_element_by_css_selector("textarea[placeholder='Message...']")
    msg_bar.send_keys(msg)
    msg_bar.send_keys(Keys.ENTER)


def count_accounts(driver):
    """Count accounts of each keyword, no post, no position"""
    return WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//a[@class='-qQT3']//div[contains(@class,'rBNOH')]/div[contains(@class,'qyrsm KV-D4')]")))



def scraping_contacts_table(
    platform_name, username, followed, insta_header_full_name, insta_header_biz_category, insta_bio, insta_website, date_n_time,lock
):
    """Scrape the data to contacts table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sql = """INSERT INTO contacts (platform, username, followed, insta_header_full_name, insta_header_biz_category, insta_bio, insta_website, date_created)  VALUES (?,?,?,?,?,?,?,?)"""
            list_add = (
                platform_name, username, followed, insta_header_full_name, insta_header_biz_category, insta_bio, insta_website, date_n_time
            )
            sqlite_cursor.execute(sql, list_add)
            sqlite_connection.commit()
        # logger.info("Contacts table committed successfully.")

    except Exception as e:
        logger.error(f"Error while scraping contacts table: {e} ")
        raise Exception(e)
    id_contact = sqlite_cursor.execute(
        "SELECT id FROM contacts WHERE username = ?", (username,)
    ).fetchone()[0]
    sqlite_connection.close()
    return id_contact


def scraping_actions_table(
    platform_name,
    action,
    date_n_time,
    username,
    id_contact,lock
):
    """Scrape the data to actions table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sql = """INSERT INTO actions (platform,type_action,date,id_social_account,id_contact,date_created)  VALUES (?,?,?,?,?,?)"""
            list_add = (
                platform_name,
                action,
                date_n_time,
                username,
                id_contact,
                date_n_time,
            )
            sqlite_cursor.execute(sql, list_add)
            sqlite_connection.commit()
        # logger.info("Actions table committed successfully.")
    except Exception as e:
        logger.error(f"Error while scraping actions table: {e} ")
        raise Exception(e)
    sqlite_connection.close()

def insert_actions(platform_name,action,date_n_time,new_message,username,id_contact,id_message,id_task_user,lock):
    """Insert action to actions table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sql = """INSERT INTO actions (platform,type_action,date,message,id_social_account,id_contact,date_created,id_message, id_task_user)  VALUES (?,?,?,?,?,?,?,?,?)"""
            list_add = (
                platform_name,
                action,
                date_n_time,
                new_message,
                username,
                id_contact,
                date_n_time,
                id_message,
                id_task_user
            )
            sqlite_cursor.execute(sql, list_add)
            sqlite_connection.commit()
        logger.info("Actions table committed successfully.")
    except Exception as e:
        logger.error(f"Error while inserting action to actions table: {e} ")
        raise Exception(e)
    sqlite_connection.close()



def random_abc(text_data):
    """
    Function to replace the random_abc synonyms by one word. It will pick up randomly one of the words
    :param text_data:
    :return:
    """
    random_txt_group = re.findall("\{random_abc:(.*?)\}", text_data)
    for random_txt in random_txt_group:
        random_txt_list = random_txt.split('|')
        text_data = text_data.replace('{random_abc:' + random_txt + '}', random.choice(random_txt_list))
    return text_data

def TransformMessageTMP(old_message,p_firstname):
    """
    This function will convert the placeholders:
        {firstname},
        {username},
        These values are in table 'contacts'

        {random_abc},
        These values are in the placeholder


        {affiliate_code},
        {affiliate_url},
        {affiliate_coupon}
        These values will be handle by us
    """

    new_message = random_abc(old_message)
    new_message = new_message.replace("""{firstname}""",p_firstname)

    print(f"new_message : {new_message}")
    return new_message

def get_id_message(curr_msg_id):
    """Get id of next message."""
    old_num = int(curr_msg_id[-2])
    num = old_num + 1
    new_msg_id = curr_msg_id.replace(str(old_num), str(num))
    return new_msg_id


def get_delay_type(curr_msg_id):
    """Get delay_type of current message."""
    id_msg = int(curr_msg_id[-2])
    letter = curr_msg_id.split('_')[2][1]
    if letter == 'A':
        delay_type = f"time_delay_{id_msg}A_type"

    else:
        delay_type = f"time_delay_{id_msg}B_type"

    return delay_type


def get_delay(curr_msg_id):
    """Get delay of current message."""
    id_msg = int(curr_msg_id[-2])
    letter = curr_msg_id.split('_')[2][1]
    if letter == 'A':
        delay = f"time_delay_{id_msg}A"
    else:
        delay = f"time_delay_{id_msg}B"

    return delay


def get_id_contact(
    platform_name, username,lock
):
    """Get id contact from actions table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            id_contact = sqlite_cursor.execute(
                "SELECT id FROM contacts WHERE platform = ? AND username = ?", (platform_name,username)
            ).fetchone()[0]
            sqlite_connection.close()
    except Exception as e:
        logger.error(f"Error while get id contact: {e} ")
        raise Exception(e)
    return id_contact


def Influencers_Instagram_Influencers_21(
    p_browser, p_taskuser_id, p_username, password, p_quantity_actions, label_log, lock
):
    # on va récupérer les détails de la tache
    details_task=mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    logger.info(f"details_task : {details_task}")

    # A --- ON CONTROLE QUI A REPONDU ---------------------------------------------------------
    # --- A.1 on récupère la liste des usernames a qui on a envoyé (p_username) un message avec la date de dernier message
	# --- on récupère la liste des id_contacts
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()


    logger.info("# =========================== AVANT CHECKING REPONSES =================================")
    with lock:
        list_contacts_who_received_message = sqlite_cursor.execute("SELECT id_contact, id_social_account,id_message, date_created,replied FROM actions t1 WHERE id_task_user=? AND type_action != ? AND t1.date_created = (SELECT MAX(t2.date_created) FROM actions t2 WHERE t2.id_contact = t1.id_contact)",
            (p_taskuser_id, "last_message")).fetchall()
    logger.info(f"list_contacts_who_received_message : {list_contacts_who_received_message}")
    for contact in list_contacts_who_received_message:
        logger.info(f"contact : {contact}")

    logger.info("          ")
    logger.info("# =========================== SELENIUM CHECKING INBOX QUI A REPONDU =================================")

    # --- A.2 on ouvre la page INBOX SELENIUM
    logger.info("=== [1] Open Browser =======================================")
    # Open browser
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
    url = "https://www.instagram.com/"
    driver.get(url)
    driver.implicitly_wait(2)

    try:
        driver.get("https://www.instagram.com/direct/inbox/")
    except Exception as e:
        logger.error(f"Error when trying to get the inbox {e}")


    # # --- A.3 ON vérifie qui a répondu SELENIUM
    # # code selenium pour ouvrir inbox et controler qui a répondu

    list_new_reply = driver.find_elements_by_css_selector(".KV-D4._7UhW9.fDxYl.qyrsm.xLCgt")

    # # --- A.4 ON met à jour la table actions & contacts reply=1 et date_update=date de réponse SQLITE3
    logger.info("          ")
    logger.info("# =========================== APRES CHECKING REPONSES =================================")
    date_n_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for row in list_new_reply:
        # with lock:
        sqlite_cursor.execute(
            "UPDATE actions set replied=?, date_update=? WHERE id_task_user=? and id_social_account=?",
            (1,date_n_time,int(p_taskuser_id),row.text))
        sqlite_connection.commit()
        logger.info("# ================ UPDATE actions table DONE! ==========================")
        Sleeping_Bot(2.0, 3.0)
        sqlite_cursor.execute(
            "UPDATE contacts set replied=?, date_update=? WHERE id_task_user=? and username=?",
            (1,date_n_time,int(p_taskuser_id),row.text))
        sqlite_connection.commit()
        logger.info("# ================ UPDATE contacts table DONE! ==========================")

        # Messsage_received:
        username = row.text
        row.click()
        msg_received = driver.find_elements_by_xpath("//div[@class='   CMoMH     _8_yLp  ']//div//div//div//span")
        last_msg = (msg_received[len(msg_received)-1]).text
        id_contact = get_id_contact("instagram", username)
        id_message = sqlite_cursor.execute("SELECT id_message FROM actions WHERE id_social_account = ? AND platform = ?", (username,"instagram")).fetchone()[0]

        # inserer message de réponse
        try:
            logger.info("# on ajoute message_received")
            sqlite_cursor.execute("INSERT INTO actions (platform, type_action, date, message, id_social_account, id_contact, id_message,id_task_user) VALUES(?,?,?,?,?,?,?,?)",("instagram","message_received",date_n_time, last_msg, username, id_contact,id_message,p_taskuser_id))
            sqlite_connection.commit()
            logger.info("# ================ INSERT INTO actions DONE! ==========================")
        except Exception as e:
            logger.info(f"Error insertion {e}")
        Sleeping_Bot(2.0, 3.0)
        driver.back()
        Sleeping_Bot(2.0, 3.0)

    # # B --- ON PREPARE LA LISTE DES MESSAGES PLANIFIES A ENVOYER
    #     # 2 cas de figures:
    #        # - until_reply
    #        # - no_stop
    #
    # # --- B.1 serie_type == 'until_reply'
    if details_task['serie_type']=='until_reply':
        logger.info("          ")
        logger.info("# =========================== until_reply =================================")

        #on supprime tous les messages dans la table messaging_queue pour ceux qui ont répondu
        for row in list_new_reply:
            list_contacts_who_replied = sqlite_cursor.execute(
                "SELECT actions.id_contact, contacts.username,actions.id_message, actions.date_created,actions.replied FROM actions INNER JOIN contacts ON actions.id_contact=contacts.id WHERE actions.id_task_user=? AND actions.id_social_account=? AND actions.replied=? GROUP BY actions.id_contact ORDER BY actions.date_created DESC",
                (int(p_taskuser_id), row.text, 1)).fetchall()
            logger.info(f"list_contacts_who_replied_message : {list_contacts_who_replied}")
        for contact in list_contacts_who_replied:
            logger.info(f"contact : {contact}")
            with lock:
                remove_users_who_replied = sqlite_cursor.execute(
                    "DELETE FROM messaging_queue WHERE id_contact=? AND id_task_user=? AND id_social_account=?",
                    (int(contact[0]), int(p_taskuser_id), contact[1]))
                sqlite_connection.commit()
                logger.info("# ================ DELETE FROM messaging_queue DONE! ==========================")


        # =========================================================
        # Liste des contacts qui ont recu messsages sauf qui avec type_action "last_message"
        list_contacts_who_didnt_replied = sqlite_cursor.execute("SELECT id_contact, id_social_account,id_message, date_created,replied FROM actions t1 WHERE id_task_user=? AND type_action != ? AND (replied<>? OR replied IS ?) AND t1.date_created = (SELECT MAX(t2.date_created) FROM actions t2 WHERE t2.id_contact = t1.id_contact)",
            (int(p_taskuser_id),"last_message", 1,None)).fetchall()
        logger.info(f"list_contacts_who_didnt_replied : {list_contacts_who_didnt_replied}")
        for contact in list_contacts_who_didnt_replied:
            logger.info("--------------------------------------------")
            logger.info(f"contact who didn't reply: {contact}")

            id_prochain_message =''
            id_delay_type = get_delay_type(contact[2])
            delay_type = details_task[id_delay_type]
            print("delay type", delay_type)
            id_delay = get_delay(contact[2])
            delay = details_task[id_delay]
            print("delay", delay)
            id_prochain_message = get_id_message(contact[2])
            print("new id :", id_prochain_message)

            # On va chercher le delai d'attente
            logger.info(f"contact[3] : {type(contact[3])} - {contact[3]}")
            #on calcule le delay en temps
            if delay_type == 'days':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(days=delay)
            elif delay_type == 'months':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(months=delay)
            elif delay_type == 'hours':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(hours=delay)
            elif delay_type == 'weeks':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(weeks=delay)

            logger.info(f"date_scheduled : {date_scheduled}")


            # On ajoute les lignes dans messaging_queue

            #On teste d’abord si la ligne n’a pas déjà été ajouté précédement
            with lock:
                if not sqlite_cursor.execute("SELECT * FROM messaging_queue WHERE id_message=? AND id_contact =?  \
                 AND id_social_account=? AND id_task_user=?",(contact[2],contact[0],contact[1],p_taskuser_id)).fetchone():
                    # on ajoute les prochains messages à envoyer en fonction des délais (récupérés dans detail_task)
                    try:
                        logger.info("# on ajoute les prochains messages à envoyer en fonction des délais (récupérés dans detail_task)")
                        sqlite_cursor.execute("INSERT INTO messaging_queue (id_message,id_contact,id_social_account,schedule_date,id_task_user) VALUES(?,?,?,?,?)",(id_prochain_message,contact[0],contact[1],date_scheduled,p_taskuser_id))
                        sqlite_connection.commit()
                        logger.info("# ================ INSERT INTO messaging_queue DONE! ==========================")
                    except Exception as e:
                        logger.info(f"Error insertion {e}")
                else:
                    try:
                        logger.info("# Update new id_message to send")
                        print("id pro", id_prochain_message)
                        sqlite_cursor.execute("UPDATE messaging_queue set id_message =?, schedule_date=? WHERE id_social_account=? AND id_task_user=?",(id_prochain_message,date_scheduled,contact[1],p_taskuser_id))
                        sqlite_connection.commit()
                        logger.info("# ================ UPDATE messaging_queue DONE! ==========================")
                    except Exception as e:
                        logger.info(f"Error update {e}")


    elif details_task['serie_type']=='no_stop':

        for contact in list_contacts_who_received_message:
            logger.info("--------------------------------------------")
            logger.info(f"contact who received message: {contact}")

            id_prochain_message =''

            #on va maintenant ajouter les lignes dans messaging_queue
            # ================= QUELS MESSAGES ET QUAND =========================
            id_delay_type = get_delay_type(contact[2])
            delay_type = details_task[id_delay_type]
            print("delay type", delay_type)
            id_delay = get_delay(contact[2])
            delay = details_task[id_delay]
            print("delay", delay)
            id_prochain_message = get_id_message(contact[2])
            print("new id :", id_prochain_message)

            # On va chercher le delai d'attente
            logger.info(f"contact[3] : {type(contact[3])} - {contact[3]}")
            #on calcule le delay en temps
            if delay_type == 'days':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(days=delay)
            elif delay_type == 'months':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(months=delay)
            elif delay_type == 'hours':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(hours=delay)
            elif delay_type == 'weeks':
                date_scheduled=datetime.strptime(contact[3], '%Y-%m-%d %H:%M:%S') + timedelta(weeks=delay)

            logger.info(f"date_scheduled : {date_scheduled}")
            # On ajoute les lignes dans messaging_queue

            #On teste d’abord si la ligne n’a pas déjà été ajouté précédement
            with lock:
                if not sqlite_cursor.execute("SELECT * FROM messaging_queue WHERE id_message=? AND id_contact =?  \
                 AND id_social_account=? AND id_task_user=?",(contact[2],contact[0],contact[1],p_taskuser_id)).fetchone():
                    # on ajoute les prochains messages à envoyer en fonction des délais (récupérés dans detail_task)
                    try:
                        logger.info("# on ajoute les prochains messages à envoyer en fonction des délais (récupérés dans detail_task)")
                        sqlite_cursor.execute("INSERT INTO messaging_queue (id_message,id_contact,id_social_account,schedule_date,id_task_user) VALUES(?,?,?,?,?)",(id_prochain_message,contact[0],contact[1],date_scheduled,p_taskuser_id))
                        sqlite_connection.commit()
                        logger.info("# ================ INSERT INTO messaging_queue DONE! ==========================")
                    except Exception as e:
                        logger.info(f"Error insertion {e}")
                else:
                    try:
                        logger.info("# Update new id_message to send")
                        print("id pro", id_prochain_message)
                        sqlite_cursor.execute("UPDATE messaging_queue set id_message =?, schedule_date=? WHERE id_social_account=? AND id_task_user=?",(id_prochain_message,date_scheduled,contact[1],p_taskuser_id))
                        sqlite_connection.commit()
                        logger.info("# ================ UPDATE messaging_queue DONE! ==========================")
                    except Exception as e:
                        logger.info(f"Error update {e}")


    # C --- ON ENVOI LES MESSAGES PLANIFIES
    logger.info("          ")
    logger.info("# =========================== ON ENVOI LES MESSAGES PLANIFIES =================================")
    with lock:
        list_influencer_to_send = sqlite_cursor.execute(
            "SELECT * FROM messaging_queue ORDER BY schedule_date ASC").fetchall()
    logger.info(f"list_influencer to send messages : {list_influencer_to_send}")


    for contact in list_influencer_to_send:
        logger.info(f"contact : {contact}")
        # current day time
        date_n_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_n_time = datetime.strptime(date_n_time,'%Y-%m-%d %H:%M:%S')
        if date_n_time >= date_scheduled:
            print("Send message!")
            s = "https://www.instagram.com/" + contact[3] + "/"
            driver.get(s)
            new_message =TransformMessageTMP(details_task[contact[1]],contact[3])
            Sleeping_Bot(2.0, 3.0)
            send_message(driver, new_message)
            Sleeping_Bot(2.0, 3.0)
            if contact[1] == "message_txt_4A" or contact[1] == "message_txt_4B":
                try:
                    logger.info("# Update type action to last_message and delete row in messaging_queue")
                    insert_actions("instagram",
                    "last_message",
                    date_n_time,
                    new_message,
                    contact[3],
                    contact[2],
                    contact[1],
                    p_taskuser_id,lock
                    )
                    Sleeping_Bot(2.0, 3.0)
                    with lock:
                        sqlite_cursor.execute(
                            "DELETE FROM messaging_queue WHERE id_contact=? AND id_task_user=? AND id_social_account=?",
                            (int(contact[2]), int(p_taskuser_id), contact[3]))
                        sqlite_connection.commit()
                        logger.info("# ================ DELETE FROM messaging_queue DONE! ==========================")

                except Exception as e:
                    logger.info(f"Error update {e}")
            else:
                insert_actions("instagram",
                "message_sent",
                date_n_time,
                new_message,
                contact[3],
                contact[2],
                contact[1],
                p_taskuser_id,lock
                )
                Sleeping_Bot(2.0, 3.0)


    index=0
    cpt=0
    # vérifier si il/elle est influencer
    check_follower = details_task["minimum"]
    keywords_list = get_keyword_city(details_task["url_keywords"])
    new_message =""
    while cpt<p_quantity_actions:
        try:
            for key in keywords_list:
                driver.get("https://www.instagram.com/")
                try:
                    search_in_instagram(driver,keywords_list,index)
                    Sleeping_Bot(2.0, 3.0)
                    list_accounts = count_accounts(driver)
                    counter_account = len(list_accounts)
                    print(counter_account)

                    for j in range(0, counter_account):
                        try:
                            if not check(list_accounts[j].text,lock):
                                scraped = False
                                list_accounts[j].click()
                                Sleeping_Bot(2.0, 3.0)
                                count_followers = driver.find_element_by_css_selector("[title]").text
                                count_followers = count_followers.replace(',', '')

                                user_name = driver.find_element_by_tag_name("h2")
                                if (int(count_followers) >= check_follower) and not check_follow(user_name.text):
                                    follow_account(driver)
                                    scraped = scraping_accounts(driver,lock)
                                    if scraped:
                                        cpt += 1
                                        Sleeping_Bot(2.0, 3.0)
                                        print("Start scraping!")
                                        Sleeping_Bot(1.0, 2.0)
                                        if cpt%2 !=0:
                                            new_message =TransformMessageTMP(details_task['message_txt_1A'],user_name.text)
                                            id_message = "message_txt_1A"
                                        else:
                                            new_message =TransformMessageTMP(details_task['message_txt_1B'],user_name.text)
                                            id_message = "message_txt_1B"
                                        send_message(driver,new_message)
                                    else:
                                        # --- D.3 Envoi message 1A
                                        new_message =TransformMessageTMP(details_task['message_txt_1A'],user_name.text)
                                        id_message = "message_txt_1A"
                                        send_message(driver,new_message)
                                    user_name = driver.find_element_by_css_selector(".eGOV_.ybXk5 .vy6Bb")
                                    id = get_id_contact(
                                        'instagram', user_name.text
                                    )
                                    insert_actions("instagram",
                                    "message_sent",
                                    date_n_time,
                                    new_message,
                                    user_name.text,
                                    id,
                                    id_message,
                                    p_taskuser_id,lock)
                                    Sleeping_Bot(1.0, 2.0)
                                    search_in_instagram(driver,keywords_list,index)
                                    Sleeping_Bot(2.0, 3.0)
                                    list_accounts = count_accounts(driver)
                                else:
                                    print("He/She isnt influencer")
                                    search_in_instagram(driver,keywords_list,index)
                                    Sleeping_Bot(2.0, 3.0)
                                    list_accounts = count_accounts(driver)
                            else:
                                logger.info(f"Scraped")


                        except Exception as e:
                            logger.info(f"Error check {e}")

                        Sleeping_Bot(2.0, 4.0)

                    index += 1
                except Exception as e:
                    logger.info(f"Error while Scraping in Instagram: {e}")

        except Exception as e:
            logger.error(
                f"Error while executing Scraping_Craigslist_Scrap_Craigslist_accounts_23(): {e}"
            )
            return False

#
# lock = threading.Lock()
# p_browser = "Firefox"
# p_taskuser_id =267
# p_driver = ""
# p_username=""
# password = ""
# label_log = ""
# p_quantity_actions = 5
#
#
# Influencers_Instagram_Influencers_21(
#     p_browser, p_taskuser_id, p_username, password, p_quantity_actions, label_log, lock
# )
