# Laurent Maréchal
# fini ?, Youtube demande un Captcha avec reconnaissance d'image pour les mails donc canceled

"""
This module contain some modules from mymodules.py improved by other developpers
https://github.com/phonebotco/phonebot
"""
import logging
import os
import shutil
import time
import random
import sqlite3
from datetime import datetime
import logging
import threading
import time
import sqlite3
from datetime import datetime
import mymodulesteam as MMTeam
from mymodulesteam import *

from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver import ActionChains, DesiredCapabilities
import pathlib
import platform
import psutil

def searchAndGetChannels(driver, channelsLinks, word_searched, numberOfChannels):
    numberOfChannelsScrapped = 0
    scrollInt = 6000
    channelsLinksName = []
    try:
        #TROUVER LA BARRE DE RECHERCHE
        searchBar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//input[contains(@id,'search')]"))))
    except Exception as ex:
        logger.error(f"{ex} - Can't find search bar in searchAndGetChannels function")
    time.sleep(random.uniform(1, 2))
    # j'utilise send_keys avec l'import "from selenium.webdriver.common.keys import Keys" pour éviter une erreur 'FirefoxWebElement' object has no attribute 'sendKeys'.
    try:
        searchBar.send_keys(word_searched)
        time.sleep(random.uniform(1, 2))
        searchBar.send_keys(Keys.ENTER)
        # attendre que toutes les chaines chargent
        time.sleep(random.uniform(1, 2))
    except Exception as ex:
        logger.error(f"{ex} - Can't send searched word or press enter key in searchAndGetChannels function")
    while True:
        # trouver le nom des chaines
        try:
            channels = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//div[contains(@id,'channel-info')]//a[contains(@class,'style-scope yt-formatted-string')]"))))    
        except Exception as ex:
            logger.error(f"{ex} - Can't find any channels in searchAndGetChannels function")
        # parcours les chaines
        for channel in channels:
            # print(f"channelLinksName = {channelsLinksName}")
            # print(channel.get_attribute("innerText"))
            # rajoute le lien des chaines si il n'est pas déjà dans la list
            if channel.get_attribute("innerText") not in channelsLinksName :
                channelsLinks.append(channel)
                channelsLinksName.append(channel.get_attribute("innerText"))
                numberOfChannelsScrapped += 1
                if numberOfChannelsScrapped == int(numberOfChannels) :
                    return channelsLinks
        driver.execute_script(f'window.scrollTo(0, {scrollInt});')
        scrollInt += 6000
        time.sleep(random.uniform(2, 3))

def goToABoutTab(driver):
    time.sleep(random.uniform(1, 2))
    # Enlève le popup des inscriptions
    driver.implicitly_wait(2)
    try:
        okButton = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, ("//div[contains(@id, 'accept-button')]"))))
        okButton.click()
    except:
        pass
    driver.implicitly_wait(10)
    try:
        getInfo = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//div[@id='tabsContent']//div"))))
    except Exception as ex:
        logger.error(f"{ex} - Can't find About tab in goToAboutTab function")
    for tab in getInfo:
        # Trouve quel élement de la liste contient "À PROPOS"
        if tab.get_attribute("innerText") == "À PROPOS" or tab.get_attribute("innerText") == "ABOUT":
            tabAbout = tab
    try:
        tabAbout.click()
    except Exception as ex:
        logger.error(f"{ex} - Can't click on About tab in goToAboutTab function")

def getUsername(driver, infos):
    try:
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//div[contains(@id, 'inner-header-container')]//yt-formatted-string[contains(@id, 'text')]"))))
        infos["username"] = (username.get_attribute("innerText"))
    except Exception as ex:
        logger.error(f"{ex} - Can't find username total views in getUsername function, skipping")
        infos["username"] = "Rien"
        return infos
        pass

# Canceled
def getMail(driver, infolist):
    # clique sur "afficher l'email"
    try:
        displayMail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//yt-formatted-string[contains(text(), 'Afficher l')]/ancestor::a"))))
        displayMail.click()
        # complete le captcha
        time.sleep(random.uniform(1, 2))
        divCaptcha = driver.find_element_by_xpath("//div[contains(@id,'recaptcha')]")
        divCaptcha.click()
        # clique sur envoyer
        time.sleep(random.uniform(1, 2))
        divSendButton = driver.find_element_by_xpath("//button[contains(@id,'submit-btn')]")
        time.sleep(random.uniform(1, 2))
        # Le bouton peut lag et ne pas afficher l'email
        divSendButton.click()
        # rejoutes les adresses email dans infolist
        infolist.append(driver.find_element_by_xpath("//a[contains(@id,'email')]").get_attribute("text"))
        return infolist
    except Exception as ex:
        logger.error(f"{ex} - Can't find email button in getMail function, skipping")
        infolist.append("Rien")
        return infolist
        pass

def getDescription(driver, infos):
    try:
        description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//div[contains(@id, 'description-container')]//yt-formatted-string[contains(@id, 'description')]"))))
        infos["influencer_bio"] = (description.get_attribute("innerText"))
    except Exception as ex:
        logger.error(f"{ex} - Can't find description in getDescription function, skipping")
        infos["influencer_bio"] = "Rien"
        return infos
        pass

def getLinks(driver, infos):
    time.sleep(random.uniform(1, 2))
    try:
        linksContainer = {}
        divLinks = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//div[contains(@id, 'link-list-container')]//a[contains(concat(' ', normalize-space(@class), ' '), ' yt-simple-endpoint ')and contains(concat(' ', normalize-space(@class), ' '), ' style-scope ')]"))))
        for link in divLinks:
            if link.get_attribute("href").startswith("https://www.youtube.com/redirect?event"):
                clearLink = link.get_attribute("href").split("&", 2)[2][2:].replace("%3A", ":").replace("%2F", "/")
                linksContainer[link.get_attribute("innerText")] = clearLink
                if "twitter" in clearLink:
                    infos["url_twitter"] += f"{clearLink} "
                if "facebook" in clearLink:
                    infos["url_facebook"] += f"{clearLink} "
                if "instagram" in clearLink:
                    infos["url_instagram"] += f"{clearLink} "
            else :
                linksContainer[link.get_attribute("innerText")] = link.get_attribute("href")
        for k, v in linksContainer.items():
            infos["influencer_links"] += f"{k} : {v} / "
        return infos
    except Exception as ex:
        logger.error(f"{ex} - Can't find any links in getLinks function, skipping")
        infos["influencer_links"] = "Rien"
        return infos
        pass

def getViews(driver, infos):
    try:
        description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//div[contains(@id, 'right-column')]//yt-formatted-string[contains(text(), 'vues') or contains(text(), 'views')]"))))
        infos["invluencer_total_views"] = (description.get_attribute("innerText"))
    except Exception as ex:
        logger.error(f"{ex} - Can't find invluencer total views in getViews function, skipping")
        infos["invluencer_total_views"] = "Rien"
        return infos
        pass

def getCountry(driver, infos):
    try:
        country = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ("//div[contains(@id, 'details-container')]//span[contains(text(), 'Pays')]/ancestor::td/following-sibling::td[1]//yt-formatted-string"))))
        infos["country"] = (country.get_attribute("innerText"))
    except Exception as ex:
        logger.error(f"{ex} - Can't find country in getCountry function, skipping")
        infos["country"] = "Rien"
        return infos
        pass        

def getInfos(driver, infos):
    getUsername(driver, infos)
    getDescription(driver, infos)
    getLinks(driver, infos)
    getViews(driver, infos)
    getCountry(driver, infos)

def checkIfColumnExist(sqlite_cursor, columnList):
    for column in columnList:
        try:
                sqlite_cursor.execute(f'ALTER TABLE contacts ADD COLUMN {column};')
                print(f"Table {column} created")
        except:
                print(f"Table {column} was already created")
                pass # handle the error

def DemoSQLITE3(columnList, infos):
    from datetime import datetime
    sqlite_connection = sqlite3.connect(MMTeam.LoadFile("db.db"))
    sqlite_cursor = sqlite_connection.cursor()
    id_task = 262
    print("checking columns")
    checkIfColumnExist(sqlite_cursor,columnList)
    try:
            sqlite_cursor.execute(f"INSERT INTO contacts(platform,type,{columnList[0]},{columnList[1]},{columnList[2]},{columnList[3]},{columnList[4]},{columnList[5]},{columnList[6]},{columnList[7]},{columnList[8]},id_task_user, date_created) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                    "Youtube",
                    "Influencers_informations",
                    f"{str(infos[columnList[0]])}",
                    f"{str(infos[columnList[1]])}",
                    f"{str(infos[columnList[2]])}",
                    f"{str(infos[columnList[3]])}",
                    f"{str(infos[columnList[4]])}",
                    f"{str(infos[columnList[5]])}",
                    f"{str(infos[columnList[6]])}",
                    f"{str(infos[columnList[7]])}",
                    f"{str(infos[columnList[8]])}",
                    id_task,
                    str(datetime.now()),
            ),
            )
            sqlite_connection.commit()

            sqlite_cursor.execute(
                "INSERT INTO actions(platform,type_action, id_social_account, source, date_created, id_task_user) VALUES (?,?,?,?,?,?)",
                ('Youtube', 'Scraping', f"{str(infos[columnList[0]])}", f"{str(infos[columnList[2]])}", str(datetime.now()), id_task))
            sqlite_connection.commit()

            sqlite_connection.close()
    except Exception as ex:
            print(f"Error when inserting in database: {ex}")

def Browser_Scrap_Youtube_Influencers(p_browser, p_taskuser_id, youtube_username, p_quantity_actions, label_log, lock):
    logger.info("=== [1] Open Browser =======================================")

    # OUVERTURE DU NAVIGATEUR
    if p_browser == "Chrome":
        driver = ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

    # CHARGEMENT DE LA PAGE
    driver.get('https://www.youtube.com/')
    driver.implicitly_wait(10)
    
    # init la list qui contiendra les chaines
    channelsLinks = []
    columnList = ("username", "country", "influencer_channel_link", "url_facebook", "url_twitter", "url_instagram", "influencer_bio", "influencer_links", "invluencer_total_views")
    # columnList = ("influencer_channel_link", "influencer_bio", "influencer_links", "invluencer_total_views", "influencer_country")
    searchAndGetChannels(driver, channelsLinks, word_searched, numberOfChannels)
    for chan in channelsLinks:
        infos = {}
        for info in columnList:
            infos[info] = ""
        chan.click()
        infos["influencer_channel_link"] = driver.current_url
        time.sleep(random.uniform(1, 2))
        goToABoutTab(driver)
        time.sleep(random.uniform(1, 2))
        # On abandonne les emails sur desktop
        # getMail(driver, infos)
        getInfos(driver, infos)
        time.sleep(1)
        DemoSQLITE3(columnList, infos)
        time.sleep(1)
        driver.back()
        driver.back()

"""
p_browser="Firefox"
p_taskuser_id="262"

getGssUrl = GetDetailsTaskUser(int(p_taskuser_id))
urlid = extract_ss_id(getGssUrl["url_keywords"])
valuesGG = GoogleSheetGetValues(urlid)
newvaluesGG = [item[0] for item in valuesGG]
print(newvaluesGG)

for word in newvaluesGG:
    numberOfChannels = input("Enter the number of channels you wish to scrap : ")
    Youtube_Influencers(p_browser, word, numberOfChannels)
"""
