import datetime
import random
import re
import sqlite3
import threading
import time
from selenium.common.exceptions import InvalidElementStateException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# import Browser_Scrap_Freelancer_Replyed_Proposals_Users as scrapper

from modules import mymodulesteam as MMT


# ********************************************* DB INTERACTIONS ********************************************************
# ======================================== update_contacts_replied =====================================================
def update_contacts_replied(user, task_user, timestamp, message, lock):
    with lock:
        # try:
        # Update contact
        conn = sqlite3.connect(MMT.LoadFile('db.db'))
        cursor = conn.cursor()
        update_query = """ UPDATE contacts SET replied = ?, date_update = ? WHERE id = ? and platform = ?"""
        update_tuple = (1, timestamp, user["id"], user["platform"])
        cursor.execute(update_query, update_tuple)
        conn.commit()

        # get last message sent to user
        select_query = """ SELECT id, id_message FROM actions 
                                    WHERE id_contact = ? AND type_action = ? ORDER BY date_created Desc"""
        select_tuple = (user["id"], 'message')
        last_sent_message = cursor.execute(select_query, select_tuple).fetchall()
        if len(last_sent_message) > 0:
            last_sent_message = last_sent_message[0]
        else:
            last_sent_message = [None, None]

        # Add latest sent message from profile to actions DB
        ins_query = """ INSERT INTO actions (
                            platform,
                            type_action,
                            message, 
                            id_smartphone, 
                            id_social_account,
                            id_contact,
                            id_message,
                            date_created,
                            id_task_user
                            ) VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        ins_tuple = (user["platform"], "message_received", str(message), p_browser, user["username"], user["id"],
                     last_sent_message[1], timestamp, task_user["id"])

        cursor.execute(ins_query, ins_tuple)
        conn.commit()

        # Update last sent message
        if last_sent_message[0] is not None and last_sent_message[1] is not None:
            update_query = """ UPDATE actions SET replied = ?, date_update = ? WHERE id = ?"""
            update_tuple = (1, timestamp, last_sent_message[0])
            cursor.execute(update_query, update_tuple)
            conn.commit()

        conn.close()

        # except Exception as e:
        #     MMT.logger.error(f'Function "update_contacts_replied" wasn\'t able to update de contact - Exception: {e}')


# ======================================================================================================================
# ====================================== Fecth freelancer profiles =====================================================
def get_freelancer_profiles(lock):
    try:
        with lock:
            conn = sqlite3.connect(MMT.LoadFile('db.db'))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            select_query = """SELECT * FROM contacts WHERE platform = ? """
            select_tuple = ("freelancer",)
            cursor.execute(select_query, select_tuple)
            profiles = dict(res=[dict(profile) for profile in cursor.fetchall()])
            conn.close()
            # print(profiles)
            if len(profiles['res']) == 0:
                return False
            return profiles
    except Exception as e:
        MMT.logger.error(f'Error fetching freelancer profiles: error msg: {e}')


# ======================================================================================================================
# ========================================= Dict Factory================================================================
# convert the tuple returned from sqlite into a dict
def dict_factory(cursor, row):
    MMT.logger.info(f'=========================== dict_factory ===========================')
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# ======================================================================================================================
# ========================================== GET USER ACTIONS ==========================================================
def get_user_actions(user, lock):
    with lock:
        try:
            conn = sqlite3.connect(MMT.LoadFile('db.db'))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            select_query = """SELECT * FROM actions WHERE id_contact = ? and type_action = ? and platform = ?
                                ORDER BY date_created DESC"""
            select_tuple = (user["id"], "message", user["platform"])
            cursor.execute(select_query, select_tuple)
            user_actions = dict(res=[dict(user_action) for user_action in cursor.fetchall()])
            conn.close()

            if len(user_actions['res']) == 0:
                return None

            return user_actions['res']
        except Exception as e:
            MMT.logger.error(f'Fail to fecth user actions')


# ======================================================================================================================
# ====================================== Add Action to DB ==============================================================
def add_action_db(lock, **kwargs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MMT.logger.info(f'========================== add_action_db =======================================================')
    MMT.logger.info(f'===================== Action : {kwargs.get("type_action")} =====================================')
    user = kwargs["user"]
    task_user = kwargs["task_user"]

    with lock:
        try:
            # Add sent message to db
            conn = sqlite3.connect(MMT.LoadFile('db.db'))
            cursor = conn.cursor()
            insert_query = """INSERT INTO actions (
                                            platform,
                                            type_action,
                                            message,
                                            id_social_account,
                                            id_contact,
                                            date_created,
                                            id_message,
                                            id_smartphone,
                                            id_task_user
                                            ) 
                                VALUES (?, ? ,? ,? ,? ,? ,?, ?, ?) 
                                """
            insert_tuple = (user["platform"], kwargs["type_action"], kwargs["message"], user["username"],
                            user["id"], timestamp, kwargs["id_message"], p_browser, task_user["id"])
            cursor.execute(insert_query, insert_tuple)
            conn.commit()

            # update contacts - reset reply and date update
            update_query = """UPDATE contacts SET replied = ?, date_update = ? WHERE id = ?"""
            update_tuple = (None, timestamp, user['id'])
            cursor.execute(update_query, update_tuple)
            conn.commit()
            conn.close()
            return 1
        except Exception as e:
            MMT.logger.error(f'Fail to update db - error: {e}')
            return 0


# ======================================================================================================================
# **********************************************************************************************************************
# ====================================== elemClick =====================================================================
def elem_click(driver, elem=None):
    if elem is None:
        raise InvalidElementStateException
    else:
        driver.execute_script('arguments[0].click()', elem)
        random_sleep()


# ======================================================================================================================
# ====================================== AB TESTING SELECTOR============================================================
def ab_testing_selector(user, lock):
    with lock:
        conn = sqlite3.connect(MMT.LoadFile('db.db'))
        cursor = conn.cursor()
        sel_query = """SELECT id_message FROM actions WHERE id_contact = ? AND type_action = ? 
                    AND platform = ? ORDER BY date_created DESC"""
        sel_tuple = (user["id"], 'message', user["platform"])
        res = cursor.execute(sel_query, sel_tuple).fetchall()

        if len(res) == 0:
            # if theres no message sent to profile
            # get id from the last sent message
            sel_query = """SELECT id_message FROM actions WHERE platform = ? AND type_action = ?
                        ORDER BY date_created DESC"""
            sel_tuple = (user["platform"], 'message')
            res = cursor.execute(sel_query, sel_tuple).fetchall()

            # if theres no sent message for Freelancer profiles sent A
            if len(res) == 0:
                MMT.logger.info(f'There is no sent messages to Freelancer user: series A selected')
                return "A"
            else:
                msg = res[0][0][-1]
                return ('A', 'B')[msg == 'A']
        else:
            # get id from the last message sent to user and return it
            return res[0][0][-1]


# ======================================================================================================================
# ====================================== date formater =================================================================
def date_formater(str_date):
    pm = False
    hour_pm = str_date[str_date.index("· "):str_date.index(":")]
    hour = str.strip(str_date[str_date.index("· ") + 1:str_date.index(":")])
    if str_date.__contains__('PM'):
        hour = int(hour) + 12
        if hour == 24:
            hour = 0
    str_date = str_date.replace(hour_pm, str(hour))

    str_date = str.lower(str_date)
    str_date = str_date.replace(' am', '').replace(' pm', '').replace('· ', '')
    mounts = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for i in range(0, len(mounts)):
        if str_date.__contains__(mounts[i]):
            m = (i + 1, f'0{i + 1}')[i + 1 < 10]
            str_date = str_date.replace(f' {mounts[i]} ', f'-{m}-')
    str_date += ':00'
    date = str_date[:str_date.index(' ')]
    str_date = str_date.replace(date, re.sub(r'(\d{1,2})-(\d{1,2})-(\d{4})', '\\3-\\2-\\1', date))
    str_date = datetime.datetime.strptime(str_date, '%Y-%m-%d  %H:%M:%S')
    return str(str_date)


# ======================================================================================================================
# ========================================= Login/logout user ==========================================================
def login_user(driver, user):
    MMT.logger.info(f'=========================== login_user ===========================')
    user_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.XPATH, '//input[@type="email"]')))
    user_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.XPATH, '//input[@type="password"]')))

    send_keys_delayed(user_email, user[0])
    send_keys_delayed(user_password, user[1])
    user_email.submit()
    random_sleep()


def logout_user(driver):
    MMT.logger.info(f'=========================== logout_user ===========================')
    MMT.logger.info(f'Log out')
    user_card = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.TAG_NAME, 'app-user-card')))
    elem_click(driver, user_card)
    random_sleep(1)
    logout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.XPATH, '//a[contains(@href, "logout")]' or '//a[contains(@href, "Déconnexion")]')))
    elem_click(driver, logout_btn)
    random_sleep()


# ======================================================================================================================
# ======================================== randomSleep==================================================================
def random_sleep(t_wait=random.randint(1, 5)):
    time.sleep(t_wait)


# ======================================================================================================================
# ==================================== Get message id ==================================================================
def get_message_id(msg_id):
    MMT.logger.info(f'=========================== get_message_id ===========================')
    return msg_id[len(msg_id) - 2:]


# ======================================================================================================================
# ================================== SendKeys_Delayed ==================================================================
def send_keys_delayed(web_elem, key):
    for char in key:
        web_elem.send_keys(char)
        time.sleep(random.randint(1, 5) / 10)

    random_sleep()


# ======================================================================================================================
# ===================================== goto_user_chat =================================================================
def goto_user_chat(driver, username):
    random_sleep()
    try:
        MMT.logger.info(f'=========================== goto_user_chat ===========================')
        driver.get(f'https://www.freelancer.com/u/{username.replace("@", "")}')
        elem_click(driver,
                   WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                       By.XPATH,
                       '//fl-bit[@class="BannerContainer-buttons"]//fl-button[contains(@class, "ChatButton")]')))
                   )
        return True
    except TimeoutException as toe:
        MMT.logger.error(f'Fail to load requested page, or profile is not available: {toe}')
        MMT.logger.info(f'Profile: {username}')
        return False


# ======================================================================================================================
# ======================================= Check for if user replied ====================================================
def did_reply(driver, task_user, user, lock):
    MMT.logger.info(f'=========================== Checking For Replies ===========================')
    replied = False
    try:
        goto_user_chat(driver, user["username"])
        chat_msgs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
            By.XPATH, '//app-message-list//app-message-item//fl-bit[contains(@class, "MessageBody")]'
        )))
        if chat_msgs[-1].get_attribute("class").__contains__('MessageBody--other'):
            timestamp = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
                By.XPATH, '//fl-bit[contains(@class, "Timestamp")]')))
            replied = True
            
            # Get my last message
            all_my_last_messages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
                By.XPATH, '//fl-bit[contains(@class, "MessageBody--mine")]')))

            my_last_message = all_my_last_messages[-1]

            # Get all users answers
            other_answers_fl_bit = my_last_message.find_elements_by_xpath("./following::fl-bit[contains(@class, 'MessageBody--other')]")

            # Build answer
            message = ""
            for other_answer_fl_bit in other_answers_fl_bit:
                message += other_answer_fl_bit.find_element_by_xpath(".//span[contains(@class, 'NativeElement')]").text + "   "
            
            """
            # Lastest message sent by the user
            message = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
                By.XPATH, '//fl-bit[contains(@class, "MessageBody--other")]//*[@class="MessageContainer"]')))
            # print(f'LN250 - Last message: {message[-1].text}')
            message = message[-1].text
            """
            print("\n\n" + message + "\n\n")
            timestamp = timestamp[-1].text
            timestamp = date_formater(timestamp)

            if user["date_update"] is not None:
                timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                date_update = datetime.datetime.strptime(user["date_update"], "%Y-%m-%d %H:%M:%S")
                # difference = timestamp - date_update
                if timestamp >= date_update:
                    MMT.logger.info(f'user {user["username"]} replied')
                    replied = True

        # message = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        #     By.XPATH, '//fl-bit[contains(@class, "MessageBody--other")]')))
        random_sleep()
        elem_click(driver,
                   WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                       By.XPATH, '//fl-button[@fltrackinglabel="closeChat"]')))
                   )

        # if user["date_update"] is not None and timestamp <= user["date_update"]:
        #     MMT.logger.info(f'User didn\'t reply since last update.')
        #     return False

    except TimeoutException as toe:
        MMT.logger.info(f'User didn\'t reply: "TimeoutException caused by lacking of user response."')
        elem_click(driver,
                   WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                       By.XPATH, '//fl-button[@fltrackinglabel="closeChat"]')))
                   )
        return False
    
    # /!\/!\/!\/!\ Generally emojis error
    except selenium.common.exceptions.NoSuchElementException as nsee:
        MMT.logger.info(f'User {user["username"]} used emojis')
        elem_click(driver,
                   WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                       By.XPATH, '//fl-button[@fltrackinglabel="closeChat"]')))
                   )
        return False

    if replied:
        update_contacts_replied(user, task_user, timestamp, message, lock)

    return replied


# ======================================================================================================================
# ====================================== Get delay =====================================================================
def get_delay(delay, d_type):
    if delay is None:
        MMT.logger.error(f'Contacts column date_update is none - Please verify the reason for this.')

    MMT.logger.info(f'=========================== get_delay ===========================')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    # print(f'delay date: {delay}')
    delay = datetime.datetime.strptime(delay, '%Y-%m-%d %H:%M:%S')
    delay = (now - delay)
    if d_type == 'hours':
        delay = int(delay.total_seconds() / 60 / 60)
    elif d_type == 'days':
        delay = int(delay.total_seconds() / 60 / 60 / 24)
    elif d_type == 'weeks':
        delay = int(delay.total_seconds() / 60 / 60 / 24 / 7)
    elif d_type == 'mounts':
        delay = int(delay.total_seconds() / 60 / 60 / 24 / 31)
    return delay


# ======================================================================================================================
# =========================================== Send next message ========================================================
def send_message(driver, user, task_user, lock, id_message=None, first_message=None):
    MMT.logger.info(f'============================ send_message =================================================')
    goto_user_chat(driver, user['username'])

    # check if AB_Testing is enabled
    if task_user['AB_testing_enable'] == 1:
        msg_ab = ab_testing_selector(user, lock)
    else:
        msg_ab = user["id_message"][-1]

    # print(id_message)
    # print(first_message)
    msg_number = 0
    if first_message:
        msg_number = 1
    else:
        # Set the number of the next message
        msg_number = id_message
        # print(f'msg >> {msg_number}')
        msg_number = msg_number[-2]
        # print(f'msg -2 >> {msg_number}')
        msg_number = int(msg_number) + 1
        # print(f'msg -2 >> {msg_number}')

    """Retrive and compose the message"""
    # print(task_user[f'message_txt_{str(msg_number)}{msg_ab}'])
    #
    message_to_send = task_user[f'message_txt_{str(msg_number)}{msg_ab}']
    message_to_send = MMT.TransformMessage(f'{message_to_send}\r', firstname=user["first_name"],
                                           username=user["username"])

    # type and send message
    msg_textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.XPATH, '//textarea[@fltrackinglabel="TypingBox"]')))
    send_keys_delayed(msg_textarea, message_to_send)
    msg_textarea.send_keys(Keys.ENTER)
    MMT.logger.info(f'Selected message: message_txt_{str(msg_number)}{msg_ab}')
    MMT.logger.info(f' message sent: {message_to_send}')

    # Close chat
    elem_click(driver,
               WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                   By.XPATH, '//fl-button[@fltrackinglabel="closeChat"]')))
               )

    # update action - add new sent message
    result = add_action_db(lock, user=user, task_user=task_user, platform="freelancer", type_action="message",
                           id_message=f'message_txt_{msg_number}{msg_ab}', message=message_to_send)
    return result


# ======================================================================================================================
# ======================================== Check send next message =====================================================
def check_send_message(driver, user, task_user, lock):
    """ Verify if the delay to the next message is passed """
    # get actions user actions
    user_actions = get_user_actions(user, lock)
    # print(f'user actions: {user_actions}')
    if user_actions is not None:
        user_actions = user_actions[0]
    if user_actions is not None and len(user_actions) > 0:
        # if the user has message actions, check delay to next message
        id_message = get_message_id(user_actions["id_message"])
        if id_message == "4A" or id_message == "4B":
            MMT.logger.info( f'all messages have been sent to user {user["username"]}')

        # print(f'ID Message >> {id_message}')
        time_delay = task_user[f'time_delay_{id_message}']
        # print(f'Delay >> {time_delay}')
        time_delay_type = task_user[f'time_delay_{id_message}_type']
        print(f'Delay type>> {time_delay_type}')

        delay = get_delay((user["date_update"], user["date_created"])[user["date_update"] is None], time_delay_type)
        if delay >= task_user[f'time_delay_{id_message}']:
            result = send_message(driver, user, task_user, lock, id_message=id_message)
        else:
            MMT.logger.info('Time delay not attained')
            return 0
        return result
    else:
        MMT.logger.info(f'User {user["username"]} has no message actions: send 1st message if daily limit not attained')
        first_message_queue.append(user)
        return 0


# ======================================================================================================================
# ============================= Browser_Cold_Messaging_Freelancer_Replyed_Proposals ====================================
def Browser_Cold_Messaging_Freelancer_Replyed_Proposals(p_browser, p_task_user, p_quantity_limit, freelancer_user, lock):
    actions_performed = 0
    # fecth user from Freelancer
    profiles = get_freelancer_profiles(lock)
    if not profiles:
        MMT.logger()
        from Browser_Scrap_Freelancer_Replyed_Proposals_Users import Browser_Scrap_Replyed_Proposals_Users as Scrapper
        Scrapper()
        profiles = get_freelancer_profiles(lock)
        # MMT.logger.error(f'No Freelancer profiles on db! the script will be stopped')
        # return False
    profiles = profiles['res']
    # print(profiles[1])
    # start browser
    if p_browser == "firefox":
        driver = MMT.FireFoxDriverWithProfile()
    else:
        driver = MMT.ChromeDriverWithProfile()

    driver.get("https://www.freelancer.com/login")
    login_user(driver, freelancer_user)
    random_sleep()
    # check for replies
    for profile in profiles:
        did_reply(driver, p_task_user, profile, lock)

    # check strategy
    if p_task_user["serie_type"] == "non_stop":
        MMT.logger.info(f' Startegy: {p_task_user["serie_type"]}')
        """Keep sending messages"""
        for profile in profiles:
            check_send_message(driver, profile, p_task_user, lock)

    elif p_task_user["serie_type"] == "until_reply":
        MMT.logger.info(f' Startegy: {p_task_user["serie_type"]}')
        """Stops sending messages after a response from user/profile"""
        # updates the data on the list profiles
        profiles = get_freelancer_profiles(lock)
        profiles = profiles['res']
        for profile in profiles:
            # if the user didn't replied check the time delay to send next message
            if profile["replied"] is None or profile["replied"] != 1:
                actions_performed += check_send_message(driver, profile, p_task_user, lock)
            # if the user replied skip to the next user

            # Check daily limit
            if actions_performed >= p_quantity_limit:
                MMT.logger.info(f'Daily limit atteined - Actions performed: {actions_performed} | '
                                f'Daily Limit: {p_task_user["daily_limit"]}')
                logout_user(driver)
                driver.quit()
                return True

        # if if the daily limit wasn't atteined, send 1st message all in first_message_queue
    if len(first_message_queue) > 0:
        MMT.logger.info(f'Sending 1st message to profiles')
    for profile in first_message_queue:
        actions_performed += send_message(driver, profile, p_task_user, lock, first_message=True)
        if actions_performed >= p_quantity_limit:
            MMT.logger.info(f'Daily limit atteined - Actions performed: {actions_performed} | '
                            f'Daily Limit: {p_task_user["daily_limit"]}')
            logout_user(driver)
            driver.quit()
            return True

    # Logout and close browser
    logout_user(driver)
    driver.quit()


# ======================================================================================================================

# Queue to store de profiles that didn't received 1st message
#first_message_queue = []
# Call function Browser_Cold_Messaging_Freelancer_Replied_Proposals
"""
freelancer_user = ['', '']
p_quantity_limit = 5
lock = threading.Lock()
p_browser = "firefox"
p_task_user = MMT.GetDetailsTaskUser(250)
Browser_Cold_Messaging_Freelancer_Replyed_Proposals(p_browser, p_task_user, p_quantity_limit, freelancer_user, lock)
"""
