import datetime
import json
import sqlite3
import logging
import threading
import time

from modules import mymodulesteam
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import random
import re

from selenium.webdriver.common.keys import Keys

# -*- coding: utf-8 -*-


"""
Author : Alexis Lafaye
Email : lafaye.alexis@gmail.com
"""


global driver
# Debug const : Set to True so the script won't click on the Send message button
const_debug = True  # !!!!!!!!!!!!!!!!!!!!!!!!!!!! SET TO FALSE WHEN TASK FINISHED AND TESTED !!!!!!!!!!!!!!!!!!!!!!!!!!!!
global g_actions_count
global g_username
global g_lock
global g_taskuser_id
global g_details_task
global g_last_msg_AB
global g_quantity_actions

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('Cold_Messaging_Reddit_Members_of_groups')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ==================== DATABASE METHODS ==================================================

def DB_Add_Action(message: str, id_contact: int, msg_id: str):
    """
        Cette méthode ajoute une nouvelle action dans la base de données

        :param message: Le message envoyé
        :param id_contact: ID du destinataire dans la base de donnée
        :param msg_id: id du message envoyé, ex: "message_txt_1A" ou "1A"

        :return: True si succés, None en cas d'erreur
    """

    if len(msg_id) == 2:
        msg_id = f"message_txt_{msg_id}"

    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            sqlite_cursor.execute(
                "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_message, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("reddit", "send_message", message, g_username, id_contact, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), msg_id, g_taskuser_id, "texte"))
            sqlite_connection.commit()
            sqlite_connection.close()
            return True
    except Exception as ex:
        logger.error(f"Error while updating database: {ex}")
        return None

def DB_Add_Contact(username):
    """
        Cette méthode ajoute un nouveau contact dans la base de données s'il n'existe pas déjà

        :param username: username du contact

        :return: True si succés, False si contact déjà existant, None si erreur
    """

    try:
        if not DB_Check_Contact_Exist(username):
            with g_lock:
                sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                sqlite_cursor = sqlite_connection.cursor()
                sqlite_cursor.execute(
                    "INSERT INTO contacts (platform, username, replied, date_created) VALUES(?, ?, ?, ?)",
                    ("reddit", username, 0, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
                sqlite_connection.commit()
                sqlite_connection.close()
                return True
        else:
            return False
    except Exception as ex:
        logger.error(f"Error while updating database: {ex}")
        return None

def DB_Check_Contact_Exist(username):
    """
        Vérifie si un contact existe dans la base de données

        :param username: username du contact à check

        :return: True si existant, False sinon, None si erreur
    """

    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            check_exist = sqlite_cursor.execute("SELECT username FROM contacts WHERE username=? AND platform='reddit'",
                                                [username]).fetchall()
            if len(check_exist) == 0:
                sqlite_connection.close()
                return False
            else:
                sqlite_connection.close()
                return True
    except Exception as ex:
        logger.error(f"Error while accessing database: {ex}")
        return None

def DB_Get_Contact_ID(username):
    """
        Obtenir l'ID d'un contact à partir de son username

        :param username: username du contact

        :return: ID du contact dans las base de données, ou None si erreur/contact inexistant
    """

    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            contact = sqlite_cursor.execute("SELECT id FROM contacts WHERE username=? AND platform='reddit'", [username]).fetchall()
            if len(contact) == 0:
                sqlite_connection.close()
                return None
            else:
                sqlite_connection.close()
                return contact[0][0]
    except Exception as ex:
        logger.error(f"Error while accessing database: {ex}")
        return None

def DB_Set_Contact_Replied(contact_id, replied, reply_msg=""):
    """
        Définit si un contact a répondu ou non dans la base de données.

        :param contact_id: ID du contact dans la base de données
        :param replied: True ou False
        :param reply_msg: Si replied est True, passer le texte de la réponse à cet argument

        :return: True si succés, False si erreur
    """

    if replied:
        replied_nb = 1
        if reply_msg != "":
            # Add replied Action

            try:
                with g_lock:
                    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                    sqlite_cursor = sqlite_connection.cursor()
                    sqlite_cursor.execute(
                        "INSERT INTO actions (platform, type_action, message, id_social_account, id_contact, date_created, id_task_user, type_message) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        ("reddit", "message_received", reply_msg, g_username, contact_id, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), g_taskuser_id, "texte"))
                    sqlite_connection.commit()
                    sqlite_connection.close()
                    return True
            except Exception as ex:
                logger.error(f"Error while updating database: {ex}")
    else:
        replied_nb = 0
    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            sqlite_cursor.execute("UPDATE contacts SET replied=?, date_update=? WHERE id=? and platform='reddit'",
                (replied_nb, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), contact_id))
            sqlite_connection.commit()
            sqlite_connection.close()
            return True
    except Exception as ex:
        logger.error(f"Error while updating database: {ex}")
        return False

def DB_Get_Last_Actions():
    """
        Récupérer les messages déjà envoyés

        :return: Liste d'éléments sous la forme (username, message, id_message, replied, date_created, type_action)
    """

    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            messages = sqlite_cursor.execute(
                "SELECT username, message, id_message, contacts.replied, actions.date_created, type_action FROM contacts INNER JOIN actions ON contacts.id=id_contact WHERE actions.platform='reddit' ORDER BY actions.date_created DESC"
            ).fetchall()
            sqlite_connection.close()
            return messages
    except Exception as ex:
        logger.error(f"Error while accessing database: {ex}")
        return None




# ==================== UTILITY METHODS ==================================================

def Remove_User_From_Queue(user, queue):
    """
        Supprime toutes les occurences concernant 'user' dans la liste 'queue' puis la renvoie

        :param user: Nom d'utilisateur à supprimer
        :param queue: Liste à modifier

        :return: Liste modifiée
    """

    new_queue = []
    for elem in queue:
        if elem[0] != user:
            new_queue.append(elem)
    return new_queue

def Get_First_Message_ID():
    """
        Renvoie l'ID réduit du prochain premier message en fonction du test A/B ou pas

        :return: '1A' ou '1B'
    """

    if g_details_task['AB_testing_enable'] == 1:
        if g_last_msg_AB == 'A':
            return "1B"
        else:
            return "1A"
    else:
        return "1A"

def Get_Reduced_Message_ID(full_msg_id):
    """
        Transforme 'message_txt_1A' --> '1A'
    """

    msg_id = full_msg_id[len(full_msg_id) - 2:]
    return msg_id

def Next_AB():
    """
        Définit le prochain message à envoyer sur A ou B
    """

    if g_details_task['AB_testing_enable'] == 1:
        global g_last_msg_AB
        if g_last_msg_AB == 'A':
            g_last_msg_AB = 'B'
        else:
            g_last_msg_AB = 'A'

def Get_Delay(msg_id):
    """
        Retourne le délai avant le prochain message

        :param msg_id: ID du message déjà envoyé

        :return: objet timedelta
    """

    if len(msg_id) > 2:
        msg_id = Get_Reduced_Message_ID(msg_id)

    delay_type = g_details_task[f'time_delay_{msg_id}_type']
    delay = g_details_task[f'time_delay_{msg_id}']

    if delay_type == "hours":
        return datetime.timedelta(hours=delay)
    elif delay_type == "days":
        return datetime.timedelta(days=delay)
    elif delay_type == "weeks":
        return datetime.timedelta(weeks=delay)
    elif delay_type == "months":
        return datetime.timedelta(days=round(30.4167*delay))
    else:
        logger.error(f"Unrecognized delay type: {delay_type}\n"
                     f"Default delay of 2 days will be used.")
        return datetime.timedelta(days=2)

def Get_Next_Message_ID(msg_id):
    """
        Renvoie l'ID du prochain message à envoyer à partir de l'ID du dernier message envoyé.
        Renvoie None si le dernier message envoyé est le dernier de la liste.
        Supporte les ID complets 'message_txt_1A' et réduits '1A'.

        :param msg_id: ID complet ou réduit du dernier message envoyé

        :return: ID complet ou réduit du prochain message à envoyer, ou None si pas de prochain message
    """

    reduced = True

    if len(msg_id) > 2:
        msg_id = Get_Reduced_Message_ID(msg_id)
        reduced = False
    msg_nb = int(msg_id[0])
    msg_nb += 1
    full_msg_id = f"message_txt_{msg_nb}{msg_id[1]}"
    if full_msg_id in g_details_task.keys():
        if g_details_task[full_msg_id] != "":
            if reduced:
                return f"{msg_nb}{msg_id[1]}"
            else:
                return full_msg_id
        else:
            return None
    else:
        return None

def Get_Message(msg_id, username):
    """
        Renvoie le message correspondant à l'ID passé

        :param msg_id: ID du message, ex: '1A' ou '3B'
        :param username: Nom d'utilisateur pour formater le message

        :return: Message formaté
    """

    if len(msg_id) > 2:
        msg_id = Get_Reduced_Message_ID(msg_id)
    msg = g_details_task[f'message_txt_{msg_id}']
    return mymodulesteam.TransformMessage(msg, username=username)

def Send_Delayed_Keys(web_elem, text):
    """
    Simule la saisie de texte d'un humain
    """

    for char in text:
        web_elem.send_keys(char)
        time.sleep(random.uniform(0.01, 0.1))




# ==================== ACTION METHODS ==================================================

def Check_Replies(from_window, username):
    """
        Ouvre la page des messages Reddit et vérifie dans les conversations ouvertes si des contacts ont répondu

        :param from_window: Numéro de la fenêtre qui appelle cette fonction
        :param username: username de la personne exécutant le script

        :return: True si succés, False si erreur/pas de messages
    """

    logger.info("\n--- Checking replies ---\n")

    driver.execute_script("window.open('" + "https://old.reddit.com/chat/" + "');")
    windows = driver.window_handles
    driver.switch_to.window(windows[len(windows) - 1])

    # Get list of convs

    try:
        convs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a/div[1]/h4[1]/span[1]")))
    except:
        logger.info(f"No conversations to check replies")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    for elem in convs:
        driver.execute_script("arguments[0].click();", elem)

        time.sleep(random.uniform(2,4))

        conv_username = elem.text

        # Only way to get username of messages is through profile pics placeholders

        try:
            messages_imgs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//span//span//img")))
        except:
            logger.error(f"Can't get messages")
            driver.close()
            driver.switch_to.window(driver.window_handles[from_window])
            return False

        # 'alt' attribute looks like 'UsernameOfSender Snoovatar' so we only need the first word
        last_msg_username = messages_imgs[len(messages_imgs) - 1].get_attribute('alt').split(" ")[0]

        if last_msg_username.lower() != username.lower():
            logger.info(f"{conv_username} has replied")

            # Check if the last action concerning this contact is a reply

            last_actions = DB_Get_Last_Actions()

            add_db = False

            for action in last_actions:
                if action[0] == conv_username:
                    if action[5] == "message_received":
                        add_db = False
                        break
                    else:
                        add_db = True
                        break

            if add_db:
                # Get message text

                try:
                    msg_txt_pres = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                        (By.XPATH, "//pre")))
                except:
                    logger.error(f"Can't get messages")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[from_window])
                    return False

                DB_Set_Contact_Replied(DB_Get_Contact_ID(conv_username), True, reply_msg=msg_txt_pres[len(msg_txt_pres) - 1].text)
            else:
                DB_Set_Contact_Replied(DB_Get_Contact_ID(conv_username), True)

        else:
            logger.info(f"{conv_username} has not replied")
            DB_Set_Contact_Replied(DB_Get_Contact_ID(conv_username), False)

        time.sleep(random.uniform(2,3))

    logger.info("\n--- Finished Checking replies ---\n")
    driver.close()
    driver.switch_to.window(driver.window_handles[from_window])
    return True

def Planned_Messages():
    """
        Cette méthode envoie des messages aux personnes déjà contactées en respectant les règles et délais établis

        :return: True si limite d'actions atteinte, False sinon
    """

    logger.info("\n--- Send planned messages ---\n")

    message_queue = DB_Get_Last_Actions()

    while g_actions_count < g_quantity_actions and len(message_queue) > 0:
        """
        Mémo :
            [0] : username
            [1] : message
            [2] : id_message
            [3] : replied
            [4] : date_created ( 2021-05-31 10:08:30 )
            [5] : type_action ('send_message' ou 'message_received')
        """

        elem = message_queue[0]

        if elem[5] == "message_received":
            message_queue.remove(elem)
            continue

        next_msg_id = Get_Next_Message_ID(elem[2])

        if next_msg_id is None:     # The last message sent was the last in the list
            message_queue = Remove_User_From_Queue(elem[0], message_queue)
            continue

        # Check for delay

        delay = Get_Delay(elem[2])
        date_created = datetime.datetime.strptime(elem[4], '%Y-%m-%d %H:%M:%S')
        date_to_send = date_created + delay

        should_send = False

        if datetime.datetime.now() >= date_to_send:     # Delay has passed
            if g_details_task['serie_type'] == "until_reply":
                if elem[3] == 1:    # user has replied
                    logger.info(f"Delay has passed for {elem[0]}, but user has replied.")
                    should_send = False
                else:
                    should_send = True
                    logger.info(f"Delay has passed for {elem[0]}")
            else:
                should_send = True
        else:
            logger.info(f"Delay for {elem[0]} has not passed.")

        if should_send:
            Send_Message(elem[0], next_msg_id, 0, debug=const_debug)

        message_queue = Remove_User_From_Queue(elem[0], message_queue)

    logger.info("\n--- Finished planned messages ---\n")

    if g_actions_count >= g_quantity_actions:
        return True
    else:
        return False

def First_Messages(url_list):
    """
        Cette méthode gère l'envoi de messages à des nouveaux contacts

        :param url_list: Liste des URL des communautés à parcourir

        :return: True une fois la limite atteinte, ou False en cas d'erreur
    """

    logger.info("\n--- Send first messages ---\n")

    for url in url_list:
        if url[len(url) - 1] != '/':
            url += '/'
        logger.info(f"\n========== New Community : {re.search('reddit.com/(.*)/', url).group(1)} ==========\n")

        # Page loading
        # Try 5 times before print an error message (Connexion's problemes ?)
        count = 0
        while count != -1:
            try:
                driver.get(url)
                time.sleep(random.uniform(7, 10))
                count = -1
            except Exception as ex:
                count = count + 1
                time.sleep(random.uniform(7, 10))
                if count >= 5:
                    count = -1
                    logger.error(f"Error when getting access to the website : {ex}")

        while g_actions_count < g_quantity_actions:
            # Get all the posts
            try:
                post_list = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@id='siteTable']/*[contains(@data-promoted, 'false')]"))
                    # This XPath doesn't take promoted posts
                )
            except Exception as ex:
                logger.error(f"Error while trying to get posts : {ex}")
                return False

            for elem in post_list:  # Looping through all posts
                # Scroll to the post
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)

                # Check post creation date
                try:
                    date_string = elem.find_element_by_xpath("./div[2]/div[1]/p[2]/time[1]").get_attribute("datetime")[:10]
                    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
                except Exception as ex:
                    logger.error(f"Error getting post's date, we'll try to process the post anyways : {ex}")
                    date = datetime.datetime.now()
                delta = datetime.datetime.now() - date

                if delta.days >= 365:
                    logger.info("Post skipped because too old. (> 1 year)")
                    continue  # We skip the post if it's too old : people may not be interested/active anymore (this can happen with pinned posts)

                # Get comments link
                try:
                    comment_link = elem.find_element_by_xpath(
                        ".//a[@data-event-action='comments']")
                except Exception as ex:
                    logger.error(f"Error while getting comments link: {ex}")
                    continue

                driver.execute_script("window.open('" + comment_link.get_attribute("href") + "');")
                windows = driver.window_handles
                driver.switch_to.window(windows[1])

                if Browse_Post():
                    return True

                driver.close()
                driver.switch_to.window(windows[0])

            try:
                next_span = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//span[@class='next-button']")))
                next_link = next_span.find_element_by_xpath(".//a")
            except Exception as ex:
                logger.error(f"Error getting next page link: {ex}")
                return False

            driver.execute_script("arguments[0].click();", next_link)

    return True

def Browse_Post():
    """
        Cette méthode est appelée après l'ouverture d'un post.
        Elle va parcourir le post et envoyer des messages à l'auteur et aux commenters

        :return: True si limite atteinte, False sinon
    """

    logger.info("\n--- [Browsing a new post] ---\n")
    global g_actions_count

    # Get the author

    author_link = None
    try:
        author_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[1]")))
    except Exception as ex:
        logger.error(f"Error while getting author : {ex}")

    if author_link is not None:
        author = author_link.get_attribute("data-author")
        if not DB_Check_Contact_Exist(author):
            if Send_Message(author, Get_First_Message_ID(), 1, debug=const_debug):
                if g_actions_count >= g_quantity_actions:
                    return True
                Next_AB()
        else:
            logger.info(f"\n- Already sent a message to {author}. -\n")

    """
        J'avais écris le code ci-dessous pour dérouler tous les liens "charger plus de commentaires" sur les posts avec
        beaucoup de commentaires, mais finalement je pense que ce n'est pas utile étant donné que sans les charger il y
        a déjà plusieurs centaines de commentaires affichés. Comme cette étape prenait du temps je l'ai enlevée, mais je
        laisse le code commenté au cas où il servirait.
    """

    # # Get the 'load more' links
    # try:
    #     more_list = WebDriverWait(driver, 10).until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//div[@data-type='morechildren']/div[1]/span[1]/a[1]")))
    # except:
    #     more_list = []
    #
    # # Expand all comments (click on all 'load more comments')
    # # This can be very long in big communities : approx. 5 mins for a post with 5348 comments
    # start_time = datetime.datetime.now()
    # logger.info("Loading all comments ...")
    # while len(more_list) > 0:
    #     if (datetime.datetime.now() - start_time).seconds > 90:     # Time limit of 90 secs as this can be very long in big communities
    #         logger.info("Loading is too long, stopping.")
    #         more_list = []
    #         continue
    #     last_more = more_list[len(more_list) - 1]
    #     try:
    #         if last_more.text == "":
    #             more_list.remove(last_more)     # Removing elements causing bug
    #             continue
    #         if not "red" in last_more.get_attribute("style"):
    #             driver.execute_script("arguments[0].scrollIntoView(true);", last_more)  # Scroll to the last 'Load more' so we can load all comments
    #             driver.execute_script("arguments[0].click();", last_more)
    #         else:
    #             driver.execute_script("arguments[0].click();", last_more)   # Sometimes we need to click several times before comments load (reddit bug)
    #             time.sleep(0.5)     # TODO: Faire plus de tests sur différents systèmes, ce délai est peu être à changer
    #     except:
    #         pass
    #     time.sleep(0.1)
    #
    #     try:
    #         more_list = WebDriverWait(driver, 10).until(
    #             EC.presence_of_all_elements_located((By.XPATH, "//div[@data-type='morechildren']/div[1]/span[1]/a[1]")))
    #     except:
    #         more_list = []

    # Get the comments

    try:
        comment_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@data-type='comment']"))
        )
    except Exception as ex:
        logger.info(f"No comment in this post.")
        return False

    # Get all commenters usernames
    all_commenters = []
    for elem in comment_list:
        all_commenters.append(elem.get_attribute("data-author"))

    total_comments = len(all_commenters)
    all_commenters = list(dict.fromkeys(all_commenters))  # Remove duplicates
    random.shuffle(all_commenters)
    print(f"Found {len(all_commenters)} unique commenters in {total_comments} comments")

    for author in all_commenters:
        if not DB_Check_Contact_Exist(author):
            if Send_Message(author, Get_First_Message_ID(), 1, debug=const_debug):
                if g_actions_count >= g_quantity_actions:
                    return True
                Next_AB()
            time.sleep(1)
        else:
            logger.info(f"\n- Already sent a message to {author}. -\n")

    return False

def Send_Message(username: str, msg_id: str, from_window, debug = False):
    """
        Cette méthode va préparer et envoyer des messages

        :param username: Nom de l'utilisateur reddit
        :param msg_id: ID du message.
        :param from_window: Numéro de la fenêtre qui appelle cette fonction
        :param debug: Si True, la fonction ne clique pas sur le bouton Envoyer (pour ne pas spam de messages pendant les tests)

        :return: True si le message a été envoyé, False sinon
    """

    message = Get_Message(msg_id, username)

    if message == "" or message is None:
        logger.error("Cannot send an empty message.")
        return False

    if username == "" or username is None:
        logger.error("No username provided to send message.")
        return False

    if username.lower() == g_username.lower():  # We don't send a message to ourself
        return False

    if username == "AutoModerator":
        return False

    logger.info(f"-- Sending a message to {username} --")

    driver.execute_script("window.open('" + "https://old.reddit.com/chat/channel/create" + "');")
    windows = driver.window_handles
    driver.switch_to.window(windows[len(windows) - 1])

    time.sleep(random.uniform(2, 3))

    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,"//input[@type='text']")))

    try:
        # input_box.send_keys(username)
        Send_Delayed_Keys(input_box, username)
    except Exception as ex:
        logger.error(f"Error while typing username: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    time.sleep(random.uniform(2, 3))

    try:
        div_user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/main[1]/form[1]/div[1]/div[1]/div[3]/div[2]")))
    except:
        logger.info(f"Can't send message to this user either because of privacy settings or account restriction")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False


    # There are 2 cases :
    #   - The user is known, so there are 2 clickable labels
    #   - The user is unknown, so there is 1 clickable label
    # div_user here is set to the div containing the label in the 2nd case.
    # So, if its child element isn't our label, we know we're in the first case.

    div_child_element = div_user.find_element_by_xpath("./*")

    if "label" not in div_child_element.tag_name:
        try:
            div_user = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/form[1]/div[1]/div[1]/div[3]/div[3]")))
        except Exception as ex:
            logger.info(f"Can't send message to this user either because of privacy settings or account restriction")
            driver.close()
            driver.switch_to.window(driver.window_handles[from_window])
            return False

    label_user = div_user.find_element_by_xpath("./label")

    try:
        driver.execute_script("arguments[0].click();", label_user)
    except Exception as ex:
        logger.error(f"Error while clicking on user: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    time.sleep(random.uniform(1, 2))

    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    try:
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as ex:
        logger.error(f"Error while clicking on 'Start a Chat' button: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    time.sleep(random.uniform(2, 3))

    try:
        textarea_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Message']")))
    except Exception as ex:
        logger.error(f"Error while getting message field: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    try:
        textarea_message.clear()
    except Exception as ex:
        logger.error(f"Error while clearing message: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])

    for index, sub_message in enumerate(message.split('\n')):
        try:
            # textarea_message.send_keys(sub_message)
            Send_Delayed_Keys(textarea_message, sub_message)
        except Exception as ex:
            logger.error(f"Error while typing message: {ex}")
            driver.close()
            driver.switch_to.window(driver.window_handles[from_window])
            return False
        if index < len(message.split('\n')) - 1:
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

    time.sleep(random.uniform(2, 3))

    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    try:
        # driver.execute_script("arguments[0].click();", submit_button)
        if debug:
            print("- [Sending message is disabled during test] -")
        else:
            driver.execute_script("arguments[0].click();", submit_button)
    except Exception as ex:
        logger.error(f"Error clicking send message button: {ex}")
        driver.close()
        driver.switch_to.window(driver.window_handles[from_window])
        return False

    time.sleep(random.uniform(2, 4))

    # Update DB
    if not DB_Add_Contact(username):
        DB_Set_Contact_Replied(DB_Get_Contact_ID(username), False)
    DB_Add_Action(message, DB_Get_Contact_ID(username), msg_id)

    driver.close()
    driver.switch_to.window(driver.window_handles[from_window])

    global g_actions_count
    g_actions_count += 1

    logger.info(f"\n- Actions : [{g_actions_count}/{g_quantity_actions}] -\n")

    return True




# ==================== MAIN METHOD ==================================================

def Cold_Messaging_Reddit_Members_of_groups(p_browser, p_taskuser_id, p_username, p_quantity_actions, lock):
    """
        Méthode principale qui est appelée au début de la tâche.
        Elle va appeler les autres méthodes pour automatiser l'envoi de messages
        aux membres d'une liste de groupes Reddit.

        :param p_browser: Navigateur à utiliser : 'Firefox' ou 'Chrome'
        :param p_taskuser_id: ID de la tâche
        :param p_username: username de la personne qui exécute la tâche
        :param p_quantity_actions: Nombre de messages max à envoyer. Le script s'arrête une fois cette limite atteinte
        :param lock: lock pour accés à la base de données

        :return: True si execution terminée, False si erreur
    """
    # on va récupérer les détails de la tache
    # Pas d'ID task pour l'instant, je récupère un fichier custom
    # details_task = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    details_task_file = open("details_task.json", 'r')
    details_task = json.load(details_task_file)
    url_list_gsheet = details_task["url_list"]
    # logger.info(f"details_task : {details_task}")
    gsheet_id = re.search('/d/(.*)/', url_list_gsheet).group(1)

    logger.info(f"Retrieving URLs list from {url_list_gsheet}")
    try:
        url_list = mymodulesteam.GoogleSheetGetValues(gsheet_id)
    except Exception as ex:
        logger.critical(f"Error getting URLs from GSheet : {ex}\nAborting.")
        return False

    # We must use the old reddit, much easier for us
    # We change URL to old reddit
    for i in range(len(url_list)):
        url_list[i] = url_list[i][0].replace("https://www", "https://old")

    # print(url_list)

    global driver
    global g_actions_count
    global g_username
    global g_lock
    global g_taskuser_id
    global g_details_task
    global g_last_msg_AB
    global g_quantity_actions
    g_actions_count = 0
    g_username = p_username
    g_lock = lock
    g_taskuser_id = p_taskuser_id
    g_details_task = details_task
    g_quantity_actions = p_quantity_actions

    # Get if last first message sent was A or B
    last_actions = []
    try:
        with g_lock:
            sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            last_actions = sqlite_cursor.execute(
                "SELECT id_message FROM actions WHERE platform='reddit' AND type_action='send_message' ORDER BY date_created DESC").fetchall()
            sqlite_connection.close()
    except Exception as ex:
        logger.error(f"Error while accessing database: {ex}")

    # print(last_actions)
    if len(last_actions) > 0:
        msg_id = Get_Reduced_Message_ID(last_actions[0][0])
        if '1' in msg_id:
            if 'A' in msg_id:
                g_last_msg_AB = 'A'
            else:
                g_last_msg_AB = 'B'
        else:
            g_last_msg_AB = ''
    else:
        g_last_msg_AB = ''


    # open the browser
    try:
        if p_browser == "Chrome":
            driver = mymodulesteam.ChromeDriverWithProfile()
        elif p_browser == "Firefox":
            driver = mymodulesteam.FireFoxDriverWithProfile()
        else:
            logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
    except Exception as ex:
        logger.error(f"Error when opening the browser : {ex}")
        return False

    driver.implicitly_wait(10)

    Check_Replies(0, p_username)

    if Planned_Messages():
        logger.info("\n========== Max number of actions reached, stopping. ==========")
        driver.quit()
        return True

    if First_Messages(url_list):
        logger.info("\n========== Max number of actions reached, stopping. ==========")
        driver.quit()
        return True

    driver.quit()
    return True



# ======================== EXECUTION DE LA TACHE ==================================
"""
_browser = "Chrome"
_taskuser_id = 1337     # ID random temporaire
_username = "skreenager42"      # Bien penser à mettre son propre username reddit
_quantity_actions = 5

_lock = threading.Lock()

Cold_Messaging_Reddit_Members_of_groups(_browser, _taskuser_id, _username, _quantity_actions, _lock)
"""
