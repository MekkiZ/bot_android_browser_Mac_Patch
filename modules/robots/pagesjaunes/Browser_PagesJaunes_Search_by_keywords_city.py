"""
    Author : Julio Morais
    Email : jjlmorais@gmail.com
"""
import logging
import random
import sqlite3
import threading
import time
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam


# ==================== LOG FILE ==================================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Browser_YellowPages_Search_by_keywords_city__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ================================================================================

# ======================== Custom class info =====================================
class Info:

    def __init__(self):
        self.platform = ''
        self.pajes_jaunes_url = ''
        self.set_platform()
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.name = ""
        self.address = ""
        self.zip = ""
        self.city = ""
        self.contact = []
        self.web_pages = []
        self.facebook = ''
        self.twitter = ''

    # = = = = = = = = = = = = = = = = = = = = SETTERS = = = = = = = = = = = = = = = = = = = =

    def set_platform(self, platform=str("pagesjaunes")):
        self.platform = platform

    def set_pajes_jaunes_url(self, pj_url):
        self.pajes_jaunes_url = pj_url

    def set_name(self, name="PNB"):  # PNB - Page Not Available
        self.name = name

    def set_address(self, address):
        if address is not None:
            self.address = self.formated_adresse(address)
        else:
            self.address = None

    def set_contact(self, contacts):
        if contacts is None:
            self.contact = None
        else:
            self.contact = self.formated_contacts(contacts)

    def set_web_pages(self, web_pages=''):
        if self.web_pages.__contains__(web_pages):
            pass
            # print(f'{web_pages} Already on web pages')
        else:
            if not web_pages == "www.facebook.com":
                self.web_pages.append(web_pages)

    def set_facebook(self, fb=''):
        self.facebook = fb

    # setting the twitter will result on the removal of twitter url from web_pages
    def set_twitter(self):
        for url in self.web_pages:
            if len(url) > 0:
                if url[0] == '@':
                    self.twitter = url
                    self.web_pages.remove(url)

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

    def get_contacts_str(self):
        contacts_str = ''
        if self.contact is not None:
            for tel in self.contact:
                contacts_str += f'{tel} - '
            contacts_str = contacts_str[:len(contacts_str) - 2]
        return ('', str(contacts_str.strip()))[self.contact is not None]

    # returns a list of string
    def get_web_pages(self):
        return self.web_pages

    def get_web_pages_str(self):
        webpages_str = ''
        if self.web_pages is not None:
            for page in self.web_pages:
                webpages_str += f'{page} '
        return ('', str(webpages_str.strip()))[self.web_pages is not None]

    def get_platform(self):
        return self.platform

    def get_facebook(self):
        return ('', str(self.facebook))[self.facebook is not None]

    def get_twitter(self):
        return ('', str(self.twitter))[self.twitter is not None]

    def get_pages_jaunes_url(self):
        return self.pajes_jaunes_url

    def get_reduced_page_jaunes_url(self):
        return self.pajes_jaunes_url.replace('https://www.', '')

    def get_contact_card(self):
        contact_card = f'\nPlatform: {self.get_platform()}\n'
        contact_card += f'Paje jaunes Url: {self.get_pages_jaunes_url()}\n'
        contact_card += f'Title: {self.get_name()}\n'
        contact_card += f'Adresse: {self.get_address()}\n'
        contact_card += f'Zip: {self.get_zip()}\n'
        contact_card += f'City: {self.get_city()}\n'
        contact_card += f'Contact: {self.get_contact()}\n'
        contact_card += f'Facebook: {self.get_facebook()}\n'
        contact_card += f'Twitter: {self.get_twitter()}\n'
        contact_card += f'Web pages:\n'
        for line in self.web_pages:
            contact_card += f'{line}\n'

        return contact_card

    # = = = = = = = = = = = = = = = = = = = = Methods = = = = = = = = = = = = = = = = = = = =

    def separateur(self):
        # sep_len = max(self.title, self.address)
        print("")
        print("*" * 100)
        print("")

    def formated_adresse(self, adresse_bloc):
        addr = ''
        zip = ''
        city = ''

        for line in adresse_bloc:
            if not addr.__contains__(line.text):
                addr += line.text

        ind = addr.index(',')

        for i in range(ind + 1, len(addr)):
            if addr[i].isdigit():
                zip += addr[i]
            else:
                city += addr[i]

        addr = addr[:ind]
        self.zip = zip.strip()
        self.city = city.strip()
        return addr

    def formated_contacts(self, contacts):
        formatted_contacts = []
        to_erase = '<span class="coord-numero-inscription"></span>'
        for contact in contacts:
            inner_html = contact.get_attribute("innerHTML")
            inner_html = inner_html.replace(to_erase, '')
            if not formatted_contacts.__contains__(inner_html):
                formatted_contacts.append(inner_html)
        return formatted_contacts


# ================================================================================
# =================== Browser selector   =========================================
def browser_selector(browser):
    if browser.__contains__("Chrome"):
        return mymodulesteam.ChromeDriverWithProfile()
    elif browser.__contains__("firefox"):
        return mymodulesteam.FireFoxDriverWithProfile()
    else:
        mymodulesteam.logger.error(f"No browser passed to function : {browser}")
        return False


# ================================================================================
# ================= Send action to action table ==================================
def store_action(date_created, id_contact, contact, user_id, lock):
    try:
        # with lock: - the function that which calls this one, uses with lock to execute
        conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        cursor = conn.cursor()
        insert_query = """INSERT INTO actions(platform, type_action, date, id_social_account, id_contact, date_created,
                        id_task_user) VALUES(?, ?, ?, ?, ?, ?, ?) """
        action_tuple = (
            contact.get_platform(), 'Scrap', date_created, contact.get_reduced_page_jaunes_url(), id_contact,
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), user_id)
        cursor.execute(insert_query, action_tuple)
        conn.commit()
        conn.close()
    except Exception as ex:
        logger.error(f'sqlite execption (store_action): {ex}')
        return False
    return True


# ================================= send contacts to contacts table =========================
def store_contact(user_id, lock, contact=None):
    date_created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        with lock:
            conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            cursor = conn.cursor()
            insert_query = """INSERT INTO contacts(platform, business_name, address, zip, city, 
                                phone, website, url_profile, twitter, url_facebook, id_task_user, date_created) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            contact_tuple = (contact.get_platform(), contact.get_name(), contact.get_address(), contact.get_zip(),
                             contact.get_city(), contact.get_contacts_str(), contact.get_web_pages_str(),
                             contact.get_pages_jaunes_url(), contact.get_twitter(), contact.get_facebook(),
                             user_id, date_created)
            cursor.execute(insert_query, contact_tuple)
            conn.commit()

            contact_id = cursor.execute("SELECT id FROM contacts WHERE url_profile = ?",
                                        [contact.get_pages_jaunes_url()]).fetchone()[0]
            conn.close()
            return (False, True)[store_action(date_created, contact_id, contact, user_id, lock)]
    except Exception as ex:
        logger.error(f'Exception thrown (store_contact): {ex} {ex.__cause__}')
        return False


# ==============================================================================================
def rand_sleep():
    time.sleep(random.randint(0, 5))


# =========================== returns a key and a list of cities ===============================
def get_keyword_city(key_city):
    if key_city is None:
        logger.info(f'Keyword / City spreadsheet not found')
        return False
    return mymodulesteam.GoogleSheetGetValues(mymodulesteam.extract_ss_id_regex(key_city))


# ==============================================================================================
def extract_pages(pages):
    pages_formated = ''
    change = False
    for char in pages:
        if char == '/':
            change = not change
        if change:
            pages_formated += ('', char)[char.isdigit()]
    return int(pages_formated)


# ================================================================================================

def get_contact_elems(driver):
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        By.XPATH, '//header[@class="v-card"]//h3//a')))


def scrappe_contact_info(driver, user_id, lock):
    rand_sleep()
    info = Info()
    try:
        nom = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '//div[@class="denom"]//h1')))
        info.set_pajes_jaunes_url(driver.current_url)
        info.set_name(nom.text)
    except TimeoutException as ex:
        logger.info(f'Page No longer available (func: s_c_i getting name): {ex}')
        return False

    try:
        tel = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
            By.XPATH, '//span[contains(@class, "coord-numero noTrad")]')))
    except Exception as ex:
        logger.info(f'Exception contact doesn\'t have any tel number (l:79): {ex}')
        tel = None
    info.set_contact(tel)

    try:
        address = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
            By.XPATH, '//div[@id="blocCoordonnees"]//span[@class ="noTrad"]')))
        info.set_address(address)
    except Exception as ex:
        logger.info(f'Adresse not available (func: sci getting adresse): {ex}')
        info.set_address(None)

    # check if there are web pages, if not sets web_pages to None
    try:
        web_pages = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
            By.XPATH, '//ul[@class="clearfix"]//span[@class="value"]')))
        try:
            fb = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH, '//a[contains(@class, "FACEBOOK_PAYANT")]')))
            click_on_element(driver, fb)
            # the link to web facebook on the pagejaunes is generated on click. to avoid an incorrect fb link
            # the script goes to fb page to fecth the profile url
            original_window = driver.current_window_handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    time.sleep(1)
                    info.set_facebook(driver.current_url)
                    driver.close()
                    driver.switch_to.window(original_window)
                    time.sleep(1)
        except Exception as ex:
            info.set_facebook()
            logger.info(f'Facebook not found: {ex}')

    except Exception as ex:
        logger.info(f'Exception contact doesn\'t have any web page (l:94): {ex}')
        # print(f'Exception contact doesn\'t have any web page (l:94): {str(ex)}')
        web_pages = None

    if web_pages is not None:
        for web_page in web_pages:
            # print(web_page.text)
            info.set_web_pages(web_page.text)
        info.set_twitter()
    elif web_pages is None:
        info.set_web_pages()

    add_db = store_contact(user_id, lock, info)
    driver.back()
    return add_db


def click_on_element(driver, element):
    driver.execute_script("arguments[0].click();", element)


def scrappe_yellow_pages(driver, kc, actions_done, quantity_actions, user_id, lock):
    driver.get('https://www.pagesjaunes.fr')

    try:
        input_search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "quoiqui")))
        input_where = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "ou")))
        input_search.send_keys(kc[0])
        input_where.send_keys(kc[1])
        input_search.submit()
    except Exception as ex:
        logger.info(f'Didn\'t not found any result, please verify Keyword and/or City (l:374): {ex}')
        return False

    try:
        sel_compteur = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'SEL-compteur')))
        pages = extract_pages(sel_compteur.text)
        # pages = extract_pages(driver.find_element(By.ID, 'SEL-compteur').text)
        # insert a breakpoint to skip CAPTCHA
    except Exception as ex:
        logger.info(f'No result found to keyword/city {kc}: {ex}')
        return True

    for i in range(0, pages):
        contacts_elems = get_contact_elems(driver)
        contacts_par_page = len(contacts_elems)

        for j in range(0, contacts_par_page):
            scrappe_contact = False
            rand_sleep()
            try:

                # driver.execute_script("arguments[0].click();", contacts_elems[j])
                click_on_element(driver, contacts_elems[j])
                scrappe_contact = scrappe_contact_info(driver, user_id, lock)
            except WebDriverException as ex:
                # logger.info(f'Exception contacts items are stale. data will be refetched (l:158): {ex}')
                contacts_elems = get_contact_elems(driver)
                # driver.execute_script("arguments[0].click();", contacts_elems[j])
                click_on_element(driver, contacts_elems[j])
                scrappe_contact = scrappe_contact_info(driver, user_id, lock)

            if scrappe_contact:
                actions_done += 1

            if actions_done == quantity_actions:
                driver.quit()
                return True

        if i < pages - 1:
            next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH, '//a[@id="pagination-next"]')))
            click_on_element(driver, next_page)
        else:
            print(f'last page reached i({i + 1}) = pages({pages})')
    return True


def in_db(text, lock):
    with lock:
        try:
            conn = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
            cursor = conn.cursor()
            select_query = """SELECT COUNT(1) FROM contacts WHERE business_name = ?"""
            select_tuple = (text,)
            res = cursor.execute(select_query, select_tuple).fetchone()[0]
            # print(res)
            return (False, True)[res > 0]
        except Exception as sqlOE:
            logger.error(f'Db Execption function in_db(): {sqlOE}')


def Browser_PagesJaunes_Search_by_keywords_city(
        p_browser, p_taskuser_id, Pagesjaunes_username, p_driver, p_quantity_actions, label_log, lock):

    scrap_result = False
    # db_result is the combined result of the execution of store_contacts() and store_actions()
    # if one of this methods fails on execution False will be return.
    db_result = False
    actions_done = 0
    task = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)

    try:
        # logger.info("=== [1] Scrapping script launched =======================================")
        # if p_browser.lower() == "Chrome":
        #     driver = MMTeam.ChromeDriverWithProfile()
        # if p_browser.lower() == "firefox":
        #     driver = MMTeam.FireFoxDriverWithProfile()

        p_driver.maximize_window()
        keyword_city = get_keyword_city(task['url_keywords'])

        for kc in keyword_city:
            # p_driver.get('https://www.pagesjaunes.fr')

            try:
                input_search = WebDriverWait(p_driver, 5).until(EC.presence_of_element_located((By.NAME, "quoiqui")))
                input_where = WebDriverWait(p_driver, 5).until(EC.presence_of_element_located((By.NAME, "ou")))
                input_search.clear()
                input_where.clear()
                input_search.send_keys(kc[0])
                input_where.send_keys(kc[1])
                input_search.submit()

                try:
                    sel_compteur = WebDriverWait(p_driver, 5).until(
                        EC.presence_of_element_located((By.ID, 'SEL-compteur')))
                    pages = extract_pages(sel_compteur.text)
                    # pages = extract_pages(driver.find_element(By.ID, 'SEL-compteur').text)
                    # insert a breakpoint to skip CAPTCHA
                except Exception as ex:
                    pages = 0
                    logger.info(f'No result found to keyword/city {kc}: {ex}')

                for i in range(0, pages):
                    contacts_elems = get_contact_elems(p_driver)
                    contacts_par_page = len(contacts_elems)

                    j = 0
                    while j <= contacts_par_page:
                        scrappe_contact = False
                        try:

                            # driver.execute_script("arguments[0].click();", contacts_elems[j])
                            if not in_db(contacts_elems[j].text, lock):
                                added_db = False
                                click_on_element(p_driver, contacts_elems[j])

                                added_db = scrappe_contact_info(p_driver, p_taskuser_id, lock)
                                if added_db:
                                    actions_done += 1
                            else:
                                logger.info(f'{contacts_elems[j].text} already scraped')
                        except WebDriverException as ex:
                            # logger.info(f'Exception contacts items are stale. data will be refetched (l:158): {ex}')
                            contacts_elems = get_contact_elems(p_driver)
                            # driver.execute_script("arguments[0].click();", contacts_elems[j])
                            if not in_db(contacts_elems[j].text, lock):
                                click_on_element(p_driver, contacts_elems[j])
                                added_db = scrappe_contact_info(p_driver, p_taskuser_id, lock)
                                if added_db:
                                    actions_done += 1
                            else:
                                logger.info(f'{contacts_elems[j].text} already scraped')

                        if actions_done >= p_quantity_actions:
                            # p_driver.quit()
                            return True, actions_done

                        j += 1

                    if i < pages - 1:
                        next_page = WebDriverWait(p_driver, 5).until(EC.presence_of_element_located((
                            By.XPATH, '//a[@id="pagination-next"]')))
                        click_on_element(p_driver, next_page)
                    else:
                        print(f'last page reached i({i + 1}) = pages({pages})')

            except Exception as ex:
                logger.info(f'Didn\'t not found any result, please verify Keyword and/or City (l:515): {ex}')

            # s_result = scrappe_yellow_pages(driver, kc, actions_done, quantity_actions, user_task_id)
            # if s_result and actions_done == quantity_actions:
            #     break
        # p_driver.quit()

    except Exception as ex:
        logger.error(f"Error while executing scrappe_yellow_pages(): {ex}")
        return False, 0

    return True, actions_done

# lock = threading.Lock()
# # Container for the contacts
# ListContacts = []
#
# p_quantity_actions = 1000
# p_browser = "Chrome"
# p_user_task_id = '274'
#
# Browse_PagesJaunes_Search_by_Keyword_City(p_browser, p_user_task_id, p_quantity_actions, lock)
