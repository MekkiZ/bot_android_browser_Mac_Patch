# -*- coding: utf-8 -*-

"""
This module contain some modules from mymodulesteam.py improved by other developpers
https://github.com/phonebotco/phonebot
"""
import sys
import base64
import configparser
import ctypes
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import datetime, timedelta
from datetime import time
import io
import logging
import os
import random
import re
import shutil
import sqlite3
import subprocess
import time
import webbrowser
import mysql.connector
import pytesseract
from PIL import Image
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver import ActionChains, DesiredCapabilities
import pathlib
import platform
import psutil
from google.oauth2 import \
    service_account  # pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
import google_auth_httplib2


def LoadFile(p_file):
    # 1rst we need to split the filename in name and extension
    p_file_split = str(p_file).split('.')
    p_name = p_file_split[0]
    if len(p_file_split) == 2:
        p_ext = p_file_split[1]
    elif len(p_file_split) == 1:
        p_ext = None
    elif len(p_file_split) > 2:
        p_name = ''
        for i in range(0, len(p_file_split) - 2):
            p_name += p_file_split[i]
        p_ext = p_file_split[len(p_file_split) - 1]

    # Let's create the HOME/PhoneBot directory

    # print(f"p_name :{p_name}")
    # print(f"p_ext :{p_ext}")
    if platform.system() == 'Darwin':
        from AppKit import NSBundle
        # FOR MAC WE NEED FULL PATH, SO LET's PREPARE IT
        HOME_DIR = os.environ['HOME']
        # If folder /PhoneBot in user's home doesn't exist
        if not os.path.isdir(HOME_DIR + '/PhoneBot'):
            os.mkdir(HOME_DIR + '/PhoneBot')
        HOME_PHONEBOT_DIR = HOME_DIR + '/PhoneBot'
        UI_DIR = HOME_PHONEBOT_DIR + '/ui'
        test_if_PhoneBot_app = NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
        # 2 For Mac, we need to check if there we are in Applications/PhoneBot.app or not

        if p_file == 'ui.json':
            # We need to test if ui.json exist in user's home folder, if not we copy paste it
            file_ui_json = pathlib.Path(HOME_PHONEBOT_DIR + '/ui.json')

            print(f"{file_ui_json}  - {type(file_ui_json)}")
            curpath = os.path.abspath(os.curdir)
            print(f"curpath : {curpath}")
            print(f"HOME_PHONEBOT_DIR + '/ui.json' : {HOME_PHONEBOT_DIR + '/ui.json'}")
            if not file_ui_json.exists():

                shutil.copyfile(curpath + '/ui.json', HOME_DIR + '/ui.json')
            elif file_ui_json.exists():
                # If ui.json in program folder is more recent that ui.json of home folder,
                # we copy paste the most recent
                mtime_uijson_home = os.path.getmtime(HOME_PHONEBOT_DIR + '/ui.json')
                mtime_uijson_program = os.path.getmtime(curpath + '/ui.json')

                if mtime_uijson_home < mtime_uijson_program:
                    shutil.copy(curpath + '/ui.json', HOME_PHONEBOT_DIR + '/ui.json')
                    # shutil.move(os.path.join(curpath , 'ui.json'), os.path.join(HOME_DIR, 'ui.json'))
                    logger.info(f"ui.json file was copied from application folder to home folder")
                else:
                    logger.info(
                        f"ui.json file from your home directory is more recent than the one in applications folder")

        if test_if_PhoneBot_app is None:
            # WE ARE NOT IN PHONEBOT APP
            # ALSO WE HAVE 2 KINDS OF FILES: THE ONES WE READ ONLY AND THE ONES WE WILL MODIFY
            # FOR THE ONES WE MODIFY OR CREATE, WE NEED TO CHANGE LOCATION TO HOME/PhoneBot
            if p_file == 'log.log' or p_file == 'db.db' or p_file == 'config.ini' or p_file == 'tmp.txt' or p_file == 'ui.txt' \
                    or p_file == 'appium.log' or p_file == 'appium.zip' or p_file == 'log.zip':
                # WE NEED TO CHECK IF THE FOLDER HOME/PhoneBot
                result = HOME_PHONEBOT_DIR + '/' + p_file
            # elif p_file == 'ui.json':
            #     # WE NEED TO CHECK IF THE FOLDER HOME/PhoneBot exist or not
            #     result = HOME_PHONEBOT_DIR + '/' + p_file
            else:
                result = p_file
        else:
            # WE ARE IN PHONEBOT APP
            # ALSO WE HAVE 2 KINDS OF FILES: THE ONES WE READ ONLY AND THE ONES WE WILL MODIFY
            # FOR THE ONES WE MODIFY OR CREATE, WE NEED TO CHANGE LOCATION TO HOME/PhoneBot
            if p_file == 'log.log' or p_file == 'db.db' or p_file == 'config.ini' or p_file == 'tmp.txt' or p_file == 'ui.txt' \
                    or p_file == 'appium.log' or p_file == 'appium.zip' or p_file == 'log.zip':

                # print(f"p_file is : {p_file}")
                # WE NEED TO CHECK IF THE FOLDER HOME/PhoneBot
                result = NSBundle.mainBundle().pathForResource_ofType_(HOME_PHONEBOT_DIR + '/' + p_name, p_ext)
                # print(f"result for log,db,config: {result}")

            # elif p_file == 'ui.json':
            #
            #     print(f"p_file is : {p_file}")
            #     #result = NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
            #     result = NSBundle.mainBundle().pathForResource_ofType_(HOME_PHONEBOT_DIR + '/' + p_name, p_ext)
            #     print(f"result for ui.json: {result}")
            else:
                # print(f"p_file is : {p_file}")
                result = NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
                # print(f"result for else : {result}")
    else:
        if os.path.isfile(p_file):
            print(f"{p_file} File exists")
            print(os.path.abspath(p_file))
        result = p_file

    # print(f"result : {result}")
    return result


open(LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__mymodulesteam__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ================================================================================
# FUNCTION DE CREATION DE DRIVER CHROME OU FIREFOX


def all_subdirs_of(b='.'):
    """
    This function return all the subdorectories of a directory
    """

    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd): result.append(bd)
    return result


def KillProgram(p_program):
    logger.info(
        f"=================================== KillProgram {p_program} ===========================================")
    if platform.system() == 'Windows':
        PROCNAME = p_program + ".exe"
        # print(f"PROCNAME : {PROCNAME}")


    elif platform.system() == 'Darwin':
        PROCNAME = p_program

    elif platform.system() == 'Linux':
        PROCNAME = p_program

    for proc in psutil.process_iter():
        # print(f"proc.name() : {proc.name()}")

        #if proc.name() == PROCNAME:
        if p_program in proc.name():
            # print(proc)
            # print(f"PhoneBot will kill this process : {proc}")
            try:
                proc.kill()
            except Exception as ex:
                logger.error(f"{ex} - PhoneBot couldn't kill the process")



def ChromeDriverWithProfile():
    """
    This function will return the chrome driver with the Chrome profile loaded
    """
    # We need to close all the instances of Chrome or it will bug
    KillProgram('chrome')

    if platform.system() == 'Linux':
        chrome_profile_path = os.environ['HOME'] + "/.config/google-chrome"
        chrome_profile_path = os.path.expandvars(chrome_profile_path)
    else:
        chrome_profile_path = r"/Users/miklar/Library/Application Support/Google/Chrome"
        #%LocalAppData%\Google\Chrome\User Data
        chrome_profile_path = os.path.expandvars(chrome_profile_path)

    print(f"chrome_profile_path : {chrome_profile_path}")
    chrome_options = Options()

    chrome_options.add_argument(r"--user-data-dir=" + chrome_profile_path)
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-session-crashed-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # overcome limited resource problems
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Bypass OS security model
    chrome_options.add_argument("--no-sandbox")
    # We need to remove the bubble popup 'Restore pages' of Chrome:
    # https://dev.to/cuongld2/get-rid-of-chrome-restore-bubble-popup-when-automate-gui-test-using-selenium-3pmh
    if platform.system() == 'Linux' or 'macOS':
        preference_file = chrome_profile_path + "/Default/Preferences"
    else:
        preference_file = chrome_profile_path + "\\Default\\Preferences"
    string_to_be_change = '"exit_type":"Crashed"'
    new_string = '"exit_type": "none"'
    # read input file
    fin = open(preference_file, "rt")
    # read file contents to string
    data = fin.read()
    # replace all occurrences of the required string
    data = data.replace(string_to_be_change, new_string)
    # close the input file
    fin.close()
    # open the input file in write mode
    fin = open(preference_file, "wt")
    # overrite the input file with the resulting data
    fin.write(data)
    # close the file
    fin.close()

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver


def FireFoxDriverWithProfile():
    print("==================== FireFoxDriverWithProfile =======================")
    """
    This function will return the chrome driver with the FireFox profile loaded
    """
    # We need to close all the instances of Firefox or it will bug
    KillProgram('firefox')

    if platform.system() == 'Linux':
        firefox_profile_folder_path = appdata = os.environ['HOME'] + "/.mozilla/firefox"  # Profile folder path on Linux

        # On linux, there is no 'Profiles' folder, so we need to filter only the profile folders
        # We remove the folders we don't want from the list
        subdirs = all_subdirs_of(firefox_profile_folder_path)
        for subdir in subdirs:
            if "Crash Reports" in subdir or "Pending Pings" in subdir:
                subdirs.remove(subdir)
        latest_profile = max(subdirs, key=os.path.getmtime)
    else:
        firefox_profile_folder_path = appdata = os.environ['APPDATA'] + "\Mozilla\Firefox\Profiles"
        latest_profile = max(all_subdirs_of(firefox_profile_folder_path), key=os.path.getmtime)
    print(f"profile : {latest_profile}")
    profile = FirefoxProfile(latest_profile)
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile,
                               desired_capabilities=desired)

    print(f"profile : {profile}")

    return driver


def GetDetailsTaskUser(p_taskuser_id):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # Connect to SQLITE
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_connection.row_factory = dict_factory
    sqlite_cursor = sqlite_connection.cursor()
    taskuser_details_dico = sqlite_cursor.execute("SELECT id,enable,id_task,id_campaign,url_keywords,minimum,url_list,  \
            url_usernames,message_txt_invitation_1B,message_txt_1A,message_txt_2A,message_txt_3A,message_txt_4A,  \
            message_voice_1A,message_voice_2A,message_voice_3A,message_voice_4A,message_txt_invitation_1A,message_txt_1B,  \
            message_txt_2B,message_txt_3B,message_txt_4B,message_voice_1B,message_voice_2B,message_voice_3B,  \
            message_voice_4B,date_counter_test_AB,time_delay_1A,time_delay_1A_type,time_delay_2A,time_delay_2A_type,  \
            time_delay_3A,time_delay_3A_type,time_delay_1B,time_delay_1B_type,time_delay_2B,time_delay_2B_type,  \
            time_delay_3B,time_delay_3B_type,message_1A_choice,message_2A_choice,message_3A_choice,message_4A_choice,  \
            message_1B_choice,message_2B_choice,message_3B_choice,message_4B_choice,AB_testing_enable,AB_testing_enable_invitation,  \
            date_AB_testing,date_AB_testing_invitation,serie_type,daily_limit  \
            FROM tasks_user where id=?", (p_taskuser_id,)).fetchone()
    return taskuser_details_dico


def random_abc(text_data):
    """
    Function to replace the random_abc synonyms by one word. It will pick up randomly one of the words
    :param text_data:
    :return:
    """
    random_txt_group = re.findall("\{random_abc:(.*?)\}", text_data)
    for random_txt in random_txt_group:
        random_txt_list = random_txt.split('|')
        text_data = text_data.replace('{random_abc:' + random_txt + '}', random.choice(random_txt_list))
    return text_data


# =========================================================================================
# ================================== Google Sheet functions ===============================
# =========================================================================================

def GoogleSheetGetValues(p_sheet_id):
    """
    This function go to Google sheet and get all the values. It will return a list of list like this:
    [['test 1', 'test 2', 'test 3', 'test 4', 'test 5', 'test 6', 'test 7'], ['test 2', 'test 3', 'test 4', 'test 5', 'test 6', 'test 7', 'test 8'], ['test 3', 'test 4', 'test 5', 'test 6', 'test 7', 'test 8', 'test 9'], ['test 4', 'test 5', 'test 6', 'test 7', 'test 8', 'test 9', 'test 10'], ['test 5', 'test 6', 'test 7', 'test 8', 'test 9', 'test 10', 'test 11'], ['test 6', 'test 7', 'test 8', 'test 9', 'test 10', 'test 11', 'test 12'], ['test 7', 'test 8', 'test 9', 'test 10', 'test 11', 'test 12', 'test 13'], ['test 8', 'test 9', 'test 10', 'test 11', 'test 12', 'test 13', 'test 14'], ['test 9', 'test 10', 'test 11', 'test 12', 'test 13', 'test 14', 'test 15'], ['test 10', 'test 11', 'test 12', 'test 13', 'test 14', 'test 15', 'test 16'], ['test 11', 'test 12', 'test 13', 'test 14', 'test 15', 'test 16', 'test 17'], ['test 12', 'test 13', 'test 14', 'test 15', 'test 16', 'test 17', 'test 18'], ['test 13', 'test 14', 'test 15', 'test 16', 'test 17', 'test 18', 'test 19'], ['test 14', 'test 15', 'test 16', 'test 17', 'test 18', 'test 19', 'test 20'], ['test 15', 'test 16', 'test 17', 'test 18', 'test 19', 'test 20', 'test 21'], ['test 16', 'test 17', 'test 18', 'test 19', 'test 20', 'test 21', 'test 22'], ['test 17', 'test 18', 'test 19', 'test 20', 'test 21', 'test 22', 'test 23'], ['test 18', 'test 19', 'test 20', 'test 21', 'test 22', 'test 23', 'test 24'], ['test 19', 'test 20', 'test 21', 'test 22', 'test 23', 'test 24', 'test 25'], ['test 20', 'test 21', 'test 22', 'test 23', 'test 24', 'test 25', 'test 26'], ['test 21', 'test 22', 'test 23', 'test 24', 'test 25', 'test 26', 'test 27'], ['test 22', 'test 23', 'test 24', 'test 25', 'test 26', 'test 27', 'test 28'], ['test 23', 'test 24', 'test 25', 'test 26', 'test 27', 'test 28', 'test 29'], ['test 24', 'test 25', 'test 26', 'test 27', 'test 28', 'test 29', 'test 30']]
    :param p_sheet_id:
    :return:
    """
    service_account_info = {
        "type": "service_account",
        "project_id": "atomic-graph-304910",
        "private_key_id": "4538cd16e5d673542dd1dd46e2091ddba5fe2588",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCGtpIa53bpJU5i\n4mfNnvxvkLfegNkH6Y81hULplUPE0Ckcx6dchcZbMtr0NcdcBHVnFKUBrvyibS03\nUZe829YCIHf1/ynTH8e6PHD4BumJI70YTmURvmjD47+mwLwVkpxFgxJlZROjPmEq\nXJw8pieFXitMewjzx0xe99AB0QSCUsZS64QMy4djKqdNhHbzci/8lcQ1x/7/3Rld\nkcl4J43Rzo6ADwQ+JNlOelu2QdFQwRTn5eCNHUdSvwQL59tgkaPz1ISRZw2lgeml\ncK6KbVPXn7PiVoExu808iRyhSI1KxJrktuGBYxendGRwsLcZ+WiwZkU0TtxjBoDs\nTX+63Qx3AgMBAAECggEAAdb2cdWdYxu2UVVkM4OrUN66FBjQXfJLmWCDhGscbNCm\n7xSu7W2KQu6T3OfrHA+XhtvaUQaRvqodBvdfSh36czb8TGi6qn5xnNJ8fHajs9LA\nH1fau35NMfenQ2C4cNb6uVxL4QSbWwxcCVcQbyeZvJGHp9i6S5H6MgXSWmP/WsQ/\njHBR3ukZZnjR/oqwxh4Hvlh8Gm357ryXwyvB7zZMUhxIbmrQ5eF2ky6GIHf6ZXn7\npNTksnJmEhKjEKaII9gaTir1n6YFmV4Yd56ZX09MIG4kMeWDAUbPQthndLxbnUBX\nGb9JQBbbdWvoBXWf4zf7s2QImT5ZoAGzsnWX0cmcGQKBgQC82tPc4MIne4a6WuMO\ntl91SXlD1hgT4BvguvZD8gXrs/JsMy8alPiPooaGW/fcazONQfDAAZibZpXkOHBI\nWgDibw/M94BOGdVY18vg253TJqNC9LHx+I8wnikWR577XnsydhifBxWSgaLAQFon\nwV+ZAHsWiwvIzxaXSDg7lpW9pQKBgQC2m+JcvMc2RECJ4Gocx9r+GJaCZod78Gix\nseeTjFuLsGwj0POPEzApc5NaEwlaBcQguq8vCQ8/8/eZ4U/gJax1WzfDJ5bfwYkl\nDNaTW6tWb7GbiVQ2U9QS2WTNGoCRLTq4Nd953GGr9/L7CdMr2ezItyVAB6rxuVBk\nBGS0KHI+6wKBgAu2Bi1MQr3wCwrDWBExffnn9H0gaZ3R5+inr13HRFa5ce8DvYgI\ndOFzUqRCT7x7aVb5H9TIRI5ebi0Y0t2ptyRTfsdXEb3GHFTGDP6En+TYIIemZOJ8\nZ2S8ag/XoSQ1V65pZF14Mv5Cy7TgSLbuZt82CGv9c12geeYntFT9oYuBAoGAeixL\nQ26N/fGmGFkLxZu1GcHLmQ0N4k8TTKfRXvdOHGR5xXC8M2JMG7+Wu3H3FMK82ITu\nRhLSoCAS7WJAdZ/fBVl1Ml1fZO7wWdiAC3EObjMmagB0VjC5t6648Tyk/fx7x9lL\nXhWjR1IJwAlvvmv8LsHR60f2B+nLLk9+LMbOwOcCgYAvly6NtvJ6TCjPhsfOlzyg\n1mrg3sKPdL7Mq7+o8PmvvjLGMWjRHnrj7kz0vNL4sslvd0kULvzmiJ1hghSs5FRV\nauwpBRtJp8M/kl1eFGqTHHIM1hmcvaJgrF927dW9B+I+L+tBl27cL9cX2RGDU0LN\ngeWGGHxRAPT0YTlmDdLYug==\n-----END PRIVATE KEY-----\n",
        "client_email": "phonebot-google-service@atomic-graph-304910.iam.gserviceaccount.com",
        "client_id": "103178224643038387088",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/phonebot-google-service%40atomic-graph-304910.iam.gserviceaccount.com"
    }

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials_Google_Sheet_API_Account.json'
    creds = None
    # creds = service_account.Credentials.from_service_account_file(
    #        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    creds = service_account.Credentials.from_service_account_info(service_account_info)

    print(f"service_account_info : {service_account_info}")
    print(f"type service_account_info : {type(service_account_info)}")
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = p_sheet_id
    # https://developers.google.com/sheets/api/quickstart/python

    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    # Call the Sheets API
    sheet = service.spreadsheets()
    try:
        """
        https://stackoverflow.com/a/51852293/10551444
        This sample retrieves the sheet name, the number of last row and last column of data range using sheet index. When 0 is used for the sheet index, it means the first sheet.
        """
        res = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
        sheetIndex = 0
        sheetName = res['sheets'][sheetIndex]['properties']['title']
        lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
        lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])
        # ==================================================
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=f"{sheetName}!a1:{lastColumn}{lastRow}").execute()
        values = result.get('values', [])
        print(values)
        if not values:
            print('No data found.')
            return None
        else:
            return values
    except Exception as ex:
        print(f"ERROR : {ex}")
        if str(ex).find("HttpError 403") != -1:
            PopupMessage("Error Google Sheet!", f"Please share for everyone the Google sheet : {ex}",
                         f"https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}")
            return None


def GoogleSheetAddValues(p_sheet_id, p_list_values):
    """
    This function go to Google sheet and Add t a row of values.
    :param p_sheet_id:
    :return:
    """
    service_account_info = {
        "type": "service_account",
        "project_id": "atomic-graph-304910",
        "private_key_id": "4538cd16e5d673542dd1dd46e2091ddba5fe2588",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCGtpIa53bpJU5i\n4mfNnvxvkLfegNkH6Y81hULplUPE0Ckcx6dchcZbMtr0NcdcBHVnFKUBrvyibS03\nUZe829YCIHf1/ynTH8e6PHD4BumJI70YTmURvmjD47+mwLwVkpxFgxJlZROjPmEq\nXJw8pieFXitMewjzx0xe99AB0QSCUsZS64QMy4djKqdNhHbzci/8lcQ1x/7/3Rld\nkcl4J43Rzo6ADwQ+JNlOelu2QdFQwRTn5eCNHUdSvwQL59tgkaPz1ISRZw2lgeml\ncK6KbVPXn7PiVoExu808iRyhSI1KxJrktuGBYxendGRwsLcZ+WiwZkU0TtxjBoDs\nTX+63Qx3AgMBAAECggEAAdb2cdWdYxu2UVVkM4OrUN66FBjQXfJLmWCDhGscbNCm\n7xSu7W2KQu6T3OfrHA+XhtvaUQaRvqodBvdfSh36czb8TGi6qn5xnNJ8fHajs9LA\nH1fau35NMfenQ2C4cNb6uVxL4QSbWwxcCVcQbyeZvJGHp9i6S5H6MgXSWmP/WsQ/\njHBR3ukZZnjR/oqwxh4Hvlh8Gm357ryXwyvB7zZMUhxIbmrQ5eF2ky6GIHf6ZXn7\npNTksnJmEhKjEKaII9gaTir1n6YFmV4Yd56ZX09MIG4kMeWDAUbPQthndLxbnUBX\nGb9JQBbbdWvoBXWf4zf7s2QImT5ZoAGzsnWX0cmcGQKBgQC82tPc4MIne4a6WuMO\ntl91SXlD1hgT4BvguvZD8gXrs/JsMy8alPiPooaGW/fcazONQfDAAZibZpXkOHBI\nWgDibw/M94BOGdVY18vg253TJqNC9LHx+I8wnikWR577XnsydhifBxWSgaLAQFon\nwV+ZAHsWiwvIzxaXSDg7lpW9pQKBgQC2m+JcvMc2RECJ4Gocx9r+GJaCZod78Gix\nseeTjFuLsGwj0POPEzApc5NaEwlaBcQguq8vCQ8/8/eZ4U/gJax1WzfDJ5bfwYkl\nDNaTW6tWb7GbiVQ2U9QS2WTNGoCRLTq4Nd953GGr9/L7CdMr2ezItyVAB6rxuVBk\nBGS0KHI+6wKBgAu2Bi1MQr3wCwrDWBExffnn9H0gaZ3R5+inr13HRFa5ce8DvYgI\ndOFzUqRCT7x7aVb5H9TIRI5ebi0Y0t2ptyRTfsdXEb3GHFTGDP6En+TYIIemZOJ8\nZ2S8ag/XoSQ1V65pZF14Mv5Cy7TgSLbuZt82CGv9c12geeYntFT9oYuBAoGAeixL\nQ26N/fGmGFkLxZu1GcHLmQ0N4k8TTKfRXvdOHGR5xXC8M2JMG7+Wu3H3FMK82ITu\nRhLSoCAS7WJAdZ/fBVl1Ml1fZO7wWdiAC3EObjMmagB0VjC5t6648Tyk/fx7x9lL\nXhWjR1IJwAlvvmv8LsHR60f2B+nLLk9+LMbOwOcCgYAvly6NtvJ6TCjPhsfOlzyg\n1mrg3sKPdL7Mq7+o8PmvvjLGMWjRHnrj7kz0vNL4sslvd0kULvzmiJ1hghSs5FRV\nauwpBRtJp8M/kl1eFGqTHHIM1hmcvaJgrF927dW9B+I+L+tBl27cL9cX2RGDU0LN\ngeWGGHxRAPT0YTlmDdLYug==\n-----END PRIVATE KEY-----\n",
        "client_email": "phonebot-google-service@atomic-graph-304910.iam.gserviceaccount.com",
        "client_id": "103178224643038387088",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/phonebot-google-service%40atomic-graph-304910.iam.gserviceaccount.com"
    }
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'credentials_Google_Sheet_API_Account.json'
    creds = None
    # creds = service_account.Credentials.from_service_account_file(
    # SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = p_sheet_id
    # https://developers.google.com/sheets/api/quickstart/python
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    # Call the Sheets API
    sheet = service.spreadsheets()

    try:
        """
        https://stackoverflow.com/a/51852293/10551444
        This sample retrieves the sheet name, the number of last row and last column of data range using sheet index. When 0 is used for the sheet index, it means the first sheet.
        """
        res = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                         fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
        sheetIndex = 0
        sheetName = res['sheets'][sheetIndex]['properties']['title']
        # === We need to check if there are some values or not in the spreadsheet
        values_spreadsheet = GoogleSheetGetValues(p_sheet_id)
        print(f"values_spreadsheet : {values_spreadsheet}")
        if values_spreadsheet:
            try:
                lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
                lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])

                # ==================================================
                # The A1 notation of a range to search for a logical table of data.
                # Values will be appended after the last row of the table.
                range_ = f"{sheetName}!A{lastRow}"  # TODO: Update placeholder value.
            except Exception as ex:
                print(f"Error : {ex}")
        else:
            range_ = f"{sheetName}!a1"
        value_range_body = {
            "majorDimension": "ROWS",
            "values": [p_list_values]
        }
        request = service.spreadsheets().values().append(spreadsheetId=p_sheet_id, range=range_,
                                                         valueInputOption='USER_ENTERED',
                                                         insertDataOption='INSERT_ROWS', body=value_range_body)
        response = request.execute()
        # TODO: Change code below to process the `response` dict:
        print(response)
        return True
    except Exception as ex:
        print(f"ERROR : {ex}")
        if str(ex).find("HttpError 403") != -1:
            PopupMessage("Error Google Sheet!", f"Please share for everyone the Google sheet : {ex}",
                         f"https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}")
            return False


# EXEMPLES CODES SQLITE3 PYTHON


# extract spreadsheet id
def extract_ss_id(spread_sheet_url):
    spread_sheet_url = spread_sheet_url.replace('https://docs.google.com/spreadsheets/d/', '')
    ind = spread_sheet_url.index('/')
    spread_sheet_url = spread_sheet_url[:ind]
    # print(spread_sheet_url)
    return spread_sheet_url


# extract spreadsheet id. uses regular expression to identify the id
def extract_ss_id_regex(spread_sheet_url):
    return re.search('/spreadsheets/d/([a-zA-Z0-9-_]+)', spread_sheet_url).group(1)


def ScrollToTheEnd(driver):
    """A method to scroll the page all the way down the bottom of the page until you can't scroll anymore."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    page_end = False
    while page_end == False:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            page_end = True

        last_height = new_height


def scrollPopup(class_name, driver):
    # Scrolls any popups. Take the popup class name as an argument
    # Simulate scrolling to capture all posts
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    js_code = "return document.getElementsByClassName('{}')[0].scrollHeight".format(class_name)
    last_height = driver.execute_script(js_code)

    while True:
        # Scroll down to bottom
        path = "//div[@class='{}']".format(class_name)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", driver.find_element_by_xpath(path))

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(js_code)
        if new_height == last_height:
            break
        last_height = new_height


# FONCTION TO TRANSFORM AND PREPARE THE MESSAGE BEFORE TO SEND IT
def TransformMessage(msg=None, **kwargs):
    # Replaces the random text
    if not msg.__contains__("random_abc"):
        return (str(msg), "Undefined Message")[msg == '']
    random_txt_group = re.findall("{random_abc:(.*?)}", msg)
    for random_txt in random_txt_group:
        random_txt_list = random_txt.split('|')
        msg = msg.replace('{random_abc:' + random_txt + '}', random.choice(random_txt_list))

    # Replaces user details
    for key in kwargs:
        if msg.__contains__(key):
            place_holder = '{' + key + '}'
            # print(rpl)
            msg = msg.replace(place_holder, kwargs.get(key))
    return msg


def TransformMessageTMP(old_message, p_firstname='', p_username=''):
    """
    This function will convert the placeholders:
        {firstname},
        {username},
        These values are in table 'contacts'

        {random_abc},
        These values are in the placeholder


        {affiliate_code},
        {affiliate_url},
        {affiliate_coupon}
        These values will be handle by us
    """

    new_message = random_abc(old_message)
    new_message = new_message.replace("""{firstname}""", p_firstname).replace("""{username}""", p_username)

    print(f"new_message : {new_message}")
    return new_message


# FUNCTION FOR GOOGLE LINKEDIN PROFILES SEARCH

def NumberHoursLastAction(p_myprofile, p_platform, p_type_action):
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    list_of_dates_of_post_picture = p_cursor1.execute(
        "SELECT date FROM actions WHERE id_social_account=? AND platform=? and type_action=?",
        (p_myprofile, p_platform, p_type_action)).fetchall()
    print(f"list_of_dates_of_post_picture : {list_of_dates_of_post_picture}")
    list_date = []
    for date_picture in list_of_dates_of_post_picture:
        date = datetime.strptime(date_picture[0], "%d/%m/%Y %H:%M:%S")
        print(f"date : {date}")
        list_date.append(date)

    print(f"oldest date = {min(list_date)}")
    print(f"most recent date = {max(list_date)}")
    most_recent_date = max(list_date)

    now = datetime.now()
    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    difference_between_most_recent_and_now = now - most_recent_date
    print(f"difference_between_most_recent_and_now = {difference_between_most_recent_and_now}")
    print(f"hours = {difference_between_most_recent_and_now.total_seconds() / 3600}")
    return difference_between_most_recent_and_now.total_seconds() / 3600


# MODULES FOR prepare_env_appium


def GetPathFromDB(name):
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()

    value_tuple = cursor.execute("SELECT " + name + " FROM settings").fetchone()
    if value_tuple:
        value = value_tuple[0]
        print(f"value_tuple : {value_tuple}")
        print(f"value : {value}-{type(value)}")

        if value is not None and value != '':
            logger.info(f"PhoneBot found a path for {name} in local database.")
            if name != 'build_tools':
                if os.path.isfile(value):
                    return value
                else:
                    return None
            else:
                if os.path.isdir(value):
                    if cursor:
                        cursor.close()
                    if sqlite_connection:
                        sqlite_connection.close()
                    return value

                else:
                    if cursor:
                        cursor.close()
                    if sqlite_connection:
                        sqlite_connection.close()
                    return None


        else:
            logger.info(f"PhoneBot didn't find a path for {name} in local database.")
            if cursor:
                cursor.close()
            if sqlite_connection:
                sqlite_connection.close()
            return None
    else:
        logger.info(f"PhoneBot didn't find a path for {name} in local database.")
        if cursor:
            cursor.close()
        if sqlite_connection:
            sqlite_connection.close()
        return None


#####################################################################################
#              METHOD TO DISPLAY A POPUP MESSAGE                                    #
#####################################################################################
def PopupMessage(p_title, p_message, link=''):
    """
    This method is to show an alert popup message
    :param p_title:
    :param p_message:
    :return:
    https://stackoverflow.com/questions/34840838/how-to-specify-what-actually-happens-when-yes-no-is-clicked-with-ctypes-messageb
    MB_OK = 0
    MB_OKCANCEL = 1
    MB_YESNOCANCEL = 3
    MB_YESNO = 4

    IDOK = 1
    IDCANCEL = 2
    IDABORT = 3
    IDYES = 6
    IDNO = 7
    """
    if platform.system() == 'Windows':
        if link != '':
            result = ctypes.windll.user32.MessageBoxW(0, p_message, p_title, 4)
            if result == 6:
                # Open the Google spreadhseet
                print("user pressed ok")
                webbrowser.open(link)
            elif result == 7:
                print("user pressed no")
        else:
            ctypes.windll.user32.MessageBoxW(0, p_message, p_title, 1)

    elif platform.system() == 'Darwin':
        os.system(
            f"""osascript -e \'Tell application \"System Events\" to display dialog \"{p_message}\"with icon caution with title \"{p_title}\"' """)
    elif platform.system() == 'Linux':
        # p_message = p_message.replace("\n", "")
        os.system(f"notify-send \"{p_title}\" \"{p_message}\"")


def TestIfInstalled(p_command):
    # This function will run a shell command to test if program is installed
    # Very often, it will be a 'program --version' command
    proc = subprocess.Popen(p_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            stderr=subprocess.STDOUT, close_fds=True)
    output = ""
    if "build-tools;28.0.3" in p_command:
        output = proc.communicate(input=b'y')[0]
    returncode = proc.wait()
    print(f'returncode : {returncode} - {type(returncode)}')
    if not "build-tools;28.0.3" in p_command:
        output = proc.stdout.read()
    try:
        output = output.decode('utf-8', errors='ignore')
    except Exception as ex:
        logger.error(f"error with output decode UTF-8: {ex}")
    #
    # print(f"output : {output} returncode : {returncode}")
    if returncode != 0:
        return False
    else:
        if p_command.find("java") != -1:
            # We need to be sure it is Java8 minimum
            # position of jre folder:
            pos_jre1 = output.find('java version "')
            output_lines = output.split("\n")
            if pos_jre1 != -1:
                tmp_string = output[pos_jre1 + 14:]

                # Extract the version number
                print(f"tmp_string : {tmp_string}")
                numbers = ""
                for word in tmp_string:
                    print(f"word : {word}")
                    if word.isdigit():
                        numbers += word
                print(f"numbers : {numbers}")
                first_digit = numbers[0:1]
                print(f"first_digit : {first_digit}")
                if int(first_digit) == 1:
                    first_digit = numbers[1:2]

                if int(first_digit) > 3:
                    version_java = first_digit
                    print(f"version_java : {version_java}")
                else:
                    version_java = numbers[0:2]
                    print(f"version_java : {version_java}")
                if int(version_java) < 8:
                    java_folder_found = False
                    logger.critical("ERROR : Your version of Java is too old. Please update your Java.")
                    PopupMessage("Error Java!", "Your version of Java is too old. Please update your Java.")
                    sys.exit()

                else:
                    return True
            elif len(output_lines[0].split(" ")) == 3:
                output_split = output.split(" ")
                if '.' in output_split[1]:
                    print(f"Java version: {output_split[1]}")
                    java_version = output_split[1].split('.')
                    if int(java_version[0]) < 8:
                        logger.critical("ERROR : Your version of Java is too old. Please update your Java.")
                        PopupMessage("Error Java!", "Your version of Java is too old. Please update your Java.")
                        sys.exit()
                    else:
                        return True
        elif p_command.find("tesseract --list-langs") != -1:
            if "fra" in output:
                return True
            else:
                logger.info("French language not installed in tesseract.")
                return False
        else:
            return True


# ==================================================================================================
# APPIUM MODULES & FUNCTIONS


# ========================================================================================================
# ==================  FUNCTION TO GET THE TEXT DISPLAYED IN SCREEN  =====================================
# ========================================================================================================
def GetTextfromScreenshot(p_driver='driver', p_udid='nophone_id', p_element='', p_mode=''):
    try:
        logger.info(
            f"{p_udid}|||# ================= Make Screenshot and get text with GetFacebookTextfromScreenshot =============")
        if p_element is None:
            imagestring = p_driver.get_screenshot_as_base64()
        else:
            imagestring = p_element.screenshot_as_base64

        if p_mode == 'username_from_list':
            # Size of the image in pixels(size of orginal image)
            # (This is not mandatory)
            image_string = io.BytesIO(base64.b64decode(imagestring))
            im = Image.open(image_string)
            width, height = im.size
            # Setting the points for cropped image
            left = width * 0.235
            top = 0
            right = width * 0.847
            bottom = height
            print(f"{left}, {top}, {right}, {bottom}")
            # Cropped image of above dimension
            # (It will not change orginal image)
            image = im.crop((left, top, right, bottom))
        else:
            # pic = io.StringIO()
            image_string = io.BytesIO(base64.b64decode(imagestring))
            image = Image.open(image_string)
            # image.show()
        # print(pytesseract.image_to_string(image, lang='fra'))
        # tessdata_dir_config=r'--tessdata-dir "' + os.environ["TESSDATA_PREFIX"] + '"'
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        tesseract_command = sqlite_cursor.execute("SELECT tesseract FROM settings").fetchone()

        pytesseract.pytesseract.tesseract_cmd = tesseract_command[0]
        return pytesseract.image_to_string(image)
        # return pytesseract.image_to_string(image, lang='fra')
    # except ValueError:
    # print("error")
    except Exception as ex:

        logger.critical(
            f'''{p_udid}|||{ex} --> #ERROR! Something went wrong while making screenshot and OCR. Please check :\n
                                - you installed 'tesseract' for Windows => https://tesseract-ocr.github.io/tessdoc/4.0-with-LSTM.html#400-alpha-for-windows\n
                                - you download the french training file data => https://github.com/tesseract-ocr/tessdata/blob/master/fra.traineddata
                                - you place this french language data in the 'tessdata' folder(ex: C:\Program Files\Tesseract-OCR\\tessdata)\n
                                - you add the 'tesseract' folder in your environment variables.                        
                        ''')


# =============================================================================================================


# =====================================================================================================
#                                     UI LOG MESSAGE ERRORS
# ====================================================================================================

def DisplayMessageLogUI(p_label_log, p_text, p_color="Black", p_tab="run"):
    """
    This function will append a message line in the label_log
    THis is very useful for users
    :param p_label_log:
    :param p_text:
    :return:
    """
    print("================================= DisplayMessageLogUI ===========================================")
    if p_tab == "run_one_task":
        max_lines = 24
    elif p_tab == "run":
        max_lines = 8

    try:
        # !!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Je devrais décommenter cette ligne ci-dessous. Je l'ai désactivé le 05/07/21 pour que les développeurs
        # (qui n'ont pas l'UI) puisse executer le script
        # tmp=p_label_log.text()
        tmp = ""  # Parcontre je devrais commenter cette ligne
        # === WE NEED TO COUNT THE LINES
        counter_lines_1 = tmp.count('<br>')
        counter_lines_2 = tmp.count('<br/>')
        # print(f"tmp : {tmp} - {type(tmp)}")
        # print(f"counter_lines_2 : {counter_lines_2}")
        # print(f"counter_lines_1 : {counter_lines_1}")
        # print("-------------------------------------------------------------")
        if counter_lines_1 + counter_lines_2 > max_lines:
            # print(f"counter_lines_1 + counter_lines_2 : {counter_lines_1 + counter_lines_2}")
            pos_end_first_line_1 = tmp.find('<br>')
            pos_end_first_line_2 = tmp.find('<br/>')
            # print(f"pos_end_first_line_1 = {pos_end_first_line_1} - {type(pos_end_first_line_1)}")
            # print(f"pos_end_first_line_2 = {pos_end_first_line_2} - {type(pos_end_first_line_2)}")
            # We have only 1 <br>
            if pos_end_first_line_1 != -1 and pos_end_first_line_2 == -1:
                new_pos = pos_end_first_line_1 + 4
                # print(f"new_pos : {new_pos}")
                tmp2 = tmp[new_pos:]
                tmp = tmp2
                # print(f"We have only 1 <br> : {tmp}")

            # We have only 2 <br/>
            elif pos_end_first_line_1 == -1 and pos_end_first_line_2 != -1:
                new_pos = pos_end_first_line_2 + 5
                # print(f"new_pos : {new_pos}")
                tmp2 = tmp[new_pos:]
                tmp = tmp2
                # print(f"We have only 2 <br/> : {tmp}")

            # We have both 1 & 2 <br><br/>
            elif pos_end_first_line_1 != -1 and pos_end_first_line_2 != -1:
                if pos_end_first_line_1 < pos_end_first_line_2:
                    new_pos = pos_end_first_line_1 + 4
                    # print(f"new_pos : {new_pos}")
                    tmp2 = tmp[new_pos:]
                    tmp = tmp2
                    # print(f" We have both 1 & 2 <br><br/>: {tmp}")
                else:
                    new_pos = pos_end_first_line_2 + 5
                    # print(f"new_pos : {new_pos}")
                    tmp2 = tmp[new_pos:]
                    tmp = tmp2
                    # print(f" We have both 1 & 2 <br><br/>: {tmp}")


            # We have none 1 & 2 <br><br/>
            elif pos_end_first_line_1 == -1 and pos_end_first_line_2 == -1:
                # print("There is no lines. We need to remove all if there is a lot of text.")
                if len(tmp) > 250:
                    tmp2 = ""
                    tmp = tmp2
                    # print(f"We have none 1 & 2 <br><br/> and >150: {tmp}")

        # print("------------------- MAKE CONCATENATION -----------------------")
        tmp += f'<br><span style="color:{p_color}">' + p_text + '</span>'
        # print(f"Result : {tmp}")

        # !!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Je devrais décommenter cette ligne ci-dessous. Je l'ai désactivé le 05/07/21 pour que les développeurs
        # (qui n'ont pas l'UI) puisse executer le script
        # p_label_log.setText(tmp)
    except Exception as ex:
        logger.error(f"Error DisplayMessageLogUI : {ex}")


def GetQuantityActions(p_taskuser_id, p_username):
    """
    This function will check in SQLITE3 DB if user can still run some actions and how much
    It is a difficult method because we need to check many stuff.

    1rst we need to get the id_task and get the hourly and daily limits
    Here is a table of the hourly limits:
        For MESSAGE:
            Leboncoin => 5/h
            Facebook, Instagram, Twitter, Freelancer, Upwork, Reddit, Gmap => 10/h
            Linkedin, Whatsapp, Telegram => 20/h

        For SCRAPE:
            Facebook, Instagram, Twitter, Freelancer, Upwork, Reddit, Gmap, Linkedin, Whatsapp, Telegram => 50/h
            Craigslist, Leboncoin, Yellowpage => 500/h

        For Follow:
            Facebook, Instagram, Twitter, Snapshat, TikTok => 15/h

        For Adding Friends/contacts
            Facebook, Instagram, Twitter, Linkedin, Snapshat, Tiktok => 25/h
    Anyway, we get it from the table W551je5v_pb_tasks


    We will need to get the type task:
        1	Message
        2	Voice Message
        3	Scrape
        5	Publish Post
        6	Share Post
        7	Follow
        8	Unfollow
        9	Like
        12	Add Friends


    2nd we need to get the quantity of actions already done for this username on this platform in the last 1h and 24h


    :param p_taskuser_id:
    :param p_username:
    :return:
    """
    logger.info(
        f"# ======== GetQuantityActions ========= GET THE LIMITS {p_taskuser_id} - {p_username} ==========================")
    # ===================== DATABASES ===========================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    mysql_connection, mysql_cursor = get_mysql_connection()

    # ==================== GET id_task ==========================
    id_task = GetIDTask(p_taskuser_id)
    # Get details of task
    name_task, daily_limit, hourly_limit, id_type_task, id_platform = GetDetailsTask(p_taskuser_id)
    # Get the name of platform
    platform_name_tmp = GetPlatformName(id_platform)
    platform_name = str(platform_name_tmp).lower()
    print(f"""
    hourly_limit = {hourly_limit}
    daily_limit = {daily_limit}
    id_task = {id_task}
    id_type_task = {id_type_task}
    id_platform = {id_platform}
    platform_name {platform_name}

    """)

    # PREPARE THE STRING TO SEARCH IN SQLITE3 ACCORDING TO THE id_type_task
    if id_type_task == 1:
        string_to_search = "message"
    elif id_type_task == 2:
        string_to_search = "message"
    elif id_type_task == 3:
        string_to_search = "scrap"
    elif id_type_task == 5:
        string_to_search = "post"
    elif id_type_task == 6:
        string_to_search = "follow"
    elif id_type_task == 7:
        string_to_search = "unfollow"
    elif id_type_task == 8:
        string_to_search = "like"
    elif id_type_task == 9:
        string_to_search = "message"
    elif id_type_task == 12:
        string_to_search = "add"

    # ====================== CALCULATE ACTIONS DONE ALREADY ==========================
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    one_hour_ago = now - timedelta(hours=1)
    print(f"""
    now = {now}
    yesterday = {yesterday}
    one_hour_ago = {one_hour_ago}
    """)

    actions_done_last_1H_tuple = sqlite_cursor.execute("SELECT COUNT(*) FROM actions WHERE platform LIKE ? AND  \
        id_social_account LIKE ? AND type_action LIKE ? AND date_created >?", \
                                                       (
                                                           f"%{platform_name}%", f"%{p_username}%",
                                                           f"%{string_to_search}%",
                                                           one_hour_ago)).fetchall()
    actions_done_last_24H_tuple = sqlite_cursor.execute("SELECT COUNT(*) FROM actions WHERE platform LIKE ? AND  \
        id_social_account LIKE ? AND type_action LIKE ? AND date_created >?", \
                                                        (f"%{platform_name}%", f"%{p_username}%",
                                                         f"%{string_to_search}%", yesterday)).fetchall()
    actions_done_last_1H = actions_done_last_1H_tuple[0][0]
    actions_done_last_24H = actions_done_last_24H_tuple[0][0]
    print(f"""
    actions_done_last_1H_tuple = {actions_done_last_1H_tuple}
    actions_done_last_24H_tuple = {actions_done_last_24H_tuple}
    actions_done_last_1H = {actions_done_last_1H}
    actions_done_last_24H = {actions_done_last_24H}
    """)

    # Now let's calculate the quantity of actions possible today
    quantity_actions_possible_today = int(daily_limit) - int(actions_done_last_24H)
    if quantity_actions_possible_today > 0:
        # Now let's calculate the quantity of actions possible this hour
        quantity_actions_possible_this_hour = hourly_limit - actions_done_last_1H
        if quantity_actions_possible_this_hour > 0:
            logger.info(f"User {p_username} can make {quantity_actions_possible_this_hour} actions now")
            #if quantity_actions_possible_this_hour > 10:
            #    quantity_actions_possible_this_hour = 10

            try:
                mysql_cursor.close()
                mysql_connection.close()
            except Exception as ex:
                logger.error(f"Error closing mysql : {ex}")

            return quantity_actions_possible_this_hour
        else:
            try:
                mysql_cursor.close()
                mysql_connection.close()
            except Exception as ex:
                logger.error(f"Error closing mysql : {ex}")

            return 0
    else:

        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return 0


# =========================  MAKE A FUNCTION TO GET THE MYSQL CONNECTION  ==========================================
def get_mysql_connection():
    """
    THis function will return the connection and cursor of our Mysql database
    """
    while True:
        try:
            mysql_connection = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            mysql_cursor = mysql_connection.cursor(dictionary=True)
            break

        except Exception as ex:
            PopupMessage("Error Database!",
                         f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

            logger.info(
                f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

    return mysql_connection, mysql_cursor


# =============================================================================================================


def GetIDTask(p_taskuser_id):
    print(f"======================== GetIDTask {p_taskuser_id} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection()
        SQL_GET_ID_TASK = f"SELECT id_task FROM W551je5v_pb_tasks_users WHERE id={p_taskuser_id}"
        mysql_cursor.execute(SQL_GET_ID_TASK)
        id_task_dic = mysql_cursor.fetchone()
        id_task = int(id_task_dic['id_task'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return id_task
    except Exception as ex:
        logger.error(f"ERROR GetIDTask : {ex}")


def GetIDTaskUser(p_campaign_id, p_task_id):
    print(f"======================== GetIDTaskUser {p_campaign_id} {p_task_id} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection()
        SQL_GET_ID_TASKUSER = f"SELECT id FROM W551je5v_pb_tasks_users WHERE id_task={p_task_id} and id_campaign={p_campaign_id}"
        mysql_cursor.execute(SQL_GET_ID_TASKUSER)
        id_taskuser_dic = mysql_cursor.fetchone()
        id_taskuser = int(id_taskuser_dic['id'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return id_taskuser
    except Exception as ex:
        logger.error(f"ERROR GetIDTask : {ex}")


def GetDetailsTask(p_id_task_user):
    print(f"======================== GetDetailsTask from TaskUser_id {p_id_task_user} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection()
        SQL_GET_DETAILS_TASK = f"SELECT W551je5v_pb_tasks.name,W551je5v_pb_tasks_users.daily_limit,W551je5v_pb_tasks.hourly_limit,W551je5v_pb_tasks.id_type_task,W551je5v_pb_tasks.id_platform FROM W551je5v_pb_tasks INNER JOIN W551je5v_pb_tasks_users ON W551je5v_pb_tasks.id=W551je5v_pb_tasks_users.id_task WHERE W551je5v_pb_tasks_users.id={p_id_task_user}"
        print(f"SQL_GET_DETAILS_TASK : {SQL_GET_DETAILS_TASK}")
        mysql_cursor.execute(SQL_GET_DETAILS_TASK)
        dico = mysql_cursor.fetchone()
        print(f"dico : {dico}")
        hourly_limit = int(dico['hourly_limit'])
        daily_limit = int(dico['daily_limit'])
        id_type_task = int(dico['id_type_task'])
        id_platform = int(dico['id_platform'])
        name_task = str(dico['name'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

        return name_task, daily_limit, hourly_limit, id_type_task, id_platform

    except Exception as ex:
        logger.error(f"ERROR GetDetailsTask : {ex}")


def GetDetailsTypeTask(p_id_type_task):
    """
    This function return the name of the social platform by id_taskuser
    :param p_id_type_task:
    :return:
    """
    print(f"======================== GetDetailsTypeTask {p_id_type_task} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection()

        SQL_GET_TYPE_TASK = f"SELECT name FROM W551je5v_pb_type_tasks WHERE id={p_id_type_task}"
        mysql_cursor.execute(SQL_GET_TYPE_TASK)
        name_type_task_dic = mysql_cursor.fetchone()
        name_type_task = str(name_type_task_dic['name'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return name_type_task
    except Exception as ex:
        logger.error(f"ERROR GetDetailsTypeTask : {ex}")


def GetPlatformName(p_id_platform):
    """
    This function return the name of the social platform by id_taskuser
    :param p_id_platform:
    :return:
    """
    print(f"======================== GetPlatformName {p_id_platform} ===========================")

    mysql_connection, mysql_cursor = get_mysql_connection()
    # Get the name of platform
    SQL_GET_PLATFORM_NAME = f"SELECT name FROM W551je5v_pb_platforms WHERE id={p_id_platform}"
    mysql_cursor.execute(SQL_GET_PLATFORM_NAME)
    platform_name_dic = mysql_cursor.fetchone()
    platform_name = str(platform_name_dic['name'])
    try:
        mysql_cursor.close()
        mysql_connection.close()
    except Exception as ex:
        logger.error(f"Error closing mysql : {ex}")
    return platform_name


def GetDetailsTaskUserMysql(p_taskuser_id):
    """
    This function will return a dictionnary with all the details of task _ser
    :param p_taskuser_id:
    :return:
    """
    mysql_connection, mysql_cursor = get_mysql_connection()

    mysql_cursor.execute(f"SELECT id,enable,id_task,id_campaign,url_keywords,minimum,url_list,  \
                url_usernames,message_txt_invitation_1B,message_txt_1A,message_txt_2A,message_txt_3A,message_txt_4A,  \
                message_voice_1A,message_voice_2A,message_voice_3A,message_voice_4A,message_txt_invitation_1A,message_txt_1B,  \
                message_txt_2B,message_txt_3B,message_txt_4B,message_voice_1B,message_voice_2B,message_voice_3B,  \
                message_voice_4B,date_counter_test_AB,time_delay_1A,time_delay_1A_type,time_delay_2A,time_delay_2A_type,  \
                time_delay_3A,time_delay_3A_type,time_delay_1B,time_delay_1B_type,time_delay_2B,time_delay_2B_type,  \
                time_delay_3B,time_delay_3B_type,message_1A_choice,message_2A_choice,message_3A_choice,message_4A_choice,  \
                message_1B_choice,message_2B_choice,message_3B_choice,message_4B_choice,AB_testing_enable,AB_testing_enable_invitation,  \
                date_AB_testing,date_AB_testing_invitation,serie_type,daily_limit  \
                FROM W551je5v_pb_tasks_users where id={p_taskuser_id}")
    taskuser_details_dico = mysql_cursor.fetchone()

    try:
        mysql_cursor.close()
        mysql_connection.close()
    except Exception as ex:
        logger.error(f"Error closing mysql : {ex}")

    return taskuser_details_dico

# ----------------------------------------------------------------------------------------------------------------
# ================================================================================================================
# =========================================== APPIUM =============================================================
# ================================================================================================================



#==================================================================================================================
#============================ FUNCTION LINKEDIN TO SEARCH FOR LOCATION ============================================
#==================================================================================================================


def send_keys_linkedin_location_delay_random(p_driver,p_udid, controller, p_keys, min_delay=0.7, max_delay=1.45, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(f"{p_udid}|||---------------------------- WE START send_keys_linkedin_location_delay_random function ------------------------------")
    print(f"p_keys : {p_keys}")
    n = 0
    controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
    len_p_keys=len(p_keys)
    for p_key in p_keys:
        print(f"p_key : {p_key}")
        actions = ActionChains(p_driver)
        cpt=0
        while True:
            try:
                actions.move_to_element_with_offset(controller, p_xoffset, 0)

                break
            except Exception as ex:
                cpt+=1
                current_context = p_driver.current_context
                logger.error(f"context : {current_context}")
                p_driver.switch_to.context(current_context)
                logger.error(f"{p_udid}|||{ex} --> send_keys_linkedin_location_delay_random --> We have an error while typing in search field. Let's try again :-)")
                time.sleep(random.uniform(1, 3))
                p_driver.implicitly_wait(15)
                controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
                actions = ActionChains(p_driver)
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(4.9, 6.3))
                if cpt>3:
                    break
        actions.click()
        actions.send_keys(p_key)
        print(f"We just typed '{p_key}'")
        try:
            actions.perform()
            n += 1
        except Exception as ex:
            logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
        time.sleep(random.uniform(min_delay, max_delay))
        #if controller.text==p_keys:

    all_results = p_driver.find_elements_by_id("com.linkedin.android:id/type_ahead_small_no_icon_view_name")
    if len(all_results)!=0:
        area_string_EN = p_keys + " Area"
        area_string_FR = "Région de " + p_keys
        print(f"area_string_EN : {area_string_EN}")
        print(f"area_string_FR : {area_string_FR}")

        for result in all_results:
            if result.text==p_keys:
                result_string= result.text
                result.click()
                return result_string
            elif str(result.text).find(area_string_EN)!=-1:
                result_string = result.text
                result.click()
                return result_string
            elif str(result.text).find(area_string_FR) != -1:
                result_string = result.text
                result.click()
                return result_string
            else:
                logger.info(f"{p_udid}|||We couldn't find the location {p_keys} in search result. Please change the location in your 'Account details' on our website Phonebot.co")
                return ''
            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(0.9, 2.3))



#==================================================================================================================
#============================ FUNCTION LINKEDIN TO SEARCH FOR KEYWORD ============================================
#==================================================================================================================


def send_keys_linkedin_delay_random(p_driver,p_udid, controller, p_keys, min_delay=0.7, max_delay=1.45, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(f"{p_udid}|||---------------------------- WE START send_keys_linkedin_delay_random function ------------------------------")
    print(f"p_keys : {p_keys}")
    p_keys += '\n'
    n = 0
    controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
    len_p_keys=len(p_keys)

    for p_key in p_keys:
        print(f"p_key : {p_key}")
        actions = ActionChains(p_driver)
        while True:
            try:
                actions.move_to_element_with_offset(controller, p_xoffset, 0)

                break
            except Exception as ex:
                current_context = p_driver.current_context
                logger.error(f"context : {current_context}")
                p_driver.switch_to.context(current_context)
                logger.error(f"{ex} --> send_keys_linkedin_delay_random --> We have an error while typing in search field. Let's try again :-)")
                time.sleep(random.uniform(1, 3))
                p_driver.implicitly_wait(15)
                controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
                actions = ActionChains(p_driver)
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(4.9, 6.3))
        actions.click()
        actions.send_keys(p_key)
        print(f"We just typed '{p_key}'")
        try:
            actions.perform()
            n += 1
        except Exception as ex:
            logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
        time.sleep(random.uniform(min_delay, max_delay))
        #if controller.text==p_keys:

# ==================================================================================================================
# ============================ FUNCTION LINKEDIN TO SEARCH FOR KEYWORD ============================================
# ==================================================================================================================

def SendKeysLinkedinProfile(p_driver, p_udid, controller, p_keys, min_delay=0.7, max_delay=1.45,
                                    p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(
        f"{p_udid}|||---------------------------- WE START send_keys_linkedin_delay_random function ------------------------------")
    print(f"p_keys : {p_keys}")
    n = 0
    controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
    len_p_keys = len(p_keys)
    for p_key in p_keys:
        print(f"p_key : {p_key}")
        actions = ActionChains(p_driver)
        cpt=0
        while True:
            try:
                actions.move_to_element_with_offset(controller, p_xoffset, 0)

                break
            except Exception as ex:
                current_context = p_driver.current_context
                print(f"context : {current_context}")
                p_driver.switch_to.context(current_context)
                logger.error(f"{ex} --> SendKeysLinkedinProfile --> We have an error while typing in search field. Let's try again :-)")
                time.sleep(random.uniform(1, 3))
                p_driver.implicitly_wait(15)
                controller = p_driver.find_element_by_id("com.linkedin.android:id/search_bar_text")
                actions = ActionChains(p_driver)
                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(4.9, 6.3))
                cpt += 1
                if cpt > 3:
                    break
        actions.click()
        actions.send_keys(p_key)
        print(f"We just typed '{p_key}'")
        try:
            actions.perform()
            n += 1
        except Exception as ex:
            logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
        time.sleep(random.uniform(min_delay, max_delay))
        # if controller.text==p_keys:

    see_all_results = p_driver.find_elements_by_id("com.linkedin.android:id/search_typeahead_entity_text")
#if len(see_all_results)!=0:
#    see_all_results[0].click()
#    logger.info(f"{p_udid}|||PhoneBot click on the profile found!")




#==================================================================================================================
#=============================== FUNCTION TO SEARCH FOR KEYWORD IN INSTAGRAM ======================================
#==================================================================================================================

def send_keys_delay_random(p_driver,p_udid,controller,p_keys,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    while True:
        try:
            #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
            logger.info(f"{p_udid}|||---------------------------- WE START send_keys_delay_random function ------------------------------")
            print(f"p_keys : {p_keys}")
            n=0
            for p_key in p_keys:
                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                cpt=0
                while True:
                    try:
                        actions.move_to_element_with_offset(controller, p_xoffset, 0)
                        break
                    except Exception as ex:
                        logger.error(f"{ex} --> send_keys_delay_random --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt > 3:
                            break
                actions.click()
                actions.send_keys(p_key)
                print(f"We just typed '{p_key}'")
                try:
                    actions.perform()
                    n+=1
                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
                # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================
                search_results = p_driver.find_elements_by_id('com.instagram.android:id/row_search_user_username')

                #if len(search_results)>0 and n >= 3:
                if len(search_results) > 0:
                    print(f"We enter in the condition len(search_results)>0 and n==3 because len(search_results)= {len(search_results)} and n = {n} ")
                    for search_result in search_results:
                        print(f"search_result.text = {search_result.text}")
                        cpt=0
                        while True:
                            try:
                                if search_result.text == p_keys:
                                    time.sleep(random.uniform(1.2, 3.3))
                                    logger.info(f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                    time.sleep(random.uniform(0.9, 3.3))

                                    search_result.click()
                                    return True
                                else:
                                    break
                            except Exception as ex:
                                logger.error(f"{p_udid}|||{ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                                cpt+=1
                                logger.info(
                                    f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                time.sleep(random.uniform(1.9, 3.3))
                                if cpt>80:
                                    logger.error(
                                        f"{p_udid}|||{ex} --> Something went wrong for the {cpt}th times with search_result.text with p_keys. Let's skip it.")
                                    break

                else:
                    no_results = p_driver.find_elements_by_id("com.instagram.android:id/row_no_results_textview")
                    if len(no_results) !=0:
                        logger.info(f"{p_udid}|||Phonebot didn't find anything in search results. Let's try again!")
                        controller.clear()
                        return False





                # ======================================================================================
                time.sleep(random.uniform(min_delay, max_delay))

            break
        except Exception as ex:
            logger.error(
                f"{p_udid}|||{ex} --> Something went wrong with the function 'send_keys_delay_random'. Let's try again!")
            controller.clear()
            return False




#==================================================================================================================
#=============================== FUNCTION TO SEARCH FOR KEYWORD IN INSTAGRAM ======================================
#==================================================================================================================

def send_keys_delay_random_instagram(p_driver,p_udid,controller,p_keys,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    while True:
        try:
            #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
            logger.info(f"{p_udid}|||---------------------------- WE START send_keys_delay_random function ------------------------------")
            print(f"p_keys : {p_keys}")
            n=0
            controller.click()
            for p_key in p_keys:
                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                cpt=0
                while True:
                    try:
                        actions.move_to_element_with_offset(controller, p_xoffset, 0)
                        break
                    except Exception as ex:
                        logger.error(f"{ex} --> send_keys_delay_random --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt > 3:
                            break
                actions.click()
                actions.send_keys(p_key)
                print(f"We just typed '{p_key}'")
                try:
                    actions.perform()
                    n+=1
                except Exception as ex:
                    logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
                # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================
                search_results = p_driver.find_elements_by_id('com.instagram.android:id/row_search_user_username')

                #if len(search_results)>0 and n >= 3:
                if len(search_results) > 0:
                    print(f"We enter in the condition len(search_results)>0 and n==3 because len(search_results)= {len(search_results)} and n = {n} ")
                    for search_result in search_results:
                        print(f"search_result.text = {search_result.text}")
                        cpt=0
                        while True:
                            try:
                                if search_result.text == p_keys:
                                    time.sleep(random.uniform(1.2, 3.3))
                                    logger.info(f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                    logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                    time.sleep(random.uniform(0.9, 3.3))

                                    search_result.click()
                                    return True
                                else:
                                    break
                            except Exception as ex:
                                logger.error(f"{p_udid}|||{ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                                cpt+=1
                                logger.info(
                                    f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                time.sleep(random.uniform(1.9, 3.3))
                                if cpt>80:
                                    logger.error(
                                        f"{p_udid}|||{ex} --> Something went wrong for the {cpt}th times with search_result.text with p_keys. Let's skip it.")
                                    break

                else:
                    no_results = p_driver.find_elements_by_id("com.instagram.android:id/row_no_results_textview")
                    if len(no_results) !=0:
                        logger.info(f"{p_udid}|||Phonebot didn't find anything in search results. Let's try again!")
                        controller.clear()
                        return False





                # ======================================================================================
                time.sleep(random.uniform(min_delay, max_delay))

            break
        except Exception as ex:
            logger.error(
                f"{p_udid}|||{ex} --> Something went wrong with the function 'send_keys_delay_random'. Let's try again!")
            controller.clear()
            return False



# ==================================================================================================================
# =============================== FUNCTION TO SEARCH FOR KEYWORD IN TWITTER ======================================
# ==================================================================================================================

def send_keys_delay_random_twitter(p_driver, p_udid, controller, p_keys,p_twitter_is_bugging, min_delay=0.5, max_delay=0.75, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(
        f"{p_udid}|||---------------------------- WE START send_keys_delay_random_twitter function ------------------------------")
    p_keys = '@'+p_keys
    print(f"p_keys : {p_keys}")

    if not p_twitter_is_bugging:

        n = 0
        for p_key in p_keys:
            print(f"p_key : {p_key}")
            actions = ActionChains(p_driver)
            cpt=0
            while True:
                try:
                    actions.move_to_element_with_offset(controller, p_xoffset, 0)
                    break
                except Exception as ex:
                    logger.error(f"{ex} --> send_keys_delay_random_twitter --> We have an error while typing in search field. Let's try again :-)")
                    time.sleep(random.uniform(1, 3))
                    cpt += 1
                    if cpt > 3:
                        break
            actions.click()
            actions.send_keys(p_key)
            print(f"We just typed '{p_key}'")
            try:
                actions.perform()
                n += 1
            except Exception as ex:
                logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
            # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================

            if n > 2:
                logger.info(
                    f"{p_udid}|||The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.5, 0.8))
                try:
                    search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
                    # if len(search_results)>0 and n >= 3:
                except:
                    logger.info(f"{p_udid}|||There isn't any result.")
                    search_results=''


                if len(search_results) > 0:
                    print(f"We enter in the condition len(search_results)>0 and n==3 because len(search_results)= {len(search_results)} and n = {n} ")

                    try:
                        WebDriverWait(p_driver, 30).until(
                            EC.presence_of_element_located((By.ID, "com.twitter.android:id/screenname_item")))
                        search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
                        cpt_compare_search_result=0
                        for i in range(0,len(search_results)-1):
                            print(f"search_results[i].text = {search_results[i].text}")
                            while True:
                                try:

                                    if str(search_results[i].text).replace('@','') == p_keys:
                                        time.sleep(random.uniform(1.2, 3.3))
                                        logger.info(
                                            f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                        logger.info(
                                            f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                        time.sleep(random.uniform(0.9, 3.3))

                                        search_results[i].click()
                                        return True
                                    else:
                                        break
                                except Exception as ex:
                                    cpt_compare_search_result+=1
                                    if cpt_compare_search_result>2:
                                        logger.error(
                                            f"{p_udid}|||{ex} --> Something went wrong for the 3rd time when we compare search_result.text with p_keys. We need to skip this search {p_keys}.")
                                        WebDriverWait(p_driver, 30).until(
                                            EC.presence_of_element_located(
                                               (By.ID, "com.twitter.android:id/screenname_item")))
                                        search_results = p_driver.find_elements_by_id(
                                            'com.twitter.android:id/screenname_item')
                                        break

                                    else:
                                        logger.error(
                                            f"{p_udid}|||{ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                                        WebDriverWait(p_driver, 30).until(
                                            EC.presence_of_element_located(
                                               (By.ID, "com.twitter.android:id/screenname_item")))
                                        search_results = p_driver.find_elements_by_id(
                                            'com.twitter.android:id/screenname_item')
                            if cpt_compare_search_result > 2:
                                logger.error(
                                    f"{p_udid}|||{ex} --> Something went wrong for the 3rd time when we compare search_result.text with p_keys. We need to skip this search {p_keys}.")
                            WebDriverWait(p_driver, 30).until(
                                EC.presence_of_element_located(
                                   (By.ID, "com.twitter.android:id/screenname_item")))
                            search_results = p_driver.find_elements_by_id(
                                'com.twitter.android:id/screenname_item')
                            break

                    except Exception as ex:
                        logger.info(f"{p_udid}|||{ex} --> There was a error while trying to read the results.")
            # ======================================================================================
            time.sleep(random.uniform(min_delay, max_delay))
        return False
    else:
        controller.clear()
        p_keys_n=p_keys+'\\n'
        controller.send_keys(p_keys_n)
        time.sleep(random.uniform(0.9, 3.3))


        # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================
        try:
            search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
            # if len(search_results)>0 and n >= 3:
        except:
            logger.info(f"{p_udid}|||There isn't any result.")
            search_results = ''
        if len(search_results) > 0:
            print(f"We enter in the condition len(search_results)>0")
            WebDriverWait(p_driver, 30).until(
                EC.presence_of_element_located((By.ID, "com.twitter.android:id/screenname_item")))
            search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
            for i in range(0,len(search_results)-1):
                print(f"search_result.text = {search_results[0].text}")
                while True:
                    try:
                        if str(search_results[0].text).replace('@', '') == p_keys:
                            time.sleep(random.uniform(1.2, 3.3))
                            logger.info(
                                f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                            logger.info(
                                f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(0.9, 3.3))

                            search_results[0].click()
                            return True
                        else:
                            break
                    except Exception as ex:
                        logger.error(
                            f"{p_udid}|||{ex} --> Something went wrong when we compare search_result.text with p_keys. Let's try again!")

        # the problem now is we display a list of results mixed of contents and people. We need to tap on the "people" tab
        try:
            tab_people = p_driver.find_elements_by_xpath("*//android.widget.TextView[@text='Personnes']")
            tab_people[0].click()
        except:
            try:
                logger.info("PhoneBot didn't found the french tab 'Personnes'. Let's search it in English.")
                tab_people = p_driver.find_elements_by_xpath("*//android.widget.TextView[@text='People']")
                tab_people[0].click()
            except:
                logger.info(
                    "PhoneBot didn't found the english tab 'People'.Please contact support@phonebot.co.")

        time.sleep(random.uniform(1.9, 3.3))
        # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================
        try:
            search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
            # if len(search_results)>0 and n >= 3:
        except:
            logger.info(f"{p_udid}|||There isn't any result.")
            search_results = ''
        if len(search_results) > 0:
            print(f"We enter in the condition len(search_results)>0")
            WebDriverWait(p_driver, 30).until(
                EC.presence_of_element_located((By.ID, "com.twitter.android:id/screenname_item")))
            search_results = p_driver.find_elements_by_id('com.twitter.android:id/screenname_item')
            for i in range(0, len(search_results) - 1):

                while True:
                    try:
                        search_result_to_compare=str(search_results[0].text).replace('@', '').strip()
                        print(f"search_result_to_compare : {search_result_to_compare} =? {p_keys} : p_keys")
                        if search_result_to_compare== p_keys:
                            time.sleep(random.uniform(1.2, 3.3))
                            logger.info(
                                f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                            logger.info(
                                f"{p_udid}|||The bot will sleep just a few seconds..............................")
                            time.sleep(random.uniform(0.9, 3.3))

                            search_results[0].click()
                            return True
                        else:
                            break
                    except Exception as ex:
                        logger.error(
                            f"{p_udid}|||{ex} --> Something went wrong when we compare search_results[0].text with p_keys. Let's try again!")


        # ======================================================================================
        time.sleep(random.uniform(min_delay, max_delay))
        return False

# ==================================================================================================================
# =============================== FUNCTION TO SEARCH FOR KEYWORD IN TWITTER ======================================
# ==================================================================================================================

def send_keys_delay_random_facebook(p_driver, p_udid,controller, p_keys, min_delay=0.5, max_delay=0.75, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(
        f"{p_udid}|||---------------------------- WE START send_keys_delay_random function ------------------------------")
    print(f"p_keys : {p_keys}")


    print(f"p_key : {p_keys}")
    actions = ActionChains(p_driver)
    cpt=0
    while True:
        try:
            actions.move_to_element_with_offset(controller, p_xoffset, 0)
            break
        except Exception as ex:
            logger.error(f"{ex} --> send_keys_delay_random_facebook --> We have an error while typing in search field. Let's try again :-)")
            time.sleep(random.uniform(1, 3))
            cpt += 1
            if cpt > 3:
                break
    actions.click()
    actions.send_keys(p_keys)
    print(f"We just typed '{p_keys}'")
    try:
        actions.perform()

    except Exception as ex:
        logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")
    return True









    # ======================================================================================
    time.sleep(random.uniform(min_delay, max_delay))
    # ===================== LET'S TYPE ENTER ============================

    return True


def send_keys_delay_random_without_checking_result(p_driver,p_udid, controller, p_keys, min_delay=0.5, max_delay=0.75, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(f"{p_udid}|||---------------------------- WE START send_keys_delay_random_without_checking_result function ------------------------------")
    print(f"p_keys : {p_keys}")
    n = 0
    for p_key in p_keys:
        print(f"p_key : {p_key}")
        actions = ActionChains(p_driver)
        cpt=0
        while True:
            try:
                actions.move_to_element_with_offset(controller, p_xoffset, 0)
                break
            except Exception as ex:
                logger.error(f"{ex} --> send_keys_delay_random_without_checking_result --> We have an error while typing in search field. Let's try again :-)")
                time.sleep(random.uniform(1, 3))
                cpt += 1
                if cpt > 3:
                    break
        actions.click()
        actions.send_keys(p_key)
        print(f"We just typed '{p_key}'")
        try:
            actions.perform()
            n += 1
        except Exception as ex:
            logger.error(f"{p_udid}|||{ex} --> Error while typing a character in the search field!")

    actions.send_keys(Keys.ENTER)
    actions.perform()


    time.sleep(random.uniform(min_delay, max_delay))


#===========================================================================================
#=========================== MODULE TO SEARCK A HASHTAG ===================================

def send_keys_hashtag_delay_random(p_driver,p_udid, controller, p_keys, p_bug=False,min_delay=0.5, max_delay=0.75, p_xoffset=300):
    # https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    logger.info(f"{p_udid}|||---------------------------- WE START send_keys_delay_random function ------------------------------")
    print(f"p_keys : {p_keys}")
    p_bug=ConfigIniCheckSmartphoneBug(p_udid)
    controller.click()
    if len(p_keys) > 25 or p_bug:
        controller.send_keys(p_keys)
        p_bug = True
        return True
    else:
        n = 0
        for p_key in p_keys:
            print(f"p_key : {p_key}")
            actions = ActionChains(p_driver)
            cpt=0
            while True:
                try:
                    actions.move_to_element_with_offset(controller, p_xoffset, 0)
                    break
                except Exception as ex:
                    logger.error(" --> send_keys_hashtag_delay_random --> We have an error while typing in search field. Let's try again :-)")
                    time.sleep(random.uniform(1, 3))
                    cpt += 1
                    if cpt > 3:
                        break
            actions.click()
            actions.send_keys(p_key)
            print(f"We just typed '{p_key}'")
            try:
                actions.perform()
                n += 1
            except Exception as ex:
                logger.error(f"{p_udid}|||{ex} -->Error while typing a character in the search field!")




            # ===================== LET'S TRY TO FIND QUICKLY THE RESULT ============================
            search_results = p_driver.find_elements_by_id('com.instagram.android:id/row_hashtag_textview_tag_name')
            # if len(search_results)>0 and n >= 3:
            if len(search_results) > 0:
                print(f"We enter in the condition len(search_results)>0 and n==3 because len(search_results)= {len(search_results)} and n = {n} ")
                for search_result in search_results:
                    print(f"search_result.text = {search_result.text}")
                    while True:
                        try:
                            if search_result.text == p_keys:
                                time.sleep(random.uniform(1.2, 3.3))
                                logger.info(f"{p_udid}|||Yahoo!!! We found it in search results! Let's go for it right now!!!")
                                logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
                                time.sleep(random.uniform(0.9, 3.3))

                                search_result.click()
                                return True
                            else:
                                break
                        except Exception as ex:
                            logger.error(f"{ex} -->Something went wrong when we compare search_result.text with p_keys. Let's try again!")
                        #except ValueError:
                            #print("ERROR")

            # ======================================================================================
            time.sleep(random.uniform(min_delay, max_delay))


# ==============================================================================================================
# ======================== METHOD TO REMEMBER IF SMARTPHONE IS BUGGING ========================================
# ==============================================================================================================

def ConfigIniCheckSmartphoneBug(p_udid='',p_bug=''):
    """
    In config.ini file, smartphone_bugging contains a list of smartphones which are bugging
    This function will check the congig.ini file is smartphone_bugging has the udid of smartphone
    There are 2 parameters:
    p_udid which is smarptphone udid
    p_bug which is optional and will add the p_udid in the list if p_bug=True
    If we add the parameter p_bug, it means we want to add the smartphone in the list
    If we don't add the parameter p_bug, it means we just want to check if smartphone is in blacklist or not
    :return:
    """

    if p_udid == '':
        #We didn't pass any udid, so we just skip by returning false
        return False
    else:
        # ---on lit le fichier config.ini
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))
        #If the variable smartphone_bugging doesn't exist
        if not config.has_option('Settings', 'smartphone_bugging'):
            print(f"The variable 'smartphone_bugging' doesn't exist in config.ini file")
            #We add the variable smartphone_bugging
            if p_bug == True:
                print(f"The variable 'smartphone_bugging' doesn't exist in config.ini file and p_bug=True for smartphone {p_udid}")
                smartphone_bugging=p_udid
                with open(LoadFile('config.ini'), 'a', encoding='utf-8') as f:
                    f.write(f"smartphone_bugging = {p_udid}")
                f.close()
            else:
                print(
                    f"The variable 'smartphone_bugging' doesn't exist in config.ini file and p_bug=False for smartphone {p_udid}")
                print(f" The smartphone {p_udid} is not bugging")
                p_bug=False


        # If the variable smartphone_bugging exist
        else:
            #The variable smartphone_bugging exist already
            print(f"The variable 'smartphone_bugging' exist in config.ini file")
            if p_bug == True:
                print(
                    f"The variable 'smartphone_bugging' exist in config.ini file and p_bug=True for smartphone {p_udid}")
                #We need to build the list of blacklist smartphone bugging
                smartphone_bugging=config.get('Settings', 'smartphone_bugging')
                smartphone_bugging += ',' + p_udid
                config.set('Settings', 'smartphone_bugging', smartphone_bugging)
                with open(LoadFile('config.ini'), 'w', encoding='utf-8') as configfile:
                    config.write(configfile)

            elif p_bug == False:
                print(
                    f"The variable 'smartphone_bugging' exist in config.ini file and p_bug=False for smartphone {p_udid}")
                print(f" The smartphone {p_udid} is not bugging")
                p_bug = False

            else:
                smartphone_bugging=str(config.get('Settings', 'smartphone_bugging'))
                if smartphone_bugging.find(p_udid) != -1:
                    print(
                        f"The variable 'smartphone_bugging' exist in config.ini file and the smartphone {p_udid} was found")
                    p_bug=True
                else:
                    print(
                        f"The variable 'smartphone_bugging' exist in config.ini file and the smartphone {p_udid} was not found")
                    p_bug=False
        return p_bug



def send_keys_message_delay_random(p_platform,p_driver,controller,p_keys,p_bug,min_delay=0.5,max_delay=0.75,p_xoffset=300,p_udid=''):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        #Here we immediatly get the value of smartphone_bugging=p_udid in config.ini
        #because it is the memory of phonebot about the smartphones which bug or not.
        #if user remove this values from config.ini. It may bug
        # if config.ini[smartphone_bugging] == 0:
        #    p_bug=False
        # else:
        #    p_bug= True
        # La suite dans ligne 2512

        p_bug = ConfigIniCheckSmartphoneBug(p_udid)

        print(f"p_keys : {p_keys}")
        controller.clear()
        if not p_bug:
            #p_keys = "  " + p_keys
            counter=1
            ENTER=0
            p_keys_words=str(p_keys).split(' ')
            p_keys_word_1=str(p_keys_words[0]).strip()
            for p_key in p_keys:
                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                # conver to the list
                list_xy = bounds.split(",")
                #print(bounds)
                #print(list_xy)
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                #print(f"bounds_x1 : {bounds_x1}")
                #print(f"bounds_y1 : {bounds_y1}")
                #print(f"bounds_x2 : {bounds_x2}")
                #print(f"bounds_y2 : {bounds_y2}")

                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1
                #print(f"p_offset_x : {p_offset_x}")
                #print(f"p_offset_y : {p_offset_y}")

                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                #--- Sometimes it bugs.... so that is why we had this try
                cpt=0
                while True:
                    try:
                    #    if counter<4:
                    #       actions.move_to_element(controller)
                    #    else:
                        #if ENTER==1:
                        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                        #else:
                        #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                        break
                    except Exception as ex:
                        logger.error(f"{p_platform} --> send_keys_message_delay_random --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt > 3:
                            break
                actions.click()
                if p_key=='|':
                    actions.send_keys(Keys.ENTER)
                    ENTER=1
                else:
                    actions.send_keys(p_key)
                    ENTER=0
                print(f"We just typed '{p_key}'")
                actions.perform()
                if p_key==' ':
                    p_key_word_1=str(controller.get_attribute('text')).strip()
                    if p_keys_word_1!=p_key_word_1:
                        logger.error(f"{p_platform} PhoneBot detect an issue when the smartphone is typing some characters. This smartphone is bugging.")
                        p_bug=True
                        #Here we have this scenario
                        # PhoneBOt write a part of message.... certainly because of the smartphone as other doesn't do that.
                        #ex:
                        #    Hello toutstissimo,
                        #    Avez vous?
                        #
                        # but PhoneBot doesn't remember that this smartphone is bugging. So we need to create a blacklist of smartphone
                        # if config.ini doesn't have smartphone_bugging:
                        #          add smartphone_bugging=p_udid in config.ini
                        #
                        # The checking of config.ini[smartphone_bugging] is on line 2437!

                        p_bug = ConfigIniCheckSmartphoneBug(p_udid, True)
                        return p_bug
                    else:
                        p_bug=False
                        logger.info(f"{p_platform} This smartphone is working well while typing some characters.")
                #if counter == 1 or counter==2:
                #    time.sleep(random.uniform(7, 10))
                counter+=1
                time.sleep(random.uniform(min_delay, max_delay))
            return p_bug
        else:
            p_bug=True
            p_keys = str(p_keys).replace('|', '\n')
            controller.send_keys(p_keys)
            return p_bug

    #except ValueError:
        #print(f"{p_platform} ERROR with send_keys_message_delay_random")
    except Exception as ex:
        logger.critical(f"{ex} --> {p_platform} --> ERROR with send_keys_message_delay_random")
        p_bug = ConfigIniCheckSmartphoneBug(p_udid, True)
        return p_bug

def send_keys_message_delay_random_gmap(p_platform,p_driver,controller,p_keys,p_bug,min_delay=0.5,max_delay=0.75,p_xoffset=300,p_udid=''):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        p_bug = ConfigIniCheckSmartphoneBug(p_udid)
        return p_bug
        test_p_bug=False
        print(f"p_keys : {p_keys}")
        controller.clear()
        if not p_bug:
            #p_keys = "  " + p_keys
            counter=1
            ENTER=0
            p_keys_words=str(p_keys).split(' ')
            p_keys_word_1=str(p_keys_words[0]).strip()
            for p_key in p_keys:
                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                # conver to the list
                list_xy = bounds.split(",")
                #print(bounds)
                #print(list_xy)
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                #print(f"bounds_x1 : {bounds_x1}")
                #print(f"bounds_y1 : {bounds_y1}")
                #print(f"bounds_x2 : {bounds_x2}")
                #print(f"bounds_y2 : {bounds_y2}")

                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1
                #print(f"p_offset_x : {p_offset_x}")
                #print(f"p_offset_y : {p_offset_y}")

                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                #--- Sometimes it bugs.... so that is why we had this try
                cpt=0
                while True:
                    try:
                    #    if counter<4:
                    #       actions.move_to_element(controller)
                    #    else:
                        #if ENTER==1:
                        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                        #else:
                        #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                        break
                    except Exception as ex:
                        logger.error(f"{p_platform} --> send_keys_message_delay_random --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt > 3:
                            break
                actions.click()
                if p_key=='|':
                    actions.send_keys(Keys.ENTER)
                    ENTER=1
                else:
                    actions.send_keys(p_key)
                    ENTER=0
                print(f"We just typed '{p_key}'")
                actions.perform()

                if p_key==' ' and not test_p_bug:

                    p_key_word_1=str(controller.get_attribute('text')).strip()
                    if p_keys_word_1!=p_key_word_1:
                        logger.error(f"{p_platform} PhoneBot detect an issue when the smartphone is typing some characters. This smartphone is bugging.")
                        p_bug=True

                        p_bug = ConfigIniCheckSmartphoneBug(p_udid, True)

                        return p_bug
                    else:
                        p_bug=False
                        test_p_bug = True
                        logger.info(f"{p_platform} This smartphone is working well while typing some characters.")
                #if counter == 1 or counter==2:
                #    time.sleep(random.uniform(7, 10))
                counter+=1
                time.sleep(random.uniform(min_delay, max_delay))
            return p_bug
        else:
            p_bug=True
            p_keys = str(p_keys).replace('|', '\n')
            controller.send_keys(p_keys)
            return p_bug

    #except ValueError:
        #print(f"{p_platform} ERROR with send_keys_message_delay_random")
    except Exception as ex:
        logger.critical(f"{ex} --> {p_platform} --> ERROR with send_keys_message_delay_random")
        p_bug = ConfigIniCheckSmartphoneBug(p_udid, True)

        return p_bug

# ===============================================================================================================
# =================================== Method to send message with Linkedin ======================================
# ===============================================================================================================
def SendKeysMessageLinkedin(p_driver,controller,p_keys,p_linkedin_is_bugging,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074


    try:

        if not p_linkedin_is_bugging:
            print(f"p_keys : {p_keys}")
            #p_keys = "  " + p_keys
            counter=1
            ENTER=0
            for p_key in p_keys:
                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                # conver to the list
                list_xy = bounds.split(",")
                #print(bounds)
                #print(list_xy)
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                #print(f"bounds_x1 : {bounds_x1}")
                #print(f"bounds_y1 : {bounds_y1}")
                #print(f"bounds_x2 : {bounds_x2}")
                #print(f"bounds_y2 : {bounds_y2}")

                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1
                #print(f"p_offset_x : {p_offset_x}")
                #print(f"p_offset_y : {p_offset_y}")

                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                #--- Sometimes it bugs.... so that is why we had this try
                cpt=0
                while True:
                    try:
                    #    if counter<4:
                    #       actions.move_to_element(controller)
                    #    else:
                        #if ENTER==1:
                        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                        #else:
                        #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                        break
                    except Exception as ex:


                        logger.error(" --> SendKeysMessageLinkedin --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt>3:
                            break
                actions.click()
                if p_key=='|':
                    actions.send_keys(Keys.ENTER)
                    ENTER=1
                else:
                    actions.send_keys(p_key)
                    ENTER=0
                print(f"We just typed '{p_key}'")
                actions.perform()
                #if counter == 1 or counter==2:
                #    time.sleep(random.uniform(7, 10))
                counter+=1
                time.sleep(random.uniform(min_delay, max_delay))
        else:

            controller.clear()
            print(f"p_keys : {p_keys}")
            #actions = ActionChains(p_driver)
            p_keys=str(p_keys).replace('|','\n')

            controller.send_keys(p_keys)


    #except ValueError:
        #print(f"ERROR with send_keys_message_delay_random")
    except Exception as ex:
        logger.critical(f"{ex} --> ERROR with send_keys_message_delay_random")

# ===============================================================================================================
# ============================================= SEND MESSAGE FACEBOOK ===========================================
# ===============================================================================================================

def SendFacebookMessage(p_driver,controller,p_keys,p_bug,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        controller.clear()
        print(f"p_keys : {p_keys}")
        #p_keys = "  " + p_keys
        counter=1
        ENTER=0
        if p_bug:
            p_keys=str(p_keys).replace('|','\n')
            controller.send_keys(p_keys)
            return p_bug

        for p_key in p_keys:

            bounds = controller.get_attribute('bounds')
            bounds = bounds[1:len(bounds) - 1]
            bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
            # conver to the list
            list_xy = bounds.split(",")
            #print(bounds)
            #print(list_xy)
            bounds_x1 = int(list_xy[0])
            bounds_y1 = int(list_xy[1])
            bounds_x2 = int(list_xy[2])
            bounds_y2 = int(list_xy[3])
            #print(f"bounds_x1 : {bounds_x1}")
            #print(f"bounds_y1 : {bounds_y1}")
            #print(f"bounds_x2 : {bounds_x2}")
            #print(f"bounds_y2 : {bounds_y2}")

            p_offset_x = bounds_x2 - bounds_x1 - 1
            p_offset_y = bounds_y2 - bounds_y1 - 1
            #print(f"p_offset_x : {p_offset_x}")
            #print(f"p_offset_y : {p_offset_y}")

            print(f"p_key : {p_key}")
            actions = ActionChains(p_driver)
            #--- Sometimes it bugs.... so that is why we had this try
            cpt=0
            while True:
                try:
                #    if counter<4:
                #       actions.move_to_element(controller)
                #    else:
                    #if ENTER==1:
                    actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                    #else:
                    #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                    break
                except Exception as ex:
                    logger.error(" --> SendFacebookMessage --> We have an error while typing in search field. Let's try again :-)")
                    time.sleep(random.uniform(1,3))
                    cpt += 1
                    if cpt > 3:
                        break

            actions.click()
            if p_key=='|':
                #actions.send_keys(Keys.ENTER)
                actions.send_keys(Keys.RETURN)

                ENTER=1
            else:
                actions.send_keys(p_key)
                ENTER=0
            print(f"We just typed '{p_key}'")
            while True:
                try:
                    actions.perform()
                    break
                except Exception as ex:
                    print("ERROR with actions.perform() . Let's try again!")

                    counter+=1
            time.sleep(random.uniform(min_delay, max_delay))
        return p_bug
    except Exception as ex:
        logger.critical(f"{ex} --> ERROR with SendFacebookMessage")

# ===============================================================================================================
# ============================================= SEND MESSAGE SMS ===========================================
# ===============================================================================================================
def SendSmsTextMessage(p_driver,controller,p_keys,min_delay=0.01,max_delay=0.02,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        controller.clear()
        controller.send_keys(p_keys)



    except Exception as ex:
        print("ERROR with SendSmsTextMessage")

# ===============================================================================================================
# ============================================= TYPE GOOGLE MAP SEARCH ===========================================
# ===============================================================================================================
def GmapSearch(p_driver,controller,p_keys,p_bug,min_delay=0.3,max_delay=0.7,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        controller.clear()
        print(f"p_keys : {p_keys}")
        if not p_bug:

            #p_keys = "  " + p_keys

            actions = ActionChains(p_driver)
            for p_key in p_keys:
                pause_seconds=random.uniform(min_delay,max_delay)
                print(f"pause_seconds : {pause_seconds}")
                actions.send_keys(p_key).pause(pause_seconds)

            if controller.get_attribute('text') != p_keys:
                logger.info("There is a bug while typing a Google map search. PhoneBot will copy-paste the search terms.")
                return True
            else:
                actions.send_keys(Keys.ENTER)
                actions.perform()
                return False
        else:
            p_keys_to_search=p_keys+'\\n'
            controller.send_keys(p_keys_to_search)
            return True





    except Exception as ex :
        print("ERROR with GmapSearch")

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
def WriteFacebookPost(p_driver,controller,p_keys,p_bug,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        print(f"p_keys : {p_keys}")
        #p_keys = "  " + p_keys
        counter=1
        ENTER=0
        controller.clear()
        if p_bug:
            p_keys=str(p_keys).replace('|','\n')
            controller.send_keys(p_keys)
            return p_bug

        for p_key in p_keys:


            bounds = controller.get_attribute('bounds')
            bounds = bounds[1:len(bounds) - 1]
            bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
            # conver to the list
            list_xy = bounds.split(",")
            #print(bounds)
            #print(list_xy)
            bounds_x1 = int(list_xy[0])
            bounds_y1 = int(list_xy[1])
            bounds_x2 = int(list_xy[2])
            bounds_y2 = int(list_xy[3])
            #print(f"bounds_x1 : {bounds_x1}")
            #print(f"bounds_y1 : {bounds_y1}")
            #print(f"bounds_x2 : {bounds_x2}")
            #print(f"bounds_y2 : {bounds_y2}")

            p_offset_x = bounds_x2 - bounds_x1 - 1
            p_offset_y = bounds_y2 - bounds_y1 - 1
            #print(f"p_offset_x : {p_offset_x}")
            #print(f"p_offset_y : {p_offset_y}")

            print(f"p_key : {p_key}")
            actions = ActionChains(p_driver)
            #--- Sometimes it bugs.... so that is why we had this try
            cpt=0
            while True:
                try:
                #    if counter<4:
                #       actions.move_to_element(controller)
                #    else:
                    #if ENTER==1:
                    actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                    #else:
                    #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                    break
                except Exception as ex:
                    logger.error("WriteFacebookPost --> We have an error while typing in search field. Let's try again :-)")
                    time.sleep(random.uniform(1,3))
                    cpt += 1
                    if cpt > 3:
                        break
            actions.click()
            if p_key=='|':
                actions.send_keys(Keys.ENTER)
                ENTER=1
            else:
                actions.send_keys(p_key)
                ENTER=0
            print(f"We just typed '{p_key}'")
            actions.perform()
            #if counter == 1 or counter==2:
            #    time.sleep(random.uniform(7, 10))
            counter+=1
            time.sleep(random.uniform(min_delay, max_delay))

        bounds = controller.get_attribute('bounds')
        bounds = bounds[1:len(bounds) - 1]
        bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
        list_xy = bounds.split(",")
        bounds_x1 = int(list_xy[0])
        bounds_y1 = int(list_xy[1])
        bounds_x2 = int(list_xy[2])
        bounds_y2 = int(list_xy[3])
        p_offset_x = bounds_x2 - bounds_x1 - 1
        p_offset_y = bounds_y2 - bounds_y1 - 1

        actions = ActionChains(p_driver)
        # --- Sometimes it bugs.... so that is why we had this try
        cpt=0
        while True:
            try:
                #    if counter<4:
                #       actions.move_to_element(controller)
                #    else:
                # if ENTER==1:
                actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                # else:
                #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                break
            except Exception as ex:
                logger.error("WriteFacebookPost --> We have an error while typing in search field. Let's try again :-)")
                time.sleep(random.uniform(1, 3))
                cpt += 1
                if cpt > 3:
                    break
        actions.click()
        actions.send_keys(Keys.ENTER)
        print("We type ENTER!")
        actions.perform()

        time.sleep(random.uniform(3, 5))
        return p_bug
    except Exception as ex:
        print("ERROR with WriteFacebookPost()")

def SendKeysEnter(p_driver,controller,p_keys,min_delay=0.5,max_delay=0.75,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    while True:
        try:
            print(f"p_keys : {p_keys}")
            #p_keys = "  " + p_keys
            counter=1
            ENTER=0
            for p_key in p_keys:
                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                # conver to the list
                list_xy = bounds.split(",")
                #print(bounds)
                #print(list_xy)
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                #print(f"bounds_x1 : {bounds_x1}")
                #print(f"bounds_y1 : {bounds_y1}")
                #print(f"bounds_x2 : {bounds_x2}")
                #print(f"bounds_y2 : {bounds_y2}")

                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1
                #print(f"p_offset_x : {p_offset_x}")
                #print(f"p_offset_y : {p_offset_y}")

                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                #--- Sometimes it bugs.... so that is why we had this try
                cpt=0
                while True:
                    try:
                    #    if counter<4:
                    #       actions.move_to_element(controller)
                    #    else:
                        #if ENTER==1:
                        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                        #else:
                        #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                        break
                    except Exception as ex:
                        logger.error(f"SendKeysEnter -->{ex} We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1,3))
                        cpt += 1
                        if cpt > 3:
                            break
                actions.click()
                if p_key=='|':
                    actions.send_keys(Keys.ENTER)
                    ENTER=1
                else:
                    actions.send_keys(p_key)
                    ENTER=0
                print(f"We just typed '{p_key}'")
                actions.perform()
                #if counter == 1 or counter==2:
                #    time.sleep(random.uniform(7, 10))
                counter+=1
                time.sleep(random.uniform(min_delay, max_delay))


            bounds = controller.get_attribute('bounds')
            bounds = bounds[1:len(bounds) - 1]
            bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
            list_xy = bounds.split(",")
            bounds_x1 = int(list_xy[0])
            bounds_y1 = int(list_xy[1])
            bounds_x2 = int(list_xy[2])
            bounds_y2 = int(list_xy[3])
            p_offset_x = bounds_x2 - bounds_x1 - 1
            p_offset_y = bounds_y2 - bounds_y1 - 1

            actions = ActionChains(p_driver)
            # --- Sometimes it bugs.... so that is why we had this try
            cpt=0
            while True:
                try:
                    #    if counter<4:
                    #       actions.move_to_element(controller)
                    #    else:
                    # if ENTER==1:
                    actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                    # else:
                    #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                    break
                except Exception as ex:
                    logger.error(f"SendKeysEnter -->{ex} We have an error while typing in search field. Let's try again :-)")
                    time.sleep(random.uniform(1, 3))
                    cpt += 1
                    if cpt > 3:
                        break



            actions.click()
            actions.send_keys(Keys.ENTER)
            print("We type ENTER!")
            actions.perform()

            time.sleep(random.uniform(min_delay, max_delay))
            break
        except Exception as ex:
            while True:
                try:
                    logger.critical(f" --> SendKeysEnter --> ERROR with SendKeysEnter")
                    controller.clear()
                    break
                except Exception as ex:
                    logger.critical(f"{ex} --> SendKeysEnter --> ERROR with SendKeysEnter")

# ==============================================================================================================
# =========================================== LINKEDIN METHOD to type a message ================================
# ==============================================================================================================
def SendKeysLinkedin(p_driver,controller,p_keys,p_bug,p_mode,min_delay=1,max_delay=1.25,p_xoffset=300):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    print(f"p_bug : {p_bug}")
    if not p_bug:
        while True:
            try:
                print(f"p_keys : {p_keys}")
                #p_keys = "  " + p_keys
                counter=1
                ENTER=0

                for p_key in p_keys:

                    try:
                        bounds = controller.get_attribute('bounds')
                        time.sleep(random.uniform(min_delay, max_delay))

                    except:
                        logger.critical("Error when controller.get_attribute('bounds')")
                        current_package = p_driver.current_package
                        current_activity = p_driver.current_activity

                    bounds = bounds[1:len(bounds) - 1]
                    bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                    # conver to the list
                    list_xy = bounds.split(",")
                    #print(bounds)
                    #print(list_xy)
                    bounds_x1 = int(list_xy[0])
                    bounds_y1 = int(list_xy[1])
                    bounds_x2 = int(list_xy[2])
                    bounds_y2 = int(list_xy[3])
                    #print(f"bounds_x1 : {bounds_x1}")
                    #print(f"bounds_y1 : {bounds_y1}")
                    #print(f"bounds_x2 : {bounds_x2}")
                    #print(f"bounds_y2 : {bounds_y2}")

                    p_offset_x = bounds_x2 - bounds_x1 - 1
                    p_offset_y = bounds_y2 - bounds_y1 - 1
                    #print(f"p_offset_x : {p_offset_x}")
                    #print(f"p_offset_y : {p_offset_y}")

                    print(f"p_key : {p_key}")
                    actions = ActionChains(p_driver)
                    #--- Sometimes it bugs.... so that is why we had this try
                    cpt=0
                    while True:
                        try:
                        #    if counter<4:
                        #       actions.move_to_element(controller)
                        #    else:
                            #if ENTER==1:
                            actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                            #else:
                            #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                            break
                        except Exception as ex:
                            logger.error("SendKeysLinkedin --> We have an error while typing in search field. Let's try again :-)")
                            time.sleep(random.uniform(1,3))
                            cpt += 1
                            if cpt > 3:
                                break
                    actions.click()


                    if p_key=='|':
                        actions.send_keys(Keys.ENTER)
                        ENTER=1
                    else:
                        actions.send_keys(p_key)
                        ENTER=0
                    print(f"We just typed '{p_key}'")
                    actions.perform()

                    time.sleep(random.uniform(min_delay, max_delay))

                    #if counter == 1 or counter==2:
                    #    time.sleep(random.uniform(7, 10))
                    counter+=1
                    time.sleep(random.uniform(min_delay, max_delay))


                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                list_xy = bounds.split(",")
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1

                actions = ActionChains(p_driver)
                # --- Sometimes it bugs.... so that is why we had this try
                cpt=0
                while True:
                    try:
                        #    if counter<4:
                        #       actions.move_to_element(controller)
                        #    else:
                        # if ENTER==1:
                        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                        # else:
                        #    actions.move_to_element_with_offset(controller, p_offset_x, 0)

                        break
                    except Exception as ex:
                        logger.error("SendKeysLinkedin --> We have an error while typing in search field. Let's try again :-)")
                        time.sleep(random.uniform(1, 3))
                        cpt += 1
                        if cpt > 3:
                            break

                if controller.get_attribute('text') != p_keys:
                    logger.error("Linkedin app on this phone is bugging.")
                    p_bug=True

                    return p_bug
                else:
                    p_bug=False

                actions.click()
                actions.send_keys(Keys.ENTER)
                print("We type ENTER!")
                actions.perform()

                time.sleep(random.uniform(min_delay, max_delay))
                return p_bug
            #except ValueError:
            except Exception as ex:
                #while True:
                cpt_linkedin=0
                try:
                    logger.critical(f"{ex} --> SendKeysLinkedin --> ERROR with SendKeysLinkedin")
                    controller.clear()
                    p_bug=True
                    return p_bug
                except Exception as ex:
                    cpt_linkedin += 1
                    if cpt_linkedin > 3:
                        break
                    else:
                        logger.critical(f"{ex} --> SendKeysLinkedin --> ERROR with SendKeysLinkedin")
                        p_bug = True
                        return p_bug
    else:
        while True:
            try:
                print("Linkedin had bug with this smartphone. We will type directly the text.")
                p_keys=str(p_keys).replace('|','\\n')
                print(f"p_keys after change for back return | : {p_keys}")
                if p_mode=='url':
                    p_keys+='\\n'
                controller.send_keys(p_keys)

                if p_mode=='message':
                    controller.send_keys(p_keys)
                    controller.send_keys(Keys.ENTER)
                    #controller.send_keys(Keys.RETURN)

                p_bug=True
                return p_bug
            #except ValueError:
            except Exception as ex:
                #while True:
                try:
                    #logger.critical(f"{ex} --> ERROR with SendKeysEnter")
                    print("error")
                    controller.clear()
                    return p_bug
                except Exception as ex:
                    logger.critical(f"{ex} --> SendKeysLinkedin --> ERROR with SendKeysLinkedin")


# =============================================================================================================
# =============================================================================================================
def SearchFacebook(p_driver,controller,p_keys,p_bug,min_delay=0.5,max_delay=0.75,p_offset_x=300,p_offset_y=0):
    #https://stackoverflow.com/questions/51651732/how-to-type-like-a-human-via-actionchains-send-keys/51653074
    try:
        search_fields = p_driver.find_elements_by_class_name('android.widget.EditText')
        while len(search_fields) == 0:
            search_fields = p_driver.find_elements_by_class_name('android.widget.EditText')
            logger.info(f"SearchFacebook|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(0.9, 2.3))
            p_driver.implicitly_wait(10)

        search_field = WebDriverWait(p_driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,'android.widget.EditText')))
        controller = search_field
        p_keys_list=str(p_keys).split(' ')
        first_word=p_keys_list[0]
        if len(p_keys)>25 or p_bug:
            controller.send_keys(p_keys)
            p_bug=True
        else:
            print(f"p_keys : {p_keys}")
            counter=1
            for p_key in p_keys:
                if p_key ==' ':
                    logger.info(f"PhoneBot will test the 1rst word to see if this smartphone is bugging while typing some words.")
                    if str(controller.get_attribute('text')).strip()!= first_word:
                        logger.error("This Smartphone is bugging while typing some words. WPhoneBot will simply copy paste the text!")
                        p_bug=True
                        return p_bug

                bounds = controller.get_attribute('bounds')
                bounds = bounds[1:len(bounds) - 1]
                bounds = bounds.replace('][', ',').replace('[', ',').replace(']', ',')
                list_xy = bounds.split(",")
                bounds_x1 = int(list_xy[0])
                bounds_y1 = int(list_xy[1])
                bounds_x2 = int(list_xy[2])
                bounds_y2 = int(list_xy[3])
                p_offset_x = bounds_x2 - bounds_x1 - 1
                p_offset_y = bounds_y2 - bounds_y1 - 1
                print(f"p_key : {p_key}")
                actions = ActionChains(p_driver)
                actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
                #actions.click()
                actions.send_keys(p_key)
                print(f"We just typed '{p_key}'")
                actions.perform()
                #if counter == 1 or counter==2:
                #    time.sleep(random.uniform(7, 10))
                counter+=1
                time.sleep(random.uniform(min_delay, max_delay))


        actions = ActionChains(p_driver)
        actions.move_to_element_with_offset(controller, p_offset_x, p_offset_y)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        return p_bug

    #except ValueError:

        #print("error searchfb")
    except Exception as ex:
        logger.critical(f"{ex} --> ERROR with SearchFacebook")


# =============================================================================================================
# =============================================================================================================
