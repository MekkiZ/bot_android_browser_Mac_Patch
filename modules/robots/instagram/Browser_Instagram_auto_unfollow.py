# -*- coding: utf-8 -*-
"""
Author : Ikram Laguir
Task :  Browser Auto unfollow Instagram
Contact : Ikram.laguir@outlook.com
"""
# TODO:
#   - try & execpt
#   - ordonner les desabonnement depuis la date d'abonnement
#   - traduire les xpath en anglais
#   - faire une version si il trouves les comptes dans la base de données et une si il ne les trouves pas
#   - faire une verion du store_contact avec un insert et un update
#   - return false si erreur et counter si il ya un count
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from time import sleep
import random
import sqlite3
from datetime import datetime
import threading
from modules import mymodulesteam
from modules.mymodulesteam import LoadFile

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_auto_unfollow_Instagram__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ================================================================================


def Sleeping_Bot(borne_inf, borne_sup):
    """
    Random sleep for being a stealth bot.
    """
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    sleep(ts)


# Save action in db.db
def store_action(date_created, id_contact, p_taskuser_id, plateform=str("Instagram")):
    logger = logging.getLogger('__Browser_auto_unfollow_Instagram__')
    try:

        conn = sqlite3.connect(LoadFile('db.db'))
        cursor = conn.cursor()
        insert_query = """INSERT INTO actions(platform, type_action, date, id_contact, date_created,
                        id_task_user) VALUES(?, ?, ?, ?, ?, ?) """
        action_tuple = (
            plateform, "unfollow", str(date_created), id_contact,
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), p_taskuser_id)
        cursor.execute(insert_query, action_tuple)
        conn.commit()
        conn.close()
    except Exception as ex:
        logger.error(f'sqlite execption (store_action): {ex}')
        return False
    return True


# Save contacts in the DB
def store_contact(Instagram_username, lock, p_taskuser_id, plateform=str("Instagram")):
    logger = logging.getLogger('__Browser_auto_unfollow_Instagram__')
    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        with lock:
            Instagram_username = str(Instagram_username)
            conn = sqlite3.connect(LoadFile('db.db'))
            cursor = conn.cursor()
            insert_query = """INSERT INTO contacts(platform, Instagram_username, id_task_user, date_created, unfollowed) 
                                VALUES (?, ?, ?, ?,?) """
            contact_tuple = (plateform, Instagram_username, p_taskuser_id, date_created, 1)
            cursor.execute(insert_query, contact_tuple)
            conn.commit()

            contact_id = cursor.execute("SELECT id FROM contacts WHERE Instagram_username = ? AND date_created = ?",
                                        [Instagram_username, date_created]).fetchone()[0]
            conn.close()

            return store_action(date_created, contact_id)

    except Exception as ex:
        logger.error(f'Exception thrown (store_contact): {ex} {ex.__cause__}')
        return False


# Search followers in db
def search_followers(p_username, lock, p_quantity_actions, plateform=str("Instagram")):
    """
    This method search followers in data base.
    Return object with followers name.
    """
    try:
        with lock:
            p_username = str(p_username)
            conn = sqlite3.connect(LoadFile('db.db'))
            cursor = conn.cursor()
            search_query = """SELECT contacts.username FROM actions
                            INNER JOIN contacts
                            on actions.id_contact = contacts.id
                            WHERE actions.platform = ? AND actions.id_social_account = ?
                            AND contacts.unfollowed is "NULL"
                            ORDER BY actions.date_created ASC
                            Limit ?;"""
            contact_tuple = [plateform, p_username, p_quantity_actions]
            list_followers = cursor.execute(search_query, contact_tuple).fetchall()
            conn.close()
            return list_followers

    except Exception as ex:
        logger.error(f'Exception thrown (search_followers): {ex} {ex.__cause__}')
        return False


# This method finds the accounts who are followed by us
def instagram_unfollow(p_browser, p_taskuser_id, Instagram_username, p_driver, p_quantity_actions, label_log, lock):
    # Set a counter
    counter = 0
    p_driver.implicitly_wait(10)
    try:
        try:  # on click sur la photo de profile
            urlprofile = WebDriverWait(p_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//nav//img[contains(@data-testid, "user-avatar")]')))
            Sleeping_Bot(2.0, 4.0)
            p_driver.execute_script("arguments[0].click();", urlprofile)
            p_driver.implicitly_wait(5)

            # on click sur profile dans le pop up qui vient de s'ouvrir
            urlprofile1 = WebDriverWait(p_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, ("//div[contains(text(),'Profil')]"))))
            Sleeping_Bot(2.0, 4.0)
            p_driver.execute_script("arguments[0].click();", urlprofile1)
            p_driver.implicitly_wait(5)
        except Exception as ex:
            logger.error(f"ERROR : {ex}\nProfile not found.")
            return False

        try:
            # on trouve le liens abonnements !! trouver une solution avec contains !!
            nbFollowing = WebDriverWait(p_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, ("//header//a[text()=' abonnements']"))))
            # on affiche le nombre d'abonnés
            logger.info("You are following: " + nbFollowing.text)
            logger.info("Starting the script : _Instagram_Auto_Unfollow_")
            # Get the number from the string
            nbFollowingInt = [int(s) for s in nbFollowing.text.split() if s.isdigit()][0]
            logger.info(nbFollowingInt)
            # Set a limit to unfollow
            limitOp = min(nbFollowingInt, p_quantity_actions)
            logger.info(limitOp)

            #
            #
            # En cours de devellopement
            """

            # ici on retourne le nom des followers
            subscribers_found = search_followers(Instagram_username, lock, limitOp)


            for names in subscribers_found:
                print(names[0])
                try:################################
                    # ici on trouve la bar de recherche
                    search_bar = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ("//input[contains(@placeholder,'Rechercher')]"))))

                    # ici on entre le nom du compte a unfollow
                    search_bar.send_keys(names[0])
                    Sleeping_Bot(2.0, 4.0)
                    # ici on clic le lien du pop up qui contient le nom du compte a unfollow
                    first_profile = WebDriverWait(p_driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, (f"//nav//a[@href='/{names[0]}/']"))))
                    p_driver.execute_script("arguments[0].click();", first_profile)
                    p_driver.implicitly_wait(5)
                    # Dans la page du profile on clic sur le boutton abbonné
                    subsribed_button = WebDriverWait(p_driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, ("//header//span[contains(@aria-label,'Abonné(e)')]"))))
                    Sleeping_Bot(2.0, 4.0)
                    p_driver.execute_script("arguments[0].click();", subsribed_button)
                    p_driver.implicitly_wait(5)
                    # ici on cilic dans le pop up pour se desabonné
                    confirm_unfollow = WebDriverWait(p_driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, ("//button[contains(text(),'Se désabonner')]"))))
                    Sleeping_Bot(2.0, 12.0)
                    p_driver.execute_script("arguments[0].click();", confirm_unfollow)
                    p_driver.implicitly_wait(5)

                    counter += 1
                    logger.info(str(counter) + "- " + names[0] + " has been unfollowed")
                    print(counter)

                    # save actons
                    # update contact


                except Exception as ex:
                    logger.error(f"ERROR : {ex}\n")


                ################################





            """
            #
            #
            #
            print(counter)

            # on click sur le liens abonnements
            # p_driver.execute_script("arguments[0].click();", nbFollowing)
            # p_driver.implicitly_wait(5)

            while counter < limitOp:
                try:
                    # on recupere tout les personne avec la mention abonné
                    subsribedButtons = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ("//button[contains(text(),'Abonné(e)')]"))))

                    # on recupere le nom de tout les abonné
                    subsribName = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, ("//a[@class='FPmhX notranslate  _0imsa ']"))))

                    ########  Unfollow ########
                    for name, button in zip(subsribName, subsribedButtons[:len(subsribName)]):
                        button.click()
                        confirmUnfollow = WebDriverWait(p_driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, ("//button[contains(text(),'Se désabonner')]"))))
                        Sleeping_Bot(2.0, 12.0)
                        p_driver.execute_script("arguments[0].click();", confirmUnfollow)

                        ######### Save contact in the db ########
                        store_contact(name.text, lock, p_taskuser_id)
                        p_driver.implicitly_wait(5)

                        counter += 1
                        logger.info(str(counter) + "- " + name.text + " has been unfollowed")

                        if counter >= limitOp:
                            logger.info("Done")
                            break
                        elif (counter % 11 == 0):
                            break
                except Exception as ex:
                    logger.error(f"ERROR : {ex}\nAbonné XPATH not found.")

                ######## Reload the box  to get more followers ##########
                # Closes the following window
                closewindow = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, ("//div[contains(@aria-label,'Abonnements')]//button[contains(@class,'wpO6b')]"))))
                p_driver.execute_script("arguments[0].click();", closewindow)
                Sleeping_Bot(1, 5)

                # Refresh
                p_driver.get(p_driver.current_url)
                Sleeping_Bot(1, 5)
                p_driver.refresh()

                # !! À VOIR SI ON SUPPRIME !!
                nbFollowing = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ("//header/section[1]/ul[1]/li[3]/a[1]"))))
                p_driver.execute_script("arguments[0].click();", nbFollowing)

                p_driver.implicitly_wait(5)
        except Exception as ex:
            logger.error(f"ERROR : {ex}\nFollowers not found.")
            return False
    except Exception as ex:
        logger.error(f"Error when during unfollowing followers: '{ex}'")

    return True, counter


# === 1 OPEN BROWSER =========================================================
"""
p_browser="Chrome"
if p_browser == "Chrome":
    p_driver = mymodulesteam.ChromeDriverWithProfile()
elif p_browser == "Firefox":
    p_driver = mymodulesteam.FireFoxDriverWithProfile()
else:
    logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
    # return False

p_driver.get('https://instagram.com')

id_task= 50
p_taskuser_id= 1334
label_log_run_one_task=""
lock=threading.Lock()
current_tab=""
Instagram_username = "PhoneBot"
p_quantity_actions = 4
label_log = ""

#AA = search_followers(Instagram_username, lock, p_quantity_actions)
#print(AA)
instagram_unfollow(p_browser,p_taskuser_id,Instagram_username,p_driver,p_quantity_actions,label_log,lock)
# instagram_unfollow(p_browser,p_taskuser_id,Instagram_username,p_driver,p_quantity_actions,label_log,lock)
"""
