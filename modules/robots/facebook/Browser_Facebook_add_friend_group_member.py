# Made by Romain Brun
# Email : r.brun972@gmail.com
# 07.89.61.71.87
# TASK 278
import datetime
import logging
import sqlite3
import threading
import time

from modules import mymodulesteam

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import uniform

# =======================LOGGER=====================================#
open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Facebook_add_Group_members__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ==================================================================#
def add_action(lock, FB_username, profile_url, profile_group, platform, action, id_task_user):
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    with lock:
        try:
            # Check if member exists
            connection = sqlite3.Connection(mymodulesteam.LoadFile('db.db'))
            cursor = connection.cursor()
            select_query = """ SELECT * FROM actions WHERE id_social_account = ? and  url_post = ? """
            select_tuple = (FB_username, profile_url)
            cursor.execute(select_query, select_tuple)
            count = len(cursor.fetchall())

            print(count)
            # insert new line to actions if not already inserted
            if count == 0:
                insert_query = """INSERT INTO actions(platform, type_action, id_smartphone, id_social_account, 
                url_post, fb_group_name, fb_group_url, id_task_user, date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                insert_tuple = (platform, action, "Desktop", FB_username, profile_url, profile_group.split('/')[-2],
                                profile_group, id_task_user, date)
                cursor.execute(insert_query, insert_tuple)
                added = True
                connection.commit()
            else:
                added = False
            connection.close()

        except Exception as e:
            logger.error(f'An error occurred while trying to add actions to database - Error: {e}')
            added = False

    return added


def scroll_To(y, p_driver):  # scroll function
    y = int(y)
    y = y + 3500
    y = str(y)
    p_driver.execute_script("window.scrollTo(0," + y + ")")





def Browser_Add_Group_Member_As_Friend(p_browser, p_taskuser_id, FB_username, p_driver, p_quantity_actions, label_log,
                                       lock):
    task_details_dico = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
    googlesheet = task_details_dico["url_list"]
    googlesheet_id = str(googlesheet).split("/")[5]
    array_url_group = mymodulesteam.GoogleSheetGetValues(googlesheet_id)

    # friend_request_limit = p_quantity_actions
    counter = 0
    logger.info("=== [2] Send sub request at the url =======================================")
    try:
        for url in array_url_group:  # Url by url

            url = str(url[0])
            sub = False
            try:
                time.sleep(1)
                p_driver.get(url)
                # p_driver.maximize_window()
                p_driver.implicitly_wait(3)
            except Exception as ex:
                print("Error on the following url : " + url)
                return False

            # Join the group if we not in
            try:
                join_button = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located(
                    (By.XPATH, ("//span[(text()='Rejoindre le groupe') or (text()='Join Group')]"))))
                if len(join_button) > 1:
                    delta = len(join_button) - 1
                    print("RESULT : " + str(delta))
                    del join_button[:delta]
                print("final : " + str(len(join_button)))
                p_driver.execute_script("arguments[0].click();", join_button[0])
                rand_delay = uniform(0.5, 0.9)  # random delay to brain facebook robot
                time.sleep(rand_delay)
                sub = False
                logger.error(f"Request send : " + url)

            except Exception as ex:
                logger.error(f"You are already sub at this page: " + url)
                sub = True

            # if user is in group we get members page
            try:
                if sub == True:
                    p_driver.get(url + "members")  # redirect to the memerbers page
                    p_driver.implicitly_wait(3)
                    attempts = 0
                    y = 1500  # position of the page

                    # Open members tabs
                    see_all_counter = 0
                    # try:
                    see_all = WebDriverWait(p_driver, 2.5).until(EC.presence_of_all_elements_located((
                        By.XPATH,
                        '//a[contains(@aria-label, "Voir tout") or contains(@aria-label, "See All")]'
                    )))
                    see_all_counter = len(see_all)

                    add_button = WebDriverWait(p_driver, 2.5).until(EC.presence_of_all_elements_located((By.XPATH, (
                        "//span[(text()='Ajouter') or (text()='Add Friend')]"))))  # get the array of buttons
                    new_add_profile = []

                    for i in range(0, see_all_counter):
                        p_driver.get(url + "members")  # redirect to the memerbers page
                        see_all = WebDriverWait(p_driver, 2.5).until(EC.presence_of_all_elements_located((
                            By.XPATH,
                            '//a[contains(@aria-label, "Voir tout") or contains(@aria-label, "See All")]'
                        )))
                        p_driver.execute_script("arguments[0].click()", see_all[i])

                        print("try")

                        # while len(new_add_profile) <= p_quantity_actions: # and attempts <= 10:  # if the p_driver does not recover 20 buttons on scroll for it to load 20
                            # Scroll to page bottom to load all members
                        mymodulesteam.ScrollToTheEnd(p_driver)

                        print(attempts, len(new_add_profile), len(add_button))  # just print for debugging
                        time.sleep(1)  # to have time to see what happen in debugging
                        scroll_To(y, p_driver)  # fonction scroll 3500 by 3500
                        new_add_friend = WebDriverWait(p_driver, 2.5).until(EC.presence_of_all_elements_located((
                            By.XPATH,
                            '//span[@dir="auto"]//a[@role = "link" and contains(@href, "group") and contains(@href, "user") and not(contains(@aria-hidden, "true"))]'
                        )))
                        # new_add_friend = WebDriverWait(p_driver, 10).until(EC.presence_of_all_elements_located((
                        #     By.XPATH,
                        #     (
                        #         "//span[(text()='Ajouter') or (text()='Add Friend')]"))))  # refresh the array buttons
                        for profile in new_add_friend:
                            if profile not in new_add_profile:
                                new_add_profile.append(profile.get_attribute('href'))
                            # attempts += 1

                    # except Exception as e:
                    #     logger.info(f'Buttons SEE ALL not found')

                    # If the facebook account are not in group
                    for profile in new_add_profile:
                        # p_driver.execute_script("arguments[0].click();", new_add_profile[group])
                        # Go to profile page
                        # print(profile)
                        profile_id = profile.split("/")[-2]
                        # print(profile_id)
                        p_driver.get(f'https://www.facebook.com/profile.php?id={profile_id}')

                        try:
                            # Add friend
                            add_button = WebDriverWait(p_driver, 2.5).until(EC.presence_of_element_located((
                                By.XPATH,
                                '//div[contains(@data-pagelet, "ProfileAction")]//*[contains(@aria-label, "Add") '
                                'or contains(@aria-label, "Ajouter")]'
                            )))

                            # Get profile data
                            profile_name = WebDriverWait(p_driver, 2.5).until(EC.presence_of_element_located((
                                By.TAG_NAME,
                                'h1'
                            ))).text
                            profile_url = f'https://www.facebook.com/profile.php?id={profile_id}'
                            profile_group = url

                            added = add_action(lock, FB_username, profile_url, profile_group, "facebook", "add_friend",
                                               p_taskuser_id)

                            if added:
                                p_driver.execute_script("arguments[0].click();", add_button)
                                logger.info(f'{profile_name} add as a friend on your account')
                                counter += 1
                            else:
                                logger.info(f'Fail to add friend')


                        except Exception as e:
                            logger.info(f'Profile do not belong to a person, but to a organization')

                        if counter >= p_quantity_actions:
                            p_driver.get("https://www.facebook.com")
                            return True, counter
                        rand_delay = uniform(1.5, 2.5)
                        time.sleep(rand_delay)
                elif not sub:
                    logger.error(
                        f"Your are not in the group, Phonebot sent the request for you but it is possible that you will not be accepted or that the request is pending : " + url)

            except Exception as ex:
                logger.error(f"Page Members not found or you are not part of this group {ex} : " + url)

    except Exception as ex:
        logger.error(f"Error when during the extraction of the urls: '{ex}'")
        return False, counter

    p_driver.get("https://www.facebook.com")
    return True, counter
# p_taskuser_id = 3295
# p_browser = "Firefox"
# FB_username = "ScriptTest"
# label_log = ""
# lock = threading.Lock()
# p_quantity_actions = 5.0
# p_driver = mymodulesteam.FireFoxDriverWithProfile()
# p_driver.get("http://www.facebook.com")
#
# result = Browser_Add_Group_Member_As_Friend(p_browser, p_taskuser_id, p_driver, FB_username, p_quantity_actions,
#                                             label_log,
#                                             lock)
# p_driver.quit()
