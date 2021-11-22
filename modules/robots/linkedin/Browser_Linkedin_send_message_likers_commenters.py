# -*- coding: utf-8 -*-

"""
Auteur : Billy NGUEDJIO
Email : nguedjiobilly@gmail.com

identifiant de connexion pour le test :
    username: 'TheMouMou_2'
    password: '1234AZER'
"""
import os
import datetime
import logging
import sqlite3
import threading
import time
from modules import mymodulesteam
import random
import re
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

#---------------------------------------------------------------------------------------------------------------------#
"""
*****************************************************************************************************************
Fonctions à compléter
*****************************************************************************************************************
"""
def contact_has_replied(driver, contact, last_message):
    """
    La fonction contact_has_replied permet de savoir si un contact a répondu à notre message précédent
    :param contact: un dictionnaire contenant toutes les infos du contact (voir les colonnes de la table "contacts")
            Par exemple: * contact["username"] donne username du contact en question
                         * contact["url_..."] donne url de contact en question
    
    :param last_message: le dernier message qu'on a envoyé
    :return: une liste sous format suivant [True/False (le contact a répondu ou non), la réponse de contact]
            Par exemple: [True, "Bonjour, je veux bien !"] signifie que le contact a répondu et la réponse est
            "Bonjour, je veux bien !"
    """

    # initialiser les variables de retour
    has_replied = False
    answer = ""

    """
        Code pour savoir si le contact a répondu et récupérer la réponse
    """
    # Go to message section 
    driver.get(contact["url_profile"])
    
    time.sleep(2)
    #on clique sélection le compte 
    sendmess=driver.find_element_by_xpath("//a[@role='button']")
    driver.execute_script("arguments[0].click();", sendmess)

    time.sleep(4)
    # On cherche la balise "<span>" qui contient notre message
    messageList=driver.find_elements_by_xpath("(//div[contains(@class, 'msg-s-event-listitem') and not(contains(@class,'msg-s-event-listitem--other')) and  not(contains(@class,'msg-s-event-listitem__message-bubble')) and not(contains(@class, 'msg-s-event-listitem__seen-receipts'))])[last()]//p[contains(@class, 'msg-s-event-listitem__body')]/following::p[contains(@class, 'msg-s-event-listitem__body')]")
  
    has_replied = len(messageList) >= 1

    for msg in messageList:
        message = msg.text
        answer += message + " "

    return [has_replied, answer.strip()]
    
def send_message(driver, contact, message):
    """
    La fonction send_message permet d'envoyer le message à une personne sur la plateform
    :param contact: contient toutes les infos de la personne à qui on envoie le message (table "contacts")
                Par exemple: contact["username"] ---> username de la personne à contacter
                             contact["url_..."]  ---> l'url de la personne à contacter
    :param message: le message à envoyer
    :return: True / False indiquant si on a réussi à envoyer le message
    """

    try:
        # Go to message section 
        driver.get(contact["url_profile"])
    
        time.sleep(2)
        #on clique sélection le compte 
        sendmess=driver.find_element_by_xpath("//a[@role='button']")
        driver.execute_script("arguments[0].click();", sendmess)

        #envoyer le message: 
        textbox= driver.find_element_by_xpath("//div[@role='textbox']")
        automaticSendKeys(textbox,message)

        #cliquer sur le boutton envoyer 
        btnSen= driver.find_element_by_xpath("//button[@type='submit']")
        clickOnElement(driver,btnSen)

        time.sleep(5)
        

        return True
    except:
        return False
    

def contact_has_replied_invitation(driver, contact):
    """
    La fonction contact_has_replied_invitation permet de savoir si la personne a accepté notre invitation
    :param contact: contient toutes les infos de la personne en question (voir la table "contacts")
            Par exemple: contact["username"] ---> username de la personne en question
    :return: True / False indiquant s'il a accepté notre invitation
    """
       

    """
    Code pour savoir si le contact a accepté notre invitation
        ...
        ...
        has_replied_invitation = True / False
    """
    
    try:
        driver.find_element_by_xpath("//a[@role='button']")
        return True
    except:
        return False

    

def need_invitation(driver, url_contact):
    """
    La fonction need_invitation permet de savoir si on doit lui lancer une invitation pour pouvoir parler à ce dernie
    :param url_contact: l'url de la personne en question
    :return: True / False indiquant si oui ou non on doit lui inviter de l'invitation pour parler
    """

    need_invitation = True

    """
    Code pour savoir s'il faut lui lancer une invitation pour pouvoir parler à ce dernier
    ...
    ...
    ...
    """

    return need_invitation

def send_invitation(driver, url_contact, invitation_message):
    """
    La fonction send_invitation permet d'envoyer une invitation à la personne avec qui on veut parler
    :param url_contact: l'url de la personne en question
    :return: True / False indiquant si l'envoi de l'invitation est avec succès
    """
    driver.get(url_contact)

    try:
        button_connect = driver.find_element_by_xpath("//button[@data-control-name='connect']")
        clickOnElement(driver,button_connect)
        
        time.sleep(3)

        button_sennote = driver.find_element_by_xpath("//button[@aria-label='Ajouter une note' or @aria-label='Add a note']")
        clickOnElement(driver,button_sennote)
        
        button_aeramessage = driver.find_element_by_xpath("//textarea[@name='message']")
        automaticSendKeys(button_aeramessage,invitation_message)

        time.sleep(2)

        button_sennote = driver.find_element_by_xpath("//button[@aria-label='Envoyer maintenant' or @aria-label='Send now']")
        clickOnElement(driver,button_sennote)
        
        return True
        
    except:
        return False


def contact_in_database(dataBaseTool, logger, platform, browser, id_task_user, current_username, contact_to_check, today):
    """
    La fonction contact_in_database permet de savoir si conact_to_check (usernameà est dans la base)
    à customiser si nécessaire
    :param dataBaseTool:
    :param logger:
    :param platform:
    :param browser:
    :param id_task_user:
    :param current_username:
    :param contact_to_check: l'username de la personne à vérifier
    :param today:
    :return: True / False indiquant s'il existe
    """
    res = dataBaseTool.getLinesRequest("SELECT * FROM contacts "
        "WHERE platform=? AND id_task_user=? AND username=?", (platform, id_task_user, contact_to_check))

    if not res["ok"]:
        logger.info("Error while checking contact existence !")
        return None

    # contacts: OK
    if len(res["data"]) >= 1:
        res2 = dataBaseTool.getLinesRequest("SELECT * FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND contacts.username=? AND actions.type_action=? AND actions.id_social_account=?",
                               (platform, id_task_user, contact_to_check, "scrap", current_username))

        if not res2["ok"]:
            logger.info("Error while checking contact existence !")
            return None

        # actions: not OK
        if len(res2["data"]) == 0:
            if not dataBaseTool.addLine("actions", ("platform", "type_action", "id_smartphone", "id_social_account",
                                             "id_contact", "date_created", "date_update", "id_task_user"),
                           (platform, "scrap", browser, current_username, res["data"][0]["id"], today, today,
                            id_task_user))["ok"]:
                logger.info("add new action \"scrap\" failed !")
                return None

        return True

    # contacts: not OK
    else:
        return False

def search_new_contacts(driver, dataBaseTool, logger, platform, browser, id_task_user, current_username, today, rest):
    """
    La fonction search_new_contacts permet d'avoir une liste de nouveaux contacts à ajouter dans la base
    :param driver: le driver
    :return: une liste de contact sous format [[username1, url1], [username2, url2], ...]
    """
    list_of_contacts = getColumnsFromGoogleSheetByURL("https://docs.google.com/spreadsheets/d/1if1G9g9cpOXrdFdzR_dHENOqgZ9Wop3Osp7wWBwkU3k/edit#gid=0")



    #on se rédirige vers une url
    news_comptes=[] #liste de noms de comptes
    for url in list_of_contacts: 
        driver.get(url[0])
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 200);")
        
        if len(news_comptes)>=rest: break # on vérifie si on est bien dans la limite des comptes

        #on click sur le champ permettant d'afficher la liste des likes
        
        likers=driver.find_elements_by_xpath("//button[@class='social-details-social-counts__count-value t-12 t-black--light t-normal hoverable-link-text ']")        
        driver.execute_script("arguments[0].click();", likers[0]) #on vérifie le nombre d'élément que nous renvoie le Xpath pour cliquer sur le bon
        
        time.sleep(5)# on patiente pour que la liste des personnes qui ont aimé s'affiche totalement
    
        
        lastScrollTop=-1 #top du dernier scroll
        currentScrollTop=-2 #top du scroll actuel

        #liste entière des personnes qui ont liker/des personnes qui ont aimé un post
        likers_list= driver.find_element_by_xpath("//div[@class='social-details-reactors-tab-body']")
                        
        
        
        #on spécifie le nombre de likes maximum dans cette condition
        while lastScrollTop != currentScrollTop and len(news_comptes)<rest: # lastScrollTop -1; currentScrollTop -2; indexOfFirstLiker 0
            
            # Obtenir tous les noms de likers
            update_likers =driver.find_elements_by_xpath("//span[@dir='ltr']")
            
            # Stocker les noms de likers
            update_likers_link =driver.find_elements_by_xpath("//a")
            
            for index in range(0, len(update_likers)):
                compte=update_likers[index]
                if(compte.text not in news_comptes):
                    if not contact_in_database(dataBaseTool, logger, platform, browser, id_task_user, current_username, update_likers[index].text, today): 
                        news_comptes.append([update_likers[index].text, update_likers_link[index].get_attribute("href")])
                        
            # mise à jour de las tScrollTop 
            lastScrollTop = driver.execute_script("return arguments[0].scrollTop;",likers_list)
            #print(lastScrollTop)                    
            # On scroll
            driver.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight", likers_list)
            
            time.sleep(3)

            currentScrollTop=driver.execute_script("return arguments[0].scrollTop;",likers_list)
            #print(currentScrollTop)  
    
    return news_comptes[:rest]


def Browser_Cold_Messaging_LinkedIn_Likers_and_commenters_of_Instagram_post(p_browser, p_taskuser_id, instagram_username, p_quantity_actions, label_log, lock):

    # initialiser le logger
    logger = initLogger()

    # initialiser le driver
    driver = initDriver(p_browser, logger)

    driver.implicitly_wait(5)

    if driver is None:  # Une erreur est survenue au niveau de l'initialisation du driver
        logger.error("Error: initialize driver failed !")
        return False

    driver.get('https://www.linkedin.com/')
        
    #agrandir la page
    driver.maximize_window()

    time.sleep(5)

    return cold_messaging_all(driver, lock, logger, p_browser, "LinkedIn", p_taskuser_id, instagram_username, p_quantity_actions)

#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------#
"""
*****************************************************************************************************************
Cold Messaging Général à appeler dans votre tâche
*****************************************************************************************************************
"""
def cold_messaging_all(driver, lock, logger, p_browser, platform, p_taskuser_id, current_username, p_quantity_limit):
    """"""

    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    info_task = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    number_of_messages_sent_today = 0
    dataBaseTool = DataBaseTool("db.db", lock)

    """
    *************************************************************************
    Étape 1: Vérification de réponse et mise à jour de la base de donnée
    *************************************************************************
    """
    logger.info(logTitleMessage("Step 1: Check answers of old contacts"))

    # Obtenir les personnes ayant déjà reçu au moins 1 message
    logger.info("getting users who have received at least 1 message ...")
    response = dataBaseTool.getLinesRequest(
        "SELECT contacts.* FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact"
        " WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action LIKE ? AND "
        "actions.type_action NOT LIKE ? AND actions.id_message IS NOT NULL AND actions.id_social_account=?"
        "GROUP BY contacts.id",
        (platform, p_taskuser_id, "%message%", "%received%", current_username))

    # Exception levée au cours de l'exécution SQL
    if not response["ok"]:
        logger.info("database access failed ! " + getExceptionFormat(response["data"]))
        return False

    messageContacts = response["data"]

    # Il y effectivement des "anciens" contacts
    if len(messageContacts) != 0:
        logger.info(logSectionMessage("check answer for every old contacts"))

        # Pour chaque "anciens" contacts
        for contact in messageContacts:
            logger.info(logSectionMessage("check answer for {}".format(contact["username"])))

            # Vérifier dans la plateforme si la personne a répondu
            logger.info("check answer in platform ...")
            last_message_id = get_last_message(dataBaseTool, contact, platform, p_taskuser_id, current_username, "id_message")
            check_answer_in_database =  dataBaseTool.getLinesRequest(
                "SELECT * FROM actions WHERE platform=? AND id_task_user=? AND "
                "type_action LIKE ? AND id_social_account=? AND id_message=?",
                (platform, p_taskuser_id, "%received%", contact["username"], last_message_id))
            if len(check_answer_in_database["data"]) >= 1:
                continue

            last_message = get_last_message(dataBaseTool, contact, platform, p_taskuser_id, current_username, "message")
            res = contact_has_replied(driver, contact, last_message)

            Sleeping_Bot(2, 3)

            if res[0]:  # la personne a répondu
                # modifier le champs "replied" à 1 dans la table "contacts"
                logger.info("{} has answered, modify \"replied\" to 1 ...".format(contact["username"]))
                if not dataBaseTool.modifyLine("contacts", ["replied", "date_update"], [1, today], {"id": contact["id"]})["ok"]:
                    logger.info("database modify replied failed ! " + getExceptionFormat(response["data"]))
                    return False

                # Enregistrer la réponse reçue
                logger.info("search the message with which the user has answered ...")
                lastMessageID = get_last_message(dataBaseTool, contact, platform, p_taskuser_id, current_username, "id_message")

                if lastMessageID is None or lastMessageID is False:
                    logger.info("database get last message failed ! ")
                    return False

                logger.info("add new line \"message received\" in actions ...")
                if not dataBaseTool.addLine("actions", ("platform", "type_action", "message", "id_smartphone", "id_social_account",
                                          "id_contact", "date_created", "id_message", "date_update", "id_task_user"),
                        (platform, "message_received", res[1],
                         p_browser, contact["username"], contact["id"], today, lastMessageID, today, p_taskuser_id))[
                    "ok"]:
                    logger.info("database add line \"message received\" failed ! ")
                    return False
            Sleeping_Bot(2, 3)

    logger.info(logTitleMessage("Step 1: Check answers of old contacts ... success !"))

    """
    *************************************************************************
    Étape 2: Envoyer le prochain message pour les anciens
    *************************************************************************
    """
    logger.info(logTitleMessage("Step 2 : send next messages for old contacts"))

    response = dataBaseTool.getLinesRequest(
        "SELECT contacts.* FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact"
        " WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action LIKE ? AND "
        "actions.type_action NOT LIKE ? AND actions.id_message IS NOT NULL AND actions.id_social_account=?"
        "GROUP BY contacts.id",
        (platform, p_taskuser_id, "%message%", "%received%", current_username))

    messageContacts = response["data"]

    # Il y effectivement des "anciens" contacts
    if len(messageContacts) != 0:
        # Pour chaque "anciens" contacts
        for contact in messageContacts:
            logger.info(logSectionMessage("send next message for {}".format(contact["username"])))

            # Contrôle de serie_type
            logger.info("check serie_type ...")
            if not pass_serie_type(contact, info_task["serie_type"]):
                logger.info("Mode \"until reply\" activated and the target user has answered: next")
                continue

            # Contrôle de next_message
            logger.info("check next_message ...")
            last_message = dataBaseTool.getLinesRequest(
                "SELECT * FROM actions WHERE platform=? AND type_action LIKE ? AND type_action not LIKE ?"
                " AND id_social_account=? AND id_contact=? AND id_task_user=? ORDER BY date_created DESC",
                (platform, "%message%", "%received%", current_username, contact["id"],
                    p_taskuser_id))["data"][0]

            if not pass_next_message(last_message["id_message"], info_task):
                logger.info("no more message to send: next")
                continue

            # Contrôle de delay_limit
            logger.info("check delay_limit ...")
            message_serie = last_message["id_message"].split("_")[2]
            time_delay = "time_delay_" + message_serie
            time_delay_type = "time_delay_" + message_serie + "_type"

            if not pass_delay_limit(datetime.datetime.strptime(last_message["date_created"], "%Y-%m-%d %H:%M:%S"),
                                    info_task[time_delay], info_task[time_delay_type]):
                logger.info("time limit not yed reached: next")
                continue

            # Envoi de message
            next_message_id = get_next_message_id(last_message["id_message"])
            next_message = mymodulesteam.TransformMessage(f'{info_task[next_message_id]}\r',
                                                          firstname=contact["username"],
                                                          username=contact["username"])

            # Envoi de message sur la plateforme
            logger.info("send message in platform ...")
            if not send_message(driver, contact, next_message):
                logger.info("send message to {} failed !".format(contact["username"]))
                return False

            Sleeping_Bot(2, 3)

            # Mise à jour de la base de données
            logger.info("add new line \"send message\" in actions ...")
            if not dataBaseTool.addLine("actions", ("platform", "type_action", "message", "id_smartphone", "id_social_account",
                "id_contact", "date_created", "id_message", "date_update", "id_task_user"),(platform, "send_message",
                            next_message, p_browser, current_username, contact["id"], today, next_message_id,
                            today, p_taskuser_id))["ok"]:
                logger.info("database add line \"send message\" failed ! ")
                return False

            logger.info("send next message for {} ... success !".format(contact["username"]))
            number_of_messages_sent_today += 1

            logger.info("{} message(s) sent today !".format(number_of_messages_sent_today))
            if number_of_messages_sent_today >= p_quantity_limit:
                return True

            Sleeping_Bot(2, 3)

    logger.info(logTitleMessage("Step 2 : send next messages for old contacts ... success !"))

    """
    *************************************************************************
    Étape 3: Envoyer le premier message aux nouveaux
    *************************************************************************
    """
    """
    Les nouveaux se divisent en 3 sous-catégories:
        * les "contact" déjà existant dans la base mais qui n'a jamais reçu notre message et pas besoin de "invitation"
        * les "contact" déjà existant dans la base et on attend une acceptation de sa part
        * les "contact" non existant dans la base et on doit y ajouter
    """

    logger.info(logTitleMessage("Step 3 : send 1st message for new contacts"))
    # On vérifie qui a accepté l'invitation
    logger.info(logSectionMessage("check who accepted the invitation"))
    logger.info("Getting the list of contacts we send an invitation ...")
    contacts_waiting_for_accept = dataBaseTool.getLinesRequest(
        "SELECT contacts.* FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND contacts.replied_invitation=? AND actions.id_social_account=? "
        "AND actions.type_action LIKE ?", (platform, p_taskuser_id, 0, current_username, "%invitation%"))

    if not contacts_waiting_for_accept["ok"]:
        logger.info("Getting list of waiting accept people failed !")
        return False

    # Si il y a des personnes à qui on a envoyé une invitation
    if len(contacts_waiting_for_accept["data"]) >= 1:
        logger.info(logSectionMessage("check if contacts have accepted the invitation"))
        # Pour chacun de ces derniers
        for contact_waiting_for_accept in contacts_waiting_for_accept:
            logger.info(logSectionMessage("check invitation for {} ...".format(contact_waiting_for_accept["username"])))
            # Vérifier s'il a accepté
            if contact_has_replied_invitation(driver, contact_waiting_for_accept):
                logger.info("{} has accepted ...".format(contact_waiting_for_accept["username"]))
                logger.info("Update \"replied_invitation\" ...")
                # Modification dans la base de données
                if not dataBaseTool.modifyLine("contacts", ["replied_invitation", "date_update"], [1, today],
                                  {"id": contact_waiting_for_accept["id"]})["ok"]:
                    logger.info("Update of contact accept invitation failed !")
                    return False
            else:
                logger.info("{} hasn't yet accepted ...".format(contact_waiting_for_accept["username"]))

            Sleeping_Bot(2, 3)

    # On ajoute les nouveaux qui n'existent pas encore dans la base de données
    # Obtenir les nouveaux contacts depuis la plateforme
    logger.info(logSectionMessage("Add new contacts in database"))
    logger.info("Getting new contacts in platform ...")
    new_contacts = search_new_contacts(driver, dataBaseTool, logger, platform, p_browser, p_taskuser_id, current_username,
                                       today, p_quantity_limit - number_of_messages_sent_today)

    for new_contact in new_contacts:  # new_contacts = [[username, url], [username, url], ....]
        logger.info(logSectionMessage("Add new contact {}".format(new_contact[0])))
        logger.info("check if send invitation needed ...")
        if need_invitation(driver, new_contact[1]):  # On a besoin de lui envoyer une invitation avant de parler
            logger.info("send invitation needed ...")
            logger.info("send invitation ...")
            serie_letter = ""
            if info_task["AB_testing_enable"] == 1:  # mode test_AB activé
                serie_letter = get_next_serie_AB(dataBaseTool, platform, p_taskuser_id, current_username)
            else:  # mode test_AB désactivé
                serie_letter = get_serie_no_AB(info_task)
            invitation_message = info_task["message_txt_invitation_1" + serie_letter]
            invitation_message_translate = mymodulesteam.TransformMessage(f'{invitation_message}\r', firstname=new_contact[0],
                                                      username=new_contact[0])
            if not send_invitation(driver, new_contact[1], invitation_message_translate):  # envoyer l'invitation
                logger.info("send invitation failed !")
                return False

            logger.info("add new line in contacts ...")
            newLineContact = dataBaseTool.addLineWithID("contacts",
                ("platform", "username", "url_profile", "id_task_user", "replied_invitation", "date_created", "date_update"),
                (platform, new_contact[0], new_contact[1], p_taskuser_id, 0, today, today))
            if newLineContact["ok"] == -1:
                logger.info("add new contact failed !")
                return False

            logger.info("add new line \"send_invitation\" in actions ...")
            if not dataBaseTool.addLine("actions", ("platform", "type_action", "message", "id_smartphone", "id_social_account",
                                             "id_contact", "date_created", "date_update", "id_task_user"),
                (platform, "send_invitation", invitation_message, p_browser, current_username, newLineContact["ok"], today, today,
                           p_taskuser_id))["ok"]:
                logger.info("add new action \"send invitation\" failed !")
                return False

        else:  # On n'a pas besoin d'invitation
            logger.info("no invitation needed ...")

            logger.info("add new line in contacts ...")
            newLineContact = dataBaseTool.addLineWithID("contacts", ("platform", "username", "url_profile", "id_task_user",
                "date_created", "date_update"), (platform, new_contact[0], new_contact[1], p_taskuser_id, today, today))
            if newLineContact["ok"] == -1:
                logger.info("add new contact failed !")
                return False

        logger.info("add new line \"scrap\" in actions ...")
        if not dataBaseTool.addLine("actions", ("platform", "type_action", "id_smartphone", "id_social_account",
            "id_contact", "date_created", "date_update", "id_task_user"),
            (platform, "scrap", p_browser, current_username, newLineContact["ok"], today, today,
                p_taskuser_id))["ok"]:
            logger.info("add new action \"scrap\" failed !")
            return False

        Sleeping_Bot(2, 3)

    # On envoie le premier message à tous les nouveaux (pas besoin invitation ou ceux qui ont accepté)
    # préparer le premier message: vérifier AB_enable_testing -> choix AB (comparer nb message_txt_1A et message_txt_1B)
    logger.info("Getting 1st message ...")

    # récuperer les personnes à qui on envoie de message (replied_invitation --> NULL ou 1)
    # idée général => Personnes ayant jamais reçu de message = L'ensemble des personnes - Personne ayant reçu au moins 1 messages
    logger.info("Getting people who never received a message from us ...")
    contacts_to_send = dataBaseTool.getLinesRequest(
        "SELECT contacts.* FROM contacts LEFT JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action=? AND actions.id_social_account=? AND "
        "(contacts.replied_invitation=? OR contacts.replied_invitation IS NULL) GROUP BY contacts.id "
        "EXCEPT SELECT contacts.* FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action LIKE ? AND "
        "actions.type_action NOT LIKE ? AND actions.id_message IS NOT NULL AND actions.id_social_account=? "
        "GROUP BY contacts.id", (platform, p_taskuser_id, "scrap", current_username, 1, platform, p_taskuser_id,
                                        "%message%", "%received%", current_username))

    # Envoyer le message à chaque personne
    logger.info(logSectionMessage("send 1st message for new contacts"))
    for contact in contacts_to_send["data"]:
        logger.info(logSectionMessage("send 1st message for {} ...".format(contact["username"])))

        serie_letter = ""
        if info_task["AB_testing_enable"] == 1:  # mode test_AB activé
            serie_letter = get_next_serie_AB(dataBaseTool, platform, p_taskuser_id, current_username)
        else:  # mode test_AB désactivé
            serie_letter = get_serie_no_AB(info_task)

        next_message_id = "message_txt_1" + serie_letter
        next_message = mymodulesteam.TransformMessage(f'{info_task[next_message_id]}\r', firstname=contact["username"],
                                                      username=contact["username"])
        # envoi de message
        if not send_message(driver, contact, next_message):
            logger.info("send message to {} failed !".format(contact["username"]))
            return False

        # Mise à jour de la base de données
        logger.info("add new line \"send message\" in actions ...")
        if not dataBaseTool.addLine("actions", ("platform", "type_action", "message", "id_smartphone", "id_social_account",
            "id_contact", "date_created", "id_message", "date_update", "id_task_user"),
                       (platform, "send_message", next_message, p_browser, current_username, contact["id"], today,
                        next_message_id, today, p_taskuser_id))["ok"]:
            logger.info("database add line \"send message\" failed ! ")
            return False

        logger.info("send next message for {} ... success !".format(contact["username"]))

        number_of_messages_sent_today += 1

        logger.info("{} message(s) sent today !".format(number_of_messages_sent_today))
        if number_of_messages_sent_today >= p_quantity_limit:
            return True

        Sleeping_Bot(2, 3)

    logger.info(logTitleMessage("Step 3 : send 1st message for new contacts ... success !"))

    return True

#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------#
"""
*****************************************************************************************************************
Fonctions utilitaires
*****************************************************************************************************************
"""
def pass_serie_type(contact, serie_type):
    """
    La fonction pass_serie_type permet de savoir si oui ou non on va envoyer le prochain message selon le critère de "serie_type"
    :param contact: contient toutes les infos de l'utilisateur à examiner
    :param serie_type: le type de série
    :return: True / False indiquant si oui ou non on lui envoie de prochain message
    """
    if serie_type == "until_reply":
        if contact["replied"] == 1:
            return False

    return True

def get_number_of_days_after_months(last_time, delay_months):
    """
    La fonction get_number_of_days_after_months permet d'obtenir le nombre de jours à partir d'une date et un délai de mois
    :param last_time: la dernière date en format "aaaa-mm-dd hh:mm:ss"
    :param delay_months: le délai en mois
    :return: le nombre de jours
    """
    days_of_months = {1: 31,
                      2: 28,
                      3: 31,
                      4: 30,
                      5: 31,
                      6: 30,
                      7: 31,
                      8: 31,
                      9: 30,
                      10: 31,
                      11: 30,
                      12: 31}

    last_time = str(last_time)
    last_month = int(last_time.split("-")[1])

    comp_months = 0
    total_days = 0

    while comp_months < delay_months:
        total_days += days_of_months[last_month]
        last_month += 1
        comp_months += 1

    return total_days

def pass_delay_limit(date_last_message, delay_number, delay_type):
    """
    La fonction pass_delay_limit permet de savoir si oui ou non on va envoyer le prochain message selon le critère de "delay_limit"
    :param date_last_message: la date du dernier message en format "aaaa-mm-dd hh:mm:ss"
    :param delay_number: le nombre de "temps" qu'on doit attendre
    :param delay_type:  le type de "temps" qu'on doit attendre
    :return: True / False indiquant si oui ou non on va lui envoyer le prochain message
    """
    # le délai réel (en sec)
    today = datetime.datetime.now()

    delta_time = today - date_last_message
    delta_seconds = delta_time.total_seconds()

    # le délai qu'on a voulu (en sec)
    seconds_of_time = {"hours": 60 * 60,
                       "days": 24 * 60 * 60,
                       "weeks": 7 * 24 * 60 * 60}

    delta_seconds_wanted = -1
    if delay_type == "hours" or delay_type == "days" or delay_type == "weeks":
        delta_seconds_wanted = delay_number * seconds_of_time[delay_type]

    elif delay_type == "months":
        delta_days_wanted = get_number_of_days_after_months(date_last_message, delay_number)
        delta_seconds_wanted = delta_days_wanted * seconds_of_time["days"]

    # examiner le délai
    return delta_seconds >= delta_seconds_wanted

def pass_next_message(current_message_id, info_task):
    """
    La fonction pass_next_message permet de savoir si oui ou non on va envoyer le prochain message selon le critère de "next_message"
    :param current_message_id: l'id du message courant (Ex: message_txt_2A)
    :param info_task: le dictionnaire contenant toutes les infos de la tâche cold_messaging
    :return: True / False indiquant si oui ou non on va lui envoyer le prochain message
    """

    next_message_id = get_next_message_id(current_message_id)

    if next_message_id is None:
        return False

    next_message = info_task[next_message_id]

    if next_message is None or next_message == "":
        return False

    return True

def get_last_message(dataBaseTool, contact, platform, id_task_user, current_username, field_needed):
    res = dataBaseTool.getLinesRequest(
                          "SELECT * FROM actions WHERE platform=? AND type_action LIKE ? AND type_action not LIKE ?"
                          " AND id_social_account=? AND id_contact=? AND id_task_user=? ORDER BY date_created DESC",
                          (platform, "%message%", "%received%", current_username, contact["id"], id_task_user))

    if not res["ok"]:
        return None

    if len(res["data"]) == 0:
        return False

    return res["data"][0][field_needed]

def get_next_message_id(current_message_id):
    # Format message_txt_1A

    current_message_id_splited = current_message_id.split("_")
    current_serie = current_message_id_splited[2]
    next_number = int(current_serie[0]) + 1
    next_number_str = str(next_number)

    if next_number >= 5:
        return None

    return current_message_id_splited[0] + "_" + current_message_id_splited[1] + "_" + next_number_str + current_serie[
        1]

def get_number_of_message_serie_sent(dataBaseTool, platform, id_task_user, current_username, message_id):
    res = dataBaseTool.getLinesRequestNoDict(
                                "SELECT COUNT(*) FROM actions WHERE platform=? AND type_action LIKE ? AND type_action NOT LIKE ?"
                                " AND id_task_user=? AND id_social_account=? AND id_message=?",
                                (platform, "%message%", "%received%", id_task_user,
                                 current_username, message_id))

    # res sous format {"data":[(number,)]}

    return res["data"][0][0]

def get_next_serie_AB(dataBaseTool, platform, id_task_user, current_username):
    nb_serie_A = get_number_of_message_serie_sent(dataBaseTool, platform, id_task_user, current_username, "message_txt_1A")
    nb_serie_B = get_number_of_message_serie_sent(dataBaseTool, platform, id_task_user, current_username, "message_txt_1B")

    return "A" if nb_serie_A <= nb_serie_B else "B"

def get_serie_no_AB(info_task):
    return "A" if not (info_task["message_txt_1A"] is None or info_task["message_txt_1A"] == "") else "B"


"""
    La méthode logTitleMessage crée un format pour les titres pour le différentes étapes
    Ex: **************
        *    Test    *
        **************
"""
def logTitleMessage(message):
    lengthOfFirstAndLastLine = len(message) * 3
    return "*" * lengthOfFirstAndLastLine + "\n" \
                                            "*" + (" " * (len(message) - 1)) + message + (
                       " " * (len(message) - 1)) + "*" \
           + "\n" + "*" * lengthOfFirstAndLastLine


"""
    La méthode logSectionMessage cree un format pour les sections dans les étapes
    Ex:  =============== Section ===============
"""
def logSectionMessage(message):
    return "=" * 15 + " " + message + " " + "=" * 15


"""
    La fonction initLogger permet d'initialiser le logger
"""
def initLogger():
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
    return logger
    # ================================================================================


"""
    La fonction initDriver initialise le driver
"""
def initDriver(p_browser, logger):
    driver = None

    if p_browser == "Chrome":  # Le navigateur utilisé est Chrome
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":  # Le navigateur utilisé est Firefox
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

    return driver

#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------#
"""
****************************************************************************************************************
Fonctions pour manipuler xpath
****************************************************************************************************************
"""
"""
Random time.sleep for being a stealth bot.
"""
def Sleeping_Bot(borne_inf=float, borne_sup=float):
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)

"""
    La méthode automaticSendKeys remplit les champs de saisi avec un comportement humain
"""
def automaticSendKeys(element, text):
    for letter in text:
        if letter == '\n':
            element.send_keys(Keys.SHIFT, Keys.ENTER)
        else:
            element.send_keys(letter)
        Sleeping_Bot(0.005, 0.01)

"""
    La méthode getByType fait la conversion de str vers ByType (Ex: "xpath" -> By.XPATH)
"""
def getByType(locatorType):
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
def findElement(driver, locatorType, locator):

    byType = getByType(locatorType)

    if byType is None:
        return None

    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((byType, locator)))

"""
    La méthode findElements cherche tous les éléments dans la page selon un locatorType et un locator
"""
def findElements(driver, locatorType, locator):
    byType = getByType(locatorType)

    if byType is None:
        return None

    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((byType, locator)))

"""
    La méthode clickOnElement clique sur l'élément passé en paramètre
"""
def clickOnElement(driver, element):
    driver.execute_script("arguments[0].click();", element)

"""
    La méthode scrollToElement scroll la page à l'emplacement de l'élément
"""
def scrollToElement(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

"""
    La méthode scroll monte ou descend la page
"""
def scroll(driver, x, y):
    driver.execute_script("window.scrollBy(arguments[0], arguments[1]);", x, y)
#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------#
"""
****************************************************************************************************************
Fonctions pour manipuler la base de données
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

#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------#
"""
****************************************************************************************************************
Méthodes pour gérer l'importation de Google Sheet
****************************************************************************************************************
"""
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
    idGoogleSheet = urlToID(googleSheetURL) # Obtenir id de Google Sheet
    return mymodulesteam.GoogleSheetGetValues(idGoogleSheet) # Obtenir toutes les lignes du doc

def getColumnsFromGooglesheetsByTaskUserID(p_taskuser_id):
    """
    La méthode getColumnsFromGoogleSheetByURL permet d'obtenir les valeurs dans les différentes colonnes de Google Sheet

    :param p_taskuser_id: id_task
    :type p_taskuser_id: str
    :return: Une liste contenant toutes les lignes du Google Sheet
    :rtype: list
    """
    taskUserDetails = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)  # Obtenir toutes les infos de taskUser
    googleSheetURL = str(taskUserDetails["url_list"]) # Obtenir le lien Google Sheet
    return getColumnsFromGoogleSheetByURL(googleSheetURL) # Obtenir toutes les lignes du doc
#---------------------------------------------------------------------------------------------------------------------#
 
#---------------------------------------------------------------------------------------------------------------------#
"""
****************************************************************************************************************
Exécution du Script
****************************************************************************************************************
"""

'''
p_browser_run = "Chrome"
p_taskuser_id_run = 255
facebook_username_run = "NWB"
p_quantity_actions_run = 2
label_log_run = """"""""
lock_run = threading.Lock()

Browser_Cold_Messaging_LinkedIn_Likers_and_commenters_of_Instagram_post(p_browser_run, p_taskuser_id_run, facebook_username_run, p_quantity_actions_run, label_log_run, lock_run)

"""
dataBaseTool = DataBaseTool("db.db", lock_run)
contacts_to_send = dataBaseTool.getLinesRequest(
        "SELECT contacts.* FROM contacts LEFT JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action=? AND actions.id_social_account=? AND "
        "(contacts.replied_invitation=? OR contacts.replied_invitation IS NULL) GROUP BY contacts.id "
        "EXCEPT SELECT contacts.* FROM contacts INNER JOIN actions ON contacts.id = actions.id_contact "
        "WHERE contacts.platform=? AND contacts.id_task_user=? AND actions.type_action LIKE ? AND "
        "actions.type_action NOT LIKE ? AND actions.id_message IS NOT NULL AND actions.id_social_account=? "
        "GROUP BY contacts.id", ("LinkedIn", 255, "scrap", "NWB", 1, "LinkedIn", 255,
                                        "%message%", "%received%", "NWB"))
print(contacts_to_send)
"""
'''