# -*- coding: utf-8 -*-

"""
Author : Behzad NEKOUEI
Email : behzadnekouei@gmail.com
"""
import datetime
import random
import sqlite3
import time
from modules import mymodulesteam
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# =======================LOGGER=====================================#
open(mymodulesteam.LoadFile("log.log"), "w").close()
logger = logging.getLogger("__Linkedin_Comment_Posts__")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")
file_handler = logging.FileHandler(mymodulesteam.LoadFile("log.log"))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ==================================================================#
def random_sleep():
    """
        Random time.sleep for having different sleep times.
    """
    ts = random.uniform(1, 5)
    ts = round(ts, 2)
    print(f"Sleep time: {ts}")
    time.sleep(ts)


def is_post_already_commented(lock, post_id, linkedin_username, comment):
    """
        Return True if post is already commented and False if post is not already commented.
    """
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sqlite_cursor.execute(
                "SELECT COUNT(*) FROM actions WHERE id_contact = ? AND id_social_account = ? AND message = ?", (post_id, linkedin_username, comment))
            count = sqlite_cursor.fetchone()[0]
            sqlite_connection.commit()
            sqlite_connection.close()
    except Exception as ex:
        logger.info(f"Query Failed in is_post_already_commented(), Error: {str(ex)}")
    else:
        print(count)
        if count:
            logger.info(f"Post {post_id} already commented!")
            return True
        else:
            logger.info(f"Post {post_id} is not already commented!")
            return False


def save_action_database(lock, comment, post_id, p_taskuser_id, linkedin_username):
    """
        Try to save comment details into the database and print the log by logger.info().
    """
    try:
        sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        with lock:
            sqlite_cursor.execute(
                "INSERT INTO actions (platform, type_action, id_social_account, date_created, message, id_contact, id_task_user) VALUES (?,?,?,?,?,?,?)",
                ('linkedin',
                 'comment_posts',
                 linkedin_username,
                 datetime.datetime.now(),
                 comment,
                 post_id,
                 p_taskuser_id))
            sqlite_connection.commit()
            sqlite_connection.close()
    except Exception as ex:
        logger.info(f"Query Failed in save_action_database, Error: {str(ex)}")
        return False
    else:
        logger.info(f"Comment saved to the database successfully!")
        return True

def Browser_Comment_Linkedin_Posts(p_browser, p_taskuser_id, p_driver, linkedin_username, p_quantity_actions, label_log, lock):

    """
        :param p_browser: "firefox" or "chrome"
        :param p_taskuser_id: The Id N° in database of the user task (ex: 4843 )
        :param p_quantity_actions: The quantity maximum of actions. Ex: 5 comments to 5 posts
        :param label_log: This is the label of our GUI (PyQt5). It will display the message you want to the user interface. This is very useful for displaying important error.
        :param lock: This function will be executed inside a thread. The program PhoneBot use multithread to run different tasks at same times on different devices (browser desktop, smartphones).
        If several tasks save at same time some data in SQLITE3 database, there will be some error for multiple access at same time. We need to "Lock" the access.
        You simply create it with this line of code : lock = threading.Lock()
        :return: True if everything was fine or False if error , and number of posts that commented
    """
    logger.info(f"Task number {p_taskuser_id} started for {linkedin_username} account in {p_browser} browser")
    try:
        # get all the details of task with the task_user_id in a dictionary
        task_details_dict = mymodulesteam.GetDetailsTaskUserMysql(p_taskuser_id)
        # print(task_details_dict)

        # get the url of googlesheet that contains all the keywords to search and all the messages to comment
        googlesheet_url = task_details_dict["url_keywords"]
        # print("googlesheet_url is:", googlesheet_url)

        # extract googlesheet id from the url
        googlesheet_id = str(googlesheet_url).split("/")[5]
        # print("googlesheet_id is:", googlesheet_id)

        # read all the information in the googlesheet and put them in a list
        keywords_comments_list = mymodulesteam.GoogleSheetGetValues(googlesheet_id)
        # print(" keywords_comments_list:",  keywords_comments_list)
        comment_counter = 0
        # browse the list of keywords ans
        for keyword_comment in keywords_comments_list:
            # break the loop if the maximum number of actions is not reached
            if comment_counter >= p_quantity_actions:
                break

            keyword = keyword_comment[0]
            comment = keyword_comment[1]
            print(f"keyword to search is: {keyword} and message to comment is : {comment}")

            # search keyword directly in url
            p_driver.get(f"https://www.linkedin.com/search/results/content/?keywords={keyword}")

            # wait some seconds to load the result page
            p_driver.implicitly_wait(5)

            # get the list of 10 first posts that found in the page
            posts = p_driver.find_elements(By.XPATH, "//div[@data-chameleon-result-urn]")
            print(f"{len(posts)} post found in the page.")

            while True:
                for post in posts:

                    # get the id of post
                    post_id = post.get_attribute('data-chameleon-result-urn').split(":")[3]
                    print(f"post id is: {post_id}")

                    # break the loop if the maximum number of actions is not reached
                    if comment_counter >= p_quantity_actions:
                        logger.info("The maximum number of allowed comment achieved!")
                        break
                    # pass to the next post if the post is already commented
                    if is_post_already_commented(lock, post_id, linkedin_username, comment):
                        continue
                    else:
                        # scroll to the post in the posts list
                        p_driver.execute_script("arguments[0].scrollIntoView(true);", post)
                        print("scroll to the post in the posts list")
                        random_sleep()

                        # click on the post
                        post.click()
                        print("click on the post")
                        random_sleep()

                        # find comment field and scroll to that
                        comment_field = p_driver.find_element_by_class_name('ql-editor' and 'ql-blank')
                        p_driver.execute_script("arguments[0].scrollIntoView(true);", comment_field)
                        print("find comment field and scroll to that")
                        random_sleep()

                        # write the comment into the field
                        comment_field.send_keys(comment)
                        print("write the comment into the field")
                        random_sleep()

                        # Stay to display submit button
                        print("Stay to display submit button")
                        submit_button = WebDriverWait(p_driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@class,'comments-comment-box__submit-button')]")))
                        print("submit button displayed")
                        random_sleep()

                        # submit_button.click()  # You can comment this line if you are just testing this script!
                        print("comment sent successfully")
                        logger.info(f"Post with id {post_id} commented by {linkedin_username} comment: {comment}")

                        if save_action_database(lock, comment, post_id, p_taskuser_id, linkedin_username):
                            comment_counter += 1
                            logger.info(f"comment counter is: {comment_counter}")

                # Scroll to the last post of the page
                p_driver.execute_script("arguments[0].scrollIntoView(true);", posts[-1])
                print("Scroll to the end of page")
                # wait some seconds to load the next posts in the page
                time.sleep(5)

                # check to find new posts loaded by scrolling
                updated_posts = p_driver.find_elements(By.XPATH, "//div[@data-chameleon-result-urn]")
                new_posts = len(updated_posts) - len(posts)
                logger.info(f"{new_posts} new post found in the page.")

                if new_posts == 0:
                    # break the loop and go to the next keyword if there isn't any new post
                    break
                else:
                    # make a new list from new posts recently loaded and continue with the same keyword
                    posts = [post for post in updated_posts if post not in posts]

    except Exception as ex:
        logger.info(f"Task Failed, Error: {str(ex)}")
        # return False, comment_counter
    else:
        return True, comment_counter
    finally:
        logger.info("End of task")


"""
p_taskuser_id = 4843  # This is the Task user id we get from the dashboard.phonebot.co
p_browser = "firefox"  # This is the name of the browser
linkedin_username = "Tuto"
label_log = ""
lock = threading.Lock()  # This is necessary to protect the access to the database in multithreading mode
p_quantity_actions = 20  # This is the maximum actions that every task can do
p_driver = mymodulesteam.FireFoxDriverWithProfile()
result, counter = Browser_Comment_Linkedin_Posts(p_browser, p_taskuser_id, p_driver, linkedin_username, p_quantity_actions, label_log, lock)
p_driver.quit()
"""
