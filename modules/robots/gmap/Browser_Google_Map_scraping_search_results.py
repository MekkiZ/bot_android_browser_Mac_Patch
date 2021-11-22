# -*- coding: utf-8 -*-
#################
# Dimitri Détré #
# Finished task #
#################

"""
This is a sample task for automation software Phonebot.co on Browser Firefox & Chrome
https://github.com/phonebotco/phonebot


"""
import logging
import sqlite3
import threading
from modules import mymodulesteam

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
from time import sleep
from datetime import datetime
import pathlib
import platform
import psutil
import random

# ==================== LOG FILE ==================================================
open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Google_Maps_Scrapping_By_Keyword_And_City__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# ================================================================================

"""
Random time.sleep for being a stealth bot.
"""
def Sleeping_Bot(borne_inf=float, borne_sup=float):
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    sleep(ts)

# Function that test if a data is almost in the dataBase.
def Presence_Of_Data(p_platform, p_city, p_username, p_address):
    try:
        connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        cursor = connection.cursor()
        data_Parameter = (p_platform, p_city, p_username, p_address)
        cursor.execute("SELECT * FROM contacts WHERE platform = ? AND city = ? AND username = ? AND address = ?", data_Parameter)
        logger.info("-----Request SENT-----")

        if len(cursor.fetchall()) == 0:
            logger.info("-----Element doesn't exist-----")
            connection.close() 
            return False
        else:
            logger.info("-----Element almost exist-----")
            connection.close() 
            return True
    except Exception as ex:
        logger.error(f"Error when trying to get the id in the dataBase {ex}")
        # Go to the last save.
        connection.rollback()
    finally:
        connection.close() 

# extract spreadsheet id
def extract_ss_id(spread_sheet_url):
    spread_sheet_url = spread_sheet_url.replace('https://docs.google.com/spreadsheets/d/', '')
    ind = spread_sheet_url.index('/')
    spread_sheet_url = spread_sheet_url[:ind]
    return spread_sheet_url

# returns a key and a list of cities
def get_keyword_city(key_city, min):
    # list to return
    key_city_list = []
    # get spreadsheet id
    ss_id = extract_ss_id(key_city)
    # get spreadsheet data
    values = mymodulesteam.GoogleSheetGetValues(ss_id)
    ind = []
    length = len(values)
    ind += random.sample(range(length), min)
    #print(ind)
    for i in ind:
        key_city_list.append(values[i])
    return key_city_list

def Intelli_Search_GG_Map(label_log, p_browser, p_taskuser_id, lock, keywords = str, city = str):
    logger.info("=== [1] Open Browser =======================================")


    # Open the browser
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")

    # Page loading 
    # Try 5 times before print an error message (Connexion's problemes ?)
    count = 0
    while(count != (-1)):
        try:
            driver.get('https://www.google.fr/maps')
            Sleeping_Bot(7.5, 10.5)
            driver.maximize_window()
            Sleeping_Bot(5.5, 6.5)
            count = -1
        except Exception as ex:
            count = count + 1
            Sleeping_Bot(7.5, 10.5)
            if(count >= 5):
                count = -1
                logger.error(f"Error when getting access to the website : {ex}")
    
    # Getting the search bar & write the research
    msg = keywords + ', ' + city

    count = 0
    while(count != (-1)):
        try:
            search_bar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//input[@id='searchboxinput']"))))
            driver.execute_script("arguments[0].click();", search_bar)
            Sleeping_Bot(2.5, 4.5)                    
            count = -1
        except Exception as ex:
            count = count + 1
            Sleeping_Bot(2.5, 4.5)    
            if(count >= 5):
                count = -1
                logger.error(f"Error when trying to get the search bar : {ex}")

    count = 0
    while(count != (-1)):
        try:
            search_bar.send_keys(msg)
            Sleeping_Bot(2.5, 4.5)                    
            count = -1
        except Exception as ex:
            count = count + 1
            Sleeping_Bot(2.5, 4.5)    
            if(count >= 5):
                count = -1
                logger.error(f"Error when trying to write the research : {ex}")
    
    # Send the research
    count = 0
    while(count != (-1)):
        try:
            search_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//button[@id='searchbox-searchbutton']"))))
            driver.execute_script("arguments[0].click();", search_btn)
            Sleeping_Bot(2.5, 3.5)                    
            count = -1
        except Exception as ex:
            count = count + 1
            Sleeping_Bot(2.5, 3.5)    
            if(count >= 5):
                count = -1
                logger.error(f"Error when trying to get the research button : {ex}")

    # Press the button
    count = 0
    while(count != (-1)):
        try:
            btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'result-container')]//a[contains(@class,'place-result-container-place-link')]"))))
            driver.execute_script("arguments[0].click();", btn)
            Sleeping_Bot(2.5, 3.5)                    
            count = -1
        except Exception as ex:
            count = count + 1
            Sleeping_Bot(2.5, 3.5)    
            if(count >= 5):
                count = -1
                logger.error(f"Error when trying to get the research button : {ex}")

    # Scrapping the elements
    count = 0
    list_of_all_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,("//div[@class='app-viewcard-strip']//div[@class='section-carousel-item-container']//div[contains(@class,'image-container')]//img[@role='presentation']"))))
    Sleeping_Bot(2.5, 3.5) 
    nb_of_elements = len(list_of_all_elements)
    #print(f"nb elem {nb_of_elements}.")

    for i in range(1, nb_of_elements):
        title = ""
        category = ""
        star = ""
        review = ""
        star_review = ""
        address = ""
        website = ""
        phone = ""

        # Scrapping more precisely the datas
        try:
            try:
                title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'section-hero-header-title')]//h1[contains(@class,'section-hero-header-title')]"))))
                Sleeping_Bot(2.5, 3.5) 
                newTitle = title.text
                #print(newTitle)
            except:
                if(len(newTitle) == 0):
                    newTitle = "NO TITLE"
            try:
                category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'section-rating')]//span[contains(@class,'section-rating')]//button[contains(@class,'widget-pane-link') and contains(@jsaction,'category')]"))))
                Sleeping_Bot(2.5, 3.5) 
                newCategory = category.text
                #print(newCategory)
            except:
                if(len(newCategory) == 0):
                    newCategory = "NO CATEGORY"
            try:
                stars = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'section-rating')]//div[contains(@class,'reviews-tap-area')]//span[contains(@class,'section-star')]"))))
                Sleeping_Bot(2.5, 3.5) 
                #print(stars.text)
                reviews = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'section-rating')]//span[contains(@class,'section-rating')]//button[contains(@class,'widget-pane-link') and contains(@aria-label,'avis')]"))))
                Sleeping_Bot(2.5, 3.5) 
                #print(reviews.text)
                newStarReview = str(stars.text + " stars/" + reviews.text + " reviews")
                #print(newStarReview)
            except:
                Sleeping_Bot(2.5, 4.5)  
                new_star = ""  
                new_review = ""
                if((len(new_star) or len(new_review)) == 0):
                    newStarReview = "NO RATINGS AND REVIEWS"
            try:
                address = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'content')]//div[contains(@class,'text')]//button[@data-item-id='address']//div[contains(@class,'primary-text')]"))))
                Sleeping_Bot(2.5, 3.5) 
                newAddress = address.text
                #print(newAddress)
            except:
                if(len(newAddress) == 0):
                    newAddress = "NO ADDRESS"
            try:
                website = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'content')]//div[contains(@class,'text')]//div[contains(@class,'underline_on_hover')]"))))
                Sleeping_Bot(2.5, 3.5) 
                newWebsite = website.text
                #print(newWebsite)
            except:
                if(len(newWebsite) == 0):
                    newWebsite = "NO WEBSITE"
            try:
                phone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[contains(@class,'content')]//div[contains(@class,'text')]//button[contains(@data-item-id,'phone')]//div[contains(@class,'primary-text')]"))))
                Sleeping_Bot(2.5, 3.5) 
                newPhone = phone.text
                #print(newPhone)
            except:
                if(len(newPhone) == 0):
                    newPhone = "NO PHONE NUMBER"

        except Exception as ex:
            Sleeping_Bot(2.5, 4.5)    
            logger.error(f"Error when trying to get elements : {ex}")
        
        
        p_platform = "gmap" 
        p_city = city 
        p_username = newTitle
        p_address = newAddress
        p_google_reviews = newStarReview
        p_website = newWebsite
        p_phone = newPhone
        p_category = newCategory
        date = datetime.today()
        p_type_action = "Scrap"
        

        add_or_update = Presence_Of_Data(p_platform, p_city, p_username, p_address)

        # Transfert or update of scrapped data
        if add_or_update == True:                
            # Update the data
            try:
                connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                cursor = connection.cursor()
                data_Parameter = (p_google_reviews, p_phone, date, p_platform, p_city, p_username, p_address, p_website)
                with lock:
                    cursor.execute("UPDATE contacts SET google_reviews = ?, phone = ?, date_update = ?, website = ? WHERE platform = ? AND city = ? AND username = ? AND address = ?", data_Parameter)
                    logger.info("New UPDATE in the DataBase.")
                    connection.commit()
                logger.info("Commited successfully.")                
            except Exception as ex:
                logger.error(f"Error when trying to UPDATE the dataBase {ex}")
                # Go to the last save.
                connection.rollback()
            finally:
                connection.close() 

        else:
            # Add informations in contact
            try:
                connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                cursor = connection.cursor()
                newLine = (cursor.lastrowid, p_platform, p_username, p_address, p_city, p_phone, p_category, p_google_reviews, date, p_website)
                # The '?' allows to avoid attacks by SQL's Injections 
                with lock:
                    cursor.execute("INSERT INTO contacts (id, platform, username, address, city, phone, business_category, google_reviews, date_created, website) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", newLine)
                    logger.info("New added line in the DataBase.")
                    connection.commit()
                logger.info("Commited successfully.")
            except Exception as ex:
                logger.error(f"Error when trying to commit new information in the contact {ex}")
                # Go to the last save.
                connection.rollback()
            finally:
                connection.close()

            # Add informations in actions
            try:
                connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
                cursor = connection.cursor()
                p_id_contact = cursor.execute("SELECT id FROM contacts WHERE username = ? AND phone = ?", (p_username, p_phone))
                p_id_contact = cursor.fetchone()[0]
                #print(p_id_contact)
                newLine = (p_platform, p_type_action, p_username, date, p_id_contact)
                # The '?' allows to avoid attacks by SQL's Injections 
                with lock:
                    cursor.execute("INSERT INTO actions (platform, type_action, id_social_account, date_created, id_contact) VALUES(?, ?, ?, ?, ?)", newLine)
                    logger.info("New added line in the DataBase.")
                    connection.commit()
                logger.info("Commited successfully.")
            except Exception as ex:
                logger.error(f"Error when trying to commit new information in the actions {ex}")
                # Go to the last save.
                connection.rollback()
            finally:
                connection.close() 
        
        # Scrolling
        xpathExpression = (str)
        i = str(i)
        nb_of_elements = str(nb_of_elements)
        xpathExpression = "//div[@class='app-viewcard-strip']//div[@class='section-carousel-item-container']//div[contains(@class,'card') or contains(@class,'has-image')]/preceding-sibling::*[" + nb_of_elements + "]/following-sibling::*[" + i + "]"
        try:
            nextPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,(xpathExpression))))
            Sleeping_Bot(2.5, 3.5) 
            driver.execute_script("arguments[0].click();", nextPage)
            count = count + 1
        except:
            nb_of_elements = int(nb_of_elements)
            nb_of_elements = (nb_of_elements - 1)
            nb_of_elements = str(nb_of_elements)
            xpathExpression = "//div[@class='app-viewcard-strip']//div[@class='section-carousel-item-container']//div[contains(@class,'card') or contains(@class,'has-image')]/preceding-sibling::*[" + nb_of_elements + "]/following-sibling::*[" + i + "]"
            try:
                nextPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,(xpathExpression))))
                Sleeping_Bot(2.5, 3.5) 
                driver.execute_script("arguments[0].click();", nextPage)
                count = count + 1
            except Exception as ex:
                logger.error(f"Error when trying to click on the next container : {ex}")

        if(count > 3):
            count = 0
            try:
                scroll = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,("//div[@class='app-viewcard-strip']//div[contains(@class,'next-icon')]"))))
                Sleeping_Bot(2.5, 3.5) 
                driver.execute_script("arguments[0].click();", scroll)
            except Exception as ex:
                logger.error(f"Error when trying to click on the next page : {ex}")

"""
p_browser = "Firefox"
p_taskuser_id = "272"
p_driver = ""
p_quantity_actions = 3
label_log = ""
lock = threading.Lock()
result = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
key_city = get_keyword_city(result['url_keywords'], p_quantity_actions)
#city = "Besançon"
#keywords = "Restaurants"
#print(key_city)

'''
result=mymodulesteam.GetDetailsTaskUser(272)
print(result)
'''

for i in range(0, p_quantity_actions):
    keyword = key_city[i][0]
    city = key_city[i][1]
    start = datetime.today()
    Intelli_Search_GG_Map(label_log, p_browser, p_taskuser_id, lock, keyword, city)
    end = datetime.today()
    #print(f"\\\\\ RUN DURATION : |{start}|---|{end}| /// ")

"""
