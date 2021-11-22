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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime
from modules import mymodulesteam


# ==================== INITIALISATION DU LOGGER ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_Tiktok_Like_Random_Post__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# def get_Browser_Driver(p_udid):
#     # OUVERTURE DU NAVIGATEUR
#     if p_udid == "Chrome":
#         return mymodulesteam.ChromeDriverWithProfile()
#     elif p_udid == "Firefox":
#         return mymodulesteam.FireFoxDriverWithProfile()
#     else:
#         logger.error(f"PhoneBot didn't find the browser called '{p_udid}'.")
#         return None

# ======================================================================================================================
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
# ======================================================================================================================

def Smartphone_Scraping_Facebook_Group_members(p_udid, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
                                               label_log, lock):

    result = False
    counter = 0
    task_user_detail = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)

    keyword_list = getColumnsFromGoogleSheetByURL(task_user_detail['url_keywords'])
    url_list = getColumnsFromGoogleSheetByURL(task_user_detail['url_list'])
    ff = ScrapeFacebook(url_list, keyword_list)

    time.sleep(random.uniform(1, 2))

    if ff.scrape_type == "u":
        result, counter = ff.scrape_urls(p_udid, p_taskuser_id, FB_username, p_driver, p_quantity_actions,
                                            label_log, lock)

    elif ff.scrape_type == "k" or ff.scrape_type == "a":
        result, counter = ff.scrape_keyword(p_udid, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock)

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


    # ff = ScrapeFacebook("sheet_rows")
    # baseUrl = "https://www.facebook.com/"
    # p_driver.get(baseUrl)
    #
    # p_driver.maximize_window()
    # time.sleep(random.uniform(1, 2))
    #
    # # utilisateur connecté, trouvéle groupe
    # for url in ff.url_list:
    #     is_action_up = ff.find_group(p_driver, url, p_taskuser_id)
    #     # peut continuer le scraping du groupe suivant si is_action_up = False, c'est à dire
    #     # quantité d'action pas encore atteinte
    #     if is_action_up:
    #         time.sleep(3)
    #         p_driver.close()
    #         return


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
    def scrape_urls(self, p_udid, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock):
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


    def scrape_keyword(self, p_udid, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock):
        group_scraped = []

        logger.info(f'___SCRAPING FOR KEYWORD OR/AND URL___')
        # Get all groups urls for a keyword
        for keyword in self.keyword_list:
            # Tap on groups tab
            WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.LinearLayout//android.widget.FrameLayout[3]')
            )).click()
            time.sleep(1.5)

            #Tap on search
            WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//android.view.ViewGroup[contains(@content-desc, "Search groups")]')
            )).click()
            time.sleep(1.5)

            # Type keyword
            WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//android.widget.EditText')
            )).send_keys(f"{keyword}")
            p_driver.press_keycode(66) # 66 -> ENTER
            time.sleep(1.5)

            # Select groups
            WebDriverWait(p_driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//android.view.ViewGroup[contains(@content-desc, "GROUP")]')
            )).click()
            time.sleep(1.5)

            # Get Group names
            # groups = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located(
            #     (By.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup')
            # ))

            end_results = False
            i = 0
            while not end_results:
                groups = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup')
                ))
                time.sleep(1.5)

                if i <= len(groups)-1:
                    if groups[i].get_attribute("content-desc"):
                        groups[i].click()
                        time.sleep(1)
                        p_driver.back()
                i += 1
                if i >= len(groups) - 1: end_results = True

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

        return self.scrape_urls(p_udid, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock)


    # ------------------------- END CLASS Scrape Facebook -------------------------


###############################################################################################################

"""p_taskuser_id = 2670
# sheet link
task_user_detail = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
p_udid = "Chrome"
label_log = ""
p_driver = get_Browser_Driver(p_udid)
lock = threading.Lock()
# get sheet values
sheet_rows = mymodulesteam.GoogleSheetTool.getColumnsFromGoogleSheetByURL(task_user_detail['url_list'])
p_quantity_actions = task_user_detail['minimum']

Smartphone_Scraping_Facebook_Group_members(p_udid, p_taskuser_id, p_driver, p_quantity_actions, label_log, lock)
"""
