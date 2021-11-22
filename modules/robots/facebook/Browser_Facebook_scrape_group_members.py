# -*- coding: utf-8 -*-

"""
Author : Boli Djeli Estelle Widianne
Email : boli.widianne@gmail.com
"""

import random
import threading
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime

from modules import mymodulesteam

# ==================== INITIALISATION DU LOGGER ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_Facebook_Scrape_group_members__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ------------------------ GoogleSheetTool
def urlToID(googleSheetURL):
    """
    La méthode urlToID permet d'extaire l'ID du document à partir d'un lien de Google Sheet
    :param googleSheetURL: Lien Google Sheet complet (Ex: https://docs.google.com/spreadsheets/d/1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o/edit?usp=sharing)
    :type googleSheetURL: str
    :return: id de Google Sheet
    :rtype: str
    """
    id = ""
    if googleSheetURL.__contains__("/"):
        id =  googleSheetURL.split("/")[5]  # Dans l'exemple, id est "1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o"
    return id




def getColumnsFromGoogleSheetByURL(googleSheetURL):
    """
    La méthode getColumnsFromGoogleSheetByURL permet d'obtenir les valeurs dans les différentes colonnes de Google Sheet
    :param googleSheetURL: Lien Google Sheet complet
    :type googleSheetURL: str
    :return: Une liste contenant toutes les lignes du Google Sheet
    :rtype: list
    """
    idGoogleSheet = urlToID(googleSheetURL)  # Obtenir id de Google Sheet
    if idGoogleSheet != "":
        return mymodulesteam.GoogleSheetGetValues(idGoogleSheet)  # Obtenir toutes les lignes du doc
    else:
        return ""


# ------------------------
def get_Browser_Driver(p_browser):
    # OUVERTURE DU NAVIGATEUR
    if p_browser == "Chrome":
        return mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        return mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return None


# ------------------------- CLASS Scrape Facebook -------------------------
class ScrapeFacebook:
    url_list = []
    keyword_list = []
    scrape_type = ""
    scrap_compteur = 0

    # valeurs des ligne du google sheet
    def __init__(self, urls, keywords):
        self.url_list = []
        self.keyword_list = []

        # set url list
        for row in urls:
            self.url_list.append(row[0])
        print(f"url_list: {len(self.url_list)}")

        # set keyword list
        for row in keywords:
            self.keyword_list.append(row[0])
        print(f"url_keyword: {len(self.keyword_list)}")

        self.set_scrape_type()

    def set_scrape_type(self):

        if len(self.keyword_list) > 0 and len(self.url_list) > 0:
            self.scrape_type = 'a'  # Search all
        elif len(self.keyword_list) > 0 and len(self.url_list) < 1:
            self.scrape_type = 'k'  # Search keywords
        elif len(self.keyword_list) < 1 and len(self.url_list) > 0:
            self.scrape_type = 'u'  # Search urls
        else:
            self.scrape_type = 'n'  # Nothing to search
    #
    def scrape_urls(self, p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock):
        logger.info(f'___SCRAPING FOR URLS/GROUPS___')
        # utilisateur connecté, trouver le groupe
        for url in self.url_list:
            is_action_up = self.find_group(p_driver, url, p_taskuser_id, p_quantity_actions, lock)
            # peut continuer le scraping du groupe suivant si is_action_up = False, c'est à dire
            # quantité d'action pas encore atteinte
            if is_action_up:
                time.sleep(3)
                # p_driver.close()
                return True, self.scrap_compteur


    def scrape_keyword(self, p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock):
        logger.info(f'___SCRAPING FOR KEYWORD OR/AND URL___')
        # Get all groups urls for a keyword
        for keyword in self.keyword_list:
            groups = f"https://www.facebook.com/groups/search/groups/?q={keyword}"
            p_driver.get(groups)
            time.sleep(2)
            # got to page bottom to load all groups
            mymodulesteam.ScrollToTheEnd(p_driver)

            #get all the groups urls
            try:
                groups = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located((
                    By.XPATH, '//a[contains(@href, "facebook.com/groups/")]'
                )))
                for group in groups:
                    print(group.get_attribute("href"))
                    self.url_list.append(group.get_attribute("href"))
            except Exception as e:
                logger.info(f'Group to the specified keyword was not found - Error: {e}')

        return self.scrape_urls(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock)


    # ------------------------- END CLASS Scrape Facebook -------------------------
    def find_group(self, p_driver, group_url, p_task_user_id, p_quantity_actions, lock):
        # ouvre la page du groupe
        p_driver.get(group_url)

        # ouvre la table des membres
        tabXpath = "//a[@role='tab' and contains(@href, '/members')]"
        # "//div[@class='cb02d2ww ni8dbmo4 stjgntxs l9j0dhe7 k4urcfbm du4w35lb lzcic4wl']/div[@class='soycq5t1 l9j0dhe7']/div[@class='i09qtzwb rq0escxv n7fi1qx3 pmk7jnqg j9ispegn kr520xx4']/a[4]"
        try:
            tabMembre = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, tabXpath)))
            tabMembre.click()
            # p_driver.execute_script("arguments[0].click();", tabMembre)
            time.sleep(5)

            # liste des membres
            return self.get_members(p_driver, group_url, p_task_user_id, p_quantity_actions, lock)


        except Exception as ex:
            print(f"Error on find_group: {ex}")
            return False

    def get_members(self, p_driver, group_url, p_task_user_id, p_quantity_actions, lock):
        try:
            can_scroll = True
            all_urls = []
            scroll_compte = 0
            while can_scroll:
                # On va chercher les <a> de chaque membre
                members = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//span/a[not(@aria-label) and not(contains(@href, 'help'))]")))


                urls = []
                for member in members:
                    url = {"profileLink": member.get_attribute("href"), "fullName": member.text}
                    if not url in all_urls:
                        urls.append(url)
                # ajouter les urls courants à la liste des urls
                all_urls.extend(urls)
                for url in urls:
                    # profileLink = <a href="...">
                    # on charge le profil du membre
                    p_driver.get(url["profileLink"])
                    # On scrape depuis son profile
                    is_successful = self.scrape_profil(url["profileLink"], url["fullName"], p_task_user_id, lock)
                    time.sleep(2)

                    # verifier si le quantite de scrap est suffisante
                    if is_successful:
                        self.scrap_compteur += 1
                        if self.scrap_compteur >= p_quantity_actions:
                            logger.info(f"SUCCESS SCRAP: {self.scrap_compteur} ACTIONS DONE")
                            return True

                # retourner sur l'onglet des membres avant de scrollé
                p_driver.get(group_url + "members")
                time.sleep(2)

                current_scroll = 0
                while True:
                    can_scroll = self.scroll_page(p_driver)
                    if current_scroll <= scroll_compte:
                        current_scroll = current_scroll + 1
                    else:
                        scroll_compte = scroll_compte + 1
                        break

                time.sleep(2)
        except Exception as ex:
            logger.error(f"Error on get_members : {ex}")

    def scrape_profil(self, profile_link, full_name, p_task_user_id, lock):
        if not self.is_profile_exist(profile_link, lock):
            id_contact = self.insert_to_contacts(lock, profile_link, full_name, p_task_user_id)

            # sauvegarder l'action
            if id_contact != 0:
                logger.info(f"contat save with success: id_contact= {id_contact}")
                self.insert_to_actions(lock, id_contact, p_task_user_id)
                return True
            else:
                logger.error(f"id_contact cannot be null")
        else:
            logger.warning(f"contat already exists: profle_url= {full_name}")
        return False

    def insert_to_contacts(self, lock, url_profile, full_name, p_task_user_id, platform='facebook'):
        """
            insert scraped values to contacts
        """
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()

        # inserer le contact dans la base
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO contacts(platform,id_task_user,url_profile,username, date_created,date_update)"
                " VALUES(?,?,?,?,?,?)", (
                    platform, p_task_user_id, url_profile, full_name,
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            sqlite_connection.commit()

            sqlite_cursor.execute(
                "select id from contacts where url_profile=?", (url_profile,))
            rows = sqlite_cursor.fetchall()
            id_contact = int((str(rows).split('(')[1].split(',')[0]).strip())

            logger.info(f"Insert contact contacts with fullName {full_name} success !")
            return id_contact

    def insert_to_actions(self, lock, id_contact, id_task_user, platform="facebook", type_action="scrap"):
        """
            insert scraped values to actions
        """
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()

        # inserer l'actions dans la base
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO actions(platform,type_action,date,id_contact,id_task_user,date_created,date_update) "
                "VALUES(?,?,?,?,?,?,?)", (
                    platform,
                    type_action,
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    id_contact,
                    id_task_user,
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            sqlite_connection.commit()

        logger.info(f"Insert action in actions with id contact {id_contact} with action :\'scrape\' success !")

    def is_profile_exist(self, url_profile, lock):
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sqlite_cursor.execute(
                "select id from contacts where url_profile=?", (url_profile,))
            rows = sqlite_cursor.fetchall()

            if len(rows) != 0:
                return True
            else:
                logger.error(f"le profil n'existe pas")
                return False

    def scroll_page(self, p_driver):
        SCROLL_PAUSE_TIME = 1

        # obtenir la taille du scroll
        last_height = p_driver.execute_script("return document.body.scrollHeight")
        # scrollé vers le bas
        p_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # attendre le chargement de la page
        time.sleep(SCROLL_PAUSE_TIME)

        # calculer la nouvelle taille du scroll et comparer à la precedente
        new_height = p_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            return False
        last_height = new_height

        return True


def browser_Scraping_Facebook_Group_members(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions,
                                            label_log, lock):
    result = False
    counter = 0
    task_user_detail = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)

    keyword_list = getColumnsFromGoogleSheetByURL(task_user_detail['url_keywords'])
    url_list = getColumnsFromGoogleSheetByURL(task_user_detail['url_list'])
    ff = ScrapeFacebook(url_list, keyword_list)
    # baseUrl = "https://www.facebook.com/"
    # p_driver.get(baseUrl)
    # p_driver.maximize_window()
    time.sleep(random.uniform(1, 2))

    # input('-- End press enter --')

    if ff.scrape_type == "u":
        result, counter = ff.scrape_urls(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions,
                                            label_log, lock)

    elif ff.scrape_type == "k" or ff.scrape_type == "a":
        result, counter = ff.scrape_keyword(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock)

    else:
        len_key = ""
        len_url = ""
        if ff.scrape_type == 'n':
            len_key = len(ff.keyword_list)
            len_url = len(ff.url_list)
        logger.error(f'___NO SCRAPING DATA RECEIVED___ :')
        logger.error(f'LENGTH KEYWORD: {len_key}')
        logger.error(f'LENGTH KEYWORD: {len_url}')

    return result, counter

###############################################################################################################

# p_taskuser_id = 3239
# # sheet link
# FB_username = "Test script"
# p_browser = "Firefox"
# label_log = ""
# lock = threading.Lock()
# # get sheet values
# p_quantity_actions = 5
# p_driver = mymodulesteam.FireFoxDriverWithProfile()
#
# browser_Scraping_Facebook_Group_members(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log,
#                                         lock)
