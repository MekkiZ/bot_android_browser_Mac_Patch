# -*- coding: utf-8 -*-
"""
Author : Thi Phan
Email : thiphan94@gmail.com
"""

import logging
import threading
import time
import sys
import sqlite3
import pathlib
import platform
import psutil
import random

sys.path.append("..")
sys.path.append(".")
from modules import mymodulesteam
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Scrap_Craigslist_Ads__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
)
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def Sleeping_Bot(borne_inf=float, borne_sup=float):
    """Random time.sleep for being a stealth bot."""
    ts = random.uniform(borne_inf, borne_sup)
    ts = round(ts, 2)
    time.sleep(ts)


def get_keyword_city(keywords_list):
    """Returns a key and a list of cities."""
    if keywords_list is None:
        logger.info(f"Keyword / City spreadsheet not found")
        return False
    return mymodulesteam.GoogleSheetGetValues(
        mymodulesteam.extract_ss_id_regex(keywords_list)
    )


def check(title):
    """Check if data existed in DataBase."""
    with lock:
        try:
            connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
            cursor = connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM contacts WHERE business_name LIKE ?", (title,)
            )
            data = cursor.fetchone()[0]
            if data == 0:
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"Error when trying to get the title in the dataBase {e}")


def scraping_ads(driver, keywords_list, index,p_taskuser_id,lock):
    """Elements for scraping."""
    try:
        # name of city
        city_name = keywords_list[index][0]
        # current day time
        date_n_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # message
        msg = (driver.find_element_by_xpath("//section[@id='postingbody']")).text
        # url of picture: test if ads has image
        try:
            url_picture = (
                driver.find_element_by_css_selector(".first.slide.visible>img[alt='1']")
            ).get_attribute("src")
        except Exception:
            url_picture = None
        # source: url
        get_url = driver.current_url
        # date_created
        date_posted = (
            driver.find_element_by_xpath(
                "//p[@id='display-date']//time[@class='date timeago']"
            )
        ).get_attribute("datetime")
        # date_update: test if ads has datetime updated
        try:
            date_update = (
                driver.find_element_by_xpath(
                    "//*[contains(text(),'updated:')]//time[@class='date timeago']"
                )
            ).get_attribute("datetime")
        except Exception:
            date_update = None
        # id message : forme "id post: xxxxxxxxxx"
        id_post = (
            driver.find_element_by_xpath(
                "//section[@class='page-container']/section[@class='body']/section[@class='userbody']/div[@class='postinginfos']/p[1]"
            ).text
        ).split(":")[1:][0]
        # type_message (type of ads)
        type_msg = (driver.find_element_by_css_selector(".crumb.section>p>a")).text
        # title of ads
        title = (driver.find_element_by_xpath("//span[@id='titletextonly']")).text
        platform_name = "craigslist"
        # type_action
        action = "scrap"
        ### Scraping for contacts and actions tables ###
        id_contact = scraping_contacts_table(
            platform_name, title, city_name, get_url, date_posted, date_update,p_taskuser_id,lock
        )
        # call function to scrape data to actions table
        scraping_actions_table(
            platform_name,
            action,
            date_n_time,
            msg,
            id_contact,
            url_picture,
            get_url,
            date_posted,
            date_update,
            id_post,
            type_msg,p_taskuser_id,lock
        )
        return True
    except Exception as e:
        logger.info(f"Error while scraping data to tables '{e}' ")
        return False


def open_craigslist(driver, keywords_list, index):
    """Open Craigslist with keywords."""
    # Load page craigslist thanks to Google
    # name of city
    city = keywords_list[index][0]
    # string for search "{name city} craigslist"
    city_for_search = city + " " + "craigslist"
    url = "https://www.google.com/"
    driver.get(url)
    driver.implicitly_wait(10)
    # search bar og Google
    search_field = driver.find_element_by_xpath("//input[@role='combobox']")
    search_field.clear()
    search_field.send_keys(city_for_search)
    search_field.submit()
    Sleeping_Bot(1.0, 3.0)
    # click link craigslist
    driver.find_element_by_partial_link_text("craigslist").click()


def search_in_craigslist(driver, keywords_list, index):
    """Search on Craigslist with keywords."""
    # search bar
    input_search = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "query"))
    )
    input_search.clear()
    # enter keyword in search bar
    input_search.send_keys(keywords_list[index][2])
    select_list = driver.find_elements_by_xpath(
        "//ul[@id='ui-id-1']//li[@class='ui-menu-item']/a"
    )
    # Have results with keyword and category?
    try:
        for web_elem in select_list:
            if (keywords_list[index][1].lower()) in web_elem.text:
                web_elem.click()
                break
    except Exception as e:
        logger.info(
            f"Not results were found with key word {keywords_list[index][2]} and category {keywords_list[index][1].lower()}"
        )
        return False


def count_pages(driver, keywords_list):
    """Count pages."""
    paginator = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".bottom.search-legend>.buttongroup.firstpage.paginator")
        )
    )
    return int((paginator.text).split("/")[1:][0].split(" ")[1:][0])


def count_ads(driver, keywords_list):
    """Count ads on each page."""
    return WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='sortable-results']/ul[@class='rows']//h3/a")
        )
    )


def scraping_contacts_table(
    platform_name, title, city_name, get_url, date_posted, date_update,p_taskuser_id,lock
):
    """Scrape the data to contacts table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sql = """INSERT INTO contacts (platform,business_name,city,url_profile,id_task_user,date_created,date_update)  VALUES (?,?,?,?,?,?,?)"""
            list_add = (
                platform_name,
                title,
                city_name,
                get_url,
                p_taskuser_id,
                date_posted,
                date_update,
            )
            sqlite_cursor.execute(sql, list_add)
            sqlite_connection.commit()
        # logger.info("Contacts table committed successfully.")

    except Exception as e:
        logger.error(f"Error while scraping contacts table: {e} ")
        raise Exception(e)
    id_contact = sqlite_cursor.execute(
        "SELECT id FROM contacts WHERE url_profile = ?", (get_url,)
    ).fetchone()[0]
    sqlite_connection.close()
    return id_contact


def scraping_actions_table(
    platform_name,
    action,
    date_n_time,
    msg,
    id_contact,
    url_picture,
    get_url,
    date_posted,
    date_update,
    id_post,
    type_msg,p_taskuser_id,lock
):
    """Scrape the data to actions table."""
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile("db.db"))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sql = """INSERT INTO actions (platform,type_action,date,message,id_contact,picture, source, date_created, date_update, id_message,id_task_user,type_message)  VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
            list_add = (
                platform_name,
                action,
                date_n_time,
                msg,
                id_contact,
                url_picture,
                get_url,
                date_posted,
                date_update,
                id_post,
                p_taskuser_id,
                type_msg,
            )
            sqlite_cursor.execute(sql, list_add)
            sqlite_connection.commit()
        # logger.info("Actions table committed successfully.")
    except Exception as e:
        logger.error(f"Error while scraping actions table: {e} ")
        raise Exception(e)
    sqlite_connection.close()


def Scraping_Craigslist_Scrap_Craigslist_Ads_23(p_browser, p_taskuser_id, p_quantity_actions, Craigslist_username,label_log, lock):
    # count scraping done
    counter_scraping = 0
    index = 0
    # Get details of the taskuser
    result = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
    # check if list of keywords is empty
    keywords_list = get_keyword_city(result["url_keywords"])

    if keywords_list is None:
        logger.error("Empty list!")
        return False
    try:
        logger.info("=== [1] Open Browser =======================================")
        # Open browser
        if p_browser == "Chrome":
            driver = mymodulesteam.ChromeDriverWithProfile()
        elif p_browser == "Firefox":
            driver = mymodulesteam.FireFoxDriverWithProfile()
        else:
            logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        # call function to scrape ads
        for ad in keywords_list:
            open_craigslist(driver, keywords_list, index)
            try:
                search_in_craigslist(driver, keywords_list, index)
                try:
                    counter_page = count_pages(driver, keywords_list)
                except Exception as e:
                    logger.info(f"No result found for keyword/city {e}")
                for i in range(0, counter_page):
                    list_ads = count_ads(driver, keywords_list)
                    counter_ad = len(list_ads)
                    for j in range(0, counter_ad):
                        try:
                            if not check(list_ads[j].text):
                                scraped = False
                                list_ads[j].click()
                                scraped = scraping_ads(driver, keywords_list, index,p_taskuser_id,lock)
                                if scraped:
                                    counter_scraping += 1
                                driver.back()
                            else:
                                logger.info(f"Already scraped")

                        except Exception as e:
                            list_ads = count_ads(driver, keywords_list)
                            if not check(list_ads[j].text):
                                list_ads[j].click()
                                scraped = scraping_ads(driver, keywords_list, index,p_taskuser_id,lock)
                                if scraped:
                                    counter_scraping += 1
                                driver.back()
                            else:
                                logger.info(f"Already scraped")
                        Sleeping_Bot(2.0, 4.0)
                        if counter_scraping == p_quantity_actions:
                            driver.quit()
                            return True

                    if i < counter_page - 1:
                        next_page = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//div[@class='search-legend bottom']//a[@class='button next']",
                                )
                            )
                        )
                        next_page.click()
                    else:
                        print(f"Last page reached!")
                index += 1
            except Exception as e:
                logger.info(f"Error while searching in Craigslist: {e}")

        driver.quit()

    except Exception as e:
        logger.error(
            f"Error while executing Scraping_Craigslist_Scrap_Craigslist_Ads_23(): {e}"
        )
        return False
#
# lock = threading.Lock()
# p_browser = "Firefox"
# p_taskuser_id = "269"
# p_driver = ""
# Linkedin_username = ""
# p_quantity_actions = 1000
# label_log = ""
# result = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)
#
# Scraping_Craigslist_Scrap_Craigslist_Ads_23(
#     p_browser, p_taskuser_id, p_quantity_actions, label_log, lock
# )
