# -*- coding: utf-8 -*-
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from modules import mymodules
from modules import mymodules

import logging
from . import Browser_Facebook_like_random, Browser_Facebook_share_posts_in_groups, \
    Browser_Facebook_add_friend_group_member, \
    Browser_Facebook_send_message_group_admins, Browser_Facebook_send_message_group_members, \
    Browser_Facebook_send_message_likers_commenters, Browser_Facebook_scrape_group_members, \
    Browser_Facebook_comment_some_posts, Browser_Facebook_send_message_Page_Admins

# ================================ LOGGER ====================================
from modules import mymodulesteam

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Facebook_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# =========================================================================================
# =================================== FACEBOOK DESKTOP METHODS ============================
# =========================================================================================

def RunMultiAccountsTask(p_driver, p_browser, p_function, p_taskuser_id, label_log, lock):
    # We need now to execute the task with other FB accounts
    logger.info(f"PhoneBot is NOT logged in Facebook")
    cpt = 0
    while True:
        are_we_profiles_FB_pages, list_FB_profiles = AreWeinFBProfilesPage(p_driver)
        if are_we_profiles_FB_pages:
            break
        else:
            cpt += 1
            if cpt < 2:
                p_driver.get("https://facebook.com")
                time.sleep(random.uniform(4, 6))
            else:
                logger.info(f"COMPUTER|||{p_browser}||Facebook|| PhoneBot didn't found multi accounts page.")
                mymodules.DisplayMessageLogUI(label_log,
                                              f"COMPUTER|||{p_browser}||Facebook|| PhoneBot didn't found multi accounts page.",
                                              "Red")
                break

    if are_we_profiles_FB_pages:
        mymodules.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}||Facebook|| PhoneBot found multi accounts page.",
                                      "Black")
        logger.info(f"PhoneBot is in Facebook page list of profiles {list_FB_profiles}")
        # WE WILL RUN THE TASK FOR EACH PROFILE EXCEPT THE ONE WE JUST DID
        for FB_profile in list_FB_profiles:
            logger.info(f"We will start automation on Facebook with profile {FB_profile}.")
            FBLogin(p_driver, FB_profile, p_browser, label_log, lock)
            # === TEST IF WE SUCCESSFULLY LOGGED IN
            are_we_connected_FB, FB_username = AreWeFBLoggedIn(p_driver)
            if not are_we_connected_FB:
                logger.error(f"PhoneBot couldn't login with profile {FB_profile}!")
                mymodules.DisplayMessageLogUI(label_log,
                                              f"COMPUTER|||{p_browser}||Facebook||{FB_profile}| PhoneBot couldn't login with profile {FB_profile}!",
                                              "Red")
            else:
                # ===================================================================================
                # Let's get the quantity of actions possible
                quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, FB_username)
                if quantity_actions > 0:
                    # ===================================================================================
                    # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                    # ===================================================================================

                    result, counter = p_function(p_browser, p_taskuser_id, p_driver, FB_username, quantity_actions,
                                                 label_log, lock)

                    FBLogout(p_driver)
                    logger.info(f"Profile {FB_profile} logout of Facebook .")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"COMPUTER|||{p_browser}||Facebook||{FB_profile}| Profile {FB_profile} logout of Facebook.",
                                                  "Black")
                else:
                    FBLogout(p_driver)
                    logger.info(
                        f"Profile {FB_profile} logout of Facebook because he/she did too many actions.")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"COMPUTER|||{p_browser}||Facebook||{FB_profile}| Profile {FB_profile} logout of Facebook because he/she did too many actions.",
                                                  "Black")

    else:
        logger.info(f"COMPUTER|||{p_browser}||Facebook|| PhoneBot didn't found multi accounts page.")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"COMPUTER|||{p_browser}||Facebook|| PhoneBot didn't found multi accounts page.",
                                      "Red")
    return result, counter


def AreWeFBLoggedIn(p_driver):
    """
    This function check if browser is connected to facebook or not and return True with FB username
    or False with None
    """

    logger.info("=============================== AreWeFBLoggedIn() =========================================")

    # INITIALISATION
    fb_username = None
    # ======================= ACCEPT TERMS POPUP ==============================================
    try:
        # Click on cookie popup is exists
        button_accept_cookies = p_driver.find_elements_by_xpath("//button[@data-cookiebanner='accept_button']")
        button_accept_cookies[0].click()
    except Exception as ex:
        logger.error(f"ERROR clicking on cookie popup : {ex}")

    cpt = 0
    while True:
        try:
            # Click on Account menu
            button_menu = WebDriverWait(p_driver, 15).until(EC.presence_of_element_located((By.XPATH,
                                                                                            "//div[(@role='button' and @aria-label='Account') or(@role='button' and @aria-label='Compte')]")))
            button_menu.click()

            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            # Get the username of current FB profile
            try:

                fb_username_element = WebDriverWait(p_driver, 15).until(EC.presence_of_element_located((By.XPATH,
                                                                                                        "//div[@aria-label='Account' or @aria-label='Compte']//a[@role='link']//span[@dir='auto']")))
                fb_username_brut = fb_username_element.text
                print(f"fb_username_brut : {fb_username_brut}")
                # We need to make some transformation because fb_username_brut is returning "Name\nYour profile"
                fb_username_list = fb_username_brut.split('\n')
                fb_username = fb_username_list[0]
                return True, fb_username
            except Exception as ex:
                logger.error(f"ERROR getting username : {ex}")
                return False, fb_username


        except Exception as ex:
            logger.error(f"ERROR clicking on top right menu : {ex}")
            return False, fb_username

        cpt += 1
        if cpt > 2:
            break

    return False, None


def AreWeinFBProfilesPage(p_driver):
    """
    This function will check if we are in the fb homepage where all the profiles are displayed
    """
    logger.info("=============================== AreWeinFBProfilesPage() =========================================")

    try:
        list_FB_profiles = []

        buttons_account = WebDriverWait(p_driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-userid]//a[@title]/div")))
        for button_account in buttons_account:
            list_FB_profiles.append(button_account.text)
        return True, list_FB_profiles

    except Exception as ex:
        logger.error(f"ERROR when clicking on Logout : {ex}")
        return False, None


def FBLogout(p_driver):
    """
    This method will logout of Facebook
    """
    logger.info("=============================== FBLogout() =========================================")

    while True:
        try:
            # Click on Account menu
            button_menu = WebDriverWait(p_driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Account' or @aria-label='Compte']")))
            # button_menu.click()
            p_driver.execute_script("arguments[0].click();", button_menu)

            p_driver.implicitly_wait(10)
            time.sleep(random.uniform(1, 2))
            # Click on Logout
            try:

                button_logout = WebDriverWait(p_driver, 15).until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@role='button']//span[text()='Log Out' or text()='Se déconnecter']")))
                # button_logout.click()
                p_driver.execute_script("arguments[0].click();", button_logout)

                break

            except Exception as ex:
                logger.error(f"ERROR when clicking on Logout Link in top right menu : {ex}")



        except Exception as ex:
            logger.error(f"ERROR clicking on top right menu : {ex}")


def FBLogin(p_driver, p_profile, p_browser, label_log, lock):
    """
    This method will login to Facebook with a specific profile
    """
    logger.info(f"=============================== FBLogin {p_profile} =========================================")
    cpt = 0
    while True:
        try:
            button_account = WebDriverWait(p_driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@data-userid]//a[@title]/div[text()='{p_profile}']")))
            logger.info(f"PhoneBot found {p_profile}")
            button_account.click()
            # WE CHECK IMMEDIATELY IF WE ARE LOGIN AND LEAVE THE FUNCTION OR WE MAKE SOME OTHER CHECKING
            # AND TRY AGAIN TO LOGIN IN A DIFFERENT WAY
            try:
                p_driver.find_element_by_xpath("//form[contains(@action, '/logout.php?')]")
                break
            except Exception as ex:
                logger.error(f"COMPUTER|||{p_browser}|| Error when checking quickly if logged in")
            # THE LOGIN POPUP MAY SHOW UP
            # CHECK IF PASSWORD FIELD IS FILLED OR NOT
            # password_field=WebDriverWait(p_driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@type='password']")))
            try:
                Remember_password = WebDriverWait(p_driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[text()='Remember password' or text()='Mémoriser le mot de passe']")))
                Remember_password.click()

                button_login = WebDriverWait(p_driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//button[@type='submit']")))
                # button_login.click()
                p_driver.execute_script("arguments[0].click();", button_login)
                time.sleep(random.uniform(2, 4))

                # We need to check if there is any error message regarding the password correct or not
                try:

                    wrong_password = p_driver.find_element_by_xpath(
                        "//div[contains(text(),'The password you’ve entered is incorrect') or contains(text(),'Le mot de passe entré est incorrect.')]")
                    logger.error(f"ERROR : The password for profile {p_profile} is not correct!")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"COMPUTER|||{p_browser}||Facebook||{p_profile}| ERROR : The password for profile {p_profile} is not correct!",
                                                  "Red")
                    break
                except Exception as ex:
                    logger.info(f"The password for profile {p_profile} was correct!")
                    break

            except Exception as ex:
                logger.error(
                    f"ERROR when clicking on Login popup for profile {p_profile} : {ex}. Let's try another button login")
                try:

                    button_login = WebDriverWait(p_driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and @id='loginbutton']")))
                    p_driver.execute_script("arguments[0].click();", button_login)
                    break
                except Exception as ex:
                    logger.error(
                        f"ERROR when clicking on 2nd Login button for profile {p_profile} : {ex}.")

        except Exception as ex:
            cpt += 1
            if cpt >= 2:
                break
            else:
                # In case we are in previous popup with wrong password. PhoneBOt need to come back to list of FB users page
                logger.error(f"ERROR clicking on profile {p_profile} : {ex}")
                p_driver.get('https://facebook.com')
                time.sleep(random.uniform(4, 5))


def RunFacebookBrowser(p_browser, p_function, p_taskuser_id, label_log, lock):
    """
    This method will open browser and run the task for all the profiles found in cookies Browser
    It will have to check for the daily & hourly limit
    It will return True if it run some actions, or False if nothing
    :param p_function:
    :param p_taskuser_id:
    :return:
    """
    try:
        # === 1 OPEN BROWSER
        if p_browser == "Chrome":
            driver = mymodulesteam.ChromeDriverWithProfile()
        elif p_browser == "Firefox":
            driver = mymodulesteam.FireFoxDriverWithProfile()
        else:
            logger.error(f"PhoneBot didn't find the browser called '{p_browser}'.")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER|||{p_browser}||Facebook||{p_browser}| PhoneBot didn't find the browser called '{p_browser}'.",
                                          "Red")
            return False
        driver.get('https://facebook.com')
        driver.maximize_window()
        driver.implicitly_wait(10)
        # === 2 TEST IF WE ARE ALREADY LOGGED IN
        are_we_connected_FB, FB_username = AreWeFBLoggedIn(driver)
        print(f"are_we_connected_FB : {are_we_connected_FB}")
        print(f"FB_username : {FB_username}")
        if FB_username == "":
            print(f"ERROR FB_username is empty!!!")
        if are_we_connected_FB:
            logger.info(f"PhoneBot is logged in Facebook with profile {FB_username}.")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER|||{p_browser}||Facebook||{FB_username}| PhoneBot is logged in Facebook with profile {FB_username}.",
                                          "Black")
            # ===================================================================================
            # Let's get the quantity of actions possible
            quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, FB_username)
            cpt = 0
            if quantity_actions > 0:
                # ===================================================================================
                # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
                # ===================================================================================
                result, counter = p_function(p_browser, p_taskuser_id, driver, FB_username, quantity_actions, label_log,
                                             lock)

                # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
                logger.info(f"Profile {FB_username} logout of Facebook .")
                mymodules.DisplayMessageLogUI(label_log,
                                              f"COMPUTER|||{p_browser}||Facebook||{FB_username}| Profile {FB_username} logout of Facebook.",
                                              "Black")
                FBLogout(driver)
                result, counter = RunMultiAccountsTask(driver, p_browser, p_function, p_taskuser_id, label_log, lock)
            else:
                # THis user already reach the limit, We need to logout and loop all the profiles
                logger.info(f"Profile {FB_username} logout of Facebook .")
                FBLogout(driver)
                result, counter = RunMultiAccountsTask(driver, p_browser, p_function, p_taskuser_id, label_log, lock)
        else:
            result, counter = RunMultiAccountsTask(driver, p_browser, p_function, p_taskuser_id, label_log, lock)
        return result, counter
    except Exception as ex:
        logger.error(f"COMPUTER||||{p_browser}||| ERRROR executing Facebook function task N°{p_taskuser_id} : {ex}")
        return False, counter


def Cold_Messaging_Facebook_Group_Members_3(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
                                            label_log, lock):
    logger.info(
        f"=================== Cold_Messaging_Facebook_Group_Members_3 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")

    result, counter = Browser_Facebook_send_message_group_members.Browser_Cold_Messaging_Facebook_Group_Members(
        p_browser,
        p_taskuser_id,
        FB_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}||{FB_username}| PhoneBot finished the automation Cold_Messaging_Facebook_Group_Members_3",
                                  "Black")

    return result, counter


def Influencers_Facebook_Page_Admins_13(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log,
                                        lock):
    logger.info(
        f"=================== Influencers_Facebook_Page_Admins_13 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")

    result, counter = Browser_Facebook_send_message_Page_Admins.Browser_Influencers_Facebook_Admin_Page(p_browser,
                                                                                                        p_taskuser_id,
                                                                                                        FB_username,
                                                                                                        p_driver,
                                                                                                        p_quantity_actions,
                                                                                                        label_log,
                                                                                                        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Facebook_Group_Admins_22",
                                  "Black")

    return result, counter


def Influencers_Facebook_Group_Admins_22(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log,
                                         lock):
    logger.info(
        f"=================== Influencers_Facebook_Group_Admins_22 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")

    result, counter = Browser_Facebook_send_message_group_admins.Browser_Influencers_Facebook_Group_Admins(p_browser,
                                                                                                           p_taskuser_id,
                                                                                                           FB_username,
                                                                                                           p_driver,
                                                                                                           p_quantity_actions,
                                                                                                           label_log,
                                                                                                           lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Influencers_Facebook_Group_Admins_22",
                                  "Black")

    return result, counter


def Scraping_Facebook_Group_Members_24(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log,
                                       lock):
    logger.info(
        f"=================== Scraping_Facebook_Group_Members_24 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")

    result, counter = Browser_Facebook_scrape_group_members.browser_Scraping_Facebook_Group_members(p_browser,
                                                                           p_taskuser_id,
                                                                           FB_username,
                                                                           p_driver,
                                                                           p_quantity_actions,
                                                                           label_log,
                                                                           lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Facebook_Add_Group_members_as_Friends_33",
                                  "Black")

    return result, counter


def Authority_Facebook_Add_Group_members_as_Friends_33(p_browser, p_taskuser_id, p_driver, FB_username,
                                                       p_quantity_actions, label_log, lock):
    logger.info(
        f"=================== Authority_Facebook_Add_Group_members_as_Friends_33 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Facebook_share_posts_in_groups.Browser_Authority_Facebook_share_some_posts_in_FB_groups(
        p_browser,
        p_taskuser_id,
        FB_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Facebook_Add_Group_members_as_Friends_33",
                                  "Black")

    return result, counter


def Authority_Facebook_Random_Like_56(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions, label_log,
                                      lock):
    logger.info(
        f"=================== Authority_Facebook_Random_Like_56 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Facebook_like_random.Browser_Facebook_Like_random_post(p_browser,
                                                                                     p_taskuser_id,
                                                                                     FB_username,
                                                                                     p_driver,
                                                                                     p_quantity_actions,
                                                                                     label_log,
                                                                                     lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Facebook_Random_Like_56",
                                  "Black")

    return result, counter


def Authority_Facebook_share_post_53(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
                                                label_log, lock):
    logger.info(
        f"=================== Authority_Facebook_share_posts_in_groups_53 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Facebook_share_posts_in_groups.Browser_Authority_Facebook_share_some_posts_in_FB_groups(p_browser,
        p_taskuser_id,
        FB_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)

    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Facebook_share_posts_in_groups_53",
                                  "Black")
    return result, counter


def Cold_Messaging_Facebook_Likers_Commnenters_57(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
                                                  label_log, lock):
    logger.info(
        f"=================== Cold_Messaging_Facebook_Likers_Commnenters_57 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Facebook_send_message_likers_commenters.Browser_Cold_Messaging_Likers_Commenters_Fb_post(
        p_browser,
        p_taskuser_id,
        FB_username,
        p_driver,
        p_quantity_actions,
        label_log,
        lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Cold_Messaging_Facebook_Likers_Commnenters_57",
                                  "Black")

    return result, counter


def Authority_Facebook_comment_some_posts_59(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
                                             label_log, lock):
    logger.info(
        f"=================== Authority_Facebook_comment_some_posts_58 {p_taskuser_id} - {FB_username} - {p_quantity_actions} =======================")
    result, counter = Browser_Facebook_comment_some_posts.comment_facebook_posts_by_keyword(p_browser,
                                                                                            p_taskuser_id,
                                                                                            FB_username,
                                                                                            p_driver,
                                                                                            p_quantity_actions,
                                                                                            label_log,
                                                                                            lock)
    mymodules.DisplayMessageLogUI(label_log,
                                  f"COMPUTER|||{p_browser}|| PhoneBot finished the automation Authority_Facebook_comment_some_posts_58",
                                  "Black")

    return result, counter
