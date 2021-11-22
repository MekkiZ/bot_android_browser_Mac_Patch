"""
    Author : Julio Morais
    Email : jjlmorais@gmail.com
"""

# ============================= Imports ==========================================
import logging
import random
import re
import sqlite3
import threading
import time
from datetime import datetime
from sqlite3 import OperationalError

from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam as MMTeam


# ================================================================================
# ==================== LOG FILE ==================================================

open(MMTeam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_YellowPage_Search_by_keywords_city__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(MMTeam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ================================================================================
# ============================== Custom Class Business ===========================
class Business:

    def __init__(self):
        self.platform = ''
        self.yellow_pages_url = ''
        self.set_platform()
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = ''
        self.address = ''
        self.zip = ''
        self.city = ''
        self.contact = ''
        self.site = ''
        self.email = ''

    # = = = = = = = = = = = = = = = = = = = = SETTERS = = = = = = = = = = = = = = = = = = = =

    def set_platform(self, platform=str("yellowpages")):
        self.platform = platform

    def set_yellow_pages_url(self, yp_url):
        self.yellow_pages_url = yp_url

    def set_name(self, name=''):
        self.name = name

    def set_address(self, address='', zip_code=''):
        self.address = address
        # print(f'>{address}<')
        # print(f'>{zip_code}<')
        zip_code = zip_code.replace(address, '')
        if not zip_code.__contains__(',') and address.__contains__(','):
            ind = address.index(',')
            self.zip = address[ind + 1:].strip()
            self.city = address[:ind].strip()
        elif zip_code.__contains__(','):
            ind = zip_code.index(',')
            self.zip = zip_code[ind + 1:].strip()
            self.city = zip_code[:ind].strip()
        else:
            self.zip = ''
            self.city = ''

    def set_contact(self, phone=''):
        self.contact = phone

    def set_email(self, mail=""):
        self.email = mail.replace('mailto:', '')

    def set_web_pages(self, site=''):
        self.site = site

    # = = = = = = = = = = = = = = = = = = = = GETTERS = = = = = = = = = = = = = = = = = = = =

    def get_name(self):
        return str(self.name)

    def get_address(self):
        return str(self.address)

    def get_zip(self):
        return str(self.zip)

    def get_city(self):
        return str(self.city)

    def get_contact(self):
        return str(self.contact)

    def get_email(self):
        return str(self.email)

    def get_site(self):
        return self.site

    def get_platform(self):
        return self.platform

    def get_yellow_pages_url(self):
        return self.yellow_pages_url

    def get_reduced_yp_url(self):
        return self.yellow_pages_url.replace('https://www.', '')

    def get_card(self):
        contact_card = f'\nPlatform: {self.get_platform()}\n'
        contact_card += f'Paje jaunes Url: {self.get_yellow_pages_url()}\n'
        contact_card += f'Title: {self.get_name()}\n'
        contact_card += f'Adresse: {self.get_address()}\n'
        contact_card += f'Zip: {self.get_zip()}\n'
        contact_card += f'City: {self.get_city()}\n'
        contact_card += f'Contact: {self.get_contact()}\n'
        contact_card += f'E-mail: {self.get_email()}\n'
        contact_card += f'Site: {self.get_site()}\n'

        return contact_card

    # = = = = = = = = = = = = = = = = = = = = Methods = = = = = = = = = = = = = = = = = = = =

    def separateur(self):
        # sep_len = max(self.title, self.address)
        print("")
        print("*" * 100)
        print("")

    def formated_contacts(self, contacts):
        formatted_contacts = []
        to_erase = '<span class="coord-numero-inscription"></span>'
        for contact in contacts:
            inner_html = contact.get_attribute("innerHTML")
            inner_html = inner_html.replace(to_erase, '')
            if not formatted_contacts.__contains__(inner_html):
                formatted_contacts.append(inner_html)
        return formatted_contacts

# ==================== Browser Selector ==========================================
def browser_selector(browser):
    if browser.__contains__("Chrome"):
        return MMTeam.ChromeDriverWithProfile()
    elif str.lower(browser).__contains__("firefox"):
        return MMTeam.FireFoxDriverWithProfile()
    else:
        MMTeam.logger.info(f"No browser passed to function : {browser}")
        return None


# ================================================================================
# ===================== send action to action table ==============================
def store_action(date_created, id_contact, contact, task_user_id, lock):
    if id_contact is None or contact is None:
        return None
    try:
        with lock:
            conn = sqlite3.connect(MMTeam.LoadFile('db.db'))
            cursor = conn.cursor()
            insert_query = """INSERT INTO actions(platform, type_action, date, id_social_account, id_contact, date_created,
                            id_task_user) VALUES(?, ?, ?, ?, ?, ?, ?) """
            action_tuple = (
                contact.get_platform(), 'Scrap', date_created, contact.get_reduced_yp_url(), id_contact,
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), task_user_id)
            cursor.execute(insert_query, action_tuple)
            conn.commit()
            conn.close()
            # print(f' - - action scrap contact : {contact.get_name()} added to DB')
            return True
    except Exception as ex:
        logger.error(f'Exception raised when trying to store actions (store_action): {ex}')
        return False


# ==================================================================================
# ===================== send contact to contact table ==============================
def store_contact(task_user_id, lock, contact=None):
    if contact is None:
        logger.info(f'No data was received when trying to save contact in db')
        return None
    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        with lock:
            conn = sqlite3.connect(MMTeam.LoadFile('db.db'))
            cursor = conn.cursor()
            insert_query = """INSERT INTO contacts(platform, business_name, address, zip, city, 
                                email, phone, website, url_profile, date_created) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            contact_tuple = (contact.get_platform(), contact.get_name(), contact.get_address(), contact.get_zip(),
                             contact.get_city(), contact.get_email(), contact.get_contact(), contact.get_site(),
                             contact.get_reduced_yp_url(), date_created)
            cursor.execute(insert_query, contact_tuple)
            conn.commit()

            contact_id = cursor.execute("SELECT id FROM contacts WHERE url_profile = ?",
                                        [contact.get_reduced_yp_url()]).fetchone()[0]
            conn.close()
        # print(f' - {contact.get_name()} added to DB')
        if store_action(date_created, contact_id, contact, task_user_id, lock):
            return True
    except Exception as ex:
        logger.error(f'Impossible to store {contact.get_name()} on db (store_contact):\n {ex} {ex.__cause__}')
        return False


# ================================================================================

# ================================== InDBt =======================================
def in_db(business_name, lock):
    with lock:
        try:
            conn = sqlite3.connect(MMTeam.LoadFile('db.db'))
            cursor = conn.cursor()
            select_query = """SELECT COUNT(1) FROM contacts WHERE business_name = ?"""
            select_tuple = (business_name,)
            res = cursor.execute(select_query, select_tuple).fetchone()[0]
            # print(res)
            if res == 0:
                return False
            else:
                logger.info(f'{business_name} was previously scraped - skip to next result')
                return True
        except OperationalError as sqlOE:
            logger.error(f'Db Execption function in_db(): {sqlOE}')


# ================================================================================

# ===================== Extract spreadsheet id from url ==========================

# extract spreadsheet id
# needs import re for the regex
def extract_ss_id(spread_sheet_url):
    return re.search('/spreadsheets/d/([a-zA-Z0-9-_]+)', spread_sheet_url).group(1)


# ================================================================================
# =============== Returns a random numbre of keyword / city ======================
def get_keyword_city(keyword_city_spreadsheet):
    is_spreadsheet = keyword_city_spreadsheet.__contains__('https://docs.google.com/spreadsheets/')
    if keyword_city_spreadsheet is None or not is_spreadsheet:
        return None
    return MMTeam.GoogleSheetGetValues(extract_ss_id(keyword_city_spreadsheet))


# ============================== Scrap Bloc ======================================
def get_page_result(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH, '//div[@class="search-results organic"]//a[@class="business-name"]'
        )))


# ================================================================================
# ============================= RandSleep ========================================
def rand_sleep():
    time.sleep(random.randint(0, 5))


# ================================================================================

# ============================== Scrap Bloc ======================================
def scrap_info(driver, task_user_id, lock):
    business = Business()
    rand_sleep()

    # Get buiseness name
    try:
        business_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//div[@class="sales-info"]/h1')))
        business.set_name(business_name.text)
    except WebDriverException or TimeoutException as te:
        business.set_name()

    # Get Phone
    try:
        phone = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//div[@class="contact"]//p')))
        business.set_contact(phone.text)
    except WebDriverException or TimeoutException as te:
        business.set_contact()

    # Get Address
    try:
        zip_code = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//div[@class="contact"]//h2')))
        address = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//div[@class="contact"]//h2/span')))
        business.set_address(address.text, zip_code.text)
    except WebDriverException or TimeoutException as te:
        business.set_address()

    # Get email
    try:
        email = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((
            By.XPATH, '//a[contains(@class, "email")]')))
        business.set_email(email.get_attribute("href"))
    except WebDriverException or TimeoutException as te:
        business.set_email()

    # Get site
    try:
        site = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((
            By.XPATH, '//a[contains(@class, "website-link")]')))
        business.set_web_pages(site.get_attribute('href'))
    except WebDriverException or TimeoutException as e:
        business.set_web_pages()

    business.set_yellow_pages_url(driver.current_url)
    store_contact(task_user_id, lock, business)


# ================================================================================
# ============================== Scrap Bloc ======================================
def Browser_YellowPage_Search_by_keywords_city(p_browser, p_taskuser_id, p_driver, Yellowpages_username,
                                               p_quantity_actions, label_log, lock):



    if p_quantity_actions is None or p_quantity_actions <= 0:
        logger.error(f'The quantity of actions it\'s valid: value received: {p_quantity_actions}')
        return False, 0

    task_user = MMTeam.GetDetailsTaskUserMysql(p_taskuser_id)
    key_cities = get_keyword_city(task_user['url_keywords'])

    if key_cities is None:
        logger.error(f'"url_list" is passed as :{key_cities}')
        return False
    # try:
    #     driver = browser_selector(p_browser)
    #     if driver is None:
    #         logger.critical(f'The browser selected is invalid')
    #         return False
    # except WebDriverException as e:
    #     logger.critical(f'Exception thrown when acquiring Browser: {e}')
    #     return False

    scrap_count = 0
    # Loops through all the sets in Key_cities
    for key_city in key_cities:
        # p_driver.get('https://www.yellowpages.com')

        # Get the input field for the Keyword. Returns false if it fails
        try:
            search_terms = WebDriverWait(p_driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'search_terms')))
        except WebDriverException as e:
            logger.critical(f'Html Input "search_terms" not fount: {e}')
            return False
        # Get the input field for the City. Returns false if it fails
        try:
            geo_location_terms = WebDriverWait(p_driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'geo_location_terms')))
        except WebDriverException as e:
            logger.critical(f'Web element "geo_location_terms" not found: {e}')
            return False
        # search_terms.clear()
        search_terms.send_keys(key_city[0])
        geo_location_terms.clear()
        geo_location_terms.send_keys(key_city[1])
        search_terms.submit()

        # Loops through all the results pages
        last_page = False
        nb_pages = 0
        while not last_page:
            nb_pages += 1

            # Loop through the results in page
            try:
                page_result = get_page_result(p_driver)
                nb_result = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located((
                    By.XPATH, '//h2[@class="n"]')))
                results = len(page_result)
            except WebDriverException as e:
                logger.error(f'No results were found: {e}')
                return False

            for i in range(0, results):
                try:
                    if not in_db(page_result[i].text, lock):
                        p_driver.execute_script('arguments[0].click();', page_result[i])
                        # print(f'{scrap_count} - {nb_result[i].text}')
                        scrap_info(p_driver, task_user['id'], lock)
                        scrap_count += 1
                        p_driver.back()

                except StaleElementReferenceException as e:
                    page_result = get_page_result(p_driver)
                    nb_result = WebDriverWait(p_driver, 5).until(EC.presence_of_all_elements_located((
                        By.XPATH, '//h2[@class="n"]')))

                    if not in_db(page_result[i].text, lock):
                        page_result = get_page_result(p_driver)
                        # nb_result = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
                            # By.XPATH, '//h2[@class="n"]')))
                        p_driver.execute_script("arguments[0].click();", page_result[i])
                        # print(f'{scrap_count} - {nb_result[i].text}')
                        scrap_info(p_driver, task_user['id'], lock)
                        scrap_count += 1
                        p_driver.back()

                except WebDriverException as e:
                    logger.error(f'Something went wrong when getting {nb_result[i].text}. '
                                 f'Script will try one more time {e}')

                if scrap_count >= p_quantity_actions:
                    logger.info(f'Scrap limit attained!')

                    # stop script when quantity_actions is achieved
                    # use when the limit is applied to all the sets(keyword, city) on the spreadsheet
                    # if the limit is on each set replace the return with Break
                    # this changes need to be done the else block below
                    return True, scrap_count
                    # break

            # Go to next Page
            try:
                a_next = WebDriverWait(p_driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, '//a[@class="next ajax-page"]')))
                # time.sleep(2.5)
                p_driver.execute_script("arguments[0].click();", a_next)
                # a_next.click()
                time.sleep(2.5)
            except WebDriverException as e:
                logger.info(f'Last page achieved: {e}')
                last_page = True

            rand_sleep()
        # print(f'Number of pages scraped: {nb_pages}')

    # p_driver.quit()
    return True, scrap_count


# ================================================================================

# p_quantity_actions = 1000
#
# lock = threading.Lock()
# task_id = '275'
# p_browser = 'Chrome'
# p_task_user = MMTeam.GetDetailsTaskUser(task_id)
#
# resultat = Browser_YellowPage_Search_by_keywords_city(p_browser, p_task_user, p_quantity_actions, lock)

