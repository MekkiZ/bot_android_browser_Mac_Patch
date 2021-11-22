            # ============================================================================== #
            #                                                                                #
            #                    Developer : Imad RAFAI                                      #
            #       Contact :                                                                #
            #                   WTSP : +33 7 53 16 48 12                                     #
            #                   Mail : imad.rafai@yahoo.com                                  #
            #                   FB.com/iimadrafaii                                           #
            #                   LINKEDIN.com/in/rafaiimad                                    #
            # ============================================================================== #

import logging
import threading
import time
import sqlite3
import random
import re
"""
Requires :
    pip install country_list
"""
from country_list import countries_for_language
import mymodulesteam
from mymodulesteam import LoadFile
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

open(LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Smartphone_Scrap_Craigslist_Ads__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
)
file_handler = logging.FileHandler(LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

            # ==============================================================================#
            #                                                                               #
            #                   Initializing Appium and launching driver                    #
            #                                                                               #
            # ==============================================================================#
def Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock):
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
    desired_caps['appPackage'] = 'com.google.android.youtube'
    desired_caps['appActivity'] = 'com.google.android.youtube.HomeActivity'
    cpt_appium_start = 0
    while True:
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            time.sleep(random.uniform(3.5, 5.3))
            return driver

        except Exception as ex:
            cpt_appium_start += 1
            logger.critical(f"{p_udid}|||Something went wrong when initializing driver : {ex}")
            logger.critical(
                f"{p_udid}|||We can't open Youtube. Please check if device is connected. Let's try again!")
            if str(ex).find('hang up') != -1:
                logger.error("PhoneBot caught the issue exception 'hang up' when initializing Driver!")
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
                logger.critical(
                    f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")
                logger.critical(
                    f"{p_udid}|||We can't open Facebook. Please check if device is connected. Let's try again!")
                mymodules.DisplayMessageLogUI(p_label_log,
                                              f"SMARTPHONE|||{p_udid}||Appium server may not be working. Please contact support@phonebot.co : {ex}")

            if cpt_appium_start > 3:
                mymodules.PopupMessage("Error",
                                       "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                mymodules.DisplayMessageLogUI(p_label_log,
                                              "PhoneBot couldn't initialize the driver. Please contact support@phonebot.co.")
                return None

            time.sleep(random.uniform(2.5, 3.3))

            # ==============================================================================#
            #                                                                               #
            #                    Shortcut to find an element via XPATH                      #
            #                                                                               #
            # ==============================================================================#

def findOneByXPath(xpath,time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, (xpath))))

            # ==============================================================================#
            #                                                                               #
            #                    Shortcut to find all elements via XPATH                    #
            #                                                                               #
            # ==============================================================================#

def findAllByXPath(xpath,time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, (xpath))))
    # ==============================================================================#
    #                                                                               #
    #                    Shortcut to find an element via ID                         #
    #                                                                               #
    # ==============================================================================#

def checkExistsByXpath(xpath):
    try:
        element = findOneByXPath(xpath)
    except Exception:
        return False
    return element

def checkAllExistByXpath(xpath):
    try:
        elements = findAllByXPath(xpath)
    except Exception:
        return False
    return elements

def checkExistsById(id):
    try:
        element = findOneById(id)
    except Exception:
        return False
    return element

def findOneById(id, time=5):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, (id))))

def Sleeping_Bot(borne_inf=float, borne_sup=float):
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)

def checkExistInDB(username):
    logger.info("checking if the user is already in the Database ... ")
    try:
        sqlite_cursor.execute(f"Select * from contacts where username = '{username}' ")
    except Exception:
        return False
    return len(sqlite_cursor.fetchall())!=0

def scrapChannel(newScrapedAccounts):
    try:
        scrapedData = dict()
        for info in columnList:
            scrapedData[info] = ""

        # list of country names in French & English:
        countriesEN = list(dict(countries_for_language('en')).values())
        countriesFR = list(dict(countries_for_language('fr')).values())

        logger.info(f"Scraping account ...")

        channelTitle = checkExistsById('com.google.android.youtube:id/channel_title')
        if channelTitle:
            scrapedData['username'] = channelTitle.text

        if scrapedData['username'] in newScrapedAccounts or checkExistInDB(scrapedData['username']):
            logger.info(f"{scrapedData['username']} has already been scrapped")
            return None, False

        barre = checkExistsByXpath("(//android.widget.Button[@content-desc='Accueil' or @content-desc='Home'])[1]")
        if barre:
            x, y = barre.location.values()
            driver.swipe(x + width * 0.9, y + 10, x + width * 0.1, y + 10, 2000)
            aboutSection = checkExistsByXpath(
                '//android.widget.Button[@content-desc="À propos" or @content-desc="About"]')
            aboutSection.click()
            lista = checkAllExistByXpath(
                '//android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup')

            vuesElement = mymodulesteam.GetTextfromScreenshot(driver, p_udid, lista[-1])
            if not 'vues' in vuesElement:
                driver.swipe(width / 2, height * 0.8, width / 2, height * 0.2, 2000)
                lista2 = checkAllExistByXpath(
                    '//android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup')
                if lista2:
                    lista += lista2
                    lista = list(set(lista))

            listOfLinks = []

            # Scraping BIO information:
            bio = mymodulesteam.GetTextfromScreenshot(driver, p_udid, lista[0])
            bio = bio.replace('\n', '').replace('\x0c', '')
            scrapedData['influencer_bio'] = bio
            urlsInBio = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', bio)

            logger.info(f"links : {'||'.join(urlsInBio)}")

            # Scraping other information:
            if lista:
                for elem in lista[1:]:

                    info = mymodulesteam.GetTextfromScreenshot(driver, p_udid, elem)
                    info = info[info.find(' ') + 1:]

                    if scrapedData['influencer_total_views'] == "" and ('vues' in info or 'views' in info):
                        numberOfViews = info.split('\n')[0]
                        scrapedData['influencer_total_views'] = numberOfViews
                        logger.info(f"Views found : {numberOfViews}")
                    elif (info.split('\n')[0] in countriesEN or info.split('\n')[0] in countriesFR) and scrapedData[
                        'country'] == "":
                        scrapedData['country'] = info.split('\n')[0]
                        logger.info(f"Country found : {scrapedData['country']}")
                    elif 'youtube.com' in info.lower() and scrapedData["influencer_channel_link"] == "":
                        youtubeURL = info.replace('\n', '').replace('\x0c', '').replace(' ', '')
                        scrapedData["influencer_channel_link"] = youtubeURL
                        logger.info(f"Url youtube found : {youtubeURL}")
                    else:
                        if '.' in info and len(info) < 25:
                            listOfLinks.append(info.replace('\n', '').replace('\x0c', ''))
                            logger.info(f"Link found : {listOfLinks[-1]}")

                ######################
                # Additional Scraping !
                ######################
                for _ in [0] * 3:
                    lista = checkAllExistByXpath(
                        '//android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup')
                    if lista:
                        for elem in lista[1:]:
                            info = mymodulesteam.GetTextfromScreenshot(driver, p_udid, elem)
                            info = info[info.find(' ') + 1:]
                            if scrapedData['url_facebook'] == "" and 'facebook' in info.lower():
                                elem.click()
                                fbLink = getFBLink()
                                scrapedData['url_facebook'] = fbLink
                                driver.back()
                                logger.info(f"FB found : {fbLink}")
                                break
                            elif 'instagram' in info.lower() and scrapedData['url_instagram'] == "":
                                elem.click()
                                instaLink = getInstaLink()
                                scrapedData['url_instagram'] = instaLink
                                logger.info(f"instagram found : {instaLink}")
                                break
                            elif 'twitter' in info.lower() and scrapedData['url_twitter'] == "":
                                elem.click()
                                scrapedData['url_twitter'] = getTwitterLink()
                                logger.info(f"twitter found : {scrapedData['url_twitter']}")
                                break

        scrapedData['influencer_links'] = "||".join(urlsInBio + listOfLinks)
        logger.info(f"Channel {scrapedData['username']} has been scraped")
        logger.info(f"Data collected : {scrapedData}")
        Sleeping_Bot(3, 4)
        return scrapedData, True
    except:
        logger.info(f"Failed to scrap current channel ! ")
        return "", False

def getTwitterLink():
    try:
        if checkExistsById("android:id/customPanel"):
            chromeOrFirefox = checkAllExistByXpath(
                '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
            for tex in chromeOrFirefox:
                if 'Chrome' in tex.text:
                    tex.click()
                    break
            if checkExistsById("android:id/customPanel"):
                chromeOrFirefox = checkAllExistByXpath(
                    '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
                for tex in chromeOrFirefox:
                    if 'Chrome' in tex.text:
                        x, y = tex.location.values()
                        driver.tap([(x, y)], 0)
                        time.sleep(.5)
                        driver.tap([(x, y)], 0)
                        break
            try:
                time.sleep(5)
                urlLink = checkExistsById('com.twitter.android:id/user_name').text
                driver.back()
                return urlLink.split('?')[0]
            except:
                logger.info("Failed to get Twitter link")
                return "-"
    except:
        return "-"

def getFBLink():
    try:
        if checkExistsById("android:id/customPanel"):
            chromeOrFirefox = checkAllExistByXpath(
                '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
            for tex in chromeOrFirefox:
                if 'Chrome' in tex.text:
                    tex.click()
                    break
            if checkExistsById("android:id/customPanel"):
                chromeOrFirefox = checkAllExistByXpath(
                    '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
                for tex in chromeOrFirefox:
                    if 'Chrome' in tex.text:
                        x, y = tex.location.values()
                        driver.tap([(x, y)], 0)
                        time.sleep(.5)
                        driver.tap([(x, y)], 0)
                        break
            try:
                time.sleep(5)
                urlLink = checkExistsById('com.android.chrome:id/url_bar')
                urlLink.click()
                copyButton = checkExistsByXpath('//android.widget.ImageView[@content-desc="Copy link" or @content-desc="Copier le lien"]')
                copyButton.click()
                urlLink = driver.get_clipboard_text().split('?')[0]
                driver.back()
                return urlLink
            except:
                logger.info("Failed to get FB link")
                return "-"
    except:
        return "-"

def getInstaLink():
    foundInsta = False
    urlLink = '-'
    counterOfBacksToPerform = 0
    try:
        if checkExistsById("android:id/customPanel"):
            chromeOrFirefox = checkAllExistByXpath(
                '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
            for tex in chromeOrFirefox:
                if 'nstagram' in tex.text:
                    foundInsta = True
                    counterOfBacksToPerform+=1
                    tex.click()
                    break
            if not foundInsta:
                for tex in chromeOrFirefox:
                    if 'Chrome' in tex.text:
                        foundInsta = True
                        counterOfBacksToPerform += 1
                        tex.click()
                        break

            if checkExistsById("android:id/customPanel"):
                chromeOrFirefox = checkAllExistByXpath(
                    '//android.widget.ScrollView/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/android.widget.GridView/android.widget.LinearLayout/android.widget.TextView')
                for tex in chromeOrFirefox:
                    if 'nstagram' in tex.text:
                        foundInsta = True
                        counterOfBacksToPerform += 1
                        x, y = tex.location.values()
                        driver.tap([(x, y)], 0)
                        time.sleep(.5)
                        driver.tap([(x, y)], 0)
                        break
            if foundInsta:
                try:
                    time.sleep(5)
                    barre = checkExistsById('com.instagram.android:id/action_bar_overflow_icon')
                    if barre:
                        barre.click()
                        copyButton = checkExistsByXpath('//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.Button[5]')
                        if copyButton:
                            copyButton.click()
                            urlLink = driver.get_clipboard_text().split('?')[0]
                    for _ in[0]*counterOfBacksToPerform:
                        driver.back()
                    return urlLink
                except:
                    logger.info("Failed to get Insta link")
                    for _ in[0]*counterOfBacksToPerform:
                        driver.back()
                    return "-"
    except:
        for _ in [0] * counterOfBacksToPerform:
            driver.back()
        return "-"

def checkIfColumnExist(sqlite_cursor, columnList):
    for column in columnList:
        try:
                sqlite_cursor.execute(f'ALTER TABLE contacts ADD COLUMN {column};')
        except:
                pass # We just ignore the exception

def addToBD(columnList, infos):
    from datetime import datetime

    checkIfColumnExist(sqlite_cursor,columnList)

    try:
            sqlite_cursor.execute(f"INSERT INTO contacts(platform,type,{columnList[0]},{columnList[1]},{columnList[2]},{columnList[3]},{columnList[4]},{columnList[5]},{columnList[6]},{columnList[7]},{columnList[8]},id_task_user, date_created) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                    "Youtube",
                    "Influencers_information",
                    f"{str(infos[columnList[0]])}",
                    f"{str(infos[columnList[1]])}",
                    f"{str(infos[columnList[2]])}",
                    f"{str(infos[columnList[3]])}",
                    f"{str(infos[columnList[4]])}",
                    f"{str(infos[columnList[5]])}",
                    f"{str(infos[columnList[6]])}",
                    f"{str(infos[columnList[7]])}",
                    f"{str(infos[columnList[8]])}",
                    p_taskuser_id,
                    str(datetime.now()),
            ),
            )
            sqlite_connection.commit()

            sqlite_cursor.execute(
                "INSERT INTO actions(platform,type_action, id_social_account, source, date_created, id_task_user) VALUES (?,?,?,?,?,?)",
                ('Youtube', 'Scraping', f"{str(infos[columnList[0]])}", f"{str(infos[columnList[2]])}", str(datetime.now()), p_taskuser_id))
            sqlite_connection.commit()

    except Exception as ex:
            print(f"Error when inserting in database: {ex}")

def Smartphone_Scraping_Youtube_Influencers(p_taskuser_id, p_udid, p_systemPort, p_deviceName,
                                                  p_version, p_os, p_label_log, lock,
                                                  limit_of_liked_post):
    logger.info("=== Open Smartphone =======================================")
    global driver
    global sqlite_cursor
    global sqlite_connection
    global database
    global width
    global height
    global columnList
    global newScrapedAccounts

    columnList = (
    "username", "country", "influencer_channel_link", "url_facebook", "url_twitter", "url_instagram", "influencer_bio",
    "influencer_links", "influencer_total_views")

    database = 'db.db'
    sqlite_connection = sqlite3.connect(LoadFile(database))
    sqlite_cursor = sqlite_connection.cursor()

    """
        Ajouter une fct pour ecrire lentement (simulation de l'être humain) [send_keys() + time.sleep()]
    """

    # ==============================================================================#
    #                                                                               #
    #                       Opening Youtube On SMARTPHONE                           #
    #                                                                               #
    # ==============================================================================#

    try:
        # Getting keywords :
        getGssUrl = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
        urlid = mymodulesteam.extract_ss_id(getGssUrl["url_keywords"])
        valuesGG = mymodulesteam.GoogleSheetGetValues(urlid)
        keywords = [item[0] for item in valuesGG]

        for keyword in keywords[1:]:
            logger.info(f"new keyword : {keyword}")
            driver = Initialisation_Driver(p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock)
            size = driver.get_window_size()

            width = size['width']
            height = size['height']

            # Verifying if there is a popup to close :
            popup = checkExistsById('com.google.android.youtube:id/mealbar_dismiss_button')
            if popup:
                popup.click()
                Sleeping_Bot(1,2)

            popup2 = checkExistsById('android:id/customPanel')
            if popup2:
                driver.back()

            #find search box :
            searchButton = checkExistsByXpath('//android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.LinearLayoutCompat/android.widget.FrameLayout[2]')
            searchButton.click()

            searchBox = checkExistsById('com.google.android.youtube:id/search_edit_text')
            searchBox.send_keys(keyword)
            driver.press_keycode(66)

            nonEffectiveSwipes = 0
            newScrapedAccounts = []

            driver.swipe(width / 2, height * 0.7, width / 2, height * 0.5, 2000)

            listOfResults = checkAllExistByXpath('//android.widget.ImageView[@content-desc="Accéder à la chaîne" or @content-desc="Go to channel"]')

            while nonEffectiveSwipes < 10 and len(newScrapedAccounts) < limit_of_scraped_accounts:
                foundNewAccount = False

                if listOfResults:
                    for channel in listOfResults[:1]:
                        channel.click()
                        Sleeping_Bot(2, 3)

                        # retourne couple of username + boolean : false if already Scraped (already in BD or in new Scraped accounts)
                        scrapedData, scraping = scrapChannel(newScrapedAccounts)

                        driver.back()
                        if scraping:
                            foundNewAccount = True
                            newScrapedAccounts.append(scrapedData['username'])
                            logger.info(f"Total now is : {len(newScrapedAccounts)}/20")
                            addToBD(columnList, scrapedData)
                            logger.info(f"Channel {scrapedData['username']} has been Scraped")

                if foundNewAccount:
                    nonEffectiveSwipes = 0
                else:
                    nonEffectiveSwipes += 1
                driver.swipe(width / 2, height * 0.7, width / 2, height * 0.4, 2000)
                listOfResults = checkAllExistByXpath('//android.widget.ImageView[@content-desc="Accéder à la chaîne" or @content-desc="Go to channel"]')


            time.sleep(10)


    except Exception as ex:
        logger.error(f'ERROR :  {ex}')
        return False

    finally:
        sqlite_connection.close()
        driver.quit()


"""
# Numero de task user arbitraire
p_taskuser_id = 262
limit_of_scraped_accounts = 20  # Maximum number of posts to be liked
p_deviceName = "Honor 8X"
p_udid = "9YHNW18C28002110"
p_os = "Android"
p_version = "10.0"
p_systemPort = ""
p_label_log = ""
lock = threading.Lock()

Smartphone_Scraping_Youtube_Influencers(p_taskuser_id, p_udid, p_systemPort, p_deviceName, p_version, p_os, p_label_log, lock, limit_of_scraped_accounts)
"""
