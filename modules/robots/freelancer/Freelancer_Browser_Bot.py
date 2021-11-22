# -*- coding: utf-8 -*-
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam
import logging
import pdb


# ================================ LOGGER ====================================
from . import Browser_Freelancer_reply

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Freelancer_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# =========================================================================================
# =================================== Freelancer DESKTOP METHODS ============================
# =========================================================================================


def IsMultipleAccounts_A(p_driver):
    logger.info("=============== IsMultipleAccounts_A =======================")

    Google_iframes = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, ("//iframe"))))
    logger.info(f"len(Google_iframes) : {len(Google_iframes)}")
    for Google_iframe in Google_iframes:
        try:
            sandbox = Google_iframe.get_attribute('sandbox')
        except Exception as ex:
            sandbox = None
            logger.info(f"Error {ex}")
        if sandbox:
            logger.info("It is not this Google_iframe")
        else:

            try:
                p_driver.switch_to.frame(Google_iframe)
                logger.info("Phonebot has switched to frame")
                button_more_account = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ("//div[@id='show-more-accounts']"))))
                # logger.info(f"Javascript click on {button_more_account}")
                # p_driver.execute_script("arguments[0].click();", button_more_account)
                button_more_account.click()

                # DISPLAY LIST OF GOOGLE ACCOUNTS ========================================================
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(1, 2))
                # Try to get list of Google accounts
                List_Freelancer_username = []
                try:
                    buttons_account = WebDriverWait(p_driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.XPATH, "//div[@id='credentials-picker']//div[contains(@aria-labelledby,'picker')]")))

                    for button_account in buttons_account:
                        button_account_text_brut = button_account.text
                        # Extract email and name
                        # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
                        # match = re.search(r'[\w\.-]+@[\w\.-]+', button_account_text_brut)
                        # email= match.group(0)
                        # Freelancer_username = str(button_account_text_brut.replace(email,'')).strip()
                        list_button_account_text_brut = button_account_text_brut.split("\n")
                        Freelancer_username = list_button_account_text_brut[0]
                        email = list_button_account_text_brut[1]
                        logger.info(f"email : {email}")
                        logger.info(f"Freelancer_username : {Freelancer_username}")
                        List_Freelancer_username.append(Freelancer_username)

                    p_driver.get("https://freelancer.com")
                    time.sleep(random.uniform(3, 5))
                    return List_Freelancer_username

                except Exception as ex:
                    logger.info(f"ERROR ClickOnMoreAccounts button_account in buttons_account : {ex}")
                    logger.info(" *** switch_to_default_content ***")
                    p_driver.switch_to_default_content()
                    return None


            except Exception as ex:
                logger.info(f"ERROR ClickOnMoreAccounts : {ex}")
                logger.info(" *** switch_to_default_content ***")
                p_driver.switch_to_default_content()
                return None


def AreWeFreelancerLoggedIn(p_driver):
    """
    This function check if browser is connected to Freelancer or not and return True with Freelancer username
    or False with None
    """
    logger.info("=== [2] AreWeFreelancerLoggedIn() ====================================")

    # INITIALISATION
    Freelancer_username = None

    cpt = 0
    while True:
        try:
            Freelancer_username_element = WebDriverWait(p_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-control-name='identity_welcome_message']")))
            Freelancer_username_brut = Freelancer_username_element.text
            logger.info(f"Freelancer_username_brut : {Freelancer_username_brut}")
            # We need to make some transformation because Freelancer_username_brut is returning "Name\nYour profile"

            Freelancer_username = Freelancer_username_brut
            return True, Freelancer_username
        except Exception as ex:
            p_driver.switch_to.default_content()
            print("Switch to default content")
            cpt += 1
            if cpt > 2:
                logger.error(f"ERROR Freelancer getting username : {ex}")
                return False, Freelancer_username


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
        List_Freelancer_username = []
        for button_Google_account in button_Google_accounts:
            button_account_text_brut = button_Google_account.text
            list_button_account_text_brut = button_account_text_brut.split("\n")
            Freelancer_username = list_button_account_text_brut[0]
            email = list_button_account_text_brut[1]

            logger.info(f"email : {email}")
            logger.info(f"Freelancer_username : {Freelancer_username}")

            List_Freelancer_username.append(Freelancer_username)
        return List_Freelancer_username

    except Exception as ex:
        logger.info(f"ERROR IsMultipleAccounts_B : {ex}")
        return None


def LoopAllAccounts(p_driver, p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(f"=== [5] LoopAllAccounts {p_taskuser_id} =======================================")

    list_profiles_A = IsMultipleAccounts_A(p_driver)
    logger.info(f"list_profiles_A : {list_profiles_A}")

    if list_profiles_A is not None:
        for profile in list_profiles_A:
            logger.info(f"Loop list_profiles_A profile : {profile}")

            # Let's get the quantity of actions possible
            quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, profile)
            if quantity_actions > 0:
                # LET'S GET THE IFRAMES TO FIND THE GOOGLE LOGIN ACCOUNTS IFRAME
                while True:
                    try:

                        Google_iframes = WebDriverWait(p_driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, ("//iframe"))))
                        print(f"len(Google_iframes): {len(Google_iframes)}")
                        if len(Google_iframes) == 0 or Google_iframes is None:
                            logger.error("No iframes found!")
                            # Let's go back to default frame
                            try:
                                p_driver.switch_to.default_content()
                                print("Switch to default content)")
                                time.sleep(random.uniform(0.5, 1))
                            except Exception as ex:
                                logger.error("Impossible to find iframes and click on more button!")
                                p_driver.get("https://freelancer.com")
                                time.sleep(random.uniform(3, 5))
                        else:
                            break

                    except Exception as ex:
                        logger.error("Impossible to find iframes and click on more button!")
                        p_driver.get("https://freelancer.com")
                        time.sleep(random.uniform(3, 5))

                # LET'S GO TO THE IFRAME GOOGLE LOGIN POPUP
                for Google_iframe in Google_iframes:
                    try:
                        sandbox = Google_iframe.get_attribute('sandbox')
                    except Exception as ex:
                        sandbox = None
                        logger.info(f"Error {ex}")
                    if sandbox:
                        logger.info("It is not this Google_iframe")
                    else:
                        # HERE IS THE POPUP

                        p_driver.switch_to.frame(Google_iframe)
                        logger.info("Phonebot has switched to frame")

                        try:

                            button_more_account = WebDriverWait(p_driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, ("//div[@id='show-more-accounts']"))))
                            # logger.info(f"Javascript click on {button_more_account}")
                            # p_driver.execute_script("arguments[0].click();", button_more_account)
                            button_more_account.click()
                        except Exception as ex:
                            logger.error(f"ERROR Freelancer click on 'more ...' button : {ex}")
                        # DISPLAY LIST OF GOOGLE ACCOUNTS ========================================================
                        p_driver.implicitly_wait(10)
                        time.sleep(random.uniform(1, 2))
                        try:
                            buttons_account = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located(
                                (By.XPATH,
                                 f"//div[@id='credentials-picker']//div[contains(@aria-labelledby,'picker')]//div[contains(string(), '{profile}')]")))
                            buttons_account[0].click()
                            time.sleep(random.uniform(3, 5))
                        except Exception as ex:
                            logger.error(f"ERROR Freelancer when try to get Google Sign in + Login Popup : {ex}")
                        try:
                            button_continue = WebDriverWait(p_driver, 10).until(EC.element_to_be_clickable(
                                (By.ID, "continue-as")))
                            button_continue.click()
                            time.sleep(random.uniform(3, 5))
                        except Exception as ex:
                            logger.error(
                                f"ERROR Freelancer wPhoneBot couldn't click on 'continue' button. It carries on!' : {ex}")
                        try:
                            are_we_connected_Freelancer, Freelancer_username = AreWeFreelancerLoggedIn(p_driver)
                            if are_we_connected_Freelancer:
                                # ===================================================================================
                                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                                # ===================================================================================
                                result, counter = p_function(p_browser, p_taskuser_id, p_driver, profile, quantity_actions, label_log,
                                           lock)
                                # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                                logger.info(f"Profile {profile} logout of Freelancer .")
                                FreelancerLogout(p_driver)
                                # ==============================================
                                # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                                # WE NEED TO MAKE A BREAK
                                time.sleep(random.uniform(6, 9))
                                logger.info("PAUSE....")

                                break
                            else:
                                p_driver.get("https://freelancer.com")
                                time.sleep(random.uniform(3, 5))
                                break
                        except Exception as ex:
                            logger.error(f"ERROR Freelancer when buttons_account[0].click() : {ex}")
    else:
        list_profiles_B = IsMultipleAccounts_B(p_driver)
        logger.info(f"list_profiles_B : {list_profiles_B}")
        if list_profiles_B is not None:
            for profile in list_profiles_B:

                logger.info(f"Loop list_profiles_B profile : {profile}")

                # Let's get the quantity of actions possible
                quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, profile)
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
                        are_we_connected_Freelancer, Freelancer_username = AreWeFreelancerLoggedIn(p_driver)
                        logger.info(f"are_we_connected_Freelancer : {are_we_connected_Freelancer}")
                        if are_we_connected_Freelancer:
                            # ===================================================================================
                            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                            # ===================================================================================
                            result, counter = p_function(p_browser, p_taskuser_id, p_driver, profile, quantity_actions)

                            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                            logger.info(f"Profile {profile} logout of Freelancer .")
                            FreelancerLogout(p_driver)
                            # ==============================================
                            # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                            # WE NEED TO MAKE A BREAK
                            time.sleep(random.uniform(6, 9))
                            logger.info("PAUSE....")



                        else:
                            p_driver.get('https://freelancer.com')
                            time.sleep(random.uniform(3, 5))

                    except Exception as ex:
                        logger.error(f"ERROR Freelancer when button_Google_account.click() : {ex}")
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
                logger.error(f"ERROR Freelancer Sign in Scenario A clicking on button   : {ex}")
            # login simple

            # WE NEED FIRST TO CHECK IF WE ARE LOGGED IN
            # THEN WE EXECUTE THE TASK

            are_we_connected_Freelancer, Freelancer_username = AreWeFreelancerLoggedIn(p_driver)
            logger.info(f"are_we_connected_Freelancer : {are_we_connected_Freelancer}")
            if are_we_connected_Freelancer:
                # Let's get the quantity of actions possible
                quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Freelancer_username)
                logger.info(f"quantity_actions : {quantity_actions} *****")

                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    result, counter = p_function(p_browser, p_taskuser_id, p_driver, Freelancer_username, quantity_actions)

                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {Freelancer_username} logout of Freelancer .")
                    FreelancerLogout(p_driver)

    return result, counter

def RunFreelancerBrowser(p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(
        f"================================================ RunFreelancerBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://freelancer.com')
    driver.implicitly_wait(10)

    # ======================= We need to accept Cookies popup =================================
    # try:
    #     button_Accepter_Fermer =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='didomi-notice-agree-button']")))
    #     driver.execute_script("arguments[0].click();", button_Accepter_Fermer)
    # except Exception as ex:
    #     logger.error("Phonebot didn't see any 'Cookies popup'! We carry on the job!")

    Freelancer_username = "Desktop"
    # Let's get the quantity of actions possible
    logger.info("=== [3] GetQuantityActions =======================================")
    quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Freelancer_username)
    if quantity_actions > 0:
        # ===================================================================================
        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
        # ===================================================================================
        result, counter = p_function(p_browser, p_taskuser_id, driver, Freelancer_username, quantity_actions, label_log, lock)
        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
        logger.info(f"Profile {Freelancer_username} logout of Pagesjaunes .")
        return result, counter
    else:
        logger.info(
            f"Profile {Freelancer_username} couldn't execute task because quantity_actions doesn't allow' => {quantity_actions}' .")

        return False,0


def RunFreelancerBrowser_NOT_FUNCTIONNAL(p_browser, p_function, p_taskuser_id, label_log, lock):
    logger.info(
        f"================================================ RunFreelancerBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://www.freelancer.com')
    driver.implicitly_wait(10)

    # ============================================================================

    # # Delete this lines
    # quantity_actions = 15
    # user= ""
    # p_function(p_browser, p_taskuser_id, driver, user, quantity_actions, label_log, lock)
    # # Delete this lines

    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    are_we_connected_Freelancer, Freelancer_username = AreWeFreelancerLoggedIn(driver)
    logger.info(f"are_we_connected_Freelancer : {are_we_connected_Freelancer}")
    logger.info(f"Freelancer_username : {Freelancer_username}")
    if Freelancer_username == "":
        logger.info(f"ERROR Freelancer_username is empty!!!")

    if are_we_connected_Freelancer:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Freelancer with profile {Freelancer_username}")

        # Let's get the quantity of actions possible
        logger.info("=== [3] GetQuantityActions =======================================")
        quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Freelancer_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            result, counter = p_function(p_taskuser_id, driver, Freelancer_username, quantity_actions)

            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {Freelancer_username} logout of Freelancer .")
            FreelancerLogout(driver)
            result, counter = LoopAllAccounts(driver, p_browser, p_function, p_taskuser_id, label_log, lock)
    else:
        logger.info("No Freelancer user is connected!")

        result, counter = LoopAllAccounts(driver, p_browser, p_function, p_taskuser_id, label_log, lock)

    return result, counter


def FreelancerLogout(p_driver):
    """
    This method will logout of Freelancer
    """
    logger.info("=== [4] FreelancerLogout() ===================")

    while True:
        try:
            # Click on Account menu
            button_menu = WebDriverWait(p_driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='nav.settings']")))
            button_menu.click()
            print("Click on menu settings link!")

            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            # Click on Logout
            try:

                button_logout = WebDriverWait(p_driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'logout')]")))
                button_logout.click()
                print("Click on logout link!")
                # When we logout, we need to come back to home page to be sure to have button list of accounts
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(1, 2))
                p_driver.get('https://freelancer.com')
                p_driver.implicitly_wait(10)
                time.sleep(random.uniform(1, 2))
                break

            except Exception as ex:
                logger.error(f"ERROR Freelancer when clicking on Logout Link in top right menu : {ex}")



        except Exception as ex:
            logger.error(f"ERROR Freelancer clicking on top right menu : {ex}")


def Freelancer_Freelancer_reply_52(p_browser, p_taskuser_id, p_driver, Freelancer_username, p_quantity_actions,
                                   label_log, lock):
    logger.info(
        f"=================== Freelancer_Freelancer_reply_52 {p_taskuser_id} - {Freelancer_username} - {p_quantity_actions} =======================")

    result, counter =Browser_Freelancer_reply(p_browser, p_taskuser_id, p_driver, Freelancer_username, p_quantity_actions, label_log,
                                lock)
    mymodulesteam.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Freelancer_Freelancer_reply_52",
                                      "Black")


    return result, counter


