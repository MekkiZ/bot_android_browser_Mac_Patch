# -*- coding: utf-8 -*-

"""
Auteur : Pengxiao SHI
Email : s.pengxiao57@gmail.com
Tâche: Browser Authority Facebook share some posts in FB groups
"""
import sqlite3

"""
Éléments à réunir pour exécuter le script
1) Exécuter cette commande SQL dans la base de données: ALTER TABLE actions ADD url_post TEXT
    cela permet d'ajouter une colonne "url_post" dans la table "actions"
2) Dans un dossier, mettre ces fichiers ensembles
    a) db.db
    b) mymodulesteam.py
    c) DatabaseTool.py
    d) GoogleSheetTool.py
    e) credentials_Google_Sheet_API_Account.json
    f) Browser_Authority_Facebook_share_some_posts_in_FB_groups.py
3) Ligne 43 et 44: Indiquer votre login et password de compte Facebook
4) Pour indiquer le lien Google Sheets, 2 moyens:
    a) Si "mymodulesteam.GetDetailsTaskUser(id_task_user)" est opérationnel: ligne 226 à utiliser
    b) Sinon: lignes 229 et 230 à utiliser (vous pouvez utiliser cette méthode pour le test)
    Voici un exemple de format Google Sheets: https://docs.google.com/spreadsheets/d/1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o/edit?usp=sharing
"""

import datetime
import logging
import threading
import time
from modules import mymodulesteam
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from GoogleSheetTool import GoogleSheetTool
# from DatabaseTool import DataBaseTool

"""
    ****************************************************************************************************************
    Class DataBaseTool
    ****************************************************************************************************************
"""


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
                # return True
                return self.returnData(True, "add line success !")
            except Exception as ex:
                return self.returnData(False, ex)

    def getLines(self, columnName, tableName, conditions={}, options=""):
        """
        La méthode getLines permet d'obtenir les lignes via SELECT

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
                else:  # il y a conditions et/ou option
                    rows = self.sqlite_cursor.execute(request, tuple(parameters)).fetchall()

                # Conversion en une liste de dictionnaire
                columnNames = self.getColumnNamesOfTable(tableName)

                rowsFinal = []  # La liste finale contenant toutes les lignes
                rowDict = {}  # Le dictionnaire représentant 1 ligne
                for row in rows:
                    for nbColumns in range(len(row)):
                        rowDict[columnNames[nbColumns]] = row[nbColumns]
                    rowsFinal.append(rowDict.copy())

                return self.returnData(True, rowsFinal)

            except Exception as ex:
                return self.returnData(False, ex)

    def modifyLine(self, tableName, fields, values, conditions):
        """
        La méthode modifyLine permet de modifier une ligne via UPDATE

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
            whereField = " WHERE "  # la clause de "WHERE ..."
            parameters = values.copy()  # les paramètres (value1, value2, ...)
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
                return self.returnData(True, "update line success!")
            except Exception as ex:
                return self.returnData(False, ex)

    def getColumnNamesOfTable(self, tableName):
        """
        La méthode getColumnNamesOfTable permet d'avoir les noms de tous les colonnes d'une table

        :param tableName: le nom de la table
        :type tableName: str
        :return: liste contenant les noms de tous les colonnes
        :rtype: list
        """

        # Effectuer une requête sur la table
        self.sqlite_cursor.execute("SELECT * FROM " + tableName)

        infos = self.sqlite_cursor.description
        columnNames = []

        for info in infos:
            columnNames.append(info[0])

        return columnNames

    def returnData(self, ok, data):
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


""" ************************************************************************************************************ """

"""
    ****************************************************************************************************************
    Class GoogleSheetTool
    ****************************************************************************************************************
"""


class GoogleSheetTool:
    """
    ****************************************************************************************************************
    Méthodes pour gérer l'importation de Google Sheet
    ****************************************************************************************************************
    """

    @staticmethod
    def urlToID(googleSheetURL):
        """
        La méthode urlToID permet d'extaire l'ID du document à partir d'un lien de Google Sheet

        :param googleSheetURL: Lien Google Sheet complet (Ex: https://docs.google.com/spreadsheets/d/1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o/edit?usp=sharing)
        :type googleSheetURL: str
        :return: id de Google Sheet
        :rtype: str
        """
        return googleSheetURL.split("/")[5]  # Dans l'exemple, id est "1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o"

    @staticmethod
    def getColumnsFromGoogleSheetByURL(googleSheetURL):
        """
        La méthode getColumnsFromGoogleSheetByURL permet d'obtenir les valeurs dans les différentes colonnes de Google Sheet

        :param googleSheetURL: Lien Google Sheet complet
        :type googleSheetURL: str
        :return: Une liste contenant toutes les lignes du Google Sheet
        :rtype: list
        """
        idGoogleSheet = GoogleSheetTool.urlToID(googleSheetURL)  # Obtenir id de Google Sheet
        return mymodulesteam.GoogleSheetGetValues(idGoogleSheet)  # Obtenir toutes les lignes du doc

    @staticmethod
    def getColumnsFromGooglesheetsByTaskUserID(p_taskuser_id):
        """
        La méthode getColumnsFromGoogleSheetByURL permet d'obtenir les valeurs dans les différentes colonnes de Google Sheet

        :param p_taskuser_id: id_task
        :type p_taskuser_id: str
        :return: Une liste contenant toutes les lignes du Google Sheet
        :rtype: list
        """
        taskUserDetails = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)  # Obtenir toutes les infos de taskUser
        googleSheetURL = str(taskUserDetails["url_list"])  # Obtenir le lien Google Sheet
        return GoogleSheetTool.getColumnsFromGoogleSheetByURL(googleSheetURL)  # Obtenir toutes les lignes du doc


""" ************************************************************************************************************ """


class BrowserAuthorityFacebookShareSomePostsInFBGroupsClass(object):
    def __init__(self, p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log, lock):

        # Infos pour connecter sur facebook
        self.login = ""
        self.password = ""

        # Sauvegarder les paramètres de la fonction principale
        self.p_browser = p_browser
        self.p_taskuser_id = p_taskuser_id
        self.facebook_username = FB_username
        self.p_quantity_actions = p_quantity_actions
        self.label_log = label_log
        self.lock = lock

        # Initialisation interne des outils
        self.logger = self.initLogger()
        self.driver = p_driver
        # self.driver = webdriver.Firefox()   # Attention: à changer en self.driver = ""
        # self.driver.implicitly_wait(10) # à enlever
        self.dataBaseTool = DataBaseTool("db.db", self.lock)

    """
    ****************************************************************************************************************
    Méthodes de l'initialisation
    ****************************************************************************************************************
    """

    """
        La méthode initLogger initialise le logger pour enregistrer les différents infos pendant l'exécution du Script
    """

    def initLogger(self):
        # ==================== LOG FILE ==================================================
        open(mymodulesteam.LoadFile('log.log'), 'w').close()
        logger = logging.getLogger('__NAME_OF_TASK__')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
        file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        # ================================================================================

        return logger

    """
        La méthode initDriver initialise le driver
    """

    def initDriver(self):
        driver = None

        if self.p_browser == "Chrome":  # Le navigateur utilisé est Chrome
            driver = mymodulesteam.ChromeDriverWithProfile()
        elif self.p_browser == "Firefox":  # Le navigateur utilisé est Firefox
            driver = mymodulesteam.FireFoxDriverWithProfile()
        else:
            self.logger.error(f"PhoneBot didn't find the browser called '{self.p_browser}'.")

        return driver

    """
    ****************************************************************************************************************
    Méthodes utilitaires
    ****************************************************************************************************************
    """

    """
    Random time.sleep for being a stealth bot.
    """

    def Sleeping_Bot(self, borne_inf=float, borne_sup=float):
        ts = random.uniform(borne_inf, borne_sup)
        ts = round(ts, 2)
        time.sleep(ts)

    """
        La méthode lineAlreadyExistsInTable vérifie si une ligne existe dans la table selon un certain critères
    """

    def lineAlreadyExistsInTable(self, tableName, conditions):
        rows = self.dataBaseTool.getLines("*", tableName, conditions)

        if not rows["ok"]:
            self.logger.error("Error during check of the line existence: {}".format(rows["data"]))
            return None

        return len(rows["data"]) >= 1

    """
        La méthode automaticSendKeys remplit les champs de saisi avec un comportement humain
    """

    def automaticSendKeys(self, element, text):
        for letter in text:
            element.send_keys(letter)
            self.Sleeping_Bot(0.2, 0.5)

    """
        La méthode returnData fournit un format de retour apres chaque étape
        {"ok": True/False, "message": "..."}
    """

    def returnMessage(self, ok, message="ok"):
        return {"ok": ok, "message": message}

    """
        La méthode logTitleMessage crée un format pour les titres pour le différentes étapes
        Ex: **************
            *    Test    *
            **************
    """

    def logTitleMessage(self, message):
        lengthOfFirstAndLastLine = len(message) * 3
        return "*" * lengthOfFirstAndLastLine + "\n" \
                                                "*" + (" " * (len(message) - 1)) + message + (
                           " " * (len(message) - 1)) + "*" \
               + "\n" + "*" * lengthOfFirstAndLastLine

    """
        La méthode logSectionMessage cree un format pour les sections dans les étapes
        Ex:  =============== Section ===============
    """

    def logSectionMessage(self, message):
        return "=" * 15 + " " + message + " " + "=" * 15

    """
        La méthode getByType fait la conversion de str vers ByType (Ex: "xpath" -> By.XPATH)
    """

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        byTypes = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css_selector": By.CSS_SELECTOR,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME
        }
        if locatorType not in byTypes:
            return None

        return byTypes[locatorType]

    """
        La méthode findElement cherche un élément dans la page selon un locatorType et un locator
    """

    def findElement(self, locatorType, locator):

        byType = self.getByType(locatorType)

        if byType is None:
            return None

        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((byType, locator)))

    """
        La méthode findElements cherche tous les éléments dans la page selon un locatorType et un locator
    """

    def findElements(self, locatorType, locator):
        byType = self.getByType(locatorType)

        if byType is None:
            return None

        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((byType, locator)))

    """
        La méthode clickOnElement clique sur l'élément passé en paramètre
    """

    def clickOnElement(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    """
        La méthode scrollToElement scroll la page à l'emplacement de l'élément
    """

    def scrollToElement(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    """
        La méthode scroll monte ou descend la page
    """

    def scroll(self, x, y):
        self.driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x, y)

    """
        La méthode preparePostsToShare prépare les posts à partager
    """

    def preparePostsToShare(self):
        # Version finale
        # postAndGroupsFromSpreadsheet = GoogleSheetTool.getColumnsFromGooglesheetsByTaskUserID(self.p_taskuser_id)

        # Version temporaire

        task_detail = mymodulesteam.GetDetailsTaskUserMysql(self.p_taskuser_id)
        # mymodulesteam.GoogleSheetGetValues(mymodulesteam.extract_ss_id_regex(task_detail["url_list"]))
        postAndGroupsFromSpreadsheet = GoogleSheetTool.getColumnsFromGoogleSheetByURL(task_detail["url_list"])

        postAndGroupsFinal = []

        for line in postAndGroupsFromSpreadsheet:
            lineDict = {
                "url": line[0],
                "groups": line[1].split(";")
            }
            postAndGroupsFinal.append(lineDict)

        return postAndGroupsFinal

    """
        La méthode getGroupIDsFromElement permet d'obtenir les ids des groupes à partir d'une liste d'éléments
        Ex: {'787883271852159': <selenium.webdriver.remote.webelement.WebElement...>}
    """

    def getGroupIDsFromElement(self, listElements):
        dictGroupIDs = {}
        for element in listElements:
            href = element.get_attribute("href")
            if "user" in href:
                idElement = href.split("/")[6]
            else:
                idElement = href.split("/")[4]
            dictGroupIDs[idElement] = element

        return dictGroupIDs

    """
        La méthode isThisGroupUndone permet de savoir si le groupe a déjà partagé le post
        (due a l'arrêt de p_quantuty_actions)
        Ex: {'787883271852159': <selenium.webdriver.remote.webelement.WebElement...>}
    """

    def isThisGroupUndone(self, postURL, groupId):
        groupURL = "https://www.facebook.com/groups/" + groupId
        tableName = "actions INNER JOIN contacts ON actions.id_contact = contacts.id"
        conditions = {"actions.type_action": "share_post", "actions.id_task_user": self.p_taskuser_id,
                      "actions.platform": "facebook", "contacts.type": "group", "contacts.url_facebook": groupURL,
                      "url_post": postURL}

        lineExists = self.lineAlreadyExistsInTable(tableName, conditions)

        if lineExists is None:
            return False

        return not lineExists

    """
        La méthode getUndoneGroups permet d'obtenir les groupes qu'on n'a pas encore posté
        Ex: {'787883271852159': <selenium.webdriver.remote.webelement.WebElement...>}
    """

    def getUndoneGroups(self, postURL, dictGroupIDs):
        dictUndoneGroupIDs = {}

        for groupID in dictGroupIDs:
            if self.isThisGroupUndone(postURL, groupID):
                dictUndoneGroupIDs[groupID] = dictGroupIDs[groupID]

        return dictUndoneGroupIDs

    """
        La méthode getExceptionFormat donne un format pour l'affichage des exceptions
        Ex: TimeoutException: No such element found
    """

    def getExceptionFormat(self, ex):
        return ex.__class__.__name__ + ": " + str(ex)

    """
    ****************************************************************************************************************
    Les étapes de la tâche
    ****************************************************************************************************************
    """

    """
    Étape 1 : connecter a Facebook
    """

    def facebookConnection(self):
        try:
            self.logger.info("Search textfield Email ...")
            email = self.findElement("id", "email")

            self.logger.info("Search textfield Password ...")
            password = self.findElement("id", "pass")

            self.logger.info("Search button Log In ...")
            buttonConnection = self.findElement("xpath",
                                                "//button[contains(text(), \"Connexion\") or contains(text(), \"Log In\")]")

            self.logger.info("Enter email ...")
            self.automaticSendKeys(email, self.login)

            self.logger.info("Enter password ...")
            self.automaticSendKeys(password, self.password)

            self.logger.info("Click on Log In ...")
            self.clickOnElement(buttonConnection)

            self.logger.info("Step 1 : Connection Facebook ... Success !")

            return self.returnMessage(True)

        except Exception as ex:
            return self.returnMessage(False, self.getExceptionFormat(ex))

    """
    Étape 2 : Partager les posts aux groupes
    """

    """
    La méthode getGroupsToShare permet de réaliser les étapes c.1) à c.3) de la méthode sharePostsToGroups
    """

    def getGroupsToShare(self, groupName):
        self.logger.info("Find \"share\" button ...")
        # buttonShare = self.findElement("xpath", "//span[contains(text(), \"Partager\") or contains(text(), \"Share\")]"
        #                                         "/ancestor::div[contains(@aria-label, \"publiez-le sur votre journal\")"
        #                                         "or contains(@aria-label, \"post it on your timeline\")]")
        buttonShare = self.findElement("xpath", '//div[contains(@aria-label, "publie") or contains(@aria-label, '
                                                '"post") and not(contains(@aria-haspopup, "menu"))]')

        self.logger.info("Click on \"share\" button ...")
        self.clickOnElement(buttonShare)

        self.logger.info("Find \"share to a group\" button ...")
        # buttonShareToAGroup = self.findElement("xpath", "//span[contains(text(), \"Partager dans un groupe\") "
        #                                                 "or contains(text(), \"Share to a group\")]"
        #                                                 "/ancestor::div[@role=\"button\"]")
        buttonShareToAGroup = self.findElement('xpath', '// span[contains(text(), "group")]')

        self.logger.info("Click on \"share to a group\" button ...")
        self.clickOnElement(buttonShareToAGroup)

        self.logger.info("Find textfield to filter groups ...")
        textfieldSearchGroup = self.findElement("xpath", "//input[@placeholder=\"Rechercher des groupes\""
                                                         "or @placeholder=\"Search for groups\"]")

        self.logger.info("Enter the name of the group ...")
        self.automaticSendKeys(textfieldSearchGroup, groupName)

    """
    Résumé du partage des posts aux groupes:
        a) On récupère les posts et les groupes via Google Sheet
        b) Pour chaque lien URL d'un post, on fait:
            b.1) ouvrir le lien du post
        c) Pour chaque nom de groupe de ce lien URL, on fait:
            c.1) cliquer sur "partager"
            c.2) cliquer sur "partager dans un groupe"
            c.3) on rentre le nom du groupe dans la barre de recherche pour filtrer
            c.4) Pour chaque groupe FB indiqué après filtrage, on fait:
                c.4.1) vérifier si le post a déjà été publier dans ce groupe
                c.4.2) mise à jour de la table "contacts" (si c'est pas déjà présent)
                c.4.3) cliquer sur ce groupe puis "partager"
                c.4.4) mise à jour de la table "actions)
    """

    def sharePostsToGroups(self):
        # Nombre de posts partagés
        nbSharedPosts = 0
        try:
            """--------- a) On récupère les posts et les groupes via Google Sheet ------------------------------"""
            # Obtenir les colonnes de Googles Sheets
            self.logger.info("Get Google Sheet Columns ...")

            # Convertir en "dict" pour un simple usage par la suite
            postAndGroups = self.preparePostsToShare()  # Si Exception, on ne peut pas avoir les colonnes de
            # Google Sheets, donc on quitte cette fonction

            self.logger.info("Share Posts ...")



            """--------- b) Pour chaque lien URL d'un post, on fait: ------------------------------"""
            for lineDict in postAndGroups:
                try:
                    """--------- b.1) ouvrir le lien du post ------------------------------"""
                    self.logger.info(
                        self.logTitleMessage("Share post N°{} ...".format(postAndGroups.index(lineDict) + 1)))
                    self.driver.get(lineDict["url"])  # Si Exception, on passe à la ligne suivante
                    self.Sleeping_Bot(1, 2)

                    # Scroll afin de bien voir le post en question
                    scrollElement = self.findElement("xpath", "//div[@aria-label=\"Actions pour cette publication\" or "
                                                              "@aria-label=\"Actions for this post\"]")
                    self.scrollToElement(scrollElement)  # Si Exception, on passe à la ligne suivante
                    self.scroll(0, -300)
                    self.Sleeping_Bot(0.5, 1)

                    """--------- c) Pour chaque nom de groupe de ce lien URL, on fait: ------------------------------"""
                    for group in lineDict["groups"]:
                        try:
                            # Booléen indiquant si on a fini pour un nom de groupe indiqué dans Google Sheet
                            allPosted = False

                            # Numérotation utile en cas de plusieurs groupes ayant le même nom après filtrage
                            serie = 1

                            # Tant qu'on n'a pas fini de partager dans la liste des groupes proposés après filtrage
                            while not allPosted:
                                self.logger.info(
                                    self.logSectionMessage("Share Post N°{} for Group \"{}\" serie N°{}...").format(
                                        postAndGroups.index(lineDict) + 1, group, serie))

                                """ 
                                    c.1) cliquer sur "partager"
                                    c.2) cliquer sur "partager dans un groupe"
                                    c.3) on rentre le nom du groupe dans la barre de recherche pour filtrer
                                """
                                self.getGroupsToShare(group)  # Si Exception, on passe au groupe suivant

                                # Obtenir tous les éléments <a> resultats
                                groupsAfterFilter = self.findElements("xpath", "//div[@class=\"\"]"
                                                                               "/a[starts-with(@href,\"/groups/\") or "
                                                                               "starts-with(@href,\"https://www.facebook.com/groups/\")]")  # Si Exception, on passe au groupe suivant

                                # Conversion en dictionnaire pour une simple usage par la suite
                                dictGroupIDs = self.getGroupIDsFromElement(groupsAfterFilter)

                                """---------c.4.1) vérifier si le post a déjà été publié dans ce groupe-----------"""
                                # Récupérer uniquement des groupes que l'on n'a pas encore posté
                                print(self.getUndoneGroups(lineDict["url"], dictGroupIDs))
                                self.logger.info("check already shared groups ...")
                                dictUndoneGroupIDs = self.getUndoneGroups(lineDict["url"], dictGroupIDs)

                                # Il reste encore des groupes à poster
                                if len(dictUndoneGroupIDs) >= 1:
                                    # Obtenir le groupID du premier élément
                                    groupID = list(dictUndoneGroupIDs.keys())[0]
                                    # Obtenir l'élement <a> du groupe associé
                                    element = dictUndoneGroupIDs[groupID]
                                    # Initialiser l'id_contact
                                    id_contact = -1
                                    # Initialiser la date d'aujourd'hui
                                    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                                    """---c.4.2) mise à jour de la table "contacts" (si c'est pas déjà présent)---"""
                                    urlFacebook = "https://www.facebook.com/groups/" + groupID

                                    # Vérification de l'existence de ce groupe dans la table "contact"
                                    self.logger.info("check this group in table database ...")
                                    rows = self.dataBaseTool.getLines("contacts.id", "contacts", {
                                        "platform": "facebook", "type": "group", "url_facebook": urlFacebook})

                                    # requête SELECT non réussie: on passe au groupe suivant
                                    if not rows["ok"]:
                                        self.logger.info(
                                            "SELECT failed, Impossible to know if this post is shared in this group")
                                        raise NameError(
                                            "SELECT failed, Impossible to know if this post is shared in this group")

                                    # le groupe n'existe pas encore dans la table "contacts"
                                    if len(rows["data"]) == 0:
                                        # Insertion de ce groupe dans la table "contacts"
                                        self.logger.info("Cannot find this group in database, insert it ...")
                                        groupName = dictUndoneGroupIDs[groupID].find_element_by_xpath(
                                            "./ancestor::div[@role=\"button\"]//span[1]").text

                                        addResult = self.dataBaseTool.addLine("contacts",
                                                                              ("platform", "type", "username",
                                                                               "url_facebook", "id_task_user",
                                                                               "date_created", "date_update"),
                                                                              ("facebook", "group", groupName,
                                                                               urlFacebook, self.p_taskuser_id,
                                                                               today, today))

                                        # Insertion de ce groupe dans "contacts" échoué: on passe au groupe suivant
                                        if not addResult["ok"]:
                                            self.logger.info(f"Insertion of {groupName} failed - {addResult['data']}")
                                            raise NameError(f"INSERT of {groupName} failed")

                                        self.logger.info("insertion: success ...")

                                        id_contact = self.dataBaseTool.sqlite_cursor.lastrowid

                                    # le groupe existe déjà dans la table "contacts"
                                    else:
                                        self.logger.info("This group found in database ...")
                                        id_contact = rows["data"][0]["id"]

                                    """---c.4.3) cliquer sur ce groupe puis "partager"---"""
                                    # cliquer sur ce groupe
                                    self.logger.info("find button \"share for this group\" ...")
                                    buttonShareForThisGroup = element.find_element_by_xpath(
                                        "./ancestor::div[@role=\"button\"][1]")
                                    self.logger.info("click on \"share for this group\" ...")
                                    self.clickOnElement(buttonShareForThisGroup)
                                    self.Sleeping_Bot(1, 2)

                                    # cliquer sur "publier"
                                    self.logger.info("find button \"Post\" ...")
                                    buttonPost = self.findElement("xpath",
                                                                  "//div[@aria-label=\"Post\" or @aria-label=\"Publier\"]"
                                                                  "[@role=\"button\"]")

                                    # buttonPost = self.findElements(
                                    #     'xpath', '//div[contains(@aria-label, "post") or contains(@aria-label, "publie")]')

                                    self.logger.info("click on button \"Post\" ...")
                                    self.clickOnElement(buttonPost)
                                    self.Sleeping_Bot(5, 7)

                                    """---c.4.4) Mise à jour de la table "actions"---"""
                                    self.logger.info("Insert this action in table \"actions\" ...")

                                    fields = ("platform", "type_action", "date", "id_smartphone", "id_social_account",
                                              "id_contact", "id_task_user", "url_post", "date_created", "date_update")
                                    values = ("facebook", "share_post",
                                              str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                                              self.p_browser, self.facebook_username, id_contact, self.p_taskuser_id,
                                              lineDict["url"], today, today)

                                    insertionResult = self.dataBaseTool.addLine("actions", fields, values)
                                    if not insertionResult["ok"]:
                                        self.logger.info(
                                            "\"actions\" table update failed {}".format(insertionResult["data"]))
                                    else:
                                        self.logger.info("Insertion: Success ! ...")
                                        nbSharedPosts += 1

                                        if nbSharedPosts == self.p_quantity_actions:
                                            return True, nbSharedPosts

                                    # Il s'agissait du dernier groupe proposé après le filtrage
                                    if len(dictUndoneGroupIDs) == 1:
                                        self.logger.info(
                                            self.logSectionMessage(
                                                "Share Post N°{} for Group \"{}\": Success ! ...").format(
                                                postAndGroups.index(lineDict) + 1, group, serie))
                                        allPosted = True

                                # aucun groupe après filtrage
                                else:
                                    self.logger.info("No result found for Group {}".format(group))
                                    self.logger.info(
                                        self.logSectionMessage(
                                            "Share Post N°{} for Group \"{}\": Success ! ...").format(
                                            postAndGroups.index(lineDict) + 1, group, serie))
                                    allPosted = True

                                # Augmenter la série de 1
                                serie += 1

                                """Test: à enlever dans la version finale"""
                                """
                                buttonClose = self.findElement("xpath",
                                    "//div[@aria-label = \"Fermer\" or @aria-label = \"Close\"]")
                                self.clickOnElement(buttonClose)
                                """
                                """------------------------------------"""
                                # Close share popup
                                close_popup = self.findElement("xpath",
                                                               '//*[@role="button" and contains(@aria-label, "Close") or contains(@aria-label, "Fermer")]')
                                self.clickOnElement(close_popup)

                            self.Sleeping_Bot(0.5, 1)

                        except Exception as ex:
                            close_popup = self.findElement("xpath",
                                                           '//*[@role="button" and contains(@aria-label, "Close") or contains(@aria-label, "Fermer")]')
                            self.clickOnElement(close_popup)
                            self.logger.info(f"Share to Group {group} failed: {self.getExceptionFormat(ex)}")
                except Exception as ex:
                    self.logger.info(
                        f"Open URL of Post N°{postAndGroups.index(lineDict) + 1} failed: {self.getExceptionFormat(ex)}")
            return True, nbSharedPosts
        except Exception as ex:
            return False, nbSharedPosts

    def run(self):
        # Initialiser le driver
        # self.driver = self.initDriver()
        # self.driver.implicitly_wait(10)

        # if self.driver is None:   # Une erreur est survenue au niveau de l'initialisation du driver
        #     self.logger.error("Error: initialize driver failed !")
        #     return False

        self.logger.info(self.logTitleMessage("Step 1 : Connection Facebook"))

        # Ouvrir Facebook
        # self.driver.get("https://www.facebook.com/")
        #
        # # Vérification si l'utilisateur est déjà connecté
        # self.logger.info("Check if user is already connected ...")
        # try:
        #     textfieldSearch = self.findElement("xpath", "//input[@type=\"search\"][@placeholder=\"Search Facebook\""
        #                                                 "or @placeholder=\"Rechercher sur Facebook\"]")
        # except:
        #     textfieldSearch = None
        #
        # # l'utilisateur pas encore connecté: faire la connexion
        # if textfieldSearch is None:
        #     self.logger.info("Not yet connected: connection ...")
        #     result = self.facebookConnection()
        #
        #     # connexion échoué
        #     if not result["ok"]:
        #         self.logger.error("{}: connection to Facebook failed !".format(result["message"]))
        #         return False
        #
        # # l'utilisateur déjà connecté
        # else:
        #     self.logger.info("already connected ! ")
        #     self.logger.info(self.logSectionMessage("Step 1 : Connection Facebook ... Success ! "))
        #
        # self.Sleeping_Bot(3, 5)

        # Partager les posts
        self.logger.info(self.logTitleMessage("Step 2 : Share posts"))
        result, counter = self.sharePostsToGroups()

        # if not result["ok"]:
        if not result:
            self.logger.error("{}: Share posts to Groups failed !".format(result["message"]))
            return False

        self.logger.info(self.logSectionMessage("Step 2 : Share posts ... Success ! "))

        return True, counter


def Browser_Authority_Facebook_share_some_posts_in_FB_groups(
        p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log, lock):
    """

    :param p_browser: "firefox" or "chrome"
    :param p_taskuser_id: The Id N° in database of the user task (ex: 254 )
    :param facebook_username: The username of the current user which will send the message (The Sender)
    :param p_quantity_actions: The quantity maximum of actions. Ex: 5 messages to 5 members
    :param label_log: THis is the label of our GUI (PyQt5). It will display the message you want to the user interface. THis is very useful for displaying important error.
    :param lock: This function will be executed inside a thread. The program PhoneBot use multithread to run different tasks at same times on different devices (browser desktop, smartphones).
    If several tasks save at same time some data in SQLITE3 database, there will be some error for multiple access at same time. We need to "Lock" the access.
    You simply create it with this line of code : lock = threading.Lock()
    :return: True if everything was fine or False if error
    """

    browserAuthorityFacebookShareSomePostsInFBGroupsClass = BrowserAuthorityFacebookShareSomePostsInFBGroupsClass(
        p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log, lock)

    result, counter = browserAuthorityFacebookShareSomePostsInFBGroupsClass.run()

    browserAuthorityFacebookShareSomePostsInFBGroupsClass.dataBaseTool.sqlite_connection.close()

    return result, counter


"""
****************************************************************************************************************
Phase de l'execution
****************************************************************************************************************
"""
# p_browser = "Firefox"
# p_taskuser_id = "297"
# FB_username = ""
# p_quantity_actions = 5
# label_log = ""
# lock = threading.Lock()
# p_driver = mymodulesteam.FireFoxDriverWithProfile()
#
# Browser_Authority_Facebook_share_some_posts_in_FB_groups(p_browser, p_taskuser_id, p_driver,
#                                                          FB_username, p_quantity_actions, label_log, lock)

"""
****************************************************************************************************************
Phase de Debug
****************************************************************************************************************
"""
"""
test = BrowserAuthorityFacebookShareSomePostsInFBGroupsClass(p_browser_run, p_taskuser_id_run,
            facebook_username_run, p_quantity_actions_run, label_log_run, lock_run)
test.run()
"""

# print(test.getContactIDByGroupName("facebook", "group", "haha", "277"))


# Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7(p_browser, p_taskuser_id, Linkedin_username,
#                                                     p_quantity_actions, label_log, lock)

"""
lienGoogleSheet = "https://docs.google.com/spreadsheets/d/1CQFoq_4WVsRTEts6szLn2HIx8w9fNgWy5UzqxbPR26o/edit?usp=sharing"
print(type(GoogleSheetTool.getColumnsFromGoogleSheetByURL(lienGoogleSheet)))
"""

"""
dataBaseTool = DataBaseTool("db.db", lock_run)

# test insert
res = dataBaseTool.addLine("contacts", ("platform", "type", "username"), ("facebook", "group", "haha"))
"""

"""
# test update
res = dataBaseTool.modifyLine("contacts", ["platform", "type", "username"], ["twitter", "user", "hahaha"],
                              {"username": "mom", "platform": "facebook", "type": "group"})
"""

"""
# test select
#res = dataBaseTool.getLines("*", "contacts", {"username": "hahaha", "platform": "twitter", "type": "user"}, {"ORDER BY": "id"})
#res = dataBaseTool.getLines("*", "contacts", {"type": "user"}, "ORDER BY id ASC")
#c = dataBaseTool.getColumnNamesOfTable("contacts")
"""
"""
print(res)
"""
