# -*- coding: utf-8 -*-

"""
Author : Heubo Thierry
Email : Heubothierry@gmail.com
Pour le test, un compte leboncoin est pas nécessaire !!!

Cette tâche a pour but de cliquer sur rechercher pour faire apparaitre des annonces aléatoires et puis recupére
les premiéres annonces affichées puis pour chacune d'elles, il va recupérer leur nom, leur prix et la description.
Elle peut aussi envoyer un message au vendeur si vous êtes conecté. Faudrait décommenter la fonction que j'ai mise du coup.
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

# ===========================     FONCTIONS UTILISÉES DANS LE CODE. À MODIFIER SELON LES BESOINS !!!   ======================= #
def Open_page(driver):
    # ============================ CHARGEMENT DE LA PAGE ================================ #
    # URL DU GROUPE REDDIT
    driver.get("https://www.leboncoin.fr/")
    driver.maximize_window()
    driver.implicitly_wait(10)

def Search_Keyword(driver):
    # ======== ICI J'ENTRE LE MOT CLÉ QUE JE VOUDRAIS RECHERCHER =============================== #
    try:
        # Keyword = "PS4"
        # searchArea = driver.find_element_by_xpath("//input[contains(@autocomplete,'search'  )]")
        # searchArea.send_keys(Keyword)
        # time.sleep(2)
        # # # ============== AINSI QUE LA LOCALISATION AUTOUR DE MOI DE 30 KM PAR DÉFAUT =================== #
        # # positionArea = driver.find_element_by_xpath(" //input[contains(@autocomplete,'search')]")
        # # positionArea.click()
        # # localisation = driver.find_element_by_xpath(
        # #     "//body/div[@id='__next']/div[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/li[1]/div[1]")
        # # localisation.click()
        # # time.sleep(2)
        # searchButton = driver.find_element_by_xpath("//body/div[@id='__next']/div[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[2]/div[2]/div[1]/div[1]/div[5]/div[1]/button[1]")
        # searchButton.click()
        SearchButton = driver.find_element_by_xpath("//a[@title= 'Rechercher']")
        SearchButton.click()
    except Exception as ex:
        logger.error({ex}, "CHECK THE FUNCTION Search_Keyword !")
        driver.quit()

def send_message(driver):
    # ================= LA FONCTION QUI ENVOIE UN MESSAGE AUX ACHETEURS =========================== #
    button_message = driver.find_element_by_xpath("//button[contains(text(),'Message')]")
    button_message.click()
    textarea = driver.find_element_by_xpath("//textarea[@class='_2ZiEE _1xjni']")
    message = "Je suis interessé par l'offre."
    textarea.send_keys(message)
    send_message = driver.find_element_by_xpath("//button[contains(text(),'Envoyer')]")
    send_message.click()


# =======================================      !!!!!   DEBUT DE LA TÂCHE  !!!!!                ================================= #
def Browser_leboncoin_ADS(p_browser, p_taskuser_id, Linkedin_username, p_quantity_actions, label_log, lock):
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
        Open_page(driver) # OUVERTURE DES URL. LA FONCTION EST AU DEBUT DU CODE.
    except Exception as ex:
        logger.error(f"Error profile {ex}, YOU CAN ALSO CHECK THE FUNCTION Open_page !")

    # ===================== ON RECHERCHE POUR CHAQUE MOT-CLÉ DES ANNONCES EN PRENANT JUSTE LA 1ÉRE PAGE =================== #
    try:
        Search_Keyword(driver) # LA FONCTION EST VERS LE HAUT ^
        time.sleep(3)
        ScrollToTheEnd(driver)
        tab_ads = WebDriverWait(driver, 12).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, (
                "//div[@class='sc-bdVaJa crGigL']//a"))
            )
        )
        tab_ads_url = []
        for ads in range(len(tab_ads)):
         tab_ads_url.append(tab_ads[ads].get_attribute("href"))
        time.sleep(3)

# ========================= POUR CHAQUE URL D'ANNONCE, JE M'EM VAIS RECUPÉRER LEURS INFORMATIONS ============================== #
        nom_ads = []
        prix_ads = []
        description_ads = []
        index = 0
        TaskIsDone = False
        while TaskIsDone == False:
            logger.info("___________Debut de la collecte de données_____________")
            for url in tab_ads_url:
                driver.get(url)
                name_ads = driver.find_element_by_xpath("//h1[@class='-HQxY _38n__ _2QVPN _3zIi4 _2-a8M _1JYGK _35DXM']")
                nom_ads.append(name_ads.text)
                price_ads = driver.find_element_by_xpath("//div[@class='sc-bdVaJa fGCvsR']//span")
                prix_ads.append(price_ads.text)
                info_ads = driver.find_element_by_xpath("//div[@class='_2BMZF _137P- P4PEa _3j0OU']//p")
                description_ads.append(info_ads.text)
                time.sleep(3)
                # send_message(driver) # POUR ENVOYER UN MESSAGE AU ACHETEUR, IL FAUT SE CONNECTER SUR LEBONCOIN.
                print("Nom de l'annonce : "+nom_ads[index])
                print("Prix de l'annonce : "+prix_ads[index])
                print("Description de l'annonce : "+description_ads[index])
                print(" ")
                # J'AURAIS VOULU AJOUTER CES INFORMATIONS DANS LA BASE DE DONNÉES MAIS JE NE VOIS PAS DANS QUELLE CASE DU
                # DU TABLEAU ON PEUT LES METTRE, DU COUP JE LES AFFICHE DANS LA CONSOLE.
                index = index + 1
            TaskIsDone = True
    except Exception as ex:
        logger.error(f"Error while getting url of ADS: {ex}")
        print("Finsished. The task is done. /n The end...")
        logger.info("__________ FIN DE LA TÂCHE _________ !!!!!")
    time.sleep(30) # FIN DU CODE ICI !!!!!!!!!!!!!

"""
p_browser = "Chrome"
p_taskuser_id = "254"
p_driver = ""
Linkedin_username = ""
p_quantity_actions = ""
label_log = ""
lock = threading.Lock()

Browser_leboncoin_ADS(p_browser, p_taskuser_id, Linkedin_username, p_quantity_actions, label_log, lock)
# =======================================      !!!!!   DEBUT DE LA TÂCHE  !!!!!                ================================= #
"""
    # pass
