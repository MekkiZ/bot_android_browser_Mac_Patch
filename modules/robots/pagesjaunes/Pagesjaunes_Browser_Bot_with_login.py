import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodulesteam
import logging
import pdb
from random import randint


# ================================ LOGGER ====================================

open(mymodulesteam.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Pagesjaunes_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodulesteam.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =========================================================================================
# =================================== Pagesjaunes DESKTOP METHODS ============================
# =========================================================================================


def AreWePagesjaunesLoggedIn(p_driver,profile=''):
    """
    This function check if browser is connected to Pagesjaunes or not and return True with Pagesjaunes username
    or False with None
    """
    logger.info("=== [2] AreWePagesjaunesLoggedIn() ====================================")
    
    # ======================================================================
    # INITIALISATION
    Pagesjaunes_username = None

    # If we are logged in, we suppose to find the span with id =='metanav-utilisateur-connecte'
    # otherwise it means we are not connected
    try:
        span_connecte= p_driver.find_element_by_xpath("//span[@id='metanav-utilisateur-connecte']")
    except Exception as ex:
        logger.error(f"{ex} - There is no span with id='metanav-utilisateur-connecte'! That means we are not connected!")
        return False, None

    # If we execute the lines below, it means we are connnected. So let's get the username
    # === We open gere compte page
    p_driver.get("https://www.pagesjaunes.fr/utilisateur/gerer-compte")
    time.sleep(random.uniform(3, 5))

    # We get the Pseudo:
    pseudo_element = WebDriverWait(p_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//strong[@id='mes_informations_pseudo']")))
    pseudo = pseudo_element.text
    print(f"pseudo : {pseudo}")
    Pagesjaunes_username = CheckAndChangeProfile(p_driver,pseudo)
    if Pagesjaunes_username is not None:
        logger.info(f"We are connected with Pagesjaunes_username = {Pagesjaunes_username}")
        return True,Pagesjaunes_username
    else:
        logger.info(f"We are connected but our Pseudo is waiting for approval!")
        # We need to logout immediately, return false in order to let the other accounts
        PagesjaunesLogout(p_driver)
        return False, Pagesjaunes_username

def CreateNewPseudo(p_pagesjaunes_email):
    """
    This function will return the first part of email, the domain and the new username for Pagesjaunes
    :param p_pagesjaunes_email:
    :return:
    """
    first_part_email = p_pagesjaunes_email[:p_pagesjaunes_email.find('@')]
    domain = p_pagesjaunes_email[p_pagesjaunes_email.find('@') + 1:]
    print(f"{first_part_email} @ {domain}")
    # ==== Check if domain is free email provider or not
    with open(mymodulesteam.LoadFile('free_email_provider_domains.txt')) as freeemailprovider_file:
        if str(domain).lower() in freeemailprovider_file.read():
            print(f'Domain {domain} is a free email provider')
        else:
            first_part_email = domain.replace(".", "")

        # profile must be between 3 and 20 characters
    if len(first_part_email) > 20:
        print(f"'{first_part_email}' is too long!")
        # We need to make it shorter
        profile = first_part_email[:20]
        print(f"New profile is '{profile}'")
        return profile, first_part_email, domain
    if len(first_part_email) < 3:
        # We need to make it longer
        print(f"'{first_part_email}' is too short!")
        profile = first_part_email + str(randint(10000, 99999))
        print(f"New profile is '{profile}'")
        return profile, first_part_email, domain
    return first_part_email, first_part_email, domain

def CheckAndChangeProfile (p_driver,p_pseudo):

    """
    This method will check if there is the popup 'Change username' and change it automatically
    :param p_driver:
    :return:
    """
    logger.info(f"============================= CheckAndChangeProfile {p_pseudo} ===================================")
    
    # === IF pseudo is something like ProfilXXXX
    if p_pseudo.startswith("Profil") :
        # === IF it is not '(en attente)'
        try:
            p_driver.find_element_by_xpath("//span[text()='(en attente)']")
            logger.info("Find '(en attente)' in Pseudo")
            return None
        except Exception as ex:
            logger.error(f"Didn't find '(en attente)' in Pseudo")
            # We need to change the Pseudo
            # === Get the email
            pagesjaunes_email_element = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//strong[contains (text(),'@')]")))
            pagesjaunes_email = pagesjaunes_email_element[0].text
            profile,first_part_email,domain=CreateNewPseudo(pagesjaunes_email)

            # It is time to change the Pseudo
            # === We click on button 'Modifier'
            button_modifier = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'/utilisateur/modifier-mes-informations')]")))
            p_driver.execute_script("arguments[0].click();", button_modifier)
            time.sleep(random.uniform(2, 5))
            # We need to switch to iframe

            try:
                iframe_Pagesjaunes_ChangePseudo = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ("//iframe[@title='cmpLocator']"))))
                p_driver.switch_to.frame(iframe_Pagesjaunes_ChangePseudo)

                print("PhoneBot switch to iframe CHange Pseudo")
            except:
                logger.error("No Iframe_CHange Pseudo found!")
            # === Fill the field Pseudo
            field_pseudo = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@value,'Profil')]")))
            field_pseudo.send_keys(profile)
            # === Save the change
            button_modifier2 = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@id='btnValideProfil']")))
            p_driver.execute_script("arguments[0].click();", button_modifier2)
            time.sleep(random.uniform(2, 5))
            p_driver.get("https://www.pagesjaunes.fr")
            time.sleep(random.uniform(2, 5))
            return profile


def OpenGoogleAccountPopup(p_driver):

    """
    This method will:
         - click on Pagesjaunes Log In button which will open Pagesjaunes login popup
         - click on Google Sign In popup which will open Google Account Window
    :param p_driver:
    :return:
    """
    logger.info(f"================================ OpenGoogleAccountPopup ===============================")
    
    # =======================================================================   
    # Open login popup
    try:
        p_driver.get('https://www.pagesjaunes.fr/login')
        time.sleep(random.uniform(1, 2))
    except:
        logger.error("No Pagesjaunes Login page!")
        return False


    # Click on login Google button
    try:
        button_Google_login = WebDriverWait(p_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ("//div[@gigid='googleplus']"))))
        p_driver.execute_script("arguments[0].click();", button_Google_login)
        time.sleep(random.uniform(3, 4))
        print("PhoneBot clicked on Google login")
    except:
        logger.error("No Google Log_In found!")
        return False

    # Go to Google Window and collect google usernames
    try:
        print("PhoneBot click on Google Login button")
        result = p_driver.window_handles
        logger.info(result)
        p_driver.switch_to.window(result[1])
        return True
    except:
        logger.error("No Google Window found!")
        return False

def IsMultipleAccounts(p_driver):
    pdb.set_trace()
    logger.info("==== IsMultipleAccounts =====")
    try:
        # OPen Google Accounts Window
        cpt_result_google=0
        while True:
            result_google=OpenGoogleAccountPopup(p_driver)
            if result_google:
                break
            else:
                cpt_result_google+=1
                if cpt_result_google>2:
                    return None
        button_Google_accounts = p_driver.find_elements_by_xpath("//div[contains(@data-identifier,'@')]")
        List_Pagesjaunes_username = []
        for button_Google_account in button_Google_accounts:
            button_account_text_brut = button_Google_account.text
            list_button_account_text_brut = button_account_text_brut.split("\n")
            Pagesjaunes_username = list_button_account_text_brut[0]
            email = list_button_account_text_brut[1]

            logger.info(f"email : {email}")
            logger.info(f"Pagesjaunes_username : {Pagesjaunes_username}")

            List_Pagesjaunes_username.append(Pagesjaunes_username)
        return List_Pagesjaunes_username

    except Exception as ex:
        logger.info(f"ERROR IsMultipleAccounts : {ex}")
        return None

def LoopAllAccounts(p_driver,p_function,p_taskuser_id):
    logger.info(f"=== [5] LoopAllAccounts {p_taskuser_id} =======================================")
    pdb.set_trace()
    list_profiles = IsMultipleAccounts(p_driver)
    logger.info(f"list_profiles : {list_profiles}")
    if list_profiles is not None:
        for profile in list_profiles:
            logger.info(f"Loop list_profiles profile : {profile}")
            # We need to login to pickup username and check quantity of actions
            try:
                result = p_driver.window_handles
                # IF THERE IS NOT THE 2ND WINDOW GOOGLE LOGIN ACCOUNTS, WE OPEN IT
                if len(result) == 1:
                    cpt_result_google=0
                    while True:
                        result_google = OpenGoogleAccountPopup(p_driver)
                        if result_google:
                            break
                        else:
                            cpt_result_google += 1
                            if cpt_result_google > 2:
                                return None
                    result = p_driver.window_handles
                p_driver.switch_to.window(result[1])
                # === WE CLICK ON THE PROFILE GOOGLE ACCOUNT TO LOGIN
                button_Google_account = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f"//div[contains(@data-identifier,'@')]//div[contains(string(), '{profile}')]")))
                button_Google_account[0].click()
                time.sleep(random.uniform(6, 8))
                p_driver.switch_to.window(result[0])
                logger.info("PhoneBot returned back to main Window")

                # === We need to accept Terms and COnditions if there is the ifram T&Cs
                try:
                    checkbox_accept_tc = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,"//form[@id='gigya-profile-form']//input[@type='checkbox' and @name='data.subscribe']")))
                    p_driver.execute_script("arguments[0].click();", checkbox_accept_tc)
                except Exception as ex:
                    logger.error(f"No checkbox T&Cs : {ex}")
                try:
                    button_envoyer = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                           "//button[@id='BtnSeConnecter']")))
                    p_driver.execute_script("arguments[0].click();", button_envoyer)
                    time.sleep(random.uniform(3, 5))
                except Exception as ex:
                    logger.error(f"No checkbox T&Cs : {ex}")

                # === We need to fill the 2nd step of T&Cs form
                # pseudo field
                pseudo_field = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,"//input[@id='pj_user_profile_nickname']")))
                tmp_pseudo = pseudo_field.get_attribute('value')
                if len(tmp_pseudo)!=0 and tmp_pseudo.startswith('Pseudo'):
                    # === We need to build the new profile. As we don't have email, we will use the Google username and concatenate to @gmail.com
                    profile, first_part_email, domain = CreateNewPseudo(profile + '@gmail.com')
                    pseudo_field.send_keys(profile)
                    time.sleep(random.uniform(1,2))
                # city field
                city_field = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='pj_user_profile_nickname']")))
                city = pseudo_field.get_attribute('value')
                if len(city) == 0:
                    # To make it easy, if city field is empty we put Paris
                    city_field.send_keys('Paris')
                    time.sleep(random.uniform(1, 2))

                #WebDriverWait need to check if the first checkbox is checked "receive information from Pagesjaunes"
                #UnChecker The Newsletter checkbox
                checkbox_newsletter = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,"//input[@id='pj_user_profile_inscrit_newsletter']")))

                #If it is checked, we unchecked
                if str(checkbox_newsletter.get_attribute('class')).find('pjchecked') != -1:
                    p_driver.execute_script("arguments[0].click();", checkbox_newsletter)
                    time.sleep(random.uniform(0.5, 1.3))

                # Check The T&Cs
                checkbox_tc = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='pj_user_profile_inscrit_newsletter']")))
                # If it is unchecked, we check
                if str(checkbox_tc.get_attribute('class')).find('pjchecked') == -1:
                    p_driver.execute_script("arguments[0].click();", checkbox_tc)
                    time.sleep(random.uniform(0.5, 1.3))
                # === CLick on button Envoyer
                button_Envoyer = WebDriverWait(p_driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@id='btnValideProfil']")))
                p_driver.execute_script("arguments[0].click();", checkbox_tc)
                time.sleep(random.uniform(3,5))











            except Exception as ex:
                logger.error(f"ERROR Pagesjaunes when button_Google_account.click() : {ex}")
            are_we_connected_Pagesjaunes, Pagesjaunes_username = AreWePagesjaunesLoggedIn(p_driver, profile)
            # WE NEED TO CHECK IF THERE IS THE POPUP 'CHANGE USERNAME' IN CASE IT IS A NEW REGISTRATION
            logger.info(f"are_we_connected_Pagesjaunes : {are_we_connected_Pagesjaunes}")
            if are_we_connected_Pagesjaunes:
                # Let's get the quantity of actions possible
                quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Pagesjaunes_username)
                logger.info(f"quantity_actions : {quantity_actions} *****")
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    p_function(p_taskuser_id, p_driver, Pagesjaunes_username, quantity_actions)
                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {profile} logout of Pagesjaunes .")
                    PagesjaunesLogout(p_driver)
                    # ==============================================
                    # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                    # WE NEED TO MAKE A BREAK
                    time.sleep(random.uniform(6, 9))
                    logger.info("PAUSE....")
                else:
                    p_driver.get('https://pagesjaunes.fr')
                    time.sleep(random.uniform(3, 5))

    else:
        logger.info(f"Try to click on simple 'Sign in' button ")
        # A : Only ONE user with the button "Sign in / S'identifier ..."  class=sign-in-form__submit-button
        try:
            # We open Pagesjaunes log in window
            button_Log_In = p_driver.find_element_by_xpath("//a[contains(@href,'https://www.pagesjaunes.fr/login')]")
            button_Log_In.click()
            time.sleep(random.uniform(3, 5))

        except Exception as ex:
            logger.error(f"ERROR Pagesjaunes Sign in Scenario A clicking on button   : {ex}")

        try:
            # We click on sign in button
            button_Log_In = p_driver.find_element_by_xpath("//button[@type='submit' and contains(text(),'Log In')]")
            button_Log_In.click()
            time.sleep(random.uniform(3, 5))
            are_we_connected_Pagesjaunes, Pagesjaunes_username = AreWePagesjaunesLoggedIn(p_driver)
            logger.info(f"are_we_connected_Pagesjaunes : {are_we_connected_Pagesjaunes}")
            # WE NEED TO CHECK IF THERE IS THE POPUP 'CHANGE USERNAME' IN CASE IT IS A NEW REGISTRATION

            if are_we_connected_Pagesjaunes:
                # Let's get the quantity of actions possible
                quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Pagesjaunes_username)
                logger.info(f"quantity_actions : {quantity_actions} *****")
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================
                    p_function(p_taskuser_id, p_driver, Pagesjaunes_username, quantity_actions)
                    # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                    logger.info(f"Profile {Pagesjaunes_username} logout of Pagesjaunes .")
                    PagesjaunesLogout(p_driver)
                    # ==============================================
                    # IT WILL BE SUSPICIOUS TO EXECUTE ALL PROFILES IN A BATCH
                    # WE NEED TO MAKE A BREAK
                    time.sleep(random.uniform(6, 9))
                    logger.info("PAUSE....")

                else:
                    p_driver.get('https://pagesjaunes.fr')
                    time.sleep(random.uniform(3, 5))


        except:
            logger.error("PhoneBot failed to click on 'LOGIN' button!")
            return False
        # login simple

def RunPagesjaunesBrowser(p_browser, p_function, p_taskuser_id):
    logger.info(f"================================================ RunPagesjaunesBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://pagesjaunes.fr')
    driver.implicitly_wait(10)

    # ============================================================================
    # === 2 TEST IF WE ARE ALREADY LOGGED IN
    pdb.set_trace()
    are_we_connected_Pagesjaunes, Pagesjaunes_username = AreWePagesjaunesLoggedIn(driver)
    logger.info(f"are_we_connected_Pagesjaunes : {are_we_connected_Pagesjaunes}")
    logger.info(f"Pagesjaunes_username : {Pagesjaunes_username}")
    

    if are_we_connected_Pagesjaunes:
        # ============================================================================
        # ===== A - WE ARE CONNECTED
        logger.info(f"PhoneBot is logged in Pagesjaunes with profile {Pagesjaunes_username}")
        # Let's get the quantity of actions possible
        logger.info("=== [3] GetQuantityActions =======================================")
        quantity_actions = mymodulesteam.GetQuantityActions(p_taskuser_id, Pagesjaunes_username)
        if quantity_actions > 0:
            # ===================================================================================
            # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
            # ===================================================================================
            p_function(p_taskuser_id, driver, Pagesjaunes_username, quantity_actions)
            # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
            logger.info(f"Profile {Pagesjaunes_username} logout of Pagesjaunes .")
            PagesjaunesLogout(driver)
            LoopAllAccounts(driver, p_function, p_taskuser_id)
    else:
        logger.info("No Pagesjaunes user is connected!")
        LoopAllAccounts(driver,p_function,p_taskuser_id)

    return True

def PagesjaunesLogout(p_driver):
    """
    This method will logout of Pagesjaunes
    """
    logger.info("=== [4] PagesjaunesLogout() ===================")

    while True:
        try:
            # Click on Account menu
            button_menu_username = WebDriverWait(p_driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                        "//li[@id='menu_connexion']//button[@aria-controls='metanav-menu']")))
            #button_menu_username.click()
            p_driver.execute_script("arguments[0].click();", button_menu_username)
            print("Click on username menu top right corner")
            time.sleep(random.uniform(1, 2))
            # Click on Logout
            try:
                button_logout = p_driver.find_element_by_xpath("//a[text()='Se déconnecter']")
                #button_logout.click()
                p_driver.execute_script("arguments[0].click();", button_logout)
                time.sleep(random.uniform(3, 5))
                break
            except Exception as ex:
                logger.error(f"ERROR Pagesjaunes didn't find Logout button' : {ex}")
        except Exception as ex:
            logger.error(f"ERROR Pagesjaunes clicking on top right menu : {ex}")

def Scraping_Pages_Jaunes_Search_by_keywords_city_28(p_taskuser_id,p_driver,Pagesjaunes_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Influencers_Pagesjaunes_Group_Admins_15 {p_taskuser_id} - {Pagesjaunes_username} - {p_quantity_actions} =======================")
    mymodulesteam.PopupMessage("ACTIONS", f"Pagesjaunes user {Pagesjaunes_username} can make {p_quantity_actions} actions now!")

    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodulesteam.GetDetailsTaskUser(p_taskuser_id)