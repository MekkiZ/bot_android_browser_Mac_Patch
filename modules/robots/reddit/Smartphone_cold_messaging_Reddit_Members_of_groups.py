import datetime
import json
import sqlite3
import logging
import threading
import time
import subprocess

import mymodulesteam
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import random
import re

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



#==========================================================================================================
#==============================     FUNCTION INITIALISATION OF DRIVER     =================================
#==========================================================================================================
def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os):
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
    desired_caps['appPackage'] = 'com.reddit.frontpage'
    desired_caps['appActivity'] = 'com.reddit.frontpage.main.MainActivity'
    cpt_appium_start = 0
    while True:
        try:
            p_driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            time.sleep(random.uniform(3.5, 5.3))
            return p_driver

        except Exception as ex:
            cpt_appium_start += 1
            print(f"{p_udid}|||Something went wrong when initializing driver : {ex}")
            print(
                f"{p_udid}|||We can't open Reddit. Please check if device is connected. Let's try again!")
            if str(ex).find('hang up') != -1:
                print("PhoneBot caught the issue exception 'hang up' when initializing Driver!")
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
                    f"{p_udid}|||We can't open Reddit. Please check if device is connected. Let's try again!")

            if cpt_appium_start > 3:
                print("Error", "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")

                return None

            time.sleep(random.uniform(2.5, 3.3))

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

def Send_Delayed_Keys(text):
    """
        Simule la saisie de texte d'un humain.
        Ici on utilise cette méthode quand send_keys() ne fonctionne pas,
        car elle est plutôt lente pour les longues chaines de caractères.
    """

    for char in text:
        key_code_list = Get_Key_Code(char)
        key_code = key_code_list[0]
        uppercase = key_code_list[1]
        if uppercase:
            meta_nb = 1
        else:
            meta_nb = 0
        driver.press_keycode(key_code, meta_nb)
        time.sleep(random.uniform(0.01, 0.1))

def Get_Key_Code(char):
    """
        Retourne le KeyCode d'un caractère ainsi que si c'est une majuscule ou non
        Ne supporte que les caractères alphanumériques ainsi que '-' et '_' car ce
        sont les seuls caractères autorisés dans un pseudo Reddit.

        :param char: Par ex 'b'
        :return: Liste de la forme [KeyCode, is_uppercase], par exemple : [30, True]
    """

    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ascii_numbers = '0123456789'

    uppercase = None

    if char in ascii_uppercase:
        uppercase = True
    elif char in ascii_lowercase:
        uppercase = False
    if uppercase is not None:
        if uppercase:
            return [ascii_uppercase.index(char) + 29, True]
        else:
            return [ascii_lowercase.index(char) + 29, False]
    elif char in ascii_numbers:
        return [ascii_numbers.index(char) + 7, False]
    elif char == '-':
        return [69, False]
    elif char == '_':
        return [69, True]

def Scroll_Down():
    """
        Scroller vers le bas (= swiper vers le haut) dans la vue actuelle, cette méthode devrait fonctionner
        peu importe la taille de l'écran. Les valeurs des coefficients sont adaptées pour fonctionner avec l'app Reddit.
    """

    screen_size = driver.get_window_size()
    start_x = round(0.5*screen_size['width'])
    start_y = round(0.9*screen_size['height'])
    end_y = round(0.35*screen_size['height'])

    # swipe(startX, startY, endX, endY, duration)
    driver.swipe(start_x, start_y, start_x, end_y, 1000)




# ==================== ACTION METHODS ==================================================

def Check_Replies(from_window, username):
    """
        Ouvre la page des messages Reddit et vérifie dans les conversations ouvertes si des contacts ont répondu

        :param from_window: Numéro de la fenêtre qui appelle cette fonction
        :param username: username de la personne exécutant le script

        :return: True si succés, False si erreur/pas de messages
    """

    logger.info("\n--- Checking replies ---\n")

    # Click on Chat tab

    try:
        chat_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Discussions']")))
    except:
        try:
            chat_tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Chat']")))
        except:
            logger.error("Only french and english are supported. You can change language in reddit's app settings.")
            return False

    chat_tab.click()

    # Get list of convs

    try:
        convs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.ID, "com.reddit.frontpage:id/chat_message_preview")))
    except:
        logger.info(f"No conversations to check replies")
        return False

    for i in range(len(convs)):
        try:
            convs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.ID, "com.reddit.frontpage:id/chat_message_preview")))
        except:
            logger.info(f"No conversations to check replies")
            return False

        elem = convs[i]

        if (not elem.text.startswith("You:")) and (not elem.text.startswith("Vous:")):
            elem.click()

            # Get usernames and messages

            try:
                usernames = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.ID, "com.reddit.frontpage:id/message_username")))
                messages = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.ID, "com.reddit.frontpage:id/message_content")))
            except:
                logger.info(f"Error getting messages")
                return False

            last_msg_username = usernames[len(usernames) - 1].text
            # print(f"username: {last_msg_username}")
            last_msg_txt = messages[len(messages) - 1].find_element(By.CLASS_NAME, "android.widget.TextView").text
            # print(f"message: {last_msg_txt}")

            logger.info(f"{last_msg_username} has replied")

            # Check if the last action concerning this contact is a reply

            last_actions = DB_Get_Last_Actions()

            add_db = False

            for action in last_actions:
                if action[0] == last_msg_username:
                    if action[5] == "message_received":
                        add_db = False
                        break
                    else:
                        add_db = True
                        break

            if add_db:
                DB_Set_Contact_Replied(DB_Get_Contact_ID(last_msg_username), True, reply_msg=last_msg_txt)
            else:
                DB_Set_Contact_Replied(DB_Get_Contact_ID(last_msg_username), True)
        else:
            elem.click()

            try:
                usernames = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "com.reddit.frontpage:id/toolbar")))
            except:
                logger.info(f"Error getting usernames")
                return False

            usernames_txt = usernames.find_element(By.CLASS_NAME, "android.widget.TextView").text

            conv_username = ""

            for elem_username in usernames_txt.split(", "):
                if elem_username.lower() != username.lower():
                    conv_username = elem_username
                    break

            if conv_username != "":
                logger.info(f"{conv_username} has not replied")
                DB_Set_Contact_Replied(DB_Get_Contact_ID(conv_username), False)
            else:
                logger.error("Invalid username")

        time.sleep(random.uniform(2,3))
        driver.back()

    logger.info("\n--- Finished Checking replies ---\n")
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
            Send_Message(elem[0], next_msg_id, False, debug=const_debug)

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

        community = re.search('reddit.com/(.*)/', url).group(1)

        logger.info(f"\n========== New Community : {community} ==========\n")

        # Go to the community

        try:
            browse_tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Parcourir']")))
        except:
            try:
                browse_tab = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Browse']")))
            except:
                logger.error("Only french and english are supported. You can change language in reddit's app settings.")
                return False

        browse_tab.click()

        time.sleep(random.uniform(1, 3))

        try:
            search_view = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/search_view")))
            search_view.click()
        except Exception as ex:
            logger.error(f"Error while opening search: {ex}")

        time.sleep(random.uniform(2,3))

        try:
            search_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/search")))
            search_field.send_keys(community)
        except Exception as ex:
            logger.error(f"Error while searching: {ex}")

        time.sleep(random.uniform(2, 3))

        try:
            result_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "android.widget.RelativeLayout")))
            result_elem.click()
        except Exception as ex:
            logger.error(f"Error while clicking on result: {ex}")

        browsed_posts = []
        nb_errors = 0

        while g_actions_count < g_quantity_actions:
            if nb_errors > 5:
                logger.error("Error while getting posts")
                return False
            # Get visible posts using titles
            try:
                post_titles_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.ID, "com.reddit.frontpage:id/link_title")))
            except:
                Scroll_Down()
                nb_errors += 1
                continue

            nb_errors = 0
            post_locations = []
            post_titles = []

            for elem in post_titles_elem:
                post_locations.append(elem.location_in_view)
                post_titles.append(elem.text)

            for i in range(len(post_locations)):    # Loop through all visible posts
                location = post_locations[i]

                if post_titles[i] in browsed_posts:     # Don't browse post if we already did
                    continue

                driver.tap([(location['x'], location['y'])], 10)   # Open the post

                if Browse_Post():
                    return True

                browsed_posts.append(post_titles[i])

                time.sleep(random.uniform(2,4))

            Scroll_Down()   # Show new posts in view
            time.sleep(random.uniform(2, 4))

    return True

def Browse_Post():
    """
        Cette méthode est appelée après l'ouverture d'un post.
        Elle va parcourir le post et envoyer des messages à l'auteur et aux commenters

        :return: True si limite atteinte, False sinon
    """

    logger.info("\n--- [Browsing a new post] ---\n")

    global g_actions_count

    # Check for date + promoted post detection

    try:
        date_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "com.reddit.frontpage:id/bottom_row_metadata_after_indicators")))
    except:
        logger.info("Date not found, assuming this is a promoted post.")
        driver.back()
        return False

    if ('y' in date_elem.text) or ('a' in date_elem.text):
        logger.info("Post skipped because too old. (>1y)")
        driver.back()
        return False

    # Get the author

    author_link = None
    try:
        author_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/bottom_row_metadata_before_indicators")))
    except Exception as ex:
        logger.error(f"Error while getting author : {ex}")

    contacted = []

    if author_link is not None:
        author = author_link.text.split('u/')[1]    # Transfom 'Publiée par u/username' --> 'username'

        if not DB_Check_Contact_Exist(author):
            author_link.click()     # Open actions for this user

            try:
                start_chat = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.ID, "com.reddit.frontpage:id/start_chat")))
            except Exception as ex:
                logger.error(f"Cannot get start chat button: {ex}")
                start_chat = None

            if start_chat is not None:
                start_chat.click()
                if Send_Message(author, Get_First_Message_ID(), True, debug=const_debug):
                    contacted.append(author)
                    if g_actions_count >= g_quantity_actions:
                        return True
                    Next_AB()
            else:
                logger.error("Cannot start chat")
                driver.back()
        else:
            logger.info(f"\n- Already sent a message to {author}. -\n")

    # Get the comments

    bottom = None   # there's an element called 'bottom_space' which is present only when we have reached
                    # the bottom of the post, so we keep going until we can see it

    while bottom is None:
        driver.implicitly_wait(5)   # Make those checks faster

        try:
            authors = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.ID, "com.reddit.frontpage:id/author")))
            driver.implicitly_wait(10)
        except:
            try:
                bottom = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.ID, "com.reddit.frontpage:id/bottom_space")))
                driver.implicitly_wait(10)
                continue
            except:
                bottom = None
                Scroll_Down()
                driver.implicitly_wait(10)
                continue

        for author in authors:
            author_txt = author.text
            if (not author_txt in contacted) and (not DB_Check_Contact_Exist(author_txt)):
                author.click()
                try:
                    start_chat = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.ID, "com.reddit.frontpage:id/start_chat")))
                except Exception as ex:
                    logger.error(f"Cannot get start chat button: {ex}")
                    start_chat = None
                if start_chat is not None:
                    start_chat.click()
                    if Send_Message(author_txt, Get_First_Message_ID(), True, debug=const_debug):
                        contacted.append(author_txt)
                        if g_actions_count >= g_quantity_actions:
                            driver.back()
                            return True
                        Next_AB()
                    time.sleep(1)
            else:
                logger.info(f"\n- Already sent a message to {author_txt}. -\n")

        try:
            bottom = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, "com.reddit.frontpage:id/bottom_space")))
        except:
            bottom = None

        Scroll_Down()
        time.sleep(random.uniform(2,3))

    driver.back()
    return False

def Send_Message(username: str, msg_id: str, conv_opened, debug = False):
    """
        Cette méthode va préparer et envoyer des messages

        :param username: Nom de l'utilisateur reddit
        :param msg_id: ID du message.
        :param conv_opened: True si on est déjà dans la conversation, False si il faut naviguer vers l'onglet Chat
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
        logger.info("Sending cancelled.")
        return False

    if username == "[deleted]":
        logger.info("Sending cancelled.")
        return False

    logger.info(f"-- Sending a message to {username} --")

    if not conv_opened:

        # Click on Chat tab

        try:
            chat_tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Discussions']")))
        except:
            try:
                chat_tab = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//android.view.ViewGroup[@content-desc='Chat']")))
            except:
                logger.info("Error click on Chat tab")
                return False

        chat_tab.click()

        time.sleep(random.uniform(2,3))

        # Click on New Chat

        try:
            chat_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/action_chat")))
        except:
            logger.error("Error while getting Chat button")
            return False

        chat_button.click()

        time.sleep(random.uniform(2, 3))

        Send_Delayed_Keys(username)   # Send keys to this text field crashes the app, so we have to use this workaround

        time.sleep(random.uniform(2, 3))

        try:
            check_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID,"com.reddit.frontpage:id/check_box")))
        except:
            logger.info(f"Can't send message to this user either because of privacy settings or account restriction")
            driver.back()
            time.sleep(1)
            driver.back()
            return False

        try:
            check_box.click()
        except Exception as ex:
            logger.error(f"Error while clicking on user: {ex}")
            driver.back()
            time.sleep(1)
            driver.back()
            return False

        time.sleep(random.uniform(1, 2))

        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/invite_button")))
            submit_button.click()
        except Exception as ex:
            logger.error(f"Error while clicking on 'Start a Chat' button: {ex}")
            driver.back()
            time.sleep(1)
            driver.back()
            return False

        time.sleep(random.uniform(2, 3))

    try:
        textarea_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/chatMessage")))
    except Exception as ex:
        logger.error(f"Error while getting message field: {ex}")
        driver.back()
        return False

    try:
        textarea_message.clear()
    except Exception as ex:
        logger.error(f"Error while clearing message: {ex}")
        driver.back()
        return False
    try:
        textarea_message.send_keys(message)
    except Exception as ex:
        logger.error(f"Error while typing message: {ex}")
        driver.back()
        return False

    time.sleep(random.uniform(2, 3))

    try:
        # driver.execute_script("arguments[0].click();", submit_button)
        if debug:
            print("- [Sending message is disabled during test] -")
        else:
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.reddit.frontpage:id/sendButton")))
            submit_button.click()
    except Exception as ex:
        logger.error(f"Error clicking send message button: {ex}")
        driver.back()
        return False

    time.sleep(random.uniform(2, 4))

    logger.info(f"\n-- Message Sent --\n")

    # Update DB
    if not DB_Add_Contact(username):
        DB_Set_Contact_Replied(DB_Get_Contact_ID(username), False)
    DB_Add_Action(message, DB_Get_Contact_ID(username), msg_id)

    global g_actions_count
    g_actions_count += 1

    logger.info(f"\n- Actions : [{g_actions_count}/{g_quantity_actions}] -\n")

    driver.back()

    return True




# ==================== MAIN METHOD ==================================================

def Appium_Cold_Messaging_Reddit_Members_of_groups(p_udid, p_system_port, p_device_name, p_version, p_os, p_taskuser_id, p_username, p_quantity_actions, lock):
    """
        Méthode principale qui est appelée au début de la tâche.
        Elle va appeler les autres méthodes pour automatiser l'envoi de messages
        aux membres d'une liste de groupes Reddit.

        :param p_udid: UDID du smartphone à utiliser
        :param p_system_port: Port à utiliser pour se connecter au serveur uiautomator2
        :param p_device_name: Nom du smartphone auquel se connecter
        :param p_version: Version de l'OS du smartphone
        :param p_os: OS du smartphone
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


    # Load driver
    try:
        driver = Initialisation_Driver(p_udid, p_system_port, p_device_name, p_version, p_os)
    except Exception as ex:
        logger.error(f"Error when loading driver : {ex}")
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


"""
_udid = "ac155151"
_systemPort = 8200
_deviceName = "POCOPHONE F1"
_version = "10"
_os = "Android"

_taskuser_id = 1337     # ID random temporaire
_username = "skreenager42"      # Bien penser à mettre son propre username reddit
_quantity_actions = 5

_lock = threading.Lock()



Appium_Cold_Messaging_Reddit_Members_of_groups(_udid, _systemPort, _deviceName, _version, _os, _taskuser_id, _username, _quantity_actions, _lock)
"""
