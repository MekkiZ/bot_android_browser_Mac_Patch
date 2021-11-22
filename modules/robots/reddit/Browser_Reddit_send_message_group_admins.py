# -*- coding: utf-8 -*-

"""
Author : Heubo Thierry
Email : Heubothierry@gmail.com
Pour le test, je vous prie de créer un compte reddit !!!
Si vous executez trop de fois le code, reddit vous empêchera d'envoyer des messages car il vous prendra pour un robot.
"""

import logging
import sqlite3
import threading
import time
import re
from modules import mymodulesteam
from modules.mymodulesteam import LoadFile, all_subdirs_of, KillProgram, ChromeDriverWithProfile, FireFoxDriverWithProfile, ScrollToTheEnd, GetDetailsTaskUser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import FirefoxProfile


# ================================ LOGGER ====================================
import pathlib
import platform
import psutil

# ================================ CLASSES NÉCÉSSAIRES POUR INTÉRAGIR AVEC LA BASE DE DONNÉES ========================== #
class DataBaseTool:

    def __init__(self, databaseFileName, lock):
        """
            La méthode __init__ permet d'initialiser la classe

            :param databaseFileName: Nom du fichier de la base de données (Ex: "db.db")
            :param lock: le thread lock
        """
        self.sqlite_connection = self.connecter(databaseFileName)
        self.sqlite_cursor = self.sqlite_connection.cursor()
        self.lock = lock

    """
    ****************************************************************************************************************
    Méthodes pour manipuler la base de données
    ****************************************************************************************************************
    """
    def connecter(self, databaseFileName):
        """
            La méthode connecter permet de connecter localement dans une base de données sous forme d'un fichier

            :param databaseFileName: Nom du fichier de la base de données (Ex: "db.db")
            :return: le pointeur sur la base de données
            :rtype: sqlite3.dbapi2.Connection
        """
        return sqlite3.connect(mymodulesteam.LoadFile(databaseFileName))

    def addLine(self, tableName, fields, values):
        """
        La méthode addLine permet d'ajouter une ligne dans la table via INSERT INTO

        :param lock: le lock
        :param tableName: le nom de la table
        :param fields: les champs
        :param values: les valeurs
        :param databaseFilename: le nom du fichier de la base de données
        :type tableName: str
        :type fields: tuple
        :type values: tuple
        :return: "True" si réussi, "False" sinon
        :rtype: bool
        """

        # insérer la ligne dans la table
        with self.lock:

            # Construction de la requête
            nbValues = len(values)
            request = "INSERT INTO " + tableName + " " + str(fields) + " VALUES(" + ("?," * nbValues)[:-1] + ")"

            # Exécution de la requête
            try:
                self.sqlite_cursor.execute(request, values)
                self.sqlite_connection.commit()
                result = returnData(True, "add line success !")
            except Exception as ex:
                result = returnData(False, ex)

            return result

    def addLineRequest(self, request, values):
        """
        La méthode addLine permet d'ajouter une ligne dans la table via INSERT INTO

        :param lock: le lock
        :param tableName: le nom de la table
        :param fields: les champs
        :param values: les valeurs
        :param databaseFilename: le nom du fichier de la base de données
        :type tableName: str
        :type fields: tuple
        :type values: tuple
        :return: "True" si réussi, "False" sinon
        :rtype: bool
        """

        # insérer la ligne dans la table
        with self.lock:
            # Exécution de la requête
            try:
                self.sqlite_cursor.execute(request, values)
                self.sqlite_connection.commit()
                result = returnData(True, "add line success !")
            except Exception as ex:
                result = returnData(False, ex)

            return result

    def addLineWithID(self, tableName, fields, values):
        """
        La méthode addLine permet d'ajouter une ligne dans la table via INSERT INTO

        :param lock: le lock
        :param tableName: le nom de la table
        :param fields: les champs
        :param values: les valeurs
        :param databaseFilename: le nom du fichier de la base de données
        :type tableName: str
        :type fields: tuple
        :type values: tuple
        :return: "id" si réussi, "-1" sinon
        :rtype: bool
        """

        # insérer la ligne dans la table
        with self.lock:

            # Construction de la requête
            nbValues = len(values)
            request = "INSERT INTO " + tableName + " " + str(fields) + " VALUES(" + ("?," * nbValues)[:-1] + ")"

            # Exécution de la requête
            try:
                self.sqlite_cursor.execute(request, values)
                self.sqlite_connection.commit()
                result = returnData(self.sqlite_cursor.lastrowid, "add line success !")
            except Exception as ex:
                result = returnData(-1, ex)

            return result

    def getLines(self, columnName, tableName, conditions = {}, options = ""):
        """
        La méthode getLines permet d'obtenir les lignes via SELECT

        :param lock: le lock
        :param columnName: le(s) nom(s) de(s) colonne(s)
        :param tableName: le nom de la table
        :param conditions: les conditions (Ex: {"id": 3, "nom": "Test"})
        :param options: les options (Ex: "ORDER BY date")
        :type columnName: str
        :type tableName: str
        :type conditions: dict
        :type options: str
        :return: Une liste contenant toutes les lignes trouvées (chaque ligne est un dictionnaire {"nomColonne1": "valeur1", ...})
        :rtype: list
        """

        # obtenir les lignes de la table
        with self.lock:

            # Construire la clause WHERE "WHERE ..."
            whereField = " WHERE " if len(conditions) != 0 else ""
            parameters = []

            for condition in conditions:
                whereField += condition + "=? AND "
                parameters.append(conditions[condition])

            whereField = whereField[:-5]

            # Construire la clause OPTION
            optionField = " " + options if (options != "") else ""

            # construction de la requête
            request = "SELECT " + columnName + " FROM " + tableName + whereField + optionField

            try:
                # Obtention des lignes
                if len(conditions) == 0 and len(options) == 0:  # Pas conditions ni options
                    rows = self.sqlite_cursor.execute(request).fetchall()
                else: # il y a conditions et/ou option
                    rows = self.sqlite_cursor.execute(request, tuple(parameters)).fetchall()

                # Conversion en une liste de dictionnaire
                columnNames = getColumnNamesOfTable(tableName)

                rowsFinal = []  # La liste finale contenant toutes les lignes
                rowDict = {}    # Le dictionnaire représentant 1 ligne
                for row in rows:
                    for nbColumns in range(len(row)):
                        rowDict[columnNames[nbColumns]] = row[nbColumns]
                    rowsFinal.append(rowDict.copy())

                result = returnData(True, rowsFinal)

            except Exception as ex:
                result = returnData(False, ex)

            return result

    def getLinesRequest(self, request, parameters = ""):
        """
            La méthode getLines permet d'obtenir les lignes via SELECT

            :param lock: le lock
            :param tableName: le nom de la table
            :param parameters: les paramètres
            :type tableName: str
            :type request: str
            :type parameters: tuple
            :return: Une liste contenant toutes les lignes trouvées (chaque ligne est un dictionnaire {"nomColonne1": "valeur1", ...})
            :rtype: list
            """

        if "WHERE" in request:
            res = re.search("(?<=FROM )[a-zA-Z .=_]+ WHERE", request)
            tableName = res.group(0)[:-6]

        else:
            res = re.search("(?<=FROM )[a-zA-Z .=_]+", request)
            tableName = res.group(0)

        # obtenir les lignes de la table
        with self.lock:
            try:
                # Obtention des lignes
                if parameters == "":  # Pas conditions ni options
                    rows = self.sqlite_cursor.execute(request).fetchall()
                else:  # il y a conditions et/ou option
                    rows = self.sqlite_cursor.execute(request, parameters).fetchall()

                # Conversion en une liste de dictionnaire
                columnNames = getColumnNamesOfTable(tableName)

                rowsFinal = []  # La liste finale contenant toutes les lignes
                rowDict = {}  # Le dictionnaire représentant 1 ligne
                for row in rows:
                    for nbColumns in range(len(row)):
                        rowDict[columnNames[nbColumns]] = row[nbColumns]
                    rowsFinal.append(rowDict.copy())

                result = returnData(True, rowsFinal)

            except Exception as ex:
                result = returnData(False, ex)

            return result

    def getLinesRequestNoDict(self, request, parameters = ""):
        """
            La méthode getLines permet d'obtenir les lignes via SELECT

            :param lock: le lock
            :param tableName: le nom de la table
            :param parameters: les paramètres
            :type tableName: str
            :type request: str
            :type parameters: tuple
            :return: Une liste contenant toutes les lignes trouvées (chaque ligne est un dictionnaire {"nomColonne1": "valeur1", ...})
            :rtype: list
            """

        # obtenir les lignes de la table
        with self.lock:
            try:
                # Obtention des lignes
                if parameters == "":  # Pas conditions ni options
                    rows = self.sqlite_cursor.execute(request).fetchall()
                else:  # il y a conditions et/ou option
                    rows = self.sqlite_cursor.execute(request, parameters).fetchall()

                result = returnData(True, rows)

            except Exception as ex:
                result = returnData(False, ex)

            return result

    def modifyLine(self, tableName, fields, values, conditions):
        """
        La méthode modifyLine permet de modifier une ligne via UPDATE

        :param lock: le lock
        :param tableName: le nom de la table
        :param fields: les champs
        :param values: les valeurs
        :param conditions: les conditions (Ex: {"id": 3, "nom": "Test"})
        :type tableName: str
        :type fields: list
        :type values: list
        :type conditions: dict
        :return: "True" si réussi, "False" sinon
        :rtype: bool
        """

        with self.lock:
            # construire la requête
            whereField = " WHERE "   # la clause de "WHERE ..."
            parameters = values.copy() # les paramètres (value1, value2, ...)
            for condition in conditions:
                whereField += condition + "=? AND "
                parameters.append(conditions[condition])

            whereField = whereField[:-5]
            parameters = tuple(parameters)

            # construire la requête
            request = "UPDATE " + tableName + " SET "

            for field in fields:
                request += field + "=?,"

            request = request[:-1]
            request += whereField

            # Exécution de la requete
            try:
                self.sqlite_cursor.execute(request, parameters)
                self.sqlite_connection.commit()
                result = returnData(True, "update line success!")
            except Exception as ex:
                result = returnData(False, ex)

            return result

    def modifyLineRequest(self, request, parameters):
        """
        La méthode modifyLine permet de modifier une ligne via UPDATE

        :param lock: le lock
        :param tableName: le nom de la table
        :param fields: les champs
        :param values: les valeurs
        :param conditions: les conditions (Ex: {"id": 3, "nom": "Test"})
        :type tableName: str
        :type fields: list
        :type values: list
        :type conditions: dict
        :return: "True" si réussi, "False" sinon
        :rtype: bool
        """

        with self.lock:
            # Exécution de la requete
            try:
                self.sqlite_cursor.execute(request, parameters)
                self.sqlite_connection.commit()
                result = returnData(True, "update line success!")
            except Exception as ex:
                result = returnData(False, ex)

            return result
def getColumnNamesOfTable(tableName):
    """
    La méthode getColumnNamesOfTable permet d'avoir les noms de tous les colonnes d'une table

    :param tableName: le nom de la table
    :type tableName: str
    :return: liste contenant les noms de tous les colonnes
    :rtype: list
    """

    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()

    # Effectuer une requête sur la table
    sqlite_cursor.execute("SELECT * FROM " + tableName)

    infos = sqlite_cursor.description
    columnNames = []

    for info in infos:
        columnNames.append(info[0])

    return columnNames
def returnData(ok, data):
    """
    La méthode returnData propose un format de return pour les méthodes de base de données

    :param ok: si l'operation s'est bien passée
    :type ok: bool
    :param data: le data associé a l'opération
    :type data: Any
    :return: un dictionnaire sous format {"ok": True/False, "data": "..."}
    :rtype: dict
    """

    return {"ok": ok, "data": data}
def getExceptionFormat(ex):
    return ex.__class__.__name__ + ": " + str(ex)

# ================================== INITIALISATION DU LOGGER ============================================ #
open(LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Linkedin_Browser_Bot__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")
file_handler = logging.FileHandler(LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ===================================   FONCTION D'ENVOI DE MESSAGE À UN PROFIL  ===================================== #
def send_message(driver, profile, databaseTool):
    try:
        driver.implicitly_wait(10)
        driver.get(profile)
        btn_message = driver.find_element_by_xpath("//div[@class='_3lhzE6Cg3SSeQGIHuLjILb GQV0F7lQiMOV6EofzopdJ']//div[last()]/button")
        btn_message.click()
        msg_inputBox = driver.find_element_by_xpath("//textarea[@aria-label='Message #chat']")
        time.sleep(3)
        add_message = "Hey"  # LE MESSAGE À ENVOYER EST IÇI !!!
        databaseTool.addLine("actions", ("platform", "type_action", "message"),
                             ("reddit", "Group moderators", add_message))
        msg_inputBox.send_keys(add_message)
        time.sleep(3)
        sendMessage_button = driver.find_element_by_xpath(
            "//button[@class='_3QHhpmOrsIj9Hy8FecxWKa  _1PhPhuhKHqFwivRAkg2DkH t19vywnuK8ouXSeGyGCTh']")
        sendMessage_button.click()
        time.sleep(3)
        close_btn = driver.find_element_by_xpath(
            "//button[@class='_3QHhpmOrsIj9Hy8FecxWKa  _1PhPhuhKHqFwivRAkg2DkH _2SeZKjVwSpNwqshVnDJkYF bwxXoigjZ4E9ofWIggxmp']")
        close_btn.click()
        time.sleep(5)
    except Exception as ex:
        logger.error(f"Error while sending message to profiles url: {ex}")

# =============================          OUVERTURE DE L'URL DES GROUPES        ============================== #
def urlToID(googleSheetURL):
    """
    La méthode urlToID permet d'extaire l'ID du document à partir d'un lien de Google Sheet

    :param googleSheetURL: Lien Google Sheet complet (Ex: https://docs.google.com/spreadsheets/d/1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o/edit?usp=sharing)
    :type googleSheetURL: str
    :return: id de Google Sheet
    :rtype: str
    """
    return googleSheetURL.split("/")[5]  # Dans l'exemple, id est "1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o"

def getColumnsFromGoogleSheetByURL(googleSheetURL):
    """
    La méthode getColumnsFromGoogleSheetByURL permet d'obtenir les valeurs dans les différentes colonnes de Google Sheet

    :param googleSheetURL: Lien Google Sheet complet
    :type googleSheetURL: str
    :return: Une liste contenant toutes les lignes du Google Sheet
    :rtype: list
    """
    idGoogleSheet = urlToID(googleSheetURL)  # Obtenir id de Google Sheet
    return mymodulesteam.GoogleSheetGetValues(idGoogleSheet)  # Obtenir toutes les lignes du doc

def Open_page(driver,url):
    # ============================ CHARGEMENT DE LA PAGE ================================ #
    # URL DU GROUPE REDDIT
    driver.get(url[0])
    driver.maximize_window()
    driver.implicitly_wait(10)

# =======================================         DEBUT DE LA TÂCHE                  ================================= #
def Browser_Influencers_Facebook_Group_Admins(p_browser, p_taskuser_id, Linkedin_username, p_quantity_actions, label_log, lock):
    """This functions allows to message group admins / moderators of a defined group"""
    logger.info("=============================== [1] Open Browser =======================================")

    # ==================== CHARGEMENT DE LA BASE DE DONNÉES ======================= #
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    databaseTool = DataBaseTool("db.db", lock)

    # ===================== OUVERTURE DU NAVIGATEUR ================================= #
    try:
        if p_browser == "Chrome":
            driver = ChromeDriverWithProfile()
        elif p_browser == "Firefox":
            driver = FireFoxDriverWithProfile()
        else:
            logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
            return False
        #Open_page(driver)  # OUVERTURE DES URL. LA FONCTION EST AU DEBUT DU CODE.
    except Exception as ex:
        logger.error(f"Error profile {ex}")

    tab_url = getColumnsFromGoogleSheetByURL("https://docs.google.com/spreadsheets/d/1I3FcvY-vfYg6XZMzb3jcFhZvlTJGe4GfeFIagrie8MI/edit?usp=sharing")
    for url in tab_url:
        try:
            Open_page(driver, url) # OUVERTURE DES URL. LA FONCTION EST AU DEBUT DU CODE.
            time.sleep(5)
            # ============================= ON RECUPERE LES URL DES PROFILS DES MODERATEURS =============================== #
            try:
                tab_moderators = WebDriverWait(driver, 12).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, (
                            "//div[@class='_1Y_VNBcV1dWk6Y7xcJHQyQ']//a"))
                    )
                )
                number_moderators = len(tab_moderators)
                print("Le nombre de moderateurs de ce groupe est de : " + str(number_moderators))
                time.sleep(3)

                for i in range(number_moderators):
                    print(tab_moderators[i].text[2:len(tab_moderators[i].text)])

                moderators_profiles = []
                moderators_profiles_url = []
        # ========================== C'EST ICI QUE ON AJOUTE A LA BASE DE DONNEES LE NOM DES MODERATEURS ============================ #
                for index in range(number_moderators):
                    moderators_profiles.append(tab_moderators[index].text)
                    moderators_profiles_url.append(tab_moderators[index].get_attribute("href"))
                    databaseTool.addLine("contacts", ("platform", "username"),
                                         ("Reddit", moderators_profiles[index]))
            except Exception as ex:
                logger.error(f"Error while waiting and getting profiles url: {ex}")

            TaskIsDone = False
            while TaskIsDone == False:
                for profile in moderators_profiles_url:
        # ========================== ON OUVRE LE PROFIL D'UN SEUL MODERATEUR ========================= #
                    try:
        # ========================== ON ENVOIE LE MESSAGE ICI. LA FONCTION EST AU DÉBUT DU CODE !!!   ======================== #
                        send_message(driver,profile,databaseTool)
                    except Exception as ex:
                        logger.error(f"Error while sending message to the profile: {ex}")
                TaskIsDone = True
        except Exception as ex:
            logger.error(f"Error while opening the URL: {ex}")
            print("Finsished. The task is done. /n The end...")
            time.sleep(30)  # FIN DU CODE ICI !!!!!!!!!!!!!

"""
p_browser = "Chrome"
p_taskuser_id = "254"
p_driver = ""
Linkedin_username = ""
p_quantity_actions = ""
label_log = ""
lock = threading.Lock()

Browser_Influencers_Facebook_Group_Admins(p_browser, p_taskuser_id, Linkedin_username, p_quantity_actions, label_log, lock)
"""
