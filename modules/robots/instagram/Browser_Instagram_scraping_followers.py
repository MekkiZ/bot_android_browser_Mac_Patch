# -*- coding: utf-8 -*-

"""
Author : Ilker Soyturk
Email : ilkerstrk33@gmail.com
"""

import threading
from modules import mymodulesteam
import numpy as np
import logging
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import datetime
# import phonenumbers
import re
import sys
# import js_regex

"""
To make the script work, in the same folder you should have :
    - credentials_Google_Sheet_API_Account.json
    - db.db
    - mymodulesteam.py
"""

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__SCRAPING_INSTAGRAM_FOLLOWERS__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================

login = ""
password = ""

def Sleeping_Bot(borne_inf=float, borne_sup=float):
    """
        Random time.sleep for being a stealth bot.
    """
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)

def getLinksFromGooglesheets(p_taskuser_id):
    """
        get links from the googlesheet from the id
    """
    taskUserFromDB = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    allAccountsURL_Id = str(taskUserFromDB["url_list"]).split("/")[5]
    return mymodulesteam.GoogleSheetGetValues(allAccountsURL_Id)

def getKeyWordsFromGooglesheets(p_taskuser_id):
    """
        get keywords from the googlesheet from the id
    """
    taskUserFromDB = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    allAccountsURL_Id = str(taskUserFromDB["url_keywords"]).split("/")[5]
    return mymodulesteam.GoogleSheetGetValues(allAccountsURL_Id)

def getMinimumFollowers(p_taskuser_id):
    """
        get the minimum number of followers per account corresponding to the task
    """
    return mymodulesteam.GetDetailsTaskUser(p_taskuser_id)["minimum"]

def insertScrapedValuesToContacts(username, urlProfile, instaFullName, instaCategory, bio,
                                  source, idTaskUser=271, platform='instagram', email="", phone="", website=""):
    """
        insert scraped values to contacts
    """
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()

    # INSERT DATA TO CONTACT
    with lock:
        sqlite_cursor.execute(
        "INSERT INTO contacts(platform,id_task_user,username,email,phone,website,url_profile,insta_header_full_name,insta_header_biz_category,insta_bio,source,date_created,date_update)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            platform, idTaskUser, username, email, phone, website, urlProfile, instaFullName, instaCategory, bio,
            source, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        sqlite_connection.commit()
    logger.info(
        "Insert contact contacts with username {} success !".format(username))

def insertScrapedValuesToActions(idSmartphone, idSocialAccount, idContact, platform="instagram", typeAction="scrap"):
    """
        insert scraped values to actions
    """
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()

    # INSERT DATA TO ACTIONS
    with lock:
        sqlite_cursor.execute(
        "INSERT INTO actions(platform,type_action,date,id_smartphone,id_social_account,id_contact,id_task_user,date_created,date_update) "
        "VALUES(?,?,?,?,?,?,?,?,?)", (
            platform, typeAction, str(datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")), idSmartphone,
            idSocialAccount,
            idContact, 271,
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        sqlite_connection.commit()
    logger.info(
        "Insert action in actions with id contact {} with action :\'scrape\' success !".format(idContact))

def followerIsntScrapedYet(userId):
    """
        check if the userId (username instagram) is not present in the database
    """
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        sqlite_cursor.execute(
        "select count(*) from contacts where username=?", (userId,))
        rows = sqlite_cursor.fetchall()
    if int(str(rows).split(',')[0].split('(')[1].strip()) >= 1:
        logger.info("Follower is present in the database")
        return False
    else:
        logger.info("Follower is not present in the database")
        return True

def scrollDown(listEnd, driver, myFollowersListContainer, lastPosition):
    """
        scroll down the list of followers and return a dictionnary with the new last position and if we are at the end
        of the list
    """
    if not listEnd:
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight', myFollowersListContainer)
        Sleeping_Bot(0.5, 5.0)
        newPosition = driver.execute_script(
            'return arguments[0].scrollHeight', myFollowersListContainer)
        if newPosition == lastPosition:
            listEnd = True
        lastPosition = newPosition
    return {"end": listEnd, "lastPos": lastPosition}

def discoverAllUrls(allLinks):
    """
        get all links from the googlesheet to a dictionnary
    """
    dicLinks = {}
    values = []
    for link in allLinks:
        values.append(link)
    dicLinks["urls"] = values
    return dicLinks

def discoverAllKeyWords(driver, allKeywords):
    """
        get all keywords from the googlesheet to make the search and get all result accounts urls to
        a dictionnary with the keyword as key
    """
    allAccountsUrls = {}
    # search keywords
    searchArea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("input.XTCLo.x3qfX"))))
    for keyword in allKeywords:
        searchArea.send_keys(keyword)
        Sleeping_Bot(2.0, 8.0)
        # get all results from the search
        allResults = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, (".-qQT3"))))
        values = []
        # GO TO PROFILE IN POPUP
        for result in allResults:
            if result is not None and 'explore' not in result.get_attribute("href"):
                values.append(result.get_attribute("href"))
        allAccountsUrls[str(keyword).split("'")[1]] = values
        searchArea.clear()
    return allAccountsUrls

def isAccountPrivate(driver):
    """
       check if account that we gonna get followers is private
       because we can't discover followers of a private account in instagram
    """
    try:
        # if the title "private account" is here
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("article.ySN3v>div._4Kbb_._54f4m>div.QlxVY>h2"))))
        isPrivate = True
    except:
        isPrivate = False
    return isPrivate

def getIfAccountHasMinFollowers(driver, taskId):
    """
       check if account follower number is at least equals to the minimum limit
    """
    # getting the label of followers
    nbFollowersLabel = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("a[href*='/followers/'].-nal3>span.g47SY"))))
    # get the exact number of followers through the "title" attribute
    nbFollowers = int(nbFollowersLabel.get_attribute(
        "title").replace(" ", "").strip())
    # if the nb follower of the current account is at least equals to minimum
    if nbFollowers >= getMinimumFollowers(taskId):
        return True
    else:
        return False

def clickOnFollowersLink(driver):
    """
        click on the followers label link
    """
    # click to the follower label to get the full list
    myFollowersLink = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("a[href*='/followers/'].-nal3"))))
    driver.execute_script("arguments[0].click();", myFollowersLink)

def selectContactIdByUsername(contactUsername):
    """
        select contact id by instagram username (unique username)
    """
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    with lock:
        sqlite_cursor.execute(
        "select id from contacts where username=?", (contactUsername,))
        rows = sqlite_cursor.fetchall()
    return int((str(rows).split('(')[1].split(',')[0]).strip())

def getCategoryOfAccount(driver):
    """
        get category section of an account if it's exist
    """
    try:
        category = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("span._8FvLi")))).get_attribute(
            'innerHTML')
        logger.info("We found a Category section here !")
    except:
        category = None
        logger.info("Category section is not present on this profile !")
    return category

def getFullName(driver):
    """
        get full name section of an account if it's exist
    """
    try:
        fullName = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("h1.rhpdm")))).get_attribute(
            'innerHTML')
        logger.info("We found a Full Name section here !")
    except:
        fullName = None
        logger.info("Full Name section is not present on this profile !")
    return fullName

def getWebsite(driver):
    """
        get website section of an account if it's exist
    """
    try:
        website = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("a.yLUwa")))).get_attribute(
            'innerHTML')
        logger.info("We found a website section here !")
    except:
        website = None
        logger.info("Website section is not present on this profile !")
    return website

def getPhoneNumbers(bio):
    """
        search phone numbers from the bio if there is some
        france,usa,united kingdom,russia,germany,turkey,mexico
    """
    try:
        regexPattern = '((?:(?:\+|00)33|0)\s*[1-9](?:[\s|.-]*\d{2}){4})|' \
            '([(]?\d{3}[)]?[(\s)?.-]\d{3}[\s.-]\d{4})|' \
            '((((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?)|' \
            '((\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2})|' \
            '((\(?([\d \-\)\–\+\/\(]+)\)?([ .\-–\/]?)([\d]+)))|' \
            '((([+]|00)39)?((3[1-6][0-9]))(\d{7}))|' \
            '([+]*[0-9]*[ ]{0,1}[(]{0,1}[ ]{0,1}[0-9]{1,3}[ ]{0,1}[)]{0,1}[ ]{0,1}[0-9]{1,3}[ ]{0,1}[0-9]{2}[ ]{0,1}[0-9]{2}[ ]{0,1}[-\.\/]{0,1}[ ]{0,1}[0-9]{1,5})|' \
            '((\(\d{3}\)[.-]?|\d{3}[.-]?)?\d{3}[.-]?\d{4})'
        phonesArray = re.findall(regexPattern, bio)
        phones = ''
        if len(phonesArray) > 0:
            if len(phonesArray[0]) > 0:
                for p in set(phonesArray[0]):
                    if len(p.strip()) > 8:
                        phones = phones + ';' + p.strip()
    except:
        phones = ""
    if (phones != ""):
        logger.info("We found phone number(s) in the bio section here !")
    else:
        logger.info("There is not phone numbers in the Bio section !")
    return phones

def getMails(bio):
    """
        search mails from the bio if there is some
    """
    try:
        mails = ""
        mail = re.findall(r'[\w\.-]+@[\w\.-]+', bio)
        if len(mail) > 0:
            for m in set(mail):
                mails = mails + ';' + m.strip()
    except:
        mails = ""
    if (mails != ""):
        logger.info("We found mail(s) in the bio section here !")
    else:
        logger.info("There is not mails in the bio section !")
    return mails

def getBio(driver):
    """
       get bio section if it exist
    """
    try:
        bio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ("div.-vDIg>span")))).get_attribute(
            'innerHTML').replace("<br>", "\n")
        logger.info("We found a bio section here !")
    except:
        bio = None
        logger.info("There is not Bio section on this profile !")
    return bio


def Scraping_Instagram_Followers_271(p_browser, p_taskuser_id, Instagram_username, p_quantity_actions, label_log, lock):
    """
    :param p_browser: "firefox" or "chrome"
    :param p_taskuser_id: The Id N° in database of the user task (ex: 254 )
    :param Instagram_username: The username of the current user which will send the message (The Sender)
    :param p_quantity_actions: The quantity maximum of actions. Ex: 5 messages to 5 members
    :param label_log: THis is the label of our GUI (PyQt5). It will display the message you want to the user interface. THis is very useful for displaying important error.
    :param lock: This function will be executed inside a thread. The program PhoneBot use multithread to run different tasks at same times on different devices (browser desktop, smartphones).
    If several tasks save at same time some data in SQLITE3 database, there will be some error for multiple access at same time. We need to "Lock" the access.
    You simply create it with this line of code : lock = threading.Lock()
    :return: True if everything was fine or False if error
    """

    logger.info("=== [1] Open Browser =======================================")
    """
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    START CONNECTION SECTION
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    """
    # OUVERTURE DU NAVIGATEUR
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

    # aller sur la page web chaques lien et sur chaque liens recupérer les follpwers avec du scrapping

    # CHARGEMENT DE LA PAGE
    driver.get('https://www.instagram.com/')
    driver.implicitly_wait(10)
    # cliquer sur le pop up des cookies
    cookiesAcceptButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("button.aOOlW.bIiDR"))))
    driver.execute_script("arguments[0].click();", cookiesAcceptButton)
    Sleeping_Bot(2.0, 12.0)
    driver.implicitly_wait(10)

    # Connection
    usernameTextInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("input[type='text']"))))
    for letter in login:
        usernameTextInput.send_keys(letter)
        Sleeping_Bot(0.1, 1.5)

    passwordTextInput = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("input[type='password']"))))
    for letter in password:
        passwordTextInput.send_keys(letter)
        Sleeping_Bot(0.1, 1.5)

    connectionButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ("button[type='submit']"))))
    Sleeping_Bot(2.0, 12.0)
    driver.execute_script("arguments[0].click();", connectionButton)
    """
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    END CONNECTION SECTION
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    """
    allLinks = np.array(getLinksFromGooglesheets(p_taskuser_id))
    allKeywords = np.array(getKeyWordsFromGooglesheets(p_taskuser_id))

    if (len(allLinks) == 0 and len(allKeywords) == 0):
        logger.info("Phonebot didn't found any arguments for the task 271 !!!")
        sys.exit("Phonebot didn't found any arguments for the task 271 !!!")

    # to have the pattern {source:[arrayOfUrls],source2:[arrayOfUrls2]}
    allAccountsUrls = {}
    # if we have links in the google sheet
    if (not len(allLinks) == 0):
        # treatment for urls
        allAccountsUrls.update(discoverAllUrls(allLinks))
    # we make a search by keywords
    if not len(allKeywords) == 0:
        # treatment for keywords
        allAccountsUrls.update(discoverAllKeyWords(driver, allKeywords))

    # list of followers that we gonna scrap
    followersListUrls = []

    cptScrapped = 0
    for elem in allAccountsUrls:
        for url in allAccountsUrls[elem]:
            Sleeping_Bot(2.0, 5.0)
            driver.get(str(url).split('\'')[1])
            driver.implicitly_wait(10)

            if isAccountPrivate(driver):
                continue
            else:
                pass

            if getIfAccountHasMinFollowers(driver, p_taskuser_id):
                clickOnFollowersLink(driver)

                # scroll to the down with comparing scroll position to know if is the end or the last follower
                myFollowersListContainer = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, (".isgrP"))))
                lastPosition = driver.execute_script(
                    'return arguments[0].scrollHeight', myFollowersListContainer)
                listEnd = False

                # first scroll to get a specific class name on all items in the list
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight;', myFollowersListContainer)
                driver.execute_script(
                    'arguments[0].scrollTop = 0;', myFollowersListContainer)

                # getting all followers from this specific class
                followersList = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ("span.Jv7Aj>a.FPmhX"))))

                occurenceInTheList = 0
                while cptScrapped < p_quantity_actions and not listEnd:
                    if occurenceInTheList < len(followersList) and cptScrapped < p_quantity_actions and followerIsntScrapedYet(
                            followersList[occurenceInTheList].get_attribute("href")[
                            0:len(followersList[occurenceInTheList].get_attribute("href")) - 1].split('/')[3]):
                        followersListUrls.append(
                            followersList[occurenceInTheList].get_attribute("href"))
                        cptScrapped += 1
                    if occurenceInTheList == len(followersList):
                        responseArray = scrollDown(
                            listEnd, driver, myFollowersListContainer, lastPosition)
                        listEnd = responseArray["end"]
                        lastPosition = responseArray["lastPos"]
                        followersList = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ("span.Jv7Aj>a.FPmhX"))))
                    else:
                        occurenceInTheList += 1

                if cptScrapped == p_quantity_actions:
                    # go to each profiles stored in the followersListUrls and scraping  present data
                    for urlFollowerProfile in followersListUrls:
                        Sleeping_Bot(2.0, 5.0)
                        driver.get(urlFollowerProfile)
                        driver.implicitly_wait(10)

                        # username : get url un split to get username
                        username = urlFollowerProfile.split('/')[3]
                        bio = getBio(driver)
                        insertScrapedValuesToContacts(username, urlFollowerProfile, getFullName(driver),
                                                      getCategoryOfAccount(
                                                          driver), bio,
                                                      str(url).split('\'')[1].split(
                                                          '/')[3], 271, "instagram",
                                                      getMails(bio), getPhoneNumbers(bio), getWebsite(driver))
                        insertScrapedValuesToActions(p_browser, Instagram_username, selectContactIdByUsername(username),
                                                     "instagram", "scrap")
                    return

            else:
                continue


# lock = threading.Lock()
# p_browser = "Firefox"
# p_taskuser_id = 271
# p_driver = ""
# Instagram_username = ""
# p_quantity_actions = 20
# label_log = ""
# Scraping_Instagram_Followers_271(
#     p_browser, p_taskuser_id, Instagram_username, 10, label_log, lock)
