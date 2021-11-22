# -*- coding: utf-8 -*-
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules
import logging
import pdb
from modules import mymodulesteam
from . import Browser_Linkedin_scraping_likers_commenters, Browser_Linkedin_send_message_likers_commenters, \
    Browser_Linkedin_like_random, Browser_Linkedin_comment_some_posts, Browser_Linkedin_scraping_search_result, \
    Browser_Linkedin_scraping_group_members, Browser_Linkedin_send_message_Search_By_Keywords_City

# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Linkedin_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# =========================================================================================
# =================================== Linkedin DESKTOP METHODS ============================
# =========================================================================================
def random_sleep():
    """
        Random time.sleep for having different sleep times.
    """
    ts = random.uniform(1, 5)
    ts = round(ts, 2)
    print(f"Sleep time: {ts}")
    time.sleep(ts)

def IsMultipleAccounts_A(p_driver):
    logger.info("=============== IsMultipleAccounts_A =======================")

    try:
        google_iframe = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ("//div[@id='credential_picker_container']/iframe"))))
        p_driver.switch_to.frame(google_iframe)
        random_sleep()
        logger.info("Phonebot has switched to frame")
        List_Linkedin_username = []

        # accounts = p_driver.find_elements_by_xpath("//div[@id='credentials-picker']/div")
        # # click on more accounts
        # if len(accounts) >= 3:
        #     try:
        #         buttons_more_account = p_driver.find_elements_by_id("show-more-accounts")
        #         type(buttons_more_account)
        #         random_sleep()
        #     except Exception as ex:
        #         logger.info(f"ERROR click on button show-more-accounts : {ex}")
        #         return None

        accounts = p_driver.find_elements_by_xpath("//div[@id='credentials-picker']//div[contains(@aria-labelledby,'picker')]/div[1]/div[3]/div[1]")
        for account in accounts:
            Linkedin_username = account.text
            List_Linkedin_username.append(Linkedin_username)

        return List_Linkedin_username

    except Exception as ex:
        logger.info(f"ERROR IsMultipleAccounts_A : {ex}")
        return None
    finally:
        logger.info(" *** switch_to_default_content ***")
        p_driver.switch_to.default_content()

    # Google_iframes = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//iframe"))))
    # logger.info(f"len(Google_iframes) : {len(Google_iframes)}")
    # for Google_iframe in Google_iframes:
    #     try:
    #         sandbox = Google_iframe.get_attribute('sandbox')
    #     except Exception as ex:
    #         sandbox = None
    #         logger.info(f"Error {ex}")
    #     if sandbox:
    #         logger.info("It is not this Google_iframe")
    #     else:
    #
    #         try:
    #             p_driver.switch_to.frame(Google_iframe)
    #             logger.info("Phonebot has switched to frame")
    #             button_more_account = WebDriverWait(p_driver, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, ("//div[@id='show-more-accounts']"))))
    #             # logger.info(f"Javascript click on {button_more_account}")
    #             # p_driver.execute_script("arguments[0].click();", button_more_account)
    #             button_more_account.click()
    #
    #             # DISPLAY LIST OF GOOGLE ACCOUNTS ========================================================
    #             p_driver.implicitly_wait(10)
    #             time.sleep(random.uniform(1, 2))
    #             # Try to get list of Google accounts
    #             List_Linkedin_username = []
    #             try:
    #                 buttons_account = WebDriverWait(p_driver, 10).until(
    #                     EC.presence_of_all_elements_located(
    #                         (
    #                             By.XPATH, "//div[@id='credentials-picker']//div[contains(@aria-labelledby,'picker')]")))
    #
    #                 for button_account in buttons_account:
    #                     button_account_text_brut = button_account.text
    #                     # Extract email and name
    #                     # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    #                     # match = re.search(r'[\w\.-]+@[\w\.-]+', button_account_text_brut)
    #                     # email= match.group(0)
    #                     # Linkedin_username = str(button_account_text_brut.replace(email,'')).strip()
    #                     list_button_account_text_brut = button_account_text_brut.split("\n")
    #                     Linkedin_username = list_button_account_text_brut[0]
    #                     email = list_button_account_text_brut[1]
    #                     logger.info(f"email : {email}")
    #                     logger.info(f"Linkedin_username : {Linkedin_username}")
    #                     List_Linkedin_username.append(Linkedin_username)
    #
    #                 p_driver.get("https://linkedin.com")
    #                 time.sleep(random.uniform(3, 5))
    #                 return List_Linkedin_username
    #
    #             except Exception as ex:
    #                 logger.info(f"ERROR ClickOnMoreAccounts button_account in buttons_account : {ex}")
    #                 logger.info(" *** switch_to_default_content ***")
    #                 p_driver.switch_to_default_content()
    #                 return None
    #
    #
    #         except Exception as ex:
    #             logger.info(f"ERROR ClickOnMoreAccounts : {ex}")
    #             logger.info(" *** switch_to_default_content ***")
    #             p_driver.switch_to_default_content()
    #             return None


def AreWeLinkedinLoggedIn(p_driver):
    """
    This function check if browser is connected to Linkedin or not and return True with Linkedin username
    or False with None
    """
    logger.info("=== [2] AreWeLinkedinLoggedIn() ====================================")

    # INITIALISATION
    Linkedin_username = None

    try:
        p_driver.get("https://www.linkedin.com/in/")
        random_sleep()
        # we get the new url of page
        url = p_driver.execute_script("return window.location.href;")
        logger.info(f"The new url of page is {url}")
        url_list = url.split("/")
        logger.info(f"Linkedin_username_url is : {url_list}")
        if url_list[4] and url_list[4][0] != "?":
            # get username from url
            Linkedin_username = url_list[4]
            return True, Linkedin_username
        else:
            return False, Linkedin_username

    except Exception as ex:
        logger.error(f"ERROR Linkedin getting username : {ex}")
        return False, Linkedin_username
    finally:
        random_sleep()
        p_driver.get("https://www.linkedin.com/")
        random_sleep()


    # cpt = 0
    # while True:
    #     try:
    #         Linkedin_username_element = WebDriverWait(p_driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, "//div[@data-control-name='identity_welcome_message']")))
    #         Linkedin_username_brut = Linkedin_username_element.text
    #         logger.info(f"Linkedin_username_brut : {Linkedin_username_brut}")
    #         # We need to make some transformation because Linkedin_username_brut is returning "Name\nYour profile"
    #
    #         Linkedin_username = Linkedin_username_brut
    #         return True, Linkedin_username
    #     except Exception as ex:
    #         p_driver.switch_to.default_content()
    #         print("Switch to default content")
    #         cpt += 1
    #         if cpt > 2:
    #             logger.error(f"ERROR Linkedin getting username : {ex}")
    #             return False, Linkedin_username


def IsMultipleAccounts_B(p_driver):
    try:

        logger.info("==== IsMultipleAccounts_B =====")
        button_Google_login = p_driver.find_element_by_xpath("//button[contains(@class, 'google-sign-in')]")
        button_Google_login.click()
        time.sleep(random.uniform(3, 5))
        result = p_driver.window_handles
        logger.info(result)

        p_driver.switch_to.window(result[1])

        button_Google_accounts = p_driver.find_elements_by_xpath("//div[contains(@data-identifier,'@')]")
        List_Linkedin_username = []
        for button_Google_account in button_Google_accounts:
            button_account_text_brut = button_Google_account.text
            list_button_account_text_brut = button_account_text_brut.split("\n")
            Linkedin_username = list_button_account_text_brut[0]
            email = list_button_account_text_brut[1]

            logger.info(f"email : {email}")
            logger.info(f"Linkedin_username : {Linkedin_username}")

            List_Linkedin_username.append(Linkedin_username)
        return List_Linkedin_username

    except Exception as ex:
        logger.info(f"ERROR IsMultipleAccounts_B : {ex}")
        return None


def LoopAllAccounts(p_driver, p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(f"=== [5] LoopAllAccounts {p_taskuser_id} =======================================")
    list_profiles_A = IsMultipleAccounts_A(p_driver)
    logger.info(f"list_profiles_A : {list_profiles_A}")

    if list_profiles_A is not None:
        for profile in list_profiles_A:
            # logger.info(f"Loop list_profiles_A profile : {profile}")

            # Let's get the quantity of actions possible
            quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, profile)
            if quantity_actions > 0:
                try:
                    google_iframe = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ("//div[@id='credential_picker_container']/iframe"))))
                    p_driver.switch_to.frame(google_iframe)
                    logger.info("Phonebot has switched to frame")
                    account = p_driver.find_element_by_xpath(f"//div[@id='credentials-picker']//div[contains(@aria-labelledby,'picker')]//div[contains(string(), '{profile}')]")
                    account.click()
                    time.sleep(12)
                    try:
                        are_we_connected_Linkedin, Linkedin_username = AreWeLinkedinLoggedIn(p_driver)
                        if are_we_connected_Linkedin:
                            # ===================================================================================
                            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                            # ===================================================================================
                            result, counter = p_function(p_browser, p_taskuser_id, p_driver, profile,
                                                         quantity_actions, label_log, lock)
                            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                            logger.info(f"Profile {profile} logout of Linkedin .")
                            LinkedinLogout(p_driver)
                            # ==============================================
                            # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                            # WE NEED TO MAKE A BREAK
                            time.sleep(random.uniform(6, 9))
                            logger.info("PAUSE....")

                            break
                        else:
                            p_driver.get("https://linkedin.com")
                            time.sleep(random.uniform(3, 5))
                            break
                    except Exception as ex:
                        logger.error(f"ERROR Couldn't run th task: {ex}")
                except Exception as ex:
                    logger.error(f"ERROR Linkedin when buttons_account[0].click() : {ex}")


    else:
        list_profiles_B = IsMultipleAccounts_B(p_driver)
        logger.info(f"list_profiles_B : {list_profiles_B}")
        if list_profiles_B is not None:
            for profile in list_profiles_B:

                logger.info(f"Loop list_profiles_B profile : {profile}")

                # Let's get the quantity of actions possible
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, profile)
                logger.info(f"quantity_actions : {quantity_actions} *****")

                if quantity_actions > 0:
                    result = p_driver.window_handles
                    # IF THERE IS NOT THE 2ND WINDOW GOOGLE LOGIN ACCOUNTS, WE CLICK ON SIGN IN GOOGLE BUTTON
                    if len(result) == 1:
                        button_Google_login = p_driver.find_element_by_xpath(
                            "//button[contains(@class, 'google-sign-in')]")
                        button_Google_login.click()
                        time.sleep(random.uniform(3, 5))
                        result = p_driver.window_handles
                        logger.info(result)

                    try:
                        p_driver.switch_to.window(result[1])
                        button_Google_account = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH,
                                                                 f"//div[contains(@data-identifier,'@')]//div[contains(string(), '{profile}')]")))
                        button_Google_account[0].click()

                        p_driver.switch_to.window(result[0])
                        logger.info("PhoneBot returned back to main Window")
                        are_we_connected_Linkedin, Linkedin_username = AreWeLinkedinLoggedIn(p_driver)
                        logger.info(f"are_we_connected_Linkedin : {are_we_connected_Linkedin}")
                        if are_we_connected_Linkedin:
                            # ===================================================================================
                            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                            # ===================================================================================
                            result, counter = p_function(p_browser, p_taskuser_id, p_driver, profile, quantity_actions)

                            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                            logger.info(f"Profile {profile} logout of Linkedin .")
                            LinkedinLogout(p_driver)
                            # ==============================================
                            # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                            # WE NEED TO MAKE A BREAK
                            time.sleep(random.uniform(6, 9))
                            logger.info("PAUSE....")



                        else:
                            p_driver.get('https://linkedin.com')
                            time.sleep(random.uniform(3, 5))


                    except Exception as ex:
                        logger.error(f"ERROR Linkedin when button_Google_account.click() : {ex}")




        else:
            logger.info(f"Try to click on simple 'Sign in' button ")

            # A : Only ONE user with the button "Sign in / S'identifier ..."  class=sign-in-form__submit-button
            try:
                button_sign_in = WebDriverWait(p_driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "sign-in-form__submit-button")))
                button_sign_in.click()
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(3, 5))


            except Exception as ex:
                logger.error(f"ERROR Linkedin Sign in Scenario A clicking on button   : {ex}")
            # login simple

            # WE NEED FIRST TO CHECK IF WE ARE LOGGED IN
            # THEN WE EXECUTE THE TASK

            are_we_connected_Linkedin, Linkedin_username = AreWeLinkedinLoggedIn(p_driver)
            logger.info(f"are_we_connected_Linkedin : {are_we_connected_Linkedin}")
            if are_we_connected_Linkedin:
                # Let's get the quantity of actions possible
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Linkedin_username)
                logger.info(f"quantity_actions : {quantity_actions} *****")

                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    result, counter = p_function(p_browser, p_taskuser_id, p_driver, Linkedin_username,
                                                 quantity_actions)

                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {Linkedin_username} logout of Linkedin .")
                    LinkedinLogout(p_driver)

    return result, counter


def RunLinkedinBrowser(p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(
        f"================================================ RunLinkedinBrowser {p_taskuser_id} ===================================================")

    """
        This method will open browser and run the task for all the profiles found in cookies Browser
        It will have to check for the daily & hourly limit
        It will return True if it run some actions, or False if nothing
        :param p_function:
        :param p_taskuser_id:
        :return:
    """
    # ============================================================================
    # === 1 OPEN BROWSER =========================================================
    logger.info("=== [1] Open Browser =======================================")
    if p_browser == "Chrome":
        driver = mymodulesteam.ChromeDriverWithProfile()
    elif p_browser == "Firefox":
        driver = mymodulesteam.FireFoxDriverWithProfile()
    else:
        logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
        return False
    driver.get(
        'https://www.linkedin.com')
    driver.implicitly_wait(10)

    # ============================================================================
    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_Linkedin, Linkedin_username = AreWeLinkedinLoggedIn(driver)
    logger.info(f"are_we_connected_Linkedin : {are_we_connected_Linkedin}")
    logger.info(f"Linkedin_username : {Linkedin_username}")
    if Linkedin_username == "":
        logger.info(f"ERROR Linkedin_username is empty!!!")

    if are_we_connected_Linkedin:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Linkedin with profile {Linkedin_username}")

        # Let's get the quantity of actions possible
        logger.info("=== [3] GetQuantityActions =======================================")
        quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Linkedin_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter = p_function(p_browser, p_taskuser_id, Linkedin_username, driver, quantity_actions, label_log, lock)

            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {Linkedin_username} logout of Linkedin .")
            LinkedinLogout(driver)
            result, counter = LoopAllAccounts(driver, p_browser, p_function, p_taskuser_id, label_log, lock)
    else:
        logger.info("No Linkedin user is connected!")

        result, counter = LoopAllAccounts(driver, p_browser, p_function, p_taskuser_id, label_log, lock)

    return result, counter


def LinkedinLogout(p_driver):
    """
    This method will logout of Linkedin
    """
    logger.info("=== [4] LinkedinLogout() ===================")

    # logout from account with logout url
    p_driver.get("https://www.linkedin.com/m/logout/")

    # while True:
    #     try:
    #         # Click on Account menu
    #         button_menu = WebDriverWait(p_driver, 15).until(
    #             EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='nav.settings']")))
    #         button_menu.click()
    #         print("Click on menu settings link!")
    #
    #         p_driver.implicitly_wait(10)
    #         time.sleep(random.uniform(1, 2))
    #         # Click on Logout
    #         try:
    #
    #             button_logout = WebDriverWait(p_driver, 15).until(
    #                 EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'logout')]")))
    #             button_logout.click()
    #             print("Click on logout link!")
    #             # When we logout, we need to come back to home page to be sure to have button list of accounts
    #             p_driver.implicitly_wait(10)
    #             time.sleep(random.uniform(1, 2))
    #             p_driver.get('https://linkedin.com')
    #             p_driver.implicitly_wait(10)
    #             time.sleep(random.uniform(1, 2))
    #             break
    #
    #         except Exception as ex:
    #             logger.error(f"ERROR Linkedin when clicking on Logout Link in top right menu : {ex}")
    #
    #
    #
    #     except Exception as ex:
    #         logger.error(f"ERROR Linkedin clicking on top right menu : {ex}")


def Scraping_Linkedin_Group_Members_32(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions,
                                       label_log, lock):
    logger.info(
        f"=================== Scraping_Linkedin_Group_Members_32 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS",
                           f"Linkedin user {Linkedin_username} can make {p_quantity_actions} actions now of Scraping_Linkedin_Group_Members_32!")

    result, counter = Browser_Linkedin_scraping_group_members.Browser_Scraping_Linkedin_Group_Members_32(p_browser,
                                                                                                         p_taskuser_id,
                                                                                                         Linkedin_username,
                                                                                                         p_driver,
                                                                                                         p_quantity_actions,
                                                                                                         label_log,
                                                                                                         lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Linkedin_Group_Members_32",
                                  "Black")
    return result, counter


def Scraping_Linkedin_Search_by_keywords_city_31(p_browser, p_taskuser_id, p_driver, Linkedin_username,
                                                 p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Scraping_Linkedin_Search_by_keywords_city_31 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS",
                           f"Linkedin user {Linkedin_username} can make {p_quantity_actions} actions now of Scraping_Linkedin_Search_by_keywords_city_31!")

    result, counter = Browser_Linkedin_scraping_search_result.Linkedin_Search_By_Keywords_And_City(p_browser,
                                                                                                   p_taskuser_id,
                                                                                                   Linkedin_username,
                                                                                                   p_driver,
                                                                                                   p_quantity_actions,
                                                                                                   label_log,
                                                                                                   lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Scraping_Linkedin_Search_by_keywords_city_31",
                                  "Black")
    return result, counter


def Influencers_Linkedin_Page_Admins_17(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions,
                                        label_log, lock):
    logger.info(
        f"=================== Influencers_Linkedin_Page_Admins_17 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    # THIS TASK WAS NOT DONE !!!!
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Linkedin_Page_Admins_17",
                                  "Black")


def Influencers_Linkedin_Group_Admins_6(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions,
                                        label_log, lock):
    logger.info(
        f"=================== Influencers_Linkedin_Group_Admins_6 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    # THIS TASK WAS NOT DONE !!!!
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Linkedin_Group_Admins_6",
                                  "Black")


def Cold_Messaging_Linkedin_Search_by_keywords_city_8(p_browser, p_taskuser_id, p_driver, Linkedin_username,
                                                      p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Cold_Messaging_Linkedin_Search_by_keywords_city_8 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    # THIS TASK WAS NOT DONE !!!!
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Linkedin_Search_by_keywords_city_8",
                                  "Black")

    result, counter = Browser_Linkedin_send_message_Search_By_Keywords_City.Linkedin_Search_By_Keywords_And_City(
        p_browser,
        p_taskuser_id,
        Linkedin_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Linkedin_Search_by_keywords_city_8",
                                  "Black")
    return result, counter


def Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7(p_browser, p_taskuser_id, p_driver, Linkedin_username,
                                                         p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Linkedin_send_message_likers_commenters.ColdMsgLinkedinLikersPostCommenters(p_browser,
                                                                                                          p_taskuser_id,
                                                                                                          Linkedin_username,
                                                                                                          p_driver,
                                                                                                          p_quantity_actions,
                                                                                                          label_log,
                                                                                                          lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7",
                                  "Black")
    return result, counter


def Browser_Linkedin_scraping_likers_commenters_61(p_browser, p_taskuser_id, p_driver, Linkedin_username,
                                                   p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Browser_Linkedin_scraping_likers_commenters_61 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS",
                           f"Linkedin user {Linkedin_username} can make {p_quantity_actions} actions now of Browser_Linkedin_scraping_likers_commenters_61!")

    result, counter = Browser_Linkedin_scraping_likers_commenters.ScrapPosts(p_browser,
                                                                             p_taskuser_id,
                                                                             Linkedin_username,
                                                                             p_driver,
                                                                             p_quantity_actions,
                                                                             label_log,
                                                                             lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Browser_Linkedin_scraping_likers_commenters_61",
                                  "Black")
    return result, counter


def Browser_Linkedin_like_random_47(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions,
                                    label_log, lock):
    logger.info(
        f"=================== Browser_Linkedin_like_random_47 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS",
                           f"Linkedin user {Linkedin_username} can make {p_quantity_actions} actions now of Browser_Linkedin_like_random_47!")

    result, counter = Browser_Linkedin_like_random.like_posts(p_browser,
                                                              p_taskuser_id,
                                                              Linkedin_username,
                                                              p_driver,
                                                              p_quantity_actions,
                                                              label_log,
                                                              lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Browser_Linkedin_like_random_47",
                                  "Black")
    return result, counter


def Authority_Linkedin_comment_posts_54(p_browser, p_taskuser_id, p_driver, Linkedin_username, p_quantity_actions,
                                           label_log, lock):
    logger.info(
        f"=================== Browser_Linkedin_comment_some_posts_54 {p_taskuser_id} - {Linkedin_username} - {p_quantity_actions} =======================")
    mymodules.PopupMessage("ACTIONS",
                           f"Linkedin user {Linkedin_username} can make {p_quantity_actions} actions now of Browser_Linkedin_comment_some_posts_54!")

    result, counter = Browser_Linkedin_comment_some_posts.Browser_Comment_Linkedin_Posts(p_browser,
                                                                                         p_taskuser_id,
                                                                                         Linkedin_username,
                                                                                         p_driver,
                                                                                         p_quantity_actions,
                                                                                         label_log,
                                                                                         lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Browser_Linkedin_comment_some_posts_54",
                                  "Black")
    return result, counter