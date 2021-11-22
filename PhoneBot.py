# -*- coding: utf-8 -*-

import pdb
import logging
import platform
import os
import sys
import shutil
from urllib.request import urlopen
import ntplib

import PyQt5 


# from modules import prepare_envir_appium
from modules import prepare_envir_appium
from tools import extract_items_from_gui_xml


#####################################################################

# This code below is to handle the error message:
# FileNotFoundError: 'cacert.pem' resource not found in 'certifi'
# It is a problem when importing request
# Solution: https://stackoverflow.com/questions/46119901/python-requests-cant-find-a-folder-with-a-certificate-when-converted-to-exe
# is the program compiled?


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


def GetTimeFromInternet():
    """
    This function will try from different servers to get time and date
    """

    try:
        import ntplib
        from time import ctime
        x = ntplib.NTPClient()
        date_now_online_timestamp = x.request('ch.pool.ntp.org').tx_time
        date_now_online_str = datetime.fromtimestamp(date_now_online_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        date_now_online_DATE = datetime.strptime(date_now_online_str, '%Y-%m-%d %H:%M:%S')

    except OSError:
        logger.error('Internet date and time could not be reported by server.')
        logger.error('There is not internet connection.')
        try:
            res = urlopen('http://just-the-time.appspot.com/')
            date_now_online = res.read().strip()
            date_now_online_str = date_now_online.decode('utf-8')
            date_now_online_DATE = datetime.strptime(date_now_online_str, '%Y-%m-%d %H:%M:%S')

        except Exception as ex:
            logger.error(f"Error! We couldn't get the time. Please contact the support@phonebot.co")

    print(f"date_now_online_DATE : {date_now_online_DATE}-{type(date_now_online_DATE)}")
    return date_now_online_DATE


if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()
import requests

import ctypes


def is_admin():
    try:
        is_admin = os.getuid() == 0

    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def StartPhoneBotasAdmin():
    if platform.system() == 'Windows':

        # === Hide the console
        '''
        import win32gui
        import win32.lib.win32con as win32con
        the_program_to_hide = win32gui.GetForegroundWindow ()
        win32gui.ShowWindow (the_program_to_hide, win32con.SW_HIDE)
        '''
        # ======================================================

        if not is_admin():
            print("PhoneBot didn't start as admin.")

            ctypes.windll.shell32.ShellExecuteW(None, "runas", 'PhoneBot.exe', '', None, 1)
            sys.exit()

    # elif platform.system() == 'Darwin':
    #     try:
    #         subprocess.check_call(["/bin/bash","PhoneBot_Install.sh"])
    #     except subprocess.CalledProcessError as e:
    #         print(f"error => {e}")


# === We start PhoneBot as Admin =======================================
StartPhoneBotasAdmin()

from modules import mymodules

# === We prepare the logging =================================================================================

logger = logging.getLogger('__PhoneBot__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# mymodules need to be imported after we create the folders

import json
import configparser
import sqlite3
import subprocess
import threading
import webbrowser
from datetime import datetime
import psutil
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie, QFont
import time
import traceback
from PyQt5.QtWidgets import QPlainTextEdit, QLineEdit, QLabel, QPushButton, QComboBox, QCheckBox, QWidget, QRadioButton
from gui.PhoneBotUI import Ui_MainWindow
from modules import RunBrowser
from modules import RunSmartphones

# ================================================= GLOBAL VARIABBLES =================================================
__version__ = '0.003'
number_connected_phones = 0


# === The QThreads ==========================================================================================
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, p_function, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments(re-used for processing)
        self.p_function = p_function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        logging.info(f"Working in thread {self.p_function}.")

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.p_function(*self.args, **self.kwargs)
            logging.info(f"Finish 'run()' thread {self.p_function}.")

            # QtCore.QThread.msleep(5000)  # +++ !!!!!!!!!!!!!!!!!!!!!!

        except Exception as ex:
            logger.error(f"Error Initialise the runner function {ex} ")
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


# === The UI ===============================================================================================
class Ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(Ui, self).__init__()
        self.setupUi(self)
        """
        STARTING PROGRAM
        """
        # ============================================================================================
        self.show()

        # CREATE THE BUTTONS TASKS OF TAB_RUN_ONE_TASK

        # Let's get lists of all the elements of the GUI ordered by categories
        # It will be usefull to hide/show items of the GUI when necessary
        self.list_QPushButton, self.list_QLabel, self.list_QPlainTextEdit, self.list_Line, self.list_QWidget, self.list_QLabel, self.list_QRadioButton, self.list_QComboBox, self.list_QCheckBox, self.list_QTabWidget, self.list_QLineEdit = extract_items_from_gui_xml.main()
        print(f"self.list_QLabel  : {self.list_QLabel}")
        # WE NEED LIST OF ITEMS OF GUI ORDERED BY CATEGORIES

        self.list_items_tab_run = ['label_4_Title', 'label_info_campaign', 'button_Run', 'button_Quit',
                                   'label_log', 'button_Report', 'label_logo', 'comboBox_select_campaign',
                                   'label_4_Title_2', 'checkBox_smartphones', 'label_4_Title_3', 'label',
                                   'label_info_bubble', 'label_info_bubble_2', 'label_4_Title_4', 'label_info_bubble_3',
                                   'label_info_bubble_4', 'label_info_bubble_5', 'label_info_bubble_6', 'centralwid',
                                   'label_info_devices', 'label_yourcomputer', 'checkBox_Chrome', 'checkBox_Firefox',
                                   'button_OpenLogFile']
        self.list_items_tab_run_loading = ['label_loading_run', 'label_running',
                                           'label_loading_txt_run', 'label_loading_scan_smartphones']

        self.list_items_tab_run_one_task_WITHOUT_campaign_selected = ['comboBox_select_campaign_tab_run_one_task',
                                                                      'label_select_campaign_tab_run_one_task']

        self.list_items_tab_run_one_task_WITH_campaign_selected = ['label_select_device_tab_run_one_task',
                                                                   'radioButton_Computer', 'radioButton_Smartphone',
                                                                   'comboBox_select_browser_smartphone_tab_run_one_task',
                                                                   'label_select_smartphone_or_browser_tab_run_one_task',
                                                                   'label_cold_messaging',
                                                                   'label_explanation_run_one_task',
                                                                   'label_3', 'centralwid_youtube_tab_run_one_task',
                                                                   'label_log_run_one_task',
                                                                   'label_4_see_results_tab_run_one_task',
                                                                   'button_Report_2',
                                                                   'button_OpenLogFile_2',
                                                                   'label_loading_scan_smartphones_2',
                                                                   'label_loading_searching_tasks']

        self.list_items_tab_run_one_task_loadings = ['label_loading_scan_smartphones_2',
                                                     'label_loading_searching_tasks', ]

        self.list_items_tab_run_one_task = ['comboBox_select_campaign_tab_run_one_task',
                                            'label_select_campaign_tab_run_one_task',
                                            'label_select_device_tab_run_one_task',
                                            'radioButton_Computer', 'radioButton_Smartphone',
                                            'comboBox_select_browser_smartphone_tab_run_one_task',
                                            'label_select_smartphone_or_browser_tab_run_one_task',
                                            'label_cold_messaging',
                                            'label_explanation_run_one_task',
                                            'label_3', 'centralwid_youtube_tab_run_one_task',
                                            'label_log_run_one_task',
                                            'label_4_see_results_tab_run_one_task',
                                            'button_Report_2',
                                            'button_OpenLogFile_2']

        self.list_items_tab_settings = ['label_1_Title', 'label_Email', 'lineEdit_Email', 'label_info1',
                                        'label_license', 'lineEdit_License', 'button_SaveLicense', 'label_see_license',
                                        'label_android', 'label_title_appium', 'label_tesseract', 'label_title_android',
                                        'label_java', 'label_title_tesseract', 'label_title_buildtools',
                                        'label_title_java',
                                        'label_title_sdk', 'label_appium', 'label_title_node', 'label_2_Title',
                                        'label_build_tools', 'label_node', 'label_sdk',
                                        'button_Install_Smartphone_Automation', 'label_info2', 'label_enable_usb',
                                        'label_info3', 'button_ScanSmartphones', 'label_3_Title',
                                        'plainTextEdit_Smartphones', 'line',
                                        'label_info_bubble_7', 'label_info_bubble_8', 'centralwid_youtube_tab_settings']

        self.list_items_tab_settings_loading = ['label_loading_settings',
                                                'label_loading_scan_smartphones', 'label_loading_txt_settings',
                                                'label_loading_settings_usb_debugging']

        self.list_items_tab_help = ['tab_help', 'button_Doc', 'button_Videos', 'button_Tutorials', 'button_Support',
                                    'label_contact_email', 'label_logo_telegram', 'label_join_community', 'label_phone',
                                    'centralwid_youtube_tab_help']

        # CREATE THE BUTTONS OF TASKS OF TAB RUN_ONE_TASK
        self.CreateTasksButtons_for_Run_One_Task()
        # Let's hide the grid

        # Initialisazion of VARIABLES
        self.str_list_campaigns = ""
        self.HideAllQElements(True)
        self.str_list_campaigns_names = ""
        self.is_computer_ok = False
        self.are_smartphones_ok = False
        self.automation_with_smartphones = False
        self.automation_with_computer = False
        self.current_campaign_name = None
        self.is_profile_firefox_browser_ok = False
        self.is_profile_chrome_browser_ok = False
        self.current_campaign_id = ""
        self.current_campaign_id_one_task = ""
        self.tab_run_one_task_mode = 'computer'
        self.label_log_run_one_task.setText("")
        self.checkBox_smartphones.setChecked(False)
        self.checkBox_Chrome.setChecked(False)
        self.checkBox_Firefox.setChecked(False)
        # Smartphones automation software
        self.version_build_tools = "28.0.3"
        self.java = ''
        self.node = ''
        self.android = ''
        self.appium = ''
        self.tesseract = ''
        self.sdkmanager = ''
        self.build_tools = ''
        self.env_var_changed = ''
        self.list_tasksuser = []

        # Let's enable all the fields
        self.EnableTabRun(True)
        self.TabRunOneTask_Enable_1_2(True)

        # === We empty the tablesmartphones
        mymodules.EmptyTablesmartphones()
        # ====================================================================================================
        # ======================= WE PREPARE THE LABELS AND THE LINKS OF UI ==================================
        # ====================================================================================================
        self.statusbar.showMessage("Version N° " + __version__)

        self.label_contact_email.setOpenExternalLinks(True)
        self.label_join_community.setOpenExternalLinks(True)
        self.label_see_license.setOpenExternalLinks(True)
        self.label_enable_usb.setOpenExternalLinks(True)

        # === But we show the main loading animation gear at the begining. By this way, users will see at least something is going on
        # Let's show the loading gif in first window

        # === We need to check email and license number
        # Test if attribute exist:
        self.user_id, self.subscription_id, self.license_id = self.CheckLicense()

        # === We display the UI ==========
        self.plainTextEdit_Smartphones.setStyleSheet(f"color: Black")

        # === We need to prepare the radio button to show "Select browser" or "Select smartphone" depending
        # === on radio option button checked:

        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        # WE COLLECT CAMPAIGN ID SELECTED BY USER EACH TIME DROPDOWN LIST ARE CHANGED
        self.comboBox_select_campaign.currentIndexChanged.connect(self.GetCampaignID)
        # Show the radio button when user select a campaign in tab Run one task
        self.comboBox_select_campaign_tab_run_one_task.currentIndexChanged.connect(
            lambda: self.TabRunOneTask_1_CampaignSelected())

        self.tabWidget.currentChanged.connect(self.PrepareTabSettings)
        self.tabWidget.currentChanged.connect(self.PrepareTabRunOneTask)

        # === We search for the cookies of browser selected:
        # self.CheckProfileBrowser()

        self.HideAllQElements(False)

        # Let's hide all the tasks & labels of tab_run_one_task
        self.HideButtonsRunOneTask(True)

        self.label_loading_run.setHidden(True)
        self.label_running.setHidden(True)
        self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(True)
        self.radioButton_Computer.setHidden(True)
        self.radioButton_Smartphone.setHidden(True)
        self.label_explanation_run_one_task.setHidden(True)
        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(True)
        self.label_select_device_tab_run_one_task.setHidden(True)
        self.label_loading_scan_smartphones.setHidden(True)
        # Tab run One task
        self.label_4_see_results_tab_run_one_task.setHidden(True)
        self.button_Report_2.setHidden(True)
        self.button_OpenLogFile_2.setHidden(True)
        self.label_logo.setHidden(False)
        self.label_running.setHidden(True)
        self.label_loading_run.setHidden(True)
        self.label_log.setHidden(False)

        self.label_loading_scan_smartphones.setHidden(True)

        # === We need to hide the loading animation frames at the begining
        self.label_loading_txt_settings.setHidden(True)
        self.label_loading_txt_run.setHidden(True)
        self.label_loading_scan_smartphones.setHidden(True)
        self.label_loading_scan_smartphones_2.setHidden(True)
        self.label_loading_settings.setHidden(True)

        # === THis will handle the MULTITHREAD PART ===================
        self.threadpool = QThreadPool()

        logger.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # === Associate methods to the buttons of the UI ===========================================
        self.button_SaveLicense.clicked.connect(self.ButtonSaveLicense)
        self.button_ScanSmartphones.clicked.connect(self.ButtonStartScaningSmartphones)
        self.button_Support.clicked.connect(self.ButtonOpenSupport)
        self.button_Report.clicked.connect(self.ButtonStartPhoneBotReport)
        self.button_Report_2.clicked.connect(self.ButtonStartPhoneBotReport_2)
        self.button_OpenLogFile.clicked.connect(self.ButtonOpenLogFile)
        self.button_OpenLogFile_2.clicked.connect(self.ButtonOpenLogFile)
        self.button_Videos.clicked.connect(self.ButtonOpenVideoKnowledge)
        self.button_Doc.clicked.connect(self.ButtonOpenDoc)
        self.button_Quit.clicked.connect(self.ButtonQuit)
        self.button_Run.clicked.connect(self.ButtonStartPhoneBot)
        self.button_Tutorials.clicked.connect(self.ButtonOpenTutorials)
        self.checkBox_smartphones.clicked.connect(self.CheckBoxControlSmartphones)
        self.checkBox_Chrome.clicked.connect(self.ClickCheckBoxBrowserChrome)
        self.checkBox_Firefox.clicked.connect(self.ClickCheckBoxBrowserFirefox)
        self.button_Install_Smartphone_Automation.clicked.connect(self.ButtonInstallSmartphoneAutomation)
        self.TabRunOneTask_PrepareListTasksButtons('hide')
        self.tabWidget.setCurrentIndex(0)
        self.current_tab = 'run'

    def CreateTasksButtons_for_Run_One_Task(self):
        """
        This method will create the buttons for the tasks of tab Run_one_task
        :param self:
        :return:
        """

        # grid_layout.setSizeConstraint(grid_layout.SetFixedSize)
        _translate = QtCore.QCoreApplication.translate

        mysql_connection, mysql_cursor = mymodules.get_mysql_connection()
        SQL_DETAILS_OF_TASKS = f"SELECT tasks.id as task_id, tasks.name as task_name, tasks.introduction as task_intro, platforms.name as platform_name, type_tasks.name as type_task_name, categories.name as category_name \
                                                      FROM W551je5v_pb_tasks AS tasks \
                                                      INNER JOIN W551je5v_pb_platforms AS platforms  \
                                                      ON platforms.id = tasks.id_platform  \
                                                      INNER JOIN W551je5v_pb_type_tasks AS type_tasks  \
                                                      ON tasks.id_type_task = type_tasks.id  \
                                                      INNER JOIN W551je5v_pb_categories AS categories  \
                                                      ON platforms.id_category = categories.id  \
                                                      WHERE tasks.enable=1 ORDER BY categories.id"
        mysql_cursor.execute(SQL_DETAILS_OF_TASKS)
        tuple_all_tasks_user = mysql_cursor.fetchall()

        SQL_COUNT_CATEGORIES = """SELECT COUNT(*) FROM W551je5v_pb_categories"""
        mysql_cursor.execute(SQL_COUNT_CATEGORIES)
        tuple_number_categories = mysql_cursor.fetchone()
        print(tuple_number_categories)
        number_categories = tuple_number_categories['COUNT(*)']
        print(len(tuple_all_tasks_user))
        # We need to prepare a grid of 2 columns for the tasks
        # So we get the half of quantity task and we loop in columns and rows
        total_tasks = len(tuple_all_tasks_user)
        row = 0
        col = 0
        # we need to know when we reach the half of tasks in order to start to display second column
        middle_row = total_tasks
        # old_category is necessary to display the labels titles of categories of buttons
        old_category = ''
        category_added = False

        self.tasks_buttons = []
        self.categories_labels = []

        # WE LOOP ALL THE TAKS
        for task in tuple_all_tasks_user:
            # LET's CHECK IF WE ARE IN A NEW CATEGORY
            print(f"task : {task}")
            if old_category != task['category_name']:

                # self.hLayout = QtGui.QHBoxLayout()
                self.label_category = QtWidgets.QLabel(self.tab_run_one_task)
                self.label_category.setText(task['category_name'])

                self.label_category.setObjectName(f"pushButton_{task['platform_name']}_{task['task_id']}")
                self.categories_labels.append(self.label_category)
                myFont = QtGui.QFont()
                myFont.setBold(True)
                myFont.setPointSize(12)
                self.label_category.setFont(myFont)
                # grid_layout.addLayout(self.label_category, row, col)
                if row > total_tasks / 4 and row > 18:
                    row = 0
                    col += 1

                self.gridLayout.addWidget(self.label_category, row, col)
                category_added = True
                row += 1
            else:
                # We need to change it to false or the "row" counter will be incremented +1
                category_added = False

            # PREPARE ICONS
            icon = QtGui.QIcon()
            print(f"471 : task['platform_name'] : {task['platform_name']}")
            if str(task['platform_name']).find('Facebook') != -1:
                icon.addPixmap(QtGui.QPixmap(":/facebook/logo_facebook.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Instagram') != -1:
                icon.addPixmap(QtGui.QPixmap(":/instagram/logo_instagram.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Google_Map') != -1:
                icon.addPixmap(QtGui.QPixmap(":/gmap/logo_gmap.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Linkedin') != -1:
                icon.addPixmap(QtGui.QPixmap(":/linkedin/logo_linkedin.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Twitter') != -1:
                icon.addPixmap(QtGui.QPixmap(":/twitter/logo_twitter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            elif str(task['platform_name']).find('Craigslist') != -1:
                icon.addPixmap(QtGui.QPixmap(":/craigslist/logo_craigslist.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            elif str(task['platform_name']).find('YellowPages') != -1:
                icon.addPixmap(QtGui.QPixmap(":/yellowpages/logo_yellowpages.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            elif str(task['platform_name']).find('Leboncoin') != -1:
                icon.addPixmap(QtGui.QPixmap(":/leboncoin/logo_leboncoin.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Pages Jaunes') != -1:
                icon.addPixmap(QtGui.QPixmap(":/pagesjaunes/logo_pagesjaunes.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)

            elif str(task['platform_name']).find('Youtube') != -1:
                icon.addPixmap(QtGui.QPixmap(":/youtube/logo_youtube.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

            elif str(task['platform_name']).find('TikTok') != -1:
                icon.addPixmap(QtGui.QPixmap(":/tiktok/tiktok.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Freelancer') != -1:
                icon.addPixmap(QtGui.QPixmap(":/freelancer/freelancer.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Google_Map') != -1:
                icon.addPixmap(QtGui.QPixmap(":/gmap/gmap.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Upwork') != -1:
                icon.addPixmap(QtGui.QPixmap(":/upwork/upwork.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Snapshat') != -1:
                icon.addPixmap(QtGui.QPixmap(":/snapshat/snapshat.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

            elif str(task['platform_name']).find('Reddit') != -1:
                icon.addPixmap(QtGui.QPixmap(":/reddit/logo_reddit.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            elif str(task['platform_name']).find('Telegram') != -1:
                icon.addPixmap(QtGui.QPixmap(":/telegram/telegram.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            elif str(task['platform_name']).find('Whatsapp') != -1:
                icon.addPixmap(QtGui.QPixmap(":/whatsapp/whatsapp.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            elif str(task['platform_name']).find('sms') != -1:
                icon.addPixmap(QtGui.QPixmap(":/Sms/sms.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            elif str(task['platform_name']).find('Gear') != -1:
                icon.addPixmap(QtGui.QPixmap(":/configure_task/logo_configure_task.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.On)
            else:
                icon.addPixmap(QtGui.QPixmap(":/log_icon/log_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

            # WE create temp button
            self.btn = QPushButton(self.tab_run_one_task)

            # WE PREPARE THE LABEL OF  BUTTON
            label = f"{task['platform_name']} {task['type_task_name']} {task['task_name']}"

            # DESIGN OF BUTTON
            self.btn.setText(_translate("MainWindow", label))
            font = QtGui.QFont()
            font.setPointSize(9)
            self.btn.setFont(font)
            self.btn.setStyleSheet(
                "background-color: rgb(199, 199, 199);text-align:left;padding-left:30px;")
            self.btn.setIcon(icon)
            self.btn.setObjectName(
                f"pushButton_{task['platform_name']}_{task['task_id']}")
            print(f"pushButton_{task['platform_name']}_{task['task_id']}")
            # self.btn.setGeometry(200, 150, 100, 40)
            self.tasks_buttons.append(self.btn)
            self.list_items_tab_run_one_task.append(f"pushButton_{task['platform_name']}_{task['task_id']}")
            self.list_items_tab_run_one_task_WITH_campaign_selected.append(
                f"pushButton_{task['platform_name']}_{task['task_id']}")

            # WHY IT IS ALWAYS TASK_ID = 52??????
            # solution here : https://stackoverflow.com/a/40705324/10551444
            self.btn.clicked.connect(
                lambda checked, task_id=task['task_id']: self.Click_pushButtonComputerOrSmartphone(task_id))
            # self.btn.setStyleSheet("margin-right: 5px;")
            self.gridLayout.addWidget(self.btn, row, col)
            # self.gridLayout.setColumnMinimumWidth(2 * col + 1, 10)
            row += 1

            if row < middle_row:
                if row > (total_tasks) / 4 and row > 18:
                    if category_added:
                        middle_row = row
                        row = 0
                        col += 1
            old_category = task['category_name']
        print(f"self.tasks_buttons : {self.tasks_buttons}")
        print(f"self.list_items_tab_run_one_task : {self.list_items_tab_run_one_task}")

    def CheckEnvironmentForSmartphones(self, progress_callback):
        # We need to check if smartphones necessary softwares are installed or not
        # We use function check_envrionment which is different between Mac and Windows
        from modules import prepare_envir_appium
        java, node, android, appium, tesseract, sdkmanager, build_tools, env_var_changed = False, False, False, False, False, False, False, False
        version_build_tools = 'build-tools;28.0.3'

        if platform.system() == 'Darwin':
            java, node, android, appium, tesseract, sdkmanager, build_tools = prepare_envir_appium.check_envrionment(
                java,
                node,
                android,
                appium,
                tesseract,
                sdkmanager,
                build_tools,
                version_build_tools)
        else:
            java, node, android, appium, tesseract, sdkmanager, build_tools, env_var_changed = prepare_envir_appium.check_envrionment(
                java,
                node,
                android,
                appium,
                tesseract,
                sdkmanager,
                build_tools,
                version_build_tools)

        self.java = java
        self.node = node
        self.android = android
        self.appium = appium
        self.tesseract = tesseract
        self.sdkmanager = sdkmanager
        self.build_tools = build_tools
        self.env_var_changed = env_var_changed

        # 28.0.3 is the version of build-tools

        return "The Tab Settings is ready"

    def PrepareTabRunOneTask(self):

        if self.tabWidget.currentIndex() == 2:
            if self.current_campaign_id_one_task != '' and self.current_campaign_id_one_task != None:
                self.TabRunOneTask_HideSelectSmartphoneBrowser(True)
                self.TabRunOneTask_ShowHideTasksButtons('hide')
                self.HideSelectDeviceAndBrowser(True)
                self.label_log_run_one_task.setText("Please select a campaign and a device")
                self.radioButton_Computer.setChecked(False)
                self.radioButton_Smartphone.setChecked(False)

    def PrepareTabSettings(self):

        if self.tabWidget.currentIndex() == 2:
            print("check env smartphones")

            # WE WILL NOT RUN THIS LONG TIME FUNCTION EACH TIME USER CLICK ON TABS,
            # WE WILL DO IT ONCE, AND THEN MEMORIZE IN self. VARIABLES AND TEST THEM
            self.label_loading_settings_usb_debugging.setHidden(True)

            if self.java == '' and self.node == '' and self.android == '' and self.appium == '' and \
                    self.tesseract == '' and self.sdkmanager == '' and self.build_tools == '' and \
                    self.env_var_changed == '':
                self.HideAllQElements(True)
                self.line.setHidden(True)
                self.tabWidget.setTabEnabled(0, False)
                self.tabWidget.setTabEnabled(1, False)
                self.tabWidget.setTabEnabled(3, False)
                self.label_loading_txt_settings.setHidden(True)
                self.label_loading_scan_smartphones.setHidden(True)

                # ANIMATED GIF WITH GEAR
                self.label_loading_settings.setHidden(False)
                self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_settings.setMovie(self.gif_loading)
                self.gif_loading.start()

                # ANIMATED GIF WITH USB DEBUGGING EXPLAINER
                self.label_loading_settings_usb_debugging.setHidden(False)
                self.gif_loading_settings_usb_debugging = QMovie(
                    mymodules.LoadFile("gui/img/loading_tab_settings.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_settings_usb_debugging.setMovie(self.gif_loading_settings_usb_debugging)
                self.gif_loading_settings_usb_debugging.start()

                # WE SET UP THE FUNCTION
                worker = Worker(
                    self.CheckEnvironmentForSmartphones)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)

                # Execute
                logger.info(
                    f"self. Before to run PrepareTabSettings>> CheckEnvironmentForSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                self.threadpool.start(worker)
                logger.info(
                    f"self. After to run PrepareTabSettings>> CheckEnvironmentForSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    # =============================================================================
    # ======================= TAB RUN ONE TASK ====================================
    # =============================================================================

    def GetCampaignID(self):
        """
        THis method just get the Campaign choice of user in tab Run
        :return:
        """
        self.current_campaign_name = str(self.comboBox_select_campaign.currentText())
        self.current_campaign_id = self.GetCurrentCampaignID(self.current_campaign_name)

    def TabRunOneTask_ShowHideTasksButtons(self, p_mode='', p_device=''):
        """
        This method will SHow/Enable/Disable buttons of tasks
        """
        logger.info(f"DEF ============= TabRunOneTask_ShowHideTasksButtons {p_mode} =============================")

        if p_mode == 'show':

            # Hide Openlogfile button
            self.button_OpenLogFile.setHidden(True)

            # Build a list of id_task
            self.list_id_task = []
            for taskuser in self.list_tasksuser:
                print(f"taskuser : {taskuser}")
                self.list_id_task.append(mymodules.GetIDTask(taskuser['id']))
            for button in self.tasks_buttons:
                button_name = button.objectName()
                button_id = int(mymodules.extract_numbers_from_string(button_name))
                if button_id == 16:
                    print(f"button_id: {button_id}")
                    print(f"button_name : {button_name}")
                if button_name == 'pushButton_FB_3':
                    # print(f"button_id: {button_id}")
                    print(f"button_name : {button_name}")
                # button = getattr(self, button_name)
                # print(f"button : {button} - {type(button)}")
                # IF IT IS NOT THE CONFIG BUTTON

                if button_id in self.list_id_task:
                    button.setHidden(False)
                    button.setEnabled(True)
                else:
                    button.setHidden(False)
                    if button_name.find("pushButton_config") != -1:
                        button.setEnabled(True)
                    else:
                        button.setEnabled(False)
        elif p_mode == 'hide':
            # Show Openlogfile button
            self.button_OpenLogFile.setHidden(False)
            self.label_4_see_results_tab_run_one_task.setHidden(True)
            self.button_Report_2.setHidden(True)
            self.button_OpenLogFile_2.setHidden(True)
            for button in self.tasks_buttons:
                button_name = button.objectName()
                # print(f"button_name: {button_name}")
                # button = getattr(self, button_name)
                # print(f"button : {button} - {type(button)}")
                button.setHidden(True)

    # FUNCTION FOR THE CONFIG BUTTON
    def Click_pushButtonConfig(self, id_task):
        logger.info(f"DEF ============= Click_pushButtonConfig {id_task} =============================")
        """
        Function which will open configuration page on dashboard of the task user
        """
        if self.current_campaign_id_one_task == "" or self.current_campaign_id_one_task is None:
            mymodules.PopupMessage("Error", "Please select a campaign!")
        else:

            taskuser_id = mymodules.GetIDTaskUser(self.current_campaign_id_one_task, id_task)
            webbrowser.open(f'https://dashboard.phonebot.co/task_user/{taskuser_id}/edit', new=2)

    # FUNCTION FOR THE TASK BUTTON
    def HideButtonsRunOneTask(self, p_mode=''):
        """
        This method is called when user click on a task button
        We need to hide everything and show the label_log_run_one_task
        """
        logger.info(f"DEF ============= HideButtonsRunOneTask p_mode={p_mode}=============================")

        for button in self.tasks_buttons:
            button_name = button.objectName()
            # print(f"HideButtonsRunOneTask === button_name: {button_name}")
            button.setHidden(p_mode)
        # SHOW the TITLES of buttons
        for category_label in self.categories_labels:
            category_name = category_label.objectName()
            # print(f"HideButtonsRunOneTask === button_name: {button_name}")
            category_label.setHidden(p_mode)
        # self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(p_mode)

    def Click_pushButtonComputerOrSmartphone(self, id_task):
        logger.info(f"DEF ============ Click_pushButtonComputerOrSmartphone {id_task} =========================")

        try:
            # get the taskuser ID from campaign_id and id_task:
            if self.current_campaign_id_one_task == "" or self.current_campaign_id_one_task is None:
                mymodules.PopupMessage("Error", "Please select a campaign!")
            else:
                self.browser = self.comboBox_select_browser_smartphone_tab_run_one_task.currentText()

                print(f"browser : {self.browser}")
                if self.browser == "" or self.browser is None:
                    self.label_select_smartphone_or_browser_tab_run_one_task.setStyleSheet("color:red")
                    if self.tab_run_one_task_mode == 'computer':
                        self.label_select_smartphone_or_browser_tab_run_one_task.setText("Please select a browser")
                        mymodules.PopupMessage("Error", "Please select a browser!")

                    elif self.tab_run_one_task_mode == 'smartphone':
                        self.label_select_smartphone_or_browser_tab_run_one_task.setText("Please select a smartphone")

                else:
                    self.id_task = id_task
                    taskuser_id = mymodules.GetIDTaskUser(self.current_campaign_id_one_task, id_task)
                    self.taskuser_id = taskuser_id
                    print(f"""
                            ***** Running Task on Computer ***** 
                            id_task : {id_task}
                            taskuser_id : {taskuser_id}
                            browser : {self.browser}
                            *************************************
                            """)
                    self.TabRunOneTask_Enable_1_2(False)
                    self.HideButtonsRunOneTask(True)
                    self.label_log_run_one_task.setHidden(False)
                    self.label_log_run_one_task.setText("Please wait... PhoneBot will is launching the automation...")

                    # Pass the function to execute
                    # Pass the function to execute
                    try:
                        worker = Worker(
                            self.RunOneTaskComputerOrSmartphone)  # Any other args, kwargs are passed to the run function
                        worker.signals.result.connect(self.print_output)
                        worker.signals.finished.connect(self.thread_complete)
                        worker.signals.progress.connect(self.progress_fn)
                        # Execute
                        logger.info(
                            f"self. Before to run Click_pushButtonComputerOrSmartphone : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                        self.threadpool.start(worker)
                        logger.info(
                            f"self. After to run Click_pushButtonComputerOrSmartphone : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                    except Exception as ex:
                        logger.error(f"Error worker = Worker(self.RunOneTaskComputerOrSmartphone) :{ex}")
        except Exception as ex:
            print(f"ErrorTask N° {id_task} : {ex}")

    # === SHOW/HIDE THE TASK BUTTONS OF TAB 'Run one Task'
    def TabRunOneTask_PrepareListTasksButtons(self, p_action, p_device="computer"):
        """
        This function will check show or hide the Tasks buttons depending of selected device
        For example a computer can't automate snapshat or tiktok. Only smartphone can
        SO we need first to built a list of enable and available taskusers based on fields:
        'enable"=1
        "computer"=1
        of table tables W551je5v_pb_tasks and W551je5v_pb_tasks_users

        :param p_action:
        :return:
        """
        logger.info(
            f"DEF ============= TabRunOneTask_PrepareListTasksButtons p_action={p_action} p_device {p_device}=============================")
        # SOMETIMES I DON'T KNOW WHY TabRunOneTask_1_CampaignSelected IS EXECUTED,
        # SO WE NEED TO CHECK IF CURRENT TAB IS Run One Task
        mysql_connection, mysql_cursor = mymodules.get_mysql_connection()
        if self.tabWidget.currentIndex() == 1:
            # We make the list of buttons

            if p_action == "show":
                if p_device == 'computer':
                    self.tab_run_one_task_mode = 'computer'
                    self.list_tasksuser = mymodules.GetAllTasksDetails(self.current_campaign_id_one_task, 'Computer')
                    # self.TabRunOneTask_ShowHideTasksButtons('show', 'computer')

                elif p_device == 'smartphone':
                    self.tab_run_one_task_mode = 'smartphone'
                    self.list_tasksuser = mymodules.GetAllTasksDetails(self.current_campaign_id_one_task, 'Smartphone')

                    # self.TabRunOneTask_ShowHideTasksButtons('show', 'smartphone')

            if p_action == "hide":
                self.TabRunOneTask_ShowHideTasksButtons('hide')

        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

    def GetCurrentCampaignID(self, p_campaign_name):
        """
        This function dget the ID campaign from campaign name
        :param p_campaign_name:
        :return:
        """
        # Get the current Camapign ID selected by user
        logger.info(f"DEF ============ GetCurrentCampaignID {p_campaign_name} =========================")

        pos_fin_id_campaign = str(p_campaign_name).find('-')
        return p_campaign_name[:pos_fin_id_campaign]

    # === Function to show the Select device field and label when user has selected a campaign:
    def TabRunOneTask_1_CampaignSelected(self):
        logger.info(f"DEF ============ TabRunOneTask_1_CampaignSelected =========================")
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        # HIDE ALL THE BUTTONS AND LIST BROWSERS/SMARTPHONE
        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(True)
        self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
        self.radioButton_Computer.setChecked(False)
        self.radioButton_Smartphone.setChecked(False)
        self.label_explanation_run_one_task.setHidden(True)
        # SOMETIMES I DON'T KNOW WHY TabRunOneTask_1_CampaignSelected IS EXECUTED,
        # SO WE NEED TO CHECK IF CURRENT TAB IS Run One Task
        if self.tabWidget.currentIndex() == 1:
            self.current_campaign_name_one_task = str(self.comboBox_select_campaign_tab_run_one_task.currentText())
            self.current_campaign_id_one_task = self.GetCurrentCampaignID(self.current_campaign_name_one_task)

            print(
                f"self.current_campaign_id_one_task : {self.current_campaign_id_one_task} {type(self.current_campaign_id_one_task)}")
            # IF NO CAMPAIGN IS SELECTED ---
            if self.current_campaign_id_one_task is None or self.current_campaign_id_one_task == 'None' or self.current_campaign_id_one_task == "0":

                self.label_select_campaign_tab_run_one_task.setText("1. Please select a campaign")
                # Hide labels 'Select device' & 'select smarthpone/browsers'---
                self.label_select_device_tab_run_one_task.setHidden(True)
                self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(True)
                self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
                self.label_explanation_run_one_task.setHidden(True)
                # Hide radio button ---
                self.radioButton_Computer.setHidden(True)
                self.radioButton_Smartphone.setHidden(True)

            # IF CAMPAIGN IS SELECTED ---
            else:
                print(f"Campaign has been selected : {self.current_campaign_name_one_task}")
                # WE NEED TO LOAD THE LIST OF TASKS FOR THIS SELECTED CAMPAIGN
                self.list_tasksuser = mymodules.GetAllTasksDetails(self.current_campaign_id_one_task)
                # Display radio button & '2. Select device' ---
                self.label_select_device_tab_run_one_task.setHidden(False)
                self.radioButton_Computer.setHidden(False)
                self.radioButton_Smartphone.setHidden(False)
                # self.radioButton_Computer.setChecked(True)
                self.radioButton_Computer.toggled.connect(
                    lambda: self.TabRunOneTask_2_SelectDevice(self.radioButton_Computer))
                self.radioButton_Smartphone.toggled.connect(
                    lambda: self.TabRunOneTask_2_SelectDevice(self.radioButton_Smartphone))

    # === Function to check the radio button "Computer" or "Smartphone" in tab "Run one task"
    def HideSelectDeviceAndBrowser(self, p_hidden=True):
        logger.info(f"DEF ============ HideSelectDeviceAndBrowser p_hidden {p_hidden} =========================")
        # HIDE ALL THE BUTTONS AND LIST BROWSERS/SMARTPHONE
        try:
            self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(p_hidden)
            self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(p_hidden)
            self.label_explanation_run_one_task.setHidden(p_hidden)
            self.label_select_device_tab_run_one_task(p_hidden)
            self.radioButton_Computer.setHidden(p_hidden)
            self.radioButton_Smartphone.setHidden(p_hidden)
            self.label_select_device_tab_run_one_task(p_hidden)
        except Exception as ex:
            logger.error(f"ERROR : {ex}")

    def TabRunOneTask_2_SelectDevice(self, b):
        logger.info(f"DEF ============ TabRunOneTask_2_SelectDevice b {b} =========================")
        # SOMETIMES I DON'T KNOW WHY TabRunOneTask_1_CampaignSelected IS EXECUTED,
        # SO WE NEED TO CHECK IF CURRENT TAB IS Run One Task

        """
        if self.tabWidget.currentIndex() == 1:
            self.current_tab == "run_one_task"
            # WE HIDE  LABEL explanation
            self.label_explanation_run_one_task.setText(
                "Please click one of the buttons on the left side \nto execute one single task.")
            self.label_explanation_run_one_task.setHidden(True)
            self.HideSelectDeviceAndBrowser(True)
        """
        # IF RADIO BUTTON Computer ---
        if b.text() == "Computer":
            # IF Computer is CHECKED
            if b.isChecked() == True:
                # UNCHECK OPPOSITE RADIO BUTTON
                self.radioButton_Smartphone.setChecked(False)
                print(b.text() + " is selected")

                # WE HIDE EVERYTHING BECAUSE IT WILL TAKE A LONG TIME (SCAN SMARTPHONE? CHECK SOFTWARE)
                self.HideButtonsRunOneTask(True)
                self.TabRunOneTask_Enable_1_2(False)
                self.label_log_run_one_task.setHidden(False)
                self.label_log_run_one_task.setText(
                    "Please wait... PhoneBot is detecting your smartphones connected by USB to your computer.")

                # WE SHOW ANIMATED GIF OF SCANNING SMARTPHONE
                self.label_loading_searching_tasks.setHidden(False)

                self.gif_loading_searching_tasks = QMovie(
                    mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_searching_tasks.setMovie(self.gif_loading_searching_tasks)
                self.label_log_run_one_task.setHidden(True)
                self.gif_loading_searching_tasks.start()

                # WE SET UP THE FUNCTION
                worker = Worker(self.scan_browsers_profiles)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)
                # WE Execute
                logger.info(
                    f"self. Before to run scan_browsers_profiles : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                self.threadpool.start(worker)
                logger.info(
                    f"self. After to run scan_browsers_profiles : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
            # IF Computer is NOT CHECKED
            else:
                print(b.text() + " is deselected")
                self.label_select_smartphone_or_browser_tab_run_one_task.setText("3. Please select a smartphone:")

                if self.radioButton_Smartphone.isChecked():
                    # IF Smarptohne is CHECKED, WE HIDE 'Select browser/smartphone List'
                    self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(False)

                else:
                    # IF Smarpthone is NOT CHECKED, WE SHOW 'Select browser/smartphone List'
                    self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
        # IF RADIO BUTTON Smartphone ---
        if b.text() == "Smartphone":
            # IF Smartphone is CHECKED
            if b.isChecked() == True:
                self.tab_run_one_task_mode == 'smartphone'
                # UNCHECK OPPOSITE RADIO BUTTON
                self.radioButton_Computer.setChecked(False)
                # WE HIDE EVERYTHING BECAUSE IT WILL TAKE A LONG TIME (SCAN SMARTPHONE? CHECK SOFTWARE)
                self.HideButtonsRunOneTask(True)
                self.TabRunOneTask_Enable_1_2(False)
                self.label_log_run_one_task.setText(
                    "Please wait... PhoneBot is detecting your smartphones connected by USB to your computer.")

                # WE SHOW ANIMATED GIF OF SCANNING SMARTPHONE
                self.label_loading_scan_smartphones_2.setHidden(False)
                self.gif_loading_scan = QMovie(
                    mymodules.LoadFile("gui/img/loading_scan_smartphones_V0003.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_scan_smartphones_2.setMovie(self.gif_loading_scan)
                self.label_log_run_one_task.setHidden(True)
                self.gif_loading_scan.start()

                # WE SET UP THE FUNCTION
                worker = Worker(
                    self.scan_details_smartphones_tab_run_once)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)
                # WE Execute
                logger.info(
                    f"self. Before to run ButtonStartScaningSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                self.threadpool.start(worker)
                logger.info(
                    f"self. After to run ButtonStartScaningSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
            # IF Smartphone is NOT CHECKED
            else:
                print(b.text() + " is deselected")
                self.label_select_smartphone_or_browser_tab_run_one_task.setText("3. Please select a smartphone:")

                if self.radioButton_Computer.isChecked():

                    # IF Computer is CHECKED, WE SHOW 'Select browser/smartphone List'
                    self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(False)
                    self.label_explanation_run_one_task.setHidden(False)

                else:
                    # IF Computer is NOT CHECKED, WE HIDE 'Select browser/smartphone List'
                    self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
                    self.label_explanation_run_one_task.setHidden(True)

    # =============================== FUNCTIONS FOR GUI =====================================================

    def TryToHideShow(self, item, p_hidden):
        """
        Function which will try to HideShow an item of a tab of the gui
        :return:
        """
        if item == 'label_loading_settings_usb_debugging':
            print("label_loading_settings_usb_debugging")
        try:
            self.findChild(QPushButton, item).setHidden(p_hidden)
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass
        try:
            self.findChild(QLabel, item).setHidden(p_hidden)
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass
        try:
            self.findChild(QCheckBox, item).setHidden(p_hidden)
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass
        try:
            self.findChild(QComboBox, item).setHidden(p_hidden)
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass

        try:
            self.findChild(QLineEdit, item).setHidden(p_hidden)
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass
        try:
            self.findChild(QPlainTextEdit, item).setHidden(p_hidden)
            pass
        except:
            # print("HideTabRunCampaign Failed to Hide/Show item of GUI ")
            pass

    def HideAllLoadingLabels(self, p_hidden=None):
        """
        This function will hide all the loading labels and animated gif and text informations while a task is running
        :param p_hidden:
        :return:
        """
        self.label_loading_scan_smartphones.setHidden(p_hidden)
        self.label_loading_txt_run.setHidden(p_hidden)
        self.label_loading_run.setHidden(p_hidden)
        self.label_loading_scan_smartphones_2.setHidden(p_hidden)
        self.label_log_run_one_task.setHidden(p_hidden)
        self.label_loading_settings.setHidden(p_hidden)
        self.label_loading_txt_settings.setHidden(p_hidden)
        self.label_loading_scan_smartphones.setHidden(p_hidden)

    def HideLoadingsTabRunCampaign(self, p_hidden):
        """
        This method will hide all the elements of Tab 1 Run Campaign except the Loading stuff
        :return:

        """
        for item in self.list_items_tab_run_loading:
            self.TryToHideShow(item, p_hidden)
        for item in self.list_items_tab_run:
            self.TryToHideShow(item, not p_hidden)

    def HideLoadingsTabRunOneTask(self, p_hidden):
        """
        This method will hide all the elements of Tab 1 Run Campaign except the Loading stuff
        :return:
        """
        print(f"self.list_items_tab_run_one_task_loadings : {self.list_items_tab_run_one_task_loadings}")
        for item in self.list_items_tab_run_one_task_loadings:
            self.TryToHideShow(item, p_hidden)
        for item in self.list_items_tab_run_one_task:
            self.TryToHideShow(item, not p_hidden)

    def HideLoadingsTabSettings(self, p_hidden):
        """
        This method will hide all the elements of Tab 1 Run Campaign except the Loading stuff
        :return:
        """
        for item in self.list_items_tab_settings_loading:
            self.TryToHideShow(item, p_hidden)
        for item in self.list_items_tab_settings:
            self.TryToHideShow(item, not p_hidden)

    def HideAllQElements(self, p_hidden=None):
        print("================= HideAllQElements =======================")

        for item in self.list_QPushButton:
            if item not in self.tasks_buttons and item not in [
                'button_OpenLogFile_2',
                'button_Report_2'
            ]:
                # print(f"item : {item} - {type(item)}")
                self.findChild(QPushButton, item).setHidden(p_hidden)

        for item in self.list_QLabel:
            # print(f"item : {item}")
            if item not in [
                'label_cold_messaging',
                'label_cold_messaging_2',
                'label_cold_messaging_3',
                'label_cold_messaging_4',
                'label_select_campaign_tab_run_one_task',
                'label_3',
                'label_select_device_tab_run_one_task',
                'label_select_smartphone_or_browser_tab_run_one_task',
                'label_explanation_run_one_task',
                'label_4_see_results_tab_run_one_task']:
                # print(f"1166 : item : {item}")
                self.findChild(QLabel, item).setHidden(p_hidden)

        for item in self.list_QPlainTextEdit:
            self.findChild(QPlainTextEdit, item).setHidden(p_hidden)

        self.line.setHidden(p_hidden)

        for item in self.list_QWidget:
            if item not in ['tab_run', 'tab_run_one_task', 'tab_settings', 'tab_help']:
                self.findChild(QWidget, item).setHidden(p_hidden)

        for item in self.list_QLineEdit:
            self.findChild(QLineEdit, item).setHidden(p_hidden)

        for item in self.list_QComboBox:
            if item not in ['comboBox_select_browser_smartphone_tab_run_one_task']:
                self.findChild(QComboBox, item).setHidden(p_hidden)

        for item in self.list_QRadioButton:
            if item not in ['radioButton_Computer', 'radioButton_Smartphone']:
                self.findChild(QRadioButton, item).setHidden(p_hidden)

        for item in self.list_QCheckBox:
            self.findChild(QCheckBox, item).setHidden(p_hidden)

        # WE FINISH THE JOB BY SHOWINNG OR HIDDING THE LOADING LABELS AND TEXT
        if p_hidden:
            self.HideAllLoadingLabels(False)
        else:
            self.HideAllLoadingLabels(True)

    def ChangeColorsNecessarySoftwares(self, java, node, android, appium, tesseract, sdkmanager, build_tools):
        print(
            "======================================= ChangeColorsNecessarySoftwares ===============================================")
        print(
            f"java : {java}, node: {node}, android: {android}, appium: {appium}, tesseract: {tesseract}, sdkmanager: {sdkmanager}, build_tools: {build_tools}")
        # System to display in GUI which softwares are installed and which are not!
        software_text, software_color = mymodules.return_text_color_software(java)
        self.label_java.setText(software_text)
        self.label_java.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(node)
        self.label_node.setText(software_text)
        self.label_node.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(sdkmanager)
        self.label_sdk.setText(software_text)
        self.label_sdk.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(appium)
        self.label_appium.setText(software_text)
        self.label_appium.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(tesseract)
        self.label_tesseract.setText(software_text)
        self.label_tesseract.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(build_tools)
        self.label_build_tools.setText(software_text)
        self.label_build_tools.setStyleSheet(f"color: {software_color}")

        software_text, software_color = mymodules.return_text_color_software(android)
        self.label_android.setText(software_text)
        self.label_android.setStyleSheet(f"color: {software_color}")

        if (java and node and android and appium and tesseract and build_tools and android) == False:

            self.label_2_Title.setStyleSheet(f"color: Red")
            self.label_info2.setText(
                'It is missing some softwares! You can try to install all of<br> them in 1 click with this button above. After that, if some installation fails,<br>you will have the possibility to install them one by one <br>by clicking on the links which will show up above.')
            self.label_info2.setStyleSheet(f"color: Red")
            self.label_log.setText(
                "<b>ERROR SMARTPHONE AUTOMATION:</b> It is missing some programs. Go to 'Settings' tab and click on 'Install SmartPhone Automation' button. You may need to restart PhoneBot.<br>=> If the problem persists, please contact <a href='mailto:support@phonebot.co'>support@phonebot.co</a>.<br>You can skip this part by running automation on your computer only. You will have to check only the option 'Your computer'  and uncheck the option 'Your smartphone(s).")
            self.label_log.setStyleSheet(f"color: Red")

        else:
            self.label_2_Title.setStyleSheet(f"color: Green")
            self.label_info2.setText('The softwares are correctly installed.')
            self.label_info2.setStyleSheet(f"color: Green")
            self.label_log.setText(
                "<b>SMARTPHONE AUTOMATION OK:</b> PhoneBot tested everything regarding the necessary software. Everything seems fine.")
            self.label_log.setStyleSheet(f"color: Green")
            self.checkBox_smartphones.setStyleSheet(f"color: Black")
            self.checkBox_smartphones.setText('Your smartphone(s)')

        # We will update the sqlite settings table in order to inform the GUI that softwares are fine!
        # ===================================== CREATE SQLITE3 CONNECTION ==============================================
        sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()

        sqlite_cursor.execute("UPDATE settings set java_ok=?, node_ok=?, android_ok=?, appium_ok=?, tesseract_ok=?,  \
            sdkmanager_ok=?, build_tools_ok=? WHERE id=?", (
            int(java), int(node), int(android), int(appium), int(tesseract), int(sdkmanager), int(build_tools), 1))
        sqlite_connection.commit()
        try:
            sqlite_cursor.close()
            sqlite_connection.close()
        except Exception as ex:
            logger.error(f"Error closing sqlite : {ex}")

    # =============================== FUNCTIONS FOR LICENSE =====================================================
    # ===================================================================================================================
    # ============================= FUNCTION TO CHECK THE PAYMENT OF SUBSCRIPTION, ======================================
    # ============================= THE LICENSE KEY, EXPIRATION DATE AND MAC ADDRESS ====================================
    # ===================================================================================================================
    def CheckSubscription(self, email):

        logger.info(
            f"======================================== CheckSubscription {email} - {self.license_key_config} ============================")

        """
        This function is called by CheckLicense
        It returns self.user_id, self.license_key_config, subscription_id or false, false , false
        There are 2 scenarios:
            self.license_key_config = 'affiliate' => We have to get the real email and real license_key_config of master affiliate
                                                and check if his license is ok
            else:
                it is the master user or normal user

        """

        try:
            # ===================================================================================================================
            # ==================================== CONNECTION TO MYSQL AND READ config.ini ======================================
            # ===================================================================================================================
            mysql_connection, mysql_cursor = mymodules.get_mysql_connection()

            if str(self.license_key_config).lower() == 'affiliate':
                # === Get the real email of master
                logger.info("# === 1rst affiliate details")
                sql_get_details_affiliates = f"SELECT license_id FROM W551je5v_pb_affiliates WHERE email = '{email}' AND enable=1"

                mysql_cursor.execute(sql_get_details_affiliates)
                details_affiliate = mysql_cursor.fetchone()
                if details_affiliate is None:
                    # === ERROR MESSAGE
                    logger.error("ERROR : details_affiliate is None")
                else:
                    logger.info("# === 2nd  license details")
                    sql_get_details_license = f"SELECT hash,user_id,CAST(expires_at AS CHAR),order_id,product_id,id FROM W551je5v_lmfwc_licenses WHERE id={details_affiliate[0]}"

                    mysql_cursor.execute(sql_get_details_license)
                    details_license = mysql_cursor.fetchone()

                    if details_license is None:
                        # === ERROR MESSAGE
                        logger.error("ERROR : details_license is None")
                    else:
                        try:
                            order_id_of_license = details_license[0]
                            date_expire_str = details_license[2]
                            product_id = details_license[4]
                            order_id = details_license[3]
                            self.user_id = details_license[1]
                            self.license_id = details_license[5]
                            print(f"self.license_id : {self.license_id}")
                        except Exception as ex:
                            logger.error(f"ERROR trying to get license and order details :{ex}")
                        license_key_found = True
                        logger.info(f"# === 3rd get Master user email {self.user_id}")
                        sql_get_details_master_affiliate = f"SELECT user_email FROM W551je5v_users WHERE ID={self.user_id}"

                        mysql_cursor.execute(sql_get_details_master_affiliate)
                        details_master_affiliate = mysql_cursor.fetchone()

                        if details_master_affiliate is None:
                            # === ERROR MESSAGE
                            logger.error("ERROR : details_master_affiliate is None")
                        else:
                            logger.info("# === 4th get Master user email and we substitute")
                            # === temporaly in this function with variable email
                            email = details_master_affiliate[0]
                            print(f"email : {email}")

            # ===================================================================================================================
            # === Get the date of today from online server -----------------------------------------------------------

            date_now_online_DATE = GetTimeFromInternet()

            # ===================================================================================================================
            # ==================================== GET THE USER ID FROM WP DATABASE =============================================
            # ===================================================================================================================

            logger.info(f"Your email in config.ini is '{email}")
            logger.info(f"Your license_key in config.ini is '{self.license_key_config}")
            sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
            mysql_cursor = mysql_connection.cursor(buffered=True)
            mysql_cursor.execute(sql_user_id)
            self.user_id = mysql_cursor.fetchone()
            if self.user_id is None:
                logger.critical(
                    "There are no user id in Phonebot.co Database! Check your config.ini. Maybe you did not pay your subscription or your trial period has expired.\nIf your subscription is active, try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
                mymodules.PopupMessage("No user id in Phonebot.co Database!",
                                       "There is a problem with your email. Please be sure it correspond to the one you registered on PhoneBot.co. It is it correct, maybe you did not pay your subscription or your trial period has expired. if the problem persists please contact support@phonebot.co")

                self.label_1_Title.setStyleSheet(f"color: Red")
                self.label_license.setStyleSheet(f"color: Red")
                self.label_Email.setStyleSheet(f"color: Red")
                self.label_info1.setStyleSheet(f"color: Red")
                self.label_info1.setText("Please verify your email.")
                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText("<b>ERROR EMAIL</b> Your email was not found in Phonebot.co  \
                    Database! Maybe you did not pay your subscription or your trial period has expired.<br> => If   \
                    your subscription is active, try to restart PhoneBot. if the problem persists please contact   \
                    <a href='mailto:support@phonebot.co'>support@phonebot.co</a>")
                return False, False, False
            else:
                self.user_id = str(self.user_id[0])
                logger.info("User ID found on Phonebot.co :-) :" + str(self.user_id))
            # IF WE DIDN'T ALREADY CHECK FOR THE LICENSE,
            license_key_found = False
            if str(self.license_key_config).lower() != 'affiliate':

                # ============================ GET ALL THE LICENSES OF THIS USER =========================================

                sql_find_licenses = f"SELECT hash,user_id,CAST(expires_at AS CHAR),order_id,product_id,id from W551je5v_lmfwc_licenses WHERE user_id='{self.user_id}'"
                logger.info(f"You filled your license key in configi.ini.")
                mysql_cursor.execute(sql_find_licenses)
                print(f"sql_find_licenses : {sql_find_licenses}")

                tuple_hash_license_key = mysql_cursor.fetchall()
                list_hash_license_key = [item for item in tuple_hash_license_key]

                print(f"list_hash_license_key : {list_hash_license_key}")

                for hash_license_key in list_hash_license_key:
                    if mymodules.check_license(self.license_key_config, hash_license_key[0], self.label_log):
                        logger.info("License key found in PhoneBot.co.")

                        order_id_of_license = hash_license_key[0]
                        date_expire_str = hash_license_key[2]
                        product_id = hash_license_key[4]
                        order_id = hash_license_key[3]
                        self.license_id = hash_license_key[5]
                        print(f"self.license_id : {self.license_id}")
                        license_key_found = True
                        mymodules.Save_email_license_user_id_subscription_id(email, self.license_key_config,
                                                                             self.user_id,
                                                                             None, product_id)
                        break
                    else:
                        product_id = None
                        date_expire_str = None
                        license_key_found = False
                        logger.critical("PhoneBot did not match your License key.")

            # === If we found a correct license key in MYSQL PhoneBot, we can start to check the expiration date and the mac address
            if license_key_found:

                logger.info("You filled your license key in config.ini and PhoneBot checked it correctly.")

                # === Let's get imediatly the subscription ID as we will need it for the rest
                # === 1rst we need to get all the subscription of user in relation with the product in order to get the list of orders
                sql_subscription_list_of_user_for_a_product = f"select W551je5v_postmeta.post_id FROM W551je5v_postmeta INNER JOIN W551je5v_posts ON W551je5v_postmeta.post_id = W551je5v_posts.ID WHERE W551je5v_postmeta.meta_value='{order_id}' and W551je5v_posts.post_author = '{self.user_id}' and W551je5v_posts.post_type = 'subscription'"  # and W551je5v_postmeta.meta_value LIKE '%{order_id}%'"#and W551je5v_posts.all_order_ids LIKE '%{order_id}%'
                print(
                    f"sql_subscription_list_of_user_for_a_product : {sql_subscription_list_of_user_for_a_product}")
                mysql_cursor.execute(sql_subscription_list_of_user_for_a_product)
                tuple_subscription = mysql_cursor.fetchall()
                print(f"tuple_subscription : {tuple_subscription}")

                if tuple_subscription:
                    # =========================== SUBSCRIPTION EXIST ========================================
                    # We should prefill the License/Email form here.
                    # But we don't do it because we need to check the date expiration :-)
                    list_subscription = [item[0] for item in tuple_subscription]
                    print(f"list_subscription : {list_subscription}")
                    subscription_id = list_subscription[0]
                    self.label_1_Title.setStyleSheet(f"color: Green")
                    self.label_license.setStyleSheet(f"color: Green")

                    self.label_info2.setStyleSheet(f"color: Green")
                    self.label_info2.setText('The softwares are correctly installed.')
                    self.label_info1.setStyleSheet(f"color: Green")
                    self.label_info1.setText('Your PhoneBot is activated!')
                else:
                    subscription_id = None
                    list_subscription = None
                    logger.error(
                        "PhoneBot did not find your subscritpion in our system. Please contact support@phonebot.co")

                    self.label_1_Title.setStyleSheet(f"color: Red")
                    self.label_license.setStyleSheet(f"color: Red")
                    self.label_info1.setStyleSheet(f"color: Red")
                    self.label_info1.setText('Your PhoneBot is not activated!')
                    self.label_log.setStyleSheet(f"color: Red")
                    self.label_log.setText(
                        "<b>ERROR LICENSE</b> PhoneBot did not find your subscritpion in our system.<br>=> Please verify you copied-pasted the correct license key here in the License key field.")
                    # WE NEED TO BLOCK AND EMPTY THE CAMPAIGN DROPDOWN LIST
                    self.comboBox_select_campaign.clear()
                    self.comboBox_select_campaign_tab_run_one_task.clear()

                # === let's check for expiration date ================================================================

                # =============================================================================================================
                # ===================== IF date_expire EXIST, IT MEANS IT IS A TRIAL LICENSE ==================================
                # =============================================================================================================
                if date_expire_str is not None and date_expire_str != '':
                    date_expire = datetime.strptime(date_expire_str, "%Y-%m-%d %H:%M:%S")
                    print(f"date_expire : {date_expire}-{type(date_expire)}")
                    logger.info("Your Trial License is still valid.")
                    if date_expire < date_now_online_DATE:
                        logger.info(
                            "Your Trial License expired. You need to buy a license in order to use PhoneBot. We gave you for free during 2 weeks our PhoneBot. Did it help you to growth?")
                        logger.info(
                            "We gave you for free during 2 weeks our PhoneBot. Did it help you to growth? If yes, why not to invest in a license?")
                        logger.info(
                            "Please visit https://phonebot.co/pricing/ in order to purchase a PhoneBot license.")

                        self.label_1_Title.setStyleSheet(f"color: Red")
                        self.label_license.setStyleSheet(f"color: Red")

                        self.label_info1.setStyleSheet(f"color: Red")
                        self.label_info1.setText('Your PhoneBot is not activated!')
                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(
                            "<b>ERROR LICENSE:</b> Your Trial License expired. You need to buy a license in order to use PhoneBot. We gave you for free during 2 weeks our PhoneBot. Did it help you to growth?<br>=> We gave you for free during 2 weeks our PhoneBot. Did it help you to growth? If yes, why not to invest in a license?")
                        self.comboBox_select_campaign.clear()
                        self.comboBox_select_campaign_tab_run_one_task.clear()

                        message_txt = f'Hi,\n\Your Free trial License expired. You need to buy a pay plan in order to use PhoneBot\n\nPlease visit https://phonebot.co/pricing/ in order to purchase a PhoneBot license.\n\nKind regards.\n\nPhoneBot.co\'s team\n\nhttps://phonebot.co'
                        message_html = f"""
                                        <html>
                                            <head></head>
                                            <body>
                                            <p>Hi,<br><br>
                                            Your Free trial License expired. You need to buy a pay plan in order to use PhoneBot<br><br>
                                            Please visit <a href='https://phonebot.co/pricing/'>https://phonebot.co/pricing/</a> in order to purchase a PhoneBot license.<br><br>
                                            If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                            Kind regards.<br><br>
                                            PhoneBot.co\'s team<br>
                                            https://phonebot.co
                                            </p>
                                            </body>
                                        </html>
                                            """
                        try:
                            mymodules.SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                               'ALERT: Your Free trial License expired', message_txt, message_html,
                                               email)
                        except Exception as ex:
                            logger.error(f"{ex} => Error sending mail reminder about payment.")


                    else:
                        logger.info("Your Trial license seems to be valid for the moment.")
                        logger.info("PhoneBot check now if you run the bot on correct computer...")

                        """
                            ================================================================
                            ============================= UPDATE V0.003 ====================
                            ================================================================
                            I NEED TO HANDLE THE Checkingsubscription from affiliate computer to
                            Master user email and license
                             ================================================================
                            ================================================================
                            ================================================================

                        """
                        if self.license_key_config != 'affiliate':
                            mac_address_ok = mymodules.CheckMacAddress(subscription_id)

                            if mac_address_ok:
                                logger.info(
                                    "Your MAC Address is ok. PhoneBot tested everything regarding your subscription. It can run the bots.")

                                self.label_1_Title.setStyleSheet(f"color: Green")
                                self.label_license.setStyleSheet(f"color: Green")
                                self.label_info1.setStyleSheet(f"color: Green")
                                self.label_info1.setText('Your PhoneBot is activated!')

                                mymodules.Save_email_license_user_id_subscription_id(email, self.license_key_config,
                                                                                     self.user_id, subscription_id,
                                                                                     product_id)

                                self.lineEdit_License.setStyleSheet(f"color: Black")
                                self.lineEdit_License.setText(str(self.license_key_config))

                                return self.user_id, subscription_id, self.license_id

                            else:

                                logger.critical("Your MAC Address is not ok.")
                                mymodules.PopupMessage("Problem with your License Key!",
                                                       "You cannot install one license on several computers or install several trial licenses on the same computer.")

                                self.label_1_Title.setStyleSheet(f"color: Red")
                                self.label_license.setStyleSheet(f"color: Red")
                                self.label_info1.setStyleSheet(f"color: Red")
                                self.label_info1.setText('Your PhoneBot is not activated!')
                                self.label_log.setStyleSheet(f"color: Red")
                                self.label_log.setText(
                                    "<b>ONLY 1 LICENSE PER COMPUTER!</b> Your MAC Address is not ok.<br>=> You cannot install one license on several computers or install several trial licenses on the same computer.")
                                self.tabWidget.setCurrentIndex(2)
                                self.button_Run.setEnabled(False)
                                self.comboBox_select_campaign.clear()
                                self.comboBox_select_campaign_tab_run_one_task.clear()


                else:
                    # ========================================================================================================
                    # ===================== THERE IS not date_expire, IT MEANS IT IS A PAID LICENSE ===========================
                    # ========================================================================================================
                    # === We need to get all the orders from product_id and check if the last order was paid

                    # === We just get all the subscriptions of user for the product connected to his license, now
                    # === we need to get the list of orders
                    for subscription_id in list_subscription:
                        sql_order_list_of_user_for_a_subscription = f"SELECT meta_value FROM W551je5v_postmeta WHERE W551je5v_postmeta.post_id='{subscription_id}' and meta_key='order_id'"
                        mysql_cursor.execute(sql_order_list_of_user_for_a_subscription)
                        tuple_orders = mysql_cursor.fetchall()
                        list_orders = [item[0] for item in tuple_orders]
                        print(f"list_orders : {list_orders}")

                    # === Now we have the list of orders connected to the subscription in relation of the product
                    # === connected to his license,, we need to get the last order ID as it will be the most recent
                    # === then we'll be able to check the status of this order if it is complete or not
                    order_found = False

                    print(f"product_id : {product_id} - {type(product_id)}")
                    if self.license_key_config != 'affiliate':
                        mymodules.Save_email_license_user_id_subscription_id(email, license, self.user_id,
                                                                             subscription_id,
                                                                             product_id)
                    # ========================================= LIFETIME LICENSE ==================================
                    # === We add these lines of code to handle the Lifetime license issue =========================
                    if product_id != 6005 and product_id != 12173:

                        # ==============================================================================================

                        if list_orders is None or list_orders == '' or len(list_orders) == 0:
                            logger.error(
                                f"There are no order id for subscription N° {subscription_id} - product N° {product_id} - user N° {self.user_id} in Phonebot.co Database!:-( Please contact support@phonebot.co")
                            logger.info(
                                f"PhoneBot did not find order...Mmmmm... So PhoneBot will try to search for last_order_id.")
                            sql_last_order_id = f"SELECT meta_value from W551je5v_postmeta WHERE meta_key='last_order_id' AND post_id='{subscription_id}'"
                            print(f"sql_last_order_id : {sql_last_order_id}")
                            mysql_cursor.execute(sql_last_order_id)
                            tuple_sql_last_order_id = mysql_cursor.fetchall()

                            if tuple_sql_last_order_id:

                                list_orders = [item[0] for item in tuple_sql_last_order_id]
                                print(f"list_orders : {list_orders}")
                                order_found = True
                            else:
                                logger.critical(
                                    f"There are DEFININITLY not order id for subscription N° {subscription_id} - product N° {product_id} - user N° {self.user_id} in Phonebot.co Database!:-( Please contact support@phonebot.co")
                                logger.critical(
                                    "There are no order id in Phonebot.co Database!:-( Please contact support@phonebot.co")
                                mymodules.PopupMessage("no order id in Phonebot.co Database!",
                                                       f"There are DEFININITLY not order id for subscription N° {subscription_id} - product N° {product_id} - user N° {self.user_id} in Phonebot.co Database!:-( Please contact support@phonebot.co")

                                self.label_1_Title.setStyleSheet(f"color: Red")
                                self.label_license.setStyleSheet(f"color: Red")
                                self.label_info1.setStyleSheet(f"color: Red")
                                self.label_info1.setText('Your PhoneBot is not activated!')

                                self.label_log.setStyleSheet(f"color: Red")
                                self.label_log.setText(
                                    f"<b>PROBLEM LICENSE:</b> There are DEFININITLY not order id for subscription N° {subscription_id} - product N° {product_id} - user N° {self.user_id} in Phonebot.co Database!:-(<br>=> Please contact <a href='mailto:support@phonebot.co'>support@phonebot.co</a>")
                                self.comboBox_select_campaign.clear()
                                self.comboBox_select_campaign_tab_run_one_task.clear()


                        else:
                            order_found = True

                        if order_found:
                            last_order = max(list_orders)
                            print(f"last_order : {last_order}")
                            sql_status_and_date_of_last_order = f"SELECT post_status, CAST(post_modified AS CHAR) FROM W551je5v_posts WHERE ID='{last_order}'"
                            print(f"sql_status_and_date_of_last_order : {sql_status_and_date_of_last_order}")
                            mysql_cursor.execute(sql_status_and_date_of_last_order)
                            status_and_date = mysql_cursor.fetchall()
                            print(f"status_and_date : {status_and_date}")
                            order_status = status_and_date[0][0]
                            order_date = status_and_date[0][1]
                            print(f"order_date : {order_date}/type : {type(order_date)}")

                            # order_id = str(order_id[0]) We do not need this line as we already transform the order_id tuple in list
                            logger.info(
                                f"Order id found on Phonebot.co :-) => {last_order} - Status: {order_status} - Date : {order_date}")
                            order_found = True

                            # =================================================================================================
                            # ============================= WE NEED TO CHECK THE STATUS OF THE ORDER ==========================
                            # =================================================================================================
                            # ==== IF status is not completed ------------------------------------------------------------------------
                            if order_status != 'wc-completed' and self.license_key_config != 'platinumCNRZ-HOHH-3RGP-5NYO':
                                logger.error(f"The status of your order is not 'complete'.")
                                print(f"order_status : {order_status}")

                                hours, minutes, seconds = mymodules.DifferenceBetween2Dates(date_now_online_DATE,
                                                                                            datetime.strptime(
                                                                                                order_date,
                                                                                                "%Y-%m-%d %H:%M:%S"))
                                print(f"hours : {hours}")
                                # I do not know why I choose >48. So I'll put >0
                                # if hours > 48:
                                if hours > 24 and self.license_key_config != "gold4926-2UEW-65UP-FI77" and self.license_key_config != 'platinumCNRZ-HOHH-3RGP-5NYO':
                                    logger.info(f"Payment of subscription has not been done for the moment.")
                                    message_txt = f'Hi,\n\nYour subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.\n\nWould you please update your payment method on https://phonebot.co/my-account/payment-methods/.\n\nYour PhoneBot will be blocked in 24h if you don\'t pay your subscription.\n\nIf you think this is a mistake, please contact us as soon as possible at support@phonebot.co.\n\nKind regards.\n\nPhoneBot.co\'s team\n\nhttps://phonebot.co'
                                    message_html = f"""
                                                            <html>
                                                              <head></head>
                                                              <body>
                                                                <p>Hi,<br><br>
                                                                Your subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.<br><br>
                                                                Would you please update your payment method on <a href='https://phonebot.co/my-account/payment-methods/'>https://phonebot.co/my-account/payment-methods/</a>.<br><br>
                                                                Your PhoneBot is blocked because you do not pay your subscription.<br><br>
                                                                If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                                                Kind regards.<br><br>
                                                                PhoneBot.co\'s team<br>
                                                                https://phonebot.co
                                                                </p>
                                                              </body>
                                                            </html>
                                            """
                                    try:
                                        mymodules.SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                                           'ALERT: You have to pay your subscription', message_txt,
                                                           message_html, email)
                                    except Exception as ex:
                                        print(f"{ex} => Error sending mail reminder about payment.")

                                    self.label_1_Title.setStyleSheet(f"color: Red")
                                    self.label_license.setStyleSheet(f"color: Red")
                                    self.label_info1.setStyleSheet(f"color: Red")
                                    self.label_info1.setText('Your PhoneBot is not activated!')
                                    self.label_log.setStyleSheet(f"color: Red")
                                    self.button_Run.setEnabled(False)
                                    self.label_log.setText(
                                        f"ERROR License Key :  Payment of your subscription has not been done for the moment.<br>=> There are no order id in Phonebot.co Database!:-( Please contact <a href='mailto:support@phonebot.co'>support@phonebot.co</a>")

                                    mymodules.PopupMessage('Error License Key',
                                                           "Payment of your subscription has not been done for the moment\n=> There are no order id in Phonebot.co Database!:-( \nPlease contact support@phonebot.co")
                                    self.comboBox_select_campaign.clear()
                                    self.comboBox_select_campaign_tab_run_one_task.clear()
                                else:
                                    logger.info(f"Payment of subscription has not been done for the moment.")
                                    message_txt = f'Hi,\n\nYour subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.\n\nWould you please update your payment method on https://phonebot.co/my-account/payment-methods/.\n\nYour PhoneBot will be blocked in 24h if you don\'t pay your subscription.\n\nIf you think this is a mistake, please contact us as soon as possible at support@phonebot.co.\n\nKind regards.\n\nPhoneBot.co\'s team\n\nhttps://phonebot.co'
                                    message_html = f"""
                                                                                        <html>
                                                                                          <head></head>
                                                                                          <body>
                                                                                            <p>Hi,<br><br>
                                                                                            Your subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.<br><br>
                                                                                            Would you please update your payment method on <a href='https://phonebot.co/my-account/payment-methods/'>https://phonebot.co/my-account/payment-methods/</a>.<br><br>
                                                                                            Your PhoneBot will be blocked very soon if you do not pay your subscription.<br><br>
                                                                                            If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                                                                            Kind regards.<br><br>
                                                                                            PhoneBot.co\'s team<br>
                                                                                            https://phonebot.co
                                                                                            </p>
                                                                                          </body>
                                                                                        </html>
                                                                        """
                                    try:
                                        mymodules.SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                                           'ALERT: You have to pay your subscription', message_txt,
                                                           message_html, email)
                                    except Exception as ex:
                                        print(f"{ex} => Error sending mail reminder about payment.")

                                    self.label_1_Title.setStyleSheet(f"color: Red")
                                    self.label_license.setStyleSheet(f"color: Red")
                                    self.label_info1.setStyleSheet(f"color: Red")
                                    self.label_info1.setText('Your PhoneBot is not activated!')
                                    self.label_log.setStyleSheet(f"color: Red")
                                    self.button_Run.setEnabled(False)
                                    self.comboBox_select_campaign.clear()
                                    self.comboBox_select_campaign_tab_run_one_task.clear()
                                    self.label_log.setText(
                                        f"<b>SUBSCRIPTION OK:</b> Payment of subscription has not been done for the moment. Please go to your account on PhoneBot.co and make the payment.<br>=> If you have any issue, feel free to contact contact <a href='mailto:support@phonebot.co'>support@phonebot.co</a>")

                                    if mysql_cursor:
                                        mysql_cursor.close()
                                    if mysql_connection:
                                        mysql_connection.close()

                                    mymodules.Save_email_license_user_id_subscription_id(email, self.license_key_config,
                                                                                         self.user_id,
                                                                                         subscription_id, product_id)
                                    return self.user_id, subscription_id, self.license_id


                            else:
                                # ==== IF status is completed ------------------------------------------------------------------------
                                logger.info(f"Payment of subscription is ok.")
                                if self.license_key_config != 'affiliate':
                                    logger.info(f"PhoneBot will check now your MAC Address.")
                                    # ==================================== CHECK MAC ADDRESS ============================
                                    mac_address_ok = mymodules.CheckMacAddress(subscription_id)
                                    if mac_address_ok:
                                        logger.info(
                                            "Your MAC Address is ok. PhoneBot tested everything regarding your subscription. It can run the bots.")

                                        self.label_1_Title.setStyleSheet(f"color: Green")
                                        self.label_license.setStyleSheet(f"color: Green")
                                        self.label_info1.setStyleSheet(f"color: Green")
                                        self.label_info1.setText('Your PhoneBot is activated!')
                                        self.label_log.setStyleSheet(f"color: Green")
                                        self.label_log.setText(
                                            "<b>LICENSE OK:</b> PhoneBot tested everything regarding your subscription. Everything seems fine.")

                                        if mysql_cursor:
                                            mysql_cursor.close()
                                        if mysql_connection:
                                            mysql_connection.close()

                                        mymodules.Save_email_license_user_id_subscription_id(email,
                                                                                             self.license_key_config,
                                                                                             self.user_id,
                                                                                             subscription_id,
                                                                                             product_id)
                                        self.str_list_campaigns = self.GetCampaigns()
                                        return self.user_id, subscription_id, self.license_id
                                    else:
                                        logger.critical("Your MAC Address is not ok.")
                                        mymodules.PopupMessage("Problem with your License Key!",
                                                               "You cannot install one license on several computers or install several trial licenses on the same computer.")

                                        self.label_1_Title.setStyleSheet(f"color: Red")
                                        self.label_license.setStyleSheet(f"color: Red")
                                        self.label_info1.setStyleSheet(f"color: Red")
                                        self.label_info1.setText('Your PhoneBot is not activated!')
                                        self.label_log.setStyleSheet(f"color: Red")
                                        self.button_Run.setEnabled(False)
                                        self.comboBox_select_campaign.clear()
                                        self.comboBox_select_campaign_tab_run_one_task.clear()
                                        self.label_log.setText(
                                            "<b>ONLY 1 LICENSE PER COMPUTER:</b> Your MAC Address is not ok.<br>=> You cannot install one license on several computers or install several trial licenses on the same computer.")

                        else:
                            logger.error("PhoneBot could not find your order ID. Please contact support@phonebot.co")

                            self.label_1_Title.setStyleSheet(f"color: Red")
                            self.label_license.setStyleSheet(f"color: Red")
                            self.label_info1.setStyleSheet(f"color: Red")
                            self.label_info1.setText('Your PhoneBot is not activated!')
                            self.label_log.setStyleSheet(f"color: Red")
                            self.comboBox_select_campaign.clear()
                            self.comboBox_select_campaign_tab_run_one_task.clear()
                            self.label_log.setText(
                                "<b>PROBLEM LICENSE:</b> PhoneBot could not find your order ID. Please verify your license key and email.<br>=> if the problem persistst, feel free to contact <a href='mailto:support@phonebot.co'>support@phonebot.co</a>")

                    else:

                        logger.info("You're lucky guy! You have the lifetime license! :-) Enjoy!!!")
                        if self.license_key_config != 'affiliate':
                            logger.info(f"PhoneBot will check now your MAC Address.")
                            mac_address_ok = mymodules.CheckMacAddress(subscription_id)
                            if mac_address_ok:
                                logger.info(
                                    "Your MAC Address is ok. PhoneBot tested everything regarding your subscription. It can run the bots.")

                                self.label_1_Title.setStyleSheet(f"color: Green")
                                self.label_license.setStyleSheet(f"color: Green")
                                self.label_info1.setStyleSheet(f"color: Green")
                                self.label_info1.setText('Your PhoneBot is activated!')
                                self.label_log.setStyleSheet(f"color: Green")
                                self.label_log.setText(
                                    "<b>LICENSE OK:</b> PhoneBot tested everything regarding your subscription. Everything seems fine.")

                                if mysql_cursor:
                                    mysql_cursor.close()
                                if mysql_connection:
                                    mysql_connection.close()

                                mymodules.Save_email_license_user_id_subscription_id(email, self.license_key_config,
                                                                                     self.user_id, subscription_id,
                                                                                     product_id)
                                return self.user_id, subscription_id, self.license_id
                            else:
                                logger.critical("Your MAC Address is not ok.")
                                mymodules.PopupMessage("Problem with your License Key!",
                                                       "You cannot install one license on several computers or install several trial licenses on the same computer.")

                                self.label_1_Title.setStyleSheet(f"color: Red")
                                self.label_license.setStyleSheet(f"color: Red")
                                self.label_info1.setStyleSheet(f"color: Red")
                                self.button_Run.setEnabled(False)
                                self.label_info1.setText('Your PhoneBot is not activated!')
                                self.label_log.setStyleSheet(f"color: Red")
                                self.comboBox_select_campaign.clear()
                                self.comboBox_select_campaign_tab_run_one_task.clear()
                                self.label_log.setText(
                                    "<b>ONLY 1 LICENSE PER COMPUTER:</b> Your MAC Address is not ok.<br>=> You cannot install one license on several computers or install several trial licenses on the same computer.")

            else:
                logger.critical(
                    "You filled your license key in config.ini but PhoneBot could not find it in our server. Please edit your config.ini file.")
                mymodules.PopupMessage("Error License!",
                                       "You filled your license key in the 'Settings' tab, but PhoneBot could not find it in our server. Please edit your license key.\nYou can access to your license key on your account : \nhttps://phonebot.co/my-account/view-license-keys/")
                self.label_1_Title.setStyleSheet(f"color: Red")
                self.label_license.setStyleSheet(f"color: Red")
                self.label_info1.setStyleSheet(f"color: Red")
                self.label_info1.setText('Your PhoneBot is not activated!')
                self.comboBox_select_campaign.clear()
                self.comboBox_select_campaign_tab_run_one_task.clear()
                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    "<b>PROBLEM LICENSE:</b> You filled your license key but PhoneBot could not find it in our server.<br>=> Please verify on PhoneBot.co your license key and email and edit them here in the 'Settings' tab.")

            try:
                mysql_cursor.close()
                mysql_connection.close()
            except Exception as ex:
                logger.error(f"Error closing mysql : {ex}")

            return False, False, False

        except Exception as ex:
            logger.critical(f"Error check subscription => {ex}")
            mymodules.PopupMessage(ex, f"Error when checking your subscription! => {ex}")

            self.label_1_Title.setStyleSheet(f"color: Red")
            self.label_license.setStyleSheet(f"color: Red")
            self.label_info1.setStyleSheet(f"color: Red")
            self.label_info1.setText('Your PhoneBot is not activated!')
            self.comboBox_select_campaign.clear()
            self.comboBox_select_campaign_tab_run_one_task.clear()
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR SUBSCRIPTION:</b> Error check subscription<br>=> Error when checking your subscription! => {ex}")

    def CheckLicense(self):

        """
        This function will return self.user_id, subscription_id or false false
        It needs  "CheckSubscription" function
        """
        logger.info("============================ START CheckLicense() =================================")

        # =================================================================================================================
        # =============================== CHECK IF LICENSE KEY AND EMAIL ARE FILLED =======================================
        # =================================================================================================================
        # [1] We check immediatly if license key and email client are filled in the config.ini
        # --- We use configparser to extract from config.ini the license_key ------------------------------------
        try:

            # ---on lit le fichier config.ini
            config = configparser.ConfigParser()
            config.read(mymodules.LoadFile('config.ini'))
            license_key_ok = False
            self.license_key_config = config.get('Settings', 'license_key')
            self.email = config.get('Settings', 'email')
            logger.info(f"CheckLicense()||| self.license_key_config : {self.license_key_config}")
            logger.info(f"CheckLicense()||| email : {self.email}")

            # CHECKING EMAIL & LICENSE ================================================================
            # === WE NEED TO ANTICIPATE IF WE DON'T SEE LICENSE AND EMAIL IN config.ini, MAYBE IN FIELDS
            print("# If License key is not filled in config.ini, maybe it is filled in the UI form. Let's check!")
            if self.email == '':
                print(f"self.lineEdit_Email.text() : {self.lineEdit_Email.text()}")
                if self.lineEdit_Email.text() != '':
                    self.email = self.lineEdit_Email.text()

                else:
                    logger.error("You didn't type your Email in Settings tab.")
                    mymodules.PopupMessage('Error Email!', "You didn't type your Email in Settings tab!")
                    self.label_log.setStyleSheet(f"color: Red")
                    self.label_log.setText("You didn't type your Email in Settings tab.")
            else:
                self.lineEdit_Email.setText(str(self.email))
            if self.license_key_config == '':
                print(f"self.lineEdit_License.text() : {self.lineEdit_License.text()}")
                if self.lineEdit_License.text() != '':
                    self.license_key_config = self.lineEdit_License.text()


                else:
                    logger.error("You didn't type your License in Settings tab.")
                    mymodules.PopupMessage('Error License!', "You didn't type your License in Settings tab!")
                    self.label_log.setStyleSheet(f"color: Red")
                    self.label_log.setText("You didn't type your License in Settings tab.")
            else:
                self.lineEdit_License.setText(str(self.license_key_config))

            try:
                # WE SAVE IT IN config.ini
                config = configparser.ConfigParser()
                config.read(mymodules.LoadFile('config.ini'))
                if self.license_key_config != "":
                    config.set('Settings', 'license_key', self.license_key_config)
                if self.email != "":
                    config.set('Settings', 'email', self.email)
                with open(mymodules.LoadFile('config.ini'), 'w') as configfile:
                    config.write(configfile)
                configfile.close()
            except Exception as e:
                logger.critical(f" {e} => Problem with SaveConfigFile.")

            if self.email != '' and self.email is not None and self.license_key_config != "" and self.license_key_config is not None:
                print("# CheckLicense()||| =================== Check product iD ===================")
                while True:
                    try:
                        # It will check plan_purchased, product_id,
                        is_product_id_ok = mymodules.CheckProductID(self.license_key_config)
                        break
                    except Exception as ex:
                        logger.critical(
                            f"CheckLicense()|||  {ex} -> Error with initialize_phonebot. It is certainly a problem of Internet connection. PhoneBot will try again in 15 seconds.")
                        mymodules.PopupMessage("Problem with Internet?",
                                               f"{ex} -> Error with initialize_phonebot. It is certainly a problem of Internet connection. PhoneBot will try again in 15 seconds.")
                        mymodules.CountDown(15)

                if not is_product_id_ok:
                    # === WE DIDN'T FIND PRODUCT ID
                    self.label_1_Title.setStyleSheet(f"color: Red")
                    self.label_license.setStyleSheet(f"color: Red")
                    self.label_info1.setStyleSheet(f"color: Red")
                    self.label_info1.setText('Your PhoneBot is not activated!')

                    self.label_log.setStyleSheet(f"color: Red")
                    self.label_log.setText(
                        "<b>PROBLEM LICENSE:</b> PhoneBot could not find the product associated ot this license key!<br>=> You can find your license key on PhoneBot website:https://phonebot.co/my-account/view-license-keys/")

                    logger.critical(
                        "CheckLicense()||| ERROR : PhoneBot could not find the product associated ot this license key!")
                    logger.critical(
                        "CheckLicense()||| You can find your license key on PhoneBot website:https://phonebot.co/my-account/view-license-keys/")
                    mymodules.PopupMessage("Problem with your License Key!",
                                           "PhoneBot could not find the product associated ot this license key!")
                    self.comboBox_select_campaign.clear()
                    self.comboBox_select_campaign_tab_run_one_task.clear()
                    return False, False, False
                else:
                    # === WE FOUND PRODUCT ID
                    # ==================================== UPDATE V 0.003 ============================
                    # =================================================================================
                    # ================= WE WILL CHECK IMMEDIATLY IF IT IS AFFILIATE OR NOT =========
                    campaign_id = mymodules.IsAffiliate(self.email, self.license_key_config)
                    if campaign_id is not None:
                        # IT IS AFFILIATE BECAUSE WE GET BACK A CAMPAIGN ID
                        print(f"campaign_id : {campaign_id}")
                        self.mode_license = 'affiliate'
                        logger.info(f"He's an affiliate. The campaign id is {campaign_id}")
                        logger.info("PhoneBot tested everything regarding your subscription.")
                        self.label_1_Title.setStyleSheet(f"color: Green")
                        self.label_license.setStyleSheet(f"color: Green")
                        self.label_Email.setStyleSheet(f"color: Green")
                        self.label_info1.setStyleSheet(f"color: Green")
                        self.label_info1.setText('Your PhoneBot is activated!')
                        self.label_log.setStyleSheet(f"color: Green")
                        self.label_log.setText(
                            "<b>LICENSE OK:</b> PhoneBot tested everything regarding your subscription. Everything seems fine.")

                        # Everything seems ok.

                        self.label_info_campaign.setStyleSheet(f"color: Green")
                        self.label_info_campaign.setText('PhoneBot found your campaign')
                        self.label_log.setStyleSheet(f"color: Green")
                        self.label_log.setText(
                            "<b>CAMPAIGN OK:</b> You configured some tasks for your PhoneBot.<br>=> You can select the device(s).")

                    else:
                        logger.info(f"He's not an affiliate.")
                        self.mode_license = ''
                        self.lineEdit_Email.setStyleSheet(f"color: Black")
                        self.lineEdit_Email.setText(str(self.email))

                    # ===================================================================================================================
                    # ============================= FUNCTION TO CHECK THE PAYMENT OF SUBSCRIPTION, ======================================
                    # ============================= THE LICENSE KEY, EXPIRATION DATE AND MAC ADDRESS ====================================
                    # ===================================================================================================================
                    self.user_id, subscription_id, self.license_id = self.CheckSubscription(self.email)
                    if not self.user_id:
                        return False, False, False
                    else:
                        mymodules.Save_email_license_user_id_subscription_id(self.email, self.license_key_config,
                                                                             self.user_id, subscription_id, 0)
                        self.label_1_Title.setStyleSheet(f"color: Green")
                        self.label_license.setStyleSheet(f"color: Green")
                        self.label_Email.setStyleSheet(f"color: Green")
                        self.label_info1.setStyleSheet(f"color: Green")
                        self.label_info1.setText('Your PhoneBot is activated!')
                        self.label_log.setStyleSheet(f"color: Green")
                        self.label_log.setText(
                            "<b>LICENSE OK:</b> PhoneBot tested everything regarding your subscription. Everything seems fine.")

                        self.lineEdit_License.setStyleSheet(f"color: Black")
                        self.lineEdit_License.setText(str(self.license_key_config))
                        self.str_list_campaigns = self.GetCampaigns()
                        return self.user_id, subscription_id, self.license_id
            else:
                logger.info("we didn't find email and licence key")
                return False, False, False
        except Exception as e:
            logger.critical(f"Problem with CheckLicense() function => {e}. Please have a look at the code.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(f"<b>ERROR LICENSE:</b> Problem with your config.ini! Please go to the 'Settings' tab and, your license key and click on 'Save' button.<br>=> {e}.")

            return False, False, False

    # =============================== FUNCTIONS FOR CAMPAIGN & TASKS =====================================================
    def GetCampaigns(self):
        """
        This method will collect all the campaigns names and fill the dropdownlist

        """
        # === 1rst we need to get the self.user_id
        # self.user_id, self.subscription_id = self.CheckLicense()
        # ========================== LET'S CONNECT TO MYSQL DATABASE =================================
        mysql_connection, mysql_cursor = mymodules.get_mysql_connection()

        self.list_campaigns = []
        # === We need to collect the campaigns's names in a list
        # HERE IS THE SQL REQUEST FOR CAMPAIGN
        # WE NEED TO FILTER BY LICENSE KEY ALSO
        if str(self.license_key_config).lower() == 'affiliate':
            SQL_GET_CAMPAIGNS_NAMES = f"SELECT id,name FROM W551je5v_pb_campaigns WHERE id_user={self.user_id} AND enable=1 AND license_id={self.license_id} AND affiliates=1"
        else:
            print(
                f"SELECT id,name FROM W551je5v_pb_campaigns WHERE id_user={self.user_id} AND enable=1 AND license_id={self.license_id}")
            SQL_GET_CAMPAIGNS_NAMES = f"SELECT id,name FROM W551je5v_pb_campaigns WHERE id_user={self.user_id} AND enable=1 AND license_id={self.license_id}"
        mysql_cursor.execute(SQL_GET_CAMPAIGNS_NAMES)
        tuple_campaigns_names = mysql_cursor.fetchall()
        print(f"tuple_campaigns_names : {tuple_campaigns_names}")
        # ===================================================
        # ===================================================
        # ===================================================
        # ===================================================

        self.str_list_campaigns_names = "0-Select a campaign,"
        self.list_campaigns.append((0, '0-Select a campaign'))
        # === If there are some campaigns:
        print(f"tuple_campaigns_names : {tuple_campaigns_names}")

        if len(tuple_campaigns_names) > 0:
            print(f"tuple_campaigns_names : {tuple_campaigns_names} - type : {type(tuple_campaigns_names)}")
            for campaign_name in tuple_campaigns_names:
                print(f"campaign_name : {campaign_name}")
                try:
                    self.list_campaigns.append(
                        (campaign_name['id'], f"{str(campaign_name['id'])}-{campaign_name['name']}"))
                    self.str_list_campaigns_names += str(campaign_name['id']) + '-' + campaign_name['name'] + ","
                except Exception as ex:
                    print(f"Error in loop of campaigns :{ex}")

            if self.str_list_campaigns_names[
               len(self.str_list_campaigns_names) - 1:len(self.str_list_campaigns_names)] == ",":
                self.str_list_campaigns_names = self.str_list_campaigns_names[:len(self.str_list_campaigns_names) - 1]
            print(f"self.str_list_campaigns_names : {self.str_list_campaigns_names}")

        print(f"1726 str_list_campaigns_names : {self.str_list_campaigns_names}")
        self.list_campaigns = str(self.str_list_campaigns_names).split(',')
        # We need to remove empty elements from list
        self.list_campaigns = list(filter(None, self.list_campaigns))
        print(f"1730 self.list_campaigns : {self.list_campaigns}")

        # Ajout des campagnes
        self.comboBox_select_campaign.clear()
        self.comboBox_select_campaign_tab_run_one_task.clear()
        self.comboBox_select_campaign.setStyleSheet(f"color: Black")
        self.comboBox_select_campaign_tab_run_one_task.setStyleSheet(f"color: Black")
        self.comboBox_select_campaign_tab_run_one_task.addItems(self.list_campaigns)
        self.comboBox_select_campaign.addItems(self.list_campaigns)

        self.label_info_campaign.setStyleSheet(f"color: Black")
        self.label_info_campaign.setText('Please select a campaign.')

        print(f"1739 self.str_list_campaigns : {self.str_list_campaigns}")

        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        list_campaigns = str(self.str_list_campaigns_names).split(',')

        """
        for campaign in list_campaigns:
            self.comboBox_select_campaign.addItem(campaign)
            self.comboBox_select_campaign_tab_run_one_task.addItem(campaign)
        """

        return self.str_list_campaigns
        # === Now we need to fill the select list

    def CheckCampaignsTasks(self):
        """
        This function will check if User configured some tasks and return the True orFalse
        """
        print("=============================== CheckCampaignsTasks ==========================")
        # ================ LET'S CONNECT TO MYSQL DATABASE ================================
        mysql_connection, mysql_cursor = mymodules.get_mysql_connection()

        # ================ LET'S GET HIS CAMPAIGNS =========================================
        if self.str_list_campaigns_names == "":
            # === If we didn't get any campaign, we must inform

            self.label_4_Title.setStyleSheet(f"color: Red")

            self.label_info_campaign.setStyleSheet(f"color: Red")
            self.label_info_campaign.setText("You didn't enable or you didn't create any campaign.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR CAMPAIGN!</b> Please go to your dashboard page and enable or create at least one campaign : https://dashboard.phonebot.co.<br>You will have to restart PhoneBot to see this new campaign.")

            return False
        else:
            # === User created and enable one campaign
            # === We need to check if there is at least one task enable

            # get the list of id _campaign
            list_campaign = self.str_list_campaigns_names.split(",")
            str_list_id_campaign = ""
            for campaign in list_campaign:
                str_list_id_campaign += str(campaign[0]) + ","
            # we remove last comma ","
            str_list_id_campaign = str_list_id_campaign[:len(str_list_id_campaign) - 1]

            SQL_LIST_OF_TASKS_OF_ALL_CAMPAIGNS = f"SELECT * FROM W551je5v_pb_tasks_users WHERE id_campaign IN ({str_list_id_campaign}) AND enable=1"
            mysql_cursor.execute(SQL_LIST_OF_TASKS_OF_ALL_CAMPAIGNS)
            tasks_users = mysql_cursor.fetchall()
            if len(tasks_users) <= 0:
                # We didn't find any task user enable
                self.label_4_Title.setStyleSheet(f"color: Red")

                self.label_info_campaign.setStyleSheet(f"color: Red")
                self.label_info_campaign.setText("PhoneBot found some campaign but no tasks were enable or configured.")
                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    f"<b>ERROR CAMPAIGN!</b><br>=> Please go to your dashboard page and enable or create at least one task : https://dashboard.phonebot.co<br>You will have to restart PhoneBot to see this new task")

                return False


            else:
                # Everything seems ok.

                self.label_4_Title.setStyleSheet(f"color: Green")

                self.label_info_campaign.setStyleSheet(f"color: Green")
                self.label_info_campaign.setText("PhoneBot found your campaign.")
                self.label_log.setStyleSheet(f"color: Green")
                self.label_log.setText(
                    "<b>CAMPAIGN OK:</b> You configured some tasks for your PhoneBot.<br>=> You can select the device(s).")

                return True

        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

    # =============================== FUNCTIONS FOR TABS RUN & RUN ONE TASK ========================

    def EnableTabRun(self, p_enable):
        if p_enable:
            p_color = 'Black'
        else:
            p_color = 'Grey'

        self.label_4_Title.setEnabled(p_enable)
        self.label_4_Title.setStyleSheet(f"color: {p_color}")

        self.label.setEnabled(p_enable)
        self.label.setStyleSheet(f"color: {p_color}")

        self.label_4_Title_2.setEnabled(p_enable)
        self.label_4_Title_2.setStyleSheet(f"color: {p_color}")

        self.label_yourcomputer.setEnabled(p_enable)
        self.label_yourcomputer.setStyleSheet(f"color: {p_color}")

        self.label_4_Title_3.setEnabled(p_enable)
        self.label_4_Title_3.setStyleSheet(f"color: {p_color}")

        self.label_4_Title_4.setEnabled(p_enable)
        self.label_4_Title_4.setStyleSheet(f"color: {p_color}")

        self.checkBox_Chrome.setEnabled(p_enable)
        self.checkBox_Chrome.setStyleSheet(f"color: {p_color}")

        self.checkBox_smartphones.setEnabled(p_enable)
        self.checkBox_smartphones.setStyleSheet(f"color: {p_color}")

        self.comboBox_select_campaign.setEnabled(p_enable)
        self.comboBox_select_campaign.setStyleSheet(f"color: {p_color}")

        print(f" comboBox_select_campaign is Enable ? : {self.comboBox_select_campaign.isEnabled()}")
        print(f"2387 self.str_list_campaigns_names : {self.str_list_campaigns_names}")

        self.checkBox_Firefox.setEnabled(p_enable)
        self.checkBox_Firefox.setStyleSheet(f"color: {p_color}")

        self.button_Run.setEnabled(p_enable)
        if p_enable:
            self.button_Run.setStyleSheet("background-color: rgb(85, 255, 127);")
        else:

            self.button_Run.setStyleSheet(f"color: {p_color}")

        self.button_Quit.setText('Stop')
        self.button_Quit.clicked.connect(self.ButtonQuit)

        self.button_Report.setEnabled(p_enable)
        if p_enable:
            self.button_Report.setStyleSheet(f"background-color: rgb(199, 199, 199);")
        else:
            self.button_Report.setStyleSheet(f"background-color: {p_color}")

        """
        self.tab_run_one_task.setTabEnabled(p_enable)
        self.tab_settings.setTabEnabled(p_enable)
        self.tab_help.setTabEnabled(p_enable)
        """
        self.tabWidget.setTabEnabled(1, p_enable)
        self.tabWidget.setTabEnabled(2, p_enable)
        self.tabWidget.setTabEnabled(3, p_enable)

    def TabRunOneTask_Enable_1_2(self, p_enable):
        """
        This method enable the 1. Select Campaign and 2. Select Device and Radio buttons....
        :param p_enable:
        :return:
        """
        if p_enable:
            p_color = 'Black'
            # self.label_log_run_one_task.setHidden(True)
        else:
            p_color = 'Grey'
            # self.label_log_run_one_task.setHidden(False)

        self.label_select_campaign_tab_run_one_task.setEnabled(p_enable)
        self.label_3.setEnabled(p_enable)
        self.label_select_campaign_tab_run_one_task.setEnabled(p_enable)
        self.label_select_device_tab_run_one_task.setEnabled(p_enable)
        self.label_select_smartphone_or_browser_tab_run_one_task.setEnabled(p_enable)
        self.label_explanation_run_one_task.setEnabled(p_enable)
        self.radioButton_Computer.setEnabled(p_enable)
        self.radioButton_Smartphone.setEnabled(p_enable)
        self.comboBox_select_campaign_tab_run_one_task.setEnabled(p_enable)
        self.comboBox_select_browser_smartphone_tab_run_one_task.setEnabled(p_enable)
        print(f"2434 self.str_list_campaigns_names : {self.str_list_campaigns_names}")

        """
        self.tab_run_one_task.setTabEnabled(p_enable)
        self.tab_settings.setTabEnabled(p_enable)
        self.tab_help.setTabEnabled(p_enable)
        """
        self.tabWidget.setTabEnabled(0, p_enable)
        self.tabWidget.setTabEnabled(2, p_enable)
        self.tabWidget.setTabEnabled(3, p_enable)

    # =============================== FUNCTIONS FOR SMARTPHONES =====================================================
    def sub_process_scan_details_smartphones(self):
        """
        This function scan and get info from connected smartphones
        It returns false if there is an issue with smartphones
        or return true
        """

        ############################################################################################
        # --- We need to count the number of connected smartphones
        # --- We nitialize dictionnary in order to store all the details of smartphones for Appium
        dico_smartphones = {}  # => Will store the id of each smartphones and desired_caps
        self.list_smartphones = []  # => Will store the dico of smartphones

        # ======================================= List the connected devices ================================================
        # ======================================= CREATION OF tmp.txt ========================================================
        try:
            self.number_connected_phones = mymodules.NumberSmartphonesConnected()
        except ValueError:
            print("Error NumberSmartphonesConnected")
        with open(mymodules.LoadFile('tmp.txt')) as f:
            lines = f.readlines()
        f.close()

        # ======================================= EMPTY TABLE smartphones ================================================
        sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()

        # ======================================= GET MAXIMUM LIMIT smartphones CONNECTED ===================================
        Maximum_number_of_phones_tuple = sqlite_cursor.execute("select value from limits where name_limit=?",
                                                               ('Maximum_number_of_phones',)).fetchone()
        if Maximum_number_of_phones_tuple:
            Maximum_number_of_phones = Maximum_number_of_phones_tuple[0]
            sqlite_cursor.execute("UPDATE smartphones SET status=?", (0,))
        else:
            Maximum_number_of_phones = 0

        if self.number_connected_phones <= 0:
            self.number_connected_phones = 0

            self.label_3_Title.setStyleSheet(f"color: Red")
            self.label_info3.setStyleSheet(f"color: Red")
            self.label_info3.setText("There is not any smartphones connected on your computer.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                "<b>ERROR SMARTPHONE:</b> PhoneBot did not find any smartphone connected to your computer.<br>=> Please check USB cable and verify your smartphone(s) have the option 'USB Debugging' enable.<br>If you checked the option 'Your computer', PhoneBot will continue with browser automation.")
            self.plainTextEdit_Smartphones.setPlainText(
                "<b>ERROR SMARTPHONE:</b> PhoneBot did not find any smartphone connected to your computer.<br>=> Please check USB cable and verify your smartphone(s) have the option 'USB Debugging' enable.<br>If you checked the option 'Your computer', PhoneBot will continue with browser automation.")
            return False


        elif self.number_connected_phones > Maximum_number_of_phones and Maximum_number_of_phones != 0:
            logger.critical(
                f"You do not have permission to connect so many smartphones. Your maximum capacity is {Maximum_number_of_phones} smartphone(s) Maximum! Please upgrate your license in order to get the possibility to connect more smartphones.")
            mymodules.PopupMessage("Too many smartphones connected!",
                                   f"You do not have permission to connect so many smartphones. Your maximum capacity is {Maximum_number_of_phones} smartphone(s) Maximum! Please upgrate your license in order to get the possibility to connect more smartphones.")

            self.label_3_Title.setStyleSheet(f"color: Red")
            self.label_info3.setStyleSheet(f"color: Red")
            self.label_info3.setText("There are too many Smartphones.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"You do not have permission to connect so many smartphones. Your maximum capacity is {Maximum_number_of_phones} smartphone(s) Maximum! Please upgrate your license in order to get the possibility to connect more smartphones.")

            return False

        # ======================================= GET DETAILS OF smartphones CONNECTED ===================================
        # ================================================================================================================
        # --- So now we will extract the ID and the deviceName from tmp.txt
        # --- We start first to extract all the lines in a list

        # --- then we can extract the id  in a list of dictionnary
        # At the end, it should look something like this
        # list = [
        #    {'smartphone_ID': '41492968379078', 'deviceName': 'S6S5IN3G'},
        #    {'smartphone_ID': '53519716736397', 'deviceName': 'S6S5IN3G'}
        # ]

        i = 0
        final_message_missing_packages = ""
        print(f"self.number_connected_phones : {self.number_connected_phones}")
        # ======================================= LOOP IN ALL smartphones CONNECTED ===================================
        while i < (self.number_connected_phones + 1):

            # --- We extract the ID If we are not reading the first line and the last line of tmp.txt
            try:
                if i != 0 and i != (self.number_connected_phones + 1):
                    if 'offline' in lines[i]:
                        logger.error(f"One smartphone is not connected to computer.")

                        self.label_3_Title.setStyleSheet(f"color: Red")
                        self.label_3.setStyleSheet(f"color: Red")
                        self.label_info3.setStyleSheet(f"color: Red")
                        self.label_info3.setText("One smartphone is not well connected to computer.")
                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(f"<b>ERROR SMARTPHONE:</b> Please verify connection of smartphone'  \
                                                    {lines[i]}'.<br>=> It seems to have an issue. If you have other smartphones connected, you can unplug this one and run the others.")

                    elif 'unauthorized' in lines[i]:
                        logger.error(f"There is a smartphone 'unauthorized'.")

                        self.label_3_Title.setStyleSheet(f"color: Red")
                        self.label_3.setStyleSheet(f"color: Red")
                        self.label_info3.setStyleSheet(f"color: Red")
                        self.label_info3.setText("One smartphone is not well connected to computer.")
                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(f"<b>ERROR SMARTPHONE:</b> Please verify connection of smartphone '  \
                                                    {lines[i]}'.<br>=> It seems to have an issue. If you have other smartphones connected, you can unplug this one and run the others.")

                        return False

                    else:
                        first_space_pos = lines[i].find(
                            ' ')  # We try to find position of first space in order to find the ID of smartphone
                        smartphone_id = lines[i][0:first_space_pos]  # We extract the ID of smartphone

                        # === Smartphone_ID ======================
                        dico_smartphones["Smartphone_ID"] = smartphone_id  # We add the ID in dico
                        logger.info(f"Smartphone {i} id : {smartphone_id}")
                        device_product_pos = lines[i].find('device product:') + len(
                            'device product:')  # We try now to find position of deviceName
                        model_pos = lines[i].find(
                            ' model')  # and now the position of "model" in order to extract the deviceName in the middle of the line
                        while model_pos == -1:
                            if platform.system() == 'Darwin':
                                home_user = os.environ['HOME']
                                # adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                                # proc = subprocess.Popen(adb_command_line, shell=True, stdout=True,
                                #                         stdin=subprocess.PIPE,
                                #                         stderr=subprocess.STDOUT)
                            devices = os.popen("adb devices -l").read()

                            f = open(mymodules.LoadFile('tmp.txt'), 'w')
                            f.writelines(devices)
                            f.close()
                            with open(mymodules.LoadFile('tmp.txt'))as f:
                                lines = f.readlines()
                            f.close()
                            model_pos = lines[i].find(' model')

                        device_pos = lines[i].find(' device:')
                        transport_id_pos = lines[i].find(' transport_id:')
                        deviceName = lines[i][device_product_pos:model_pos]
                        device_string = lines[i][device_pos + len(' device:'):transport_id_pos]
                        modele_device = lines[i][model_pos + len(' model:'):device_pos]
                        print("-" * 100)
                        print(f"lines[i] : {lines[i]}")
                        print(f"device_pos : {device_pos}")
                        print(f"transport_id_pos : {transport_id_pos}")
                        print(f"model_pos : {model_pos}")
                        print(f"modele_device : {modele_device}")
                        print(f"deviceName : {deviceName}")
                        print(f"device_string : {device_string}")

                        # === deviceName ======================
                        dico_smartphones["deviceName"] = deviceName  # We add the deviceName in dico
                        # We initialise the key for list of not installed app
                        dico_smartphones["missing_packages"] = ""

                        # --- Now we need to check if the apps are installed in smartphone : Facebook, Instagram, Twitter, Linkedin, Leboncoin
                        # --- And we extract the appPackage -----------------------------------------------------------------------------------
                        # --- FACEBOOK -------------------------------------------------------------------------------------------------------
                        # print(f"self.list_tasksuser: {self.list_tasksuser}")

                        # =================================== CHECK FOR THE APP WHICH ARE NOT INSTALLED ==================================
                        # ================================================================================================================
                        #
                        # It is possible user didn't select any campaign so we don't know what are the necessary apps
                        try:
                            self.MakeListNecessaryApp()  # We need to get the list of necessary task, so we need the campaign id selected
                            for application in self.list_application:
                                #
                                print(
                                    f"======================= CHECK FOR THE APP WHICH ARE NOT INSTALLED ========================")
                                print(f"application : {application}")
                                # In case there are 2 application for 1 platform, we need to split and test them all
                                # application could look like this application : ('Facebook_Orca,Facebook_Katana',)
                                # So we need to build a list and see how many element are there in this list
                                split_application = str(application[0]).split(',')
                                if len(split_application) > 1:
                                    print(f"split_application : {split_application}")
                                    for splited_application in split_application:
                                        dico_smartphones = mymodules.verify_appPackage_present(splited_application,
                                                                                               dico_smartphones)
                                else:
                                    dico_smartphones = mymodules.verify_appPackage_present(application[0],
                                                                                           dico_smartphones)
                                    print(f"application[0] : {application[0]}")
                        except Exception as ex:
                            logger.error(
                                "No campaign was selected so we can't know what are the necessary application!")

                        print(f"dico_smartphones : {dico_smartphones}")

                        # We just checked if all necessary app are installed , let's test
                        #
                        print(f"dico_smartphones['missing_packages'] : {dico_smartphones['missing_packages']}")

                        # =================================== CHECK FOR THE ANDROID VERSION ==================================
                        # ====================================================================================================

                        # --- And now the version of Android
                        # This paragraph of code below is necesssary when several smarpthones have the same udid.
                        # If this is the case, the adb command will return an error message. So we will have to try to get
                        # the android version with another parameter than udid(ex: device, model, etc...)
                        # ==> see https://stackoverflow.com/questions/30214744/using-adb-with-multiple-devices-with-the-same-serial-number

                        adb_command = "adb -s " + dico_smartphones[
                            'Smartphone_ID'] + " shell getprop ro.build.version.release"
                        adb_command_tuple = ["adb", "-s", dico_smartphones['Smartphone_ID'], "shell", "getprop",
                                             "ro.build.version.release"]

                        if platform.system() == 'Darwin':
                            home_user = os.environ['HOME']
                            # adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                            # proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                            #                         stderr=subprocess.STDOUT)
                        p = subprocess.Popen(adb_command_tuple, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        result_adb_command = str(p.communicate()[1])

                        if result_adb_command.find("error") != -1:
                            print(f"result_adb_command : {result_adb_command}")

                            adb_command = "adb -s model:" + modele_device + " shell getprop ro.build.version.release"
                            adb_command_tuple = ["adb", "-s", "model:", modele_device, "shell", "getprop",
                                                 "ro.build.version.release"]

                            if platform.system() == 'Darwin':
                                home_user = os.environ['HOME']
                                # adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                                # proc = subprocess.Popen(adb_command_line, shell=True, stdout=True,
                                #                         stdin=subprocess.PIPE,
                                #                         stderr=subprocess.STDOUT)

                            p = subprocess.Popen(adb_command_tuple, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            result_adb_command = str(p.communicate()[1])
                            if result_adb_command.find("error") != -1:
                                print(f"result_adb_command : {result_adb_command}")

                                if platform.system() == 'Darwin':
                                    home_user = os.environ['HOME']
                                    # adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                                    # proc = subprocess.Popen(adb_command_line, shell=True, stdout=True,
                                    #                         stdin=subprocess.PIPE,
                                    #                         stderr=subprocess.STDOUT)
                                adb_command = "adb -s device:" + device_string + " shell getprop ro.build.version.release"
                                adb_command_tuple = ["adb", "-s", "device:", modele_device, "shell", "getprop",
                                                     "ro.build.version.release"]

                                p = subprocess.Popen(adb_command_tuple, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                result_adb_command = str(p.communicate()[1])

                                if result_adb_command.find("error") != -1:
                                    print(f"result_adb_command : {result_adb_command}")
                                    error_adb_command = True
                                else:
                                    print("PhoneBot get the Android version")
                                    print(f"result_adb_command : {result_adb_command}")
                                    error_adb_command = False
                            else:
                                print("PhoneBot get the Android version")
                                error_adb_command = False
                        else:
                            print("PhoneBot get the Android version")
                            error_adb_command = False
                        if not error_adb_command:
                            print("We enter if not error_adb_command:")

                            result_adb_command = str(os.popen(adb_command).read())
                            print(f"result_adb_command : {result_adb_command}")
                            version_android = str(result_adb_command).strip().split('\n\n')
                            print(f"version_android : {version_android}")

                            # --- I need to remove brackets from the string ['6.0'] ---------------------
                            new_version_android_1 = str(version_android).replace("['", "")
                            new_version_android_2 = str(new_version_android_1).replace("']", "")
                            print(f"new_version_android_2 : {new_version_android_2}")
                            # -- I also need to be sure there willl be .O after the digit of version
                            if new_version_android_2.find('.0') == -1:
                                logger.info(
                                    f"OS Version = {new_version_android_2}. It miss the '.0'   \
                                    in the version of OS of Smartphone {dico_smartphones['Smartphone_ID']}. ")
                                logger.info(f"We will add '.0' at the end.")
                                new_version_android_2 = new_version_android_2 + ".0"
                                logger.info(f"OS version = {new_version_android_2}")

                            dico_smartphones['version_android'] = str(new_version_android_2)
                            logger.info(
                                f"dico_smartphones['version_android'] : {dico_smartphones['version_android']}")

                            self.list_smartphones.append(dico_smartphones.copy())  # We add the dico in our list
                        logger.info(
                            f"========================== ARE THERE SOME APP MISSING ??? =================================================")
                        logger.info(f'dico_smartphones["missing_packages"] : {dico_smartphones["missing_packages"]}')

                        # We need to prepare the final message of missing apps
                        if dico_smartphones["missing_packages"] != "":
                            final_message_missing_packages += f"Missing the application \'  \
                            {dico_smartphones['missing_packages']}\' on smartphone \'{dico_smartphones['deviceName']}\'<br>"

                i += 1
                print(f"i => {i}")
                print("-" * 100)
                print(f"i:{i}/{self.number_connected_phones}")
                print("-" * 100)

            except Exception as ex:
                # We need to filter the exception in case "name 'list_smartphones' is not defined" because user didn't select campaign
                if ex.find("name 'list_smartphones' is not defined") != -1:
                    mymodules.PopupMessage("Error!",
                                           "You didn't select a campaign. Please select a campaign before to scan for smartphones.")
                    break

                # except Exception as ex:
                logger.critical(f"{ex} -> ERROR getting list of app installed on each smartphone!")
                # mymodules.PopupMessage("ERROR",f"{ex} -> ERROR getting list of app installed on each smartphone!")

                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    f"<b>ERROR SMARTPHONE:</b> We can't get the list of app installed on each smartphone!<br>=> {ex}.<br>You can skip this part by running automation on your computer only. You will have to check only the option 'Your computer'  and uncheck the option 'Your smartphone(s).")

        logger.info("##############################")
        logger.info(f"Final dico : {dico_smartphones}")
        logger.info(f"Final list : {self.list_smartphones}")

        # ==================================================================================================================
        # --- So we have everything, we can now store everything in the table "smartphones" from our sqlight db.--------
        # ===================================================================================================================
        logger.info("------- Starting Saving smartphones details in SQLite local DB ----------")

        # --- Now that we put status=0 to all the rows of table smartphones, we can check which smartphones is connected and update table
        # --- we loop each smartphones in our list in order to update our DB -----------------------------
        # self.plainTextEdit_Smartphones.clear()
        display_smartphones_in_textarea = ""

        self.plainTextEdit_Smartphones.setStyleSheet(f"color: Black")

        counter_display_smartphones_in_textarea = 0
        for smartphone in self.list_smartphones:
            print(f"""======================================   {smartphone[
                'Smartphone_ID']}  ================================================""")
            # sql_test_exist_smartphone = "SELECT udid, COUNT(*) FROM smartphones WHERE udid = " + str(smartphone['Smartphone_ID']) + " GROUP BY udid"
            sqlite_cursor.execute("SELECT udid, COUNT(*) FROM smartphones WHERE udid =? GROUP BY udid",
                                  (str(smartphone['Smartphone_ID']),))
            exist = sqlite_cursor.fetchone()
            # check if it is empty and print error
            if not exist:

                logger.info(
                    f"The smartphone {smartphone['Smartphone_ID']} DOES NOT exist. We add its values in DB")
                logger.info(f"smartphone['version_android']) : {str(smartphone['version_android'])}")
                try:
                    sqlite_cursor.execute("INSERT INTO smartphones(udid, devicename, platformversion, OS_device, status,  \
                        missing_packages) VALUES(?,?,?,?,?,?)", (str(smartphone['Smartphone_ID']), \
                                                                 str(smartphone['deviceName']),
                                                                 str(smartphone['version_android']), 'Android', 1,
                                                                 str(smartphone['missing_packages'])))
                    sqlite_connection.commit()

                except Exception as ex:
                    logger.critical(f"ERROR when inserting smartphone row : {ex}")

            else:

                logger.info(f"str(smartphone['version_android']) : {str(smartphone['version_android'])}")
                logger.info(f"The smartphone " + str(
                    smartphone['Smartphone_ID']) + " exist. We update values for this smartphone in DB.")
                try:
                    values = (str(smartphone['deviceName']), str(smartphone['version_android']), 'Android', "1",
                              str(smartphone['Smartphone_ID']), str(smartphone['missing_packages']))
                    # sqlite_cursor.execute("UPDATE smartphones SET devicename=?, Facebook.Katana_appPackage=?, Twitter_appPackage=?, Linkedin_appPackage=?, Instagram_appPackage=?,Leboncoin_appPackage=?, platformversion=?, status=? WHERE id=? ",(str(smartphone['deviceName']), str(smartphone['Facebook.Katana_appPackage']), str(smartphone['Twitter_appPackage']), str(smartphone['Linkedin_appPackage']), str(smartphone['Instagram_appPackage']), str(smartphone['Leboncoin_appPackage']), str(smartphone['version_android']), "1", str(smartphone['Smartphone_ID'])))

                    sqlite_cursor.execute("UPDATE smartphones SET devicename=?, platformversion=?, \
                                        OS_device=?, status=? ,missing_packages WHERE udid=?", values)

                    # exist = sqlite_cursor.fetchall()
                    # logger.info(f"{p_udid}|||The fetchall give " + str(exist))
                    sqlite_connection.commit()

                except Exception as ex:
                    logger.critical(f"ERROR when updating smartphone row : {ex}")

                logger.info(f"We added the bot details successfully in the DB :-)")
            print(f"display_smartphones_in_textarea : {display_smartphones_in_textarea}")
            display_smartphones_in_textarea += str(smartphone['Smartphone_ID']) + '\t' + str(
                smartphone['deviceName']) + '\t' + 'Android ' + str(
                smartphone['version_android']) + ' \n'
            counter_display_smartphones_in_textarea += 1

        # We display error messages regarding the missing app
        if final_message_missing_packages != "":

            logger.error(f"It miss some application. See details in 'Run' tab.")
            self.label_3.setStyleSheet(f"color: Red")
            self.label_3_Title.setStyleSheet(f"color: Red")
            self.label_info3.setStyleSheet(f"color: Red")
            self.label_info3.setText("It misses some application in Smartphone. See details in 'Run' tab.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR SMARTPHONE:</b> Missing an app on smartphone.<br>{final_message_missing_packages}<br>You can still run PhoneBot but it may have some issues.")

        else:

            self.label_3.setStyleSheet(f"color: Green")
            self.label_3_Title.setStyleSheet(f"color: Green")
            self.label_info3.setStyleSheet(f"color: Green")
            self.label_info3.setText(f"{self.number_connected_phones} smartphone(s) connected to your computer.")
            self.label_log.setStyleSheet(f"color: Green")
            self.label_log.setText(
                "<b>SMARTPHONE OK:</b> Your smartphones were correctly identified by PhoneBot.<br>=> You can run PhoneBot! :-)")

        # We display list of connected smartphones
        print(f"FINAL VERSION OF display_smartphones_in_textarea : {display_smartphones_in_textarea}")
        print(f"counter_display_smartphones_in_textarea : {counter_display_smartphones_in_textarea}")
        self.plainTextEdit_Smartphones.setStyleSheet(f"color: Black")
        # self.plainTextEdit_Smartphones.setText(display_smartphones_in_textarea)
        self.plainTextEdit_Smartphones.setPlainText(display_smartphones_in_textarea)

        try:
            sqlite_cursor.close()
            sqlite_connection.close()
        except Exception as ex:
            logger.error(f"Error closing sqlite : {ex}")

        return True

    def MakeListNecessaryApp(self):
        """
        This function will get the list of nessary applications to run teh automation tasks
        It depends of the campaign and so the task enables in dashboard
        """
        try:
            self.current_campaign_name = str(self.comboBox_select_campaign.currentText())
            self.current_campaign_id = self.GetCurrentCampaignID(self.current_campaign_name)

            self.current_campaign_name_one_task = str(self.comboBox_select_campaign_tab_run_one_task.currentText())
            self.current_campaign_id_one_task = self.GetCurrentCampaignID(self.current_campaign_name_one_task)
            # 1rst - We get the list of tasks ==========================================================================================================
            # ===================================== CREATE MYSQL CONNECTION ==============================================
            mysql_connection, mysql_cursor = mymodules.get_mysql_connection()

            self.list_id_task = []
            for taskuser in self.list_tasksuser:
                self.list_id_task.append(mymodules.GetIDTask(taskuser['id']))

            # We now make the list of necessary application
            SQL_GET_LIST_OF_APPLICATION = f"SELECT application FROM W551je5v_pb_platforms p left join W551je5v_pb_tasks t on p.id=t.id_platform WHERE t.id IN ({str(self.list_id_task).replace('[', '').replace(']', '')}) "
            print(f"SQL_GET_LIST_OF_APPLICATION : {SQL_GET_LIST_OF_APPLICATION}")

            mysql_cursor.execute(SQL_GET_LIST_OF_APPLICATION)
            tuple_mysql_list_app = mysql_cursor.fetchall()
            print(f"tuple_mysql_list_app : {type(tuple_mysql_list_app)}: {tuple_mysql_list_app}")

            self.list_application = tuple_mysql_list_app

            print(f"self.list_application : {self.list_application}")

        except Exception as ex:
            logger.error(f"Error MakeListNecessaryApp : {ex}")

        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

    def StartAppiumServer(self):
        # ==========================================================================================================
        # ==========================================================================================================
        #                                          APPIUM SERVER
        # 4th We need to launch Appium server before we forgot
        # ==========================================================================================================
        # ==========================================================================================================
        cpt_appium_server = 0
        while True:
            try:
                if platform.system() == 'Windows':
                    PROCNAME_NODE = "node.exe"
                elif platform.system() == 'Darwin':
                    PROCNAME_NODE = "node"
                for proc in psutil.process_iter():
                    if proc.name() == PROCNAME_NODE:
                        print(f"PhoneBot will kill this process : {proc.name}")
                        proc.kill()

                # os.system("start /B start cmd.exe @cmd /k appium --log appium.log --log-level error:debug --debug-log-spacing --async-trace --relaxed-security")

                if platform.system() == 'Windows':
                    proc = subprocess.Popen(
                        f'appium --log appium.log --log-level error:debug --debug-log-spacing --async-trace',
                        shell=True,
                        stdin=None, stdout=None, stderr=None, close_fds=True)

                elif platform.system() == 'Darwin':
                    home_user = os.environ['HOME']
                    proc = subprocess.Popen(
                        f'appium --log {home_user}/PhoneBot/appium.log --log-level error:debug --debug-log-spacing --async-trace',
                        shell=True,
                        stdin=None, stdout=None, stderr=None, close_fds=True)

                # subprocess.Popen('appium', creationflags=subprocess.CREATE_NEW_CONSOLE)
                logger.info("Appium server starting....")
                time.sleep(15)
                return True

            except Exception as ex:
                cpt_appium_server += 1
                logger.error(
                    f"{ex} --> We could not start Appium server.... Be sure to have installed it and add the path to variable environment!")
                self.EditTextFieldUi(self.label_log, 'Red',
                                     f"We could not start Appium server.... Be sure to have installed it and add the path to variable environment!<br>{ex}.")
                if cpt_appium_server > 3:
                    return False

    # ====================================== FUNCTIONS OF BUTTONS ========================================

    def scan_details_smartphones(self, progress_callback):
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        self.are_smartphones_ok = self.sub_process_scan_details_smartphones()
        return "The scan of smartphones is done."

    def scan_browsers_profiles(self, progress_callback):
        """
        This function will check for browser profiles
        :param progress_callback:
        :return:
        """

        # CHECK BROWSERS PROFILES
        self.is_profile_chrome_browser_ok = mymodules.CheckBrowserProfile('Chrome')
        self.is_profile_firefox_browser_ok = mymodules.CheckBrowserProfile('Firefox')

        # IF BROWSERS PROFILES ARE OK
        if self.is_profile_firefox_browser_ok or self.is_profile_chrome_browser_ok:
            self.label_select_smartphone_or_browser_tab_run_one_task.setText("3. Please select a browser:")
            self.comboBox_select_browser_smartphone_tab_run_one_task.clear()

            # BUILDING LIST OF BROWSERS
            if self.is_profile_chrome_browser_ok:
                self.comboBox_select_browser_smartphone_tab_run_one_task.addItem("Chrome")
            if self.is_profile_firefox_browser_ok:
                self.comboBox_select_browser_smartphone_tab_run_one_task.addItem("Firefox")
            self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(False)
            self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(False)
            self.label_explanation_run_one_task.setHidden(False)
            # SHOW THE TASKS BUTTONS
            self.tab_run_one_task_mode == 'computer'
            self.TabRunOneTask_PrepareListTasksButtons('show', 'computer')
            self.label_log_run_one_task.setHidden(True)
            self.TabRunOneTask_ShowHideTasksButtons('show', 'computer')
            # self.HideButtonsRunOneTask(False)



        else:
            logger.error(
                f"None of your browser profiles (Firefox & Chrome) exist! Please check if you have installed correctly Chrome or Firefox.")
            mymodules.PopupMessage("Error!",
                                   f"None of your browser profiles (Firefox & Chrome) exist! Please check if you have installed correctly Chrome or Firefox.")

            self.radioButton_Smartphone.setChecked(False)
            self.radioButton_Computer.setChecked(False)

        return "The Checking of browser's profiles Firefox & Chrome is finished."

    def TabRunOneTask_HideSelectSmartphoneBrowser(self, p_value):
        # HIDE 3. Select Smartphone
        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(p_value)
        self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(p_value)
        self.label_explanation_run_one_task.setHidden(p_value)
        self.label_4_see_results_tab_run_one_task.setHidden(p_value)
        self.button_Report_2.setHidden(p_value)

    def scan_details_smartphones_tab_run_once(self, progress_callback):

        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        # WE CHECK IF SOFTWARES FOR SMARTPHONE AUTOMATION ARE READY
        if not mymodules.CheckSoftwareInstalled():
            mymodules.PopupMessage("Error!",
                                   "You try to automate smartphones but you didn't install all the necessary softwares!\nPlease go to \'Settings\' tab and click on \'Install Smartphone Automation\' button.")
            logger.error("You try to automate smartphones but you didn't install all the necessary softwares!")
            mymodules.DisplayMessageLogUI(self.label_log_run_one_task,
                                          f"SMARTPHONE||| You try to automate smartphones but you didn't install all the necessary softwares!",
                                          "Red")
            self.are_smartphones_ok = False
            self.checkBox_smartphones.setChecked(False)

            return "The scan of smartphones is done from tab 'Run one Task'FALSE."

        else:
            # USER INSTALLED THE NECESSARY SOFTWARES FOR SMARTPHONE AUTOMATION
            self.are_smartphones_ok = self.sub_process_scan_details_smartphones()
            if self.are_smartphones_ok:
                try:
                    # IF list_smartphone IS EMPTY ---
                    print(f"self.list_smartphones:{self.list_smartphones}")
                    if not self.list_smartphones or self.list_smartphones == "":
                        # ***************** POPUP *******************
                        mymodules.PopupMessage("Error",
                                               "There aren't smartphones connected to your computer.\n\nPlease go to settings and make a scan of smartphones in order to detect the ones connected by USB to your computer.")
                        self.label_select_smartphone_or_browser_tab_run_one_task.setText(
                            "3. Please select a smartphone:")
                        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(False)
                    # IF list_smartphone IS NOT EMPTY ---
                    else:
                        print(f"self.list_smartphones : {self.list_smartphones}")
                        self.comboBox_select_browser_smartphone_tab_run_one_task.clear()
                        # WE BUILD THE LIST OF UDID SMARTPHONES
                        for smartphone in self.list_smartphones:
                            try:
                                self.comboBox_select_browser_smartphone_tab_run_one_task.addItem(
                                    smartphone['Smartphone_ID'])
                            except Exception as ex:
                                logger.error(f"error when adding items in list of smartphones Run one task")

                        # SHOW THE label & list SMARTPHONES
                        self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(False)
                        self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(False)
                        self.label_explanation_run_one_task.setHidden(False)

                        # SHOW THE BUTTONS TASKS
                        self.TabRunOneTask_PrepareListTasksButtons('show', 'smartphone')
                        self.TabRunOneTask_ShowHideTasksButtons('show', 'smartphone')
                        return "The scan of smartphones is done from tab 'Run one Task'TRUE."
                except Exception as ex:
                    # !!!!!! ERROR => THE list_smarthpones DOESN'T EXIST. WE NEED SHOW POPUP AFTER HIDING EVERYTHING
                    logger.error(f"Error {ex} We need to inform user with popup to make a scan smarpthone.")
                    # UNCHECK THE RADIO BUTTONS
                    self.radioButton_Computer.setChecked(False)
                    self.radioButton_Smartphone.setChecked(False)
                    # HIDE labels & List
                    self.label_explanation_run_one_task.setHidden(True)
                    self.label_select_smartphone_or_browser_tab_run_one_task.setHidden(True)
                    self.comboBox_select_browser_smartphone_tab_run_one_task.setHidden(True)
                    # ***************** POPUP *******************
                    mymodules.PopupMessage("Error!",
                                           f"Before to run Smartphone automation task, you need to click on 'Scan smarpthones' button in the 'Settings' tab in order to detect your connected smartphone(s).")

                    self.TabRunOneTask_PrepareListTasksButtons('hide')
                    # LET'S OPEN THE SETTINGS TAB
                    self.tabWidget.setCurrentIndex(2)
                    return "The scan of smartphones is done from tab 'Run one Task'TRUE."


            else:

                self.HideButtonsRunOneTask(True)
                self.radioButton_Smartphone.setChecked(False)
                return "The scan of smartphones is done from tab 'Run one Task'FALSE."
                # self.TabRunOneTask_PrepareListTasksButtons('show', 'smartphone')

    def scan_details_smartphones_tab_run(self, progress_callback):
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")

        if not mymodules.CheckSoftwareInstalled():
            mymodules.PopupMessage("Error!",
                                   "You try to automate smartphones but you didn't install all the necessary softwares!\nPlease go to 'Settings' tab and click on 'Install Smartphone Automation' button.")
            logger.error("You try to automate smartphones but you didn't install all the necessary softwares!")
            mymodules.DisplayMessageLogUI(self.label_log,
                                          f"SMARTPHONE||| You try to automate smartphones but you didn't install all the necessary softwares!",
                                          "Red")

            self.checkBox_smartphones.setStyleSheet('color:Red')
            self.checkBox_smartphones.setChecked(False)

            self.label_log.setStyleSheet(f"color: Blackeen")
            self.label_log.setText(
                f"<b>ERROR SMARTPHONES:</b> You try to automate smartphones but you didn't install all the necessary softwares!<br>Please go to the tab 'Settings' and click on 'Install SmartPhone Automation' button. <br>You can skip this part by running automation on your computer only. You will have to check only the option 'Your computer'  and uncheck the option 'Your smartphone(s).")

            self.are_smartphones_ok = False

        else:
            # USER INSTALLED THE NECESSARY SOFTWARE

            self.checkBox_smartphones.setStyleSheet('color:Black')
            self.checkBox_smartphones.setChecked(True)
            self.automation_with_smartphones = True

            # LET'S GET THE LIST OF TASKS USER
            self.list_tasksuser = mymodules.GetAllTasksDetails(self.current_campaign_id)
            # WE CHECK IF SOFTWARES FOR SMARTPHONE AUTOMATION ARE READY
            self.are_smartphones_ok = self.sub_process_scan_details_smartphones()
            if self.are_smartphones_ok:
                try:
                    # IF list_smartphone IS EMPTY ---
                    if not self.list_smartphones or self.list_smartphones == "":
                        # ***************** POPUP *******************
                        mymodules.PopupMessage("Error",
                                               "There aren't smartphones connected to your computer.\n\nPlease go to settings and make a scan of smartphones in order to detect the ones connected by USB to your computer.")
                        self.label_log.setText(
                            "There aren't smartphones connected to your computer.\n\nPlease go to settings and make a scan of smartphones in order to detect the ones connected by USB to your computer.")

                    # IF list_smartphone IS NOT EMPTY ---
                    else:
                        print(f"self.list_smartphones : {self.list_smartphones}")
                except Exception as ex:
                    # !!!!!! ERROR => THE list_smarthpones DOESN'T EXIST. WE NEED SHOW POPUP AFTER HIDING EVERYTHING
                    logger.error(f"Error {ex} We need to inform user with popup to make a scan smarpthone.")
                    mymodules.PopupMessage("Error!",
                                           f"Before to run Smartphone automation task, you need to click on 'Scan smarpthones' button in the 'Settings' tab in order to detect your connected smartphone(s).")
                    self.TabRunOneTask_PrepareListTasksButtons('hide')
                    # LET'S OPEN THE SETTINGS TAB
                    self.tabWidget.setCurrentIndex(2)
        return "The scan of smartphones is done from tab 'Run'."

    def CheckProfileBrowserChrome(self, progress_callback):
        """
        Run in tab one 'Run'
        This function will check if we found the cookies of the selected browser
        As there are 2 checkboxes for the 2 browsers Chrome and Firefox,
        We need to check the ones which are checked by user:
        """
        # 1rst we need to get the browser choice of user:

        if self.checkBox_Chrome.isChecked():
            self.is_profile_chrome_browser_ok = mymodules.CheckBrowserProfile('Chrome')
            if self.is_profile_chrome_browser_ok:
                mymodules.DisplayMessageLogUI(self.label_log,
                                              f"COMPUTER||| PhoneBot checked if the Chrome profile exists : {self.is_profile_chrome_browser_ok}",
                                              "Black")

                self.label_4_Title_2.setStyleSheet(f"color: Green")

                self.label_info_devices.setStyleSheet(f"color: Green")
                self.label_info_devices.setText("Chrome browser is ok.")

                self.label_log.setStyleSheet(f"color: Green")
                self.label_log.setText("<b>BROWSER OK:</b> Automation should run without any issues.")

                # === WE NEED TO REMEMBER IF CHROME OR FIREFOX WERE CHECKED OR NOT
                self.checkBox_Chrome.setEnabled(True)



            else:
                mymodules.DisplayMessageLogUI(self.label_log,
                                              f"COMPUTER||| PhoneBot checked if the Chrome profile exists : {self.is_profile_chrome_browser_ok}",
                                              "Red")

                self.label_4_Title_2.setStyleSheet(f"color: Red")

                self.label_info_devices.setStyleSheet(f"color: Red")
                self.label_info_devices.setText("Chrome browser is not ok.")

                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    "<b>PROBLEM BROWSER:</b> PhoneBot couldn't find any profile for your browser Chrome.<br>=> Please select another browser or install Chrome.")

                self.checkBox_Chrome.setEnabled(False)
                self.checkBox_Chrome.setChecked(False)
                self.is_profile_chrome_browser_ok = False
        else:
            self.is_profile_chrome_browser_ok = True

        self.is_profile_browser_ok = self.is_profile_chrome_browser_ok
        return "Checking browser Chrome is finished"

    def CheckProfileBrowserFirefox(self, progress_callback):
        """
        This function will check if we found the cookies of the selected browser
        As there are 2 checkboxes for the 2 browsers Firefox and Firefox,
        We need to check the ones which are checked by user:
        """
        # 1rst we need to get the browser choice of user:
        logger.info("============ CheckProfileBrowserFirefox ================")
        if self.checkBox_Firefox.isChecked():
            self.is_profile_firefox_browser_ok = mymodules.CheckBrowserProfile('Firefox')
            if self.is_profile_firefox_browser_ok:
                mymodules.DisplayMessageLogUI(self.label_log,
                                              f"COMPUTER||| PhoneBot checked if the Firefox profile exists : {self.is_profile_firefox_browser_ok}",
                                              "Black")

                self.label_4_Title_2.setStyleSheet(f"color: Green")

                self.label_info_devices.setStyleSheet(f"color: Green")
                self.label_info_devices.setText("Firefox browser is ok.")

                self.label_log.setStyleSheet(f"color: Green")
                self.label_log.setText("<b>BROWSER OK:</b> Automation should run without any issues.")
                # === WE NEED TO REMEMBER IF CHROME OR FIREFOX WERE CHECKED OR NOT
                self.checkBox_Firefox.setEnabled(True)



            else:
                mymodules.DisplayMessageLogUI(self.label_log,
                                              f"COMPUTER||| PhoneBot checked if the Firefox profile exists : {self.is_profile_firefox_browser_ok}",
                                              "Red")

                self.label_4_Title_2.setStyleSheet(f"color: Red")
                self.label_info_devices.setStyleSheet(f"color: Red")
                self.label_info_devices.setText("No browser profile for 'Firefox'.")
                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    "<b>PROBLEM BROWSER:</b> PhoneBot couldn't find any profile for your browser Firefox.<br>=> Please select another browser or install Firefox.")
                self.checkBox_Firefox.setChecked(False)
                self.is_profile_firefox_browser_ok = False

        else:
            self.is_profile_firefox_browser_ok = True

        self.is_profile_browser_ok = self.is_profile_firefox_browser_ok
        return "Checking browser Firefox is finished"

    def InstallSmartphoneAutomation(self, progress_callback):

        """
        This method will check if the softwares for Smartphone automation are installed
        """

        # ============================================================================================================
        # ============================ We check all the necessary software and  ======================================
        # =============================== environment variable are installed =========================================
        # ============================================================================================================

        while True:
            try:

                java, node, android, appium, tesseract, sdkmanager, build_tools = prepare_envir_appium.start_checking_env_appium()
                break
            except ValueError:
                logger.info("ERROR prepare_env")

        self.ChangeColorsNecessarySoftwares(java, node, android, appium, tesseract, sdkmanager, build_tools)
        return "Preparing PhoneBot Done"

    def SaveLicense(self, progress_callback):
        """
        This function will save the license and check if it is correct
        """

        try:
            print(100 * "*")
            print(100 * "*")
            print(100 * "*")
            print(100 * "*")
            if self.lineEdit_Email.text() == "":
                mymodules.PopupMessage('Error Email!', 'Please fill the email field!')
            else:
                if self.lineEdit_License.text() == "":
                    mymodules.PopupMessage('Error License!', 'Please fill the license field!')
                else:
                    self.email = self.lineEdit_Email.text()
                    self.license_key_config = self.lineEdit_License.text()
                    print(f"self.email : {self.email} - {type(self.email)}")
                    print(f"self.license_key_config : {self.license_key_config} - {type(self.license_key_config)}")
                    config = configparser.ConfigParser()
                    config.read(mymodules.LoadFile('config.ini'))
                    config.set('Settings', 'Email', self.email)
                    config.set('Settings', 'license_key', self.license_key_config)
                    with open(mymodules.LoadFile('config.ini'), 'w') as configfile:
                        config.write(configfile)
                    configfile.close()

                    self.user_id, self.subscription_id, self.license_id = self.CheckLicense()
                    print(100 * "*")
                    print(100 * "*")
                    print(100 * "*")
                    print(100 * "*")
        except Exception as e:
            logger.critical(f" {e} => Problem with SaveConfigFile.")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(f"Problem with SaveConfigFile!<br>{e}.")
        # === [1] Check the License ============================================================
        return "Saving License Done"

    def StartPhoneBotReport(self, progress_callback):

        if self.user_id is not None and self.user_id != "":
            mymodules.UpdateMysqlDB(self.user_id)
            if self.current_tab == "run":
                webbrowser.open(f'https://dashboard.phonebot.co/campaign_report?id_campaign={self.current_campaign_id}',
                                new=2)
            elif self.current_tab == "run_one_task":
                webbrowser.open(
                    f'https://dashboard.phonebot.co/campaign_report?id_campaign={self.current_campaign_id_one_task}',
                    new=2)
        else:
            mymodules.PopupMessage("Error",
                                   "You need first to activate your PhoneBot with your email and your license key in the 'Settings' tab.")
            self.label_log.setText(
                "You need first to activate your PhoneBot with your email and your license key in the 'Settings' tab.")
        if self.current_tab == 'run':
            return "Build Report Done"
        elif self.current_tab == 'run_one_task':
            return "Build Report Done Tab Run One Task"

    def StartPhoneBot(self, progress_callback):
        """
        METHOD WHICH RUNS PHONEBOT

        THERE ARE 2 SCENARIOS:
         - automation with computer only
         - automation with smartphones (and computer) : Computer will be added as a smartphone in SQLITE3
            table 'smartphones'
        """
        # ===================================== CREATE SQLITE3 CONNECTION ==============================================
        sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        # ============================ CREATE THE LOCK FOR MULTITHREAD =====================================
        lock = threading.Lock()

        # 1rst We need to add the computer in list of smartphones in order to add it as a device in list of devices in case user
        # selected automation of Computer and Smartphone

        if self.automation_with_computer:
            logger.info("========================= AUTOMATION WITH COMPUTER ==============================")
            try:
                if self.checkBox_Chrome.isChecked():
                    sqlite_cursor.execute("INSERT INTO smartphones(udid, devicename, status) VALUES(?,?,?)", \
                                          ('Computer', 'Chrome', 1))
                    sqlite_connection.commit()
                    logger.info(f"Adding Computer Chrome as device in table smartphones")
                if self.checkBox_Firefox.isChecked():
                    sqlite_cursor.execute("INSERT INTO smartphones(udid, devicename, status) VALUES(?,?,?)", \
                                          ('Computer', 'Firefox', 1))
                    sqlite_connection.commit()
                    logger.info(f"Adding Computer Firefox as device in table smartphones")
            except Exception as ex:
                logger.critical(f"ERROR when inserting smartphone row : {ex}")

        if self.automation_with_smartphones:
            logger.info("========================= AUTOMATION WITH SMARTPHONES ==============================")
            # 2nd we need to get the list of smartphones connected
            list_smartphones_connected = mymodules.ListSmartPhonesConnected()
            print(f"list_smartphones_connected : {list_smartphones_connected}")
            # 3rd give a systemPort number to the ones who doesn't have a portnumber
            mymodules.give_systemPort_to_smartphones()

            appium_server_started = self.StartAppiumServer()
            if appium_server_started:
                # 5th, we can start the work
                list_thread_smartphone = []
                logger.info("PhoneBot will start the automation on each smartphone connected.")
                logger.info(f"list_smartphones_connected : {list_smartphones_connected}.")
                if len(list_smartphones_connected) == 0:
                    logger.critical(
                        "list_smartphones_connected = 0. PhoneBot did not find any smartphones on your computer.")
                    mymodules.PopupMessage("No smartphone found!",
                                           f"PhoneBot found {self.number_connected_phones} smartphones connected. Please check the usb cables and press a key to continue.")
                    self.label_log.setText(
                        f"PhoneBot found {self.number_connected_phones} smartphones connected. Please check the usb cables and press a key to continue.")
                    return

                print(f"list_smartphones_connected : {list_smartphones_connected} {type(list_smartphones_connected)}")

                for smartphone_connected in list_smartphones_connected:
                    try:
                        logger.info(f"Run {smartphone_connected}.............")
                        self.current_tab = "run"
                        print(f"""
                                    smartphone_connected : {smartphone_connected}
                                    self.user_id : {self.user_id}
                                    self.list_tasksuser : {self.list_tasksuser}
                                    self.label_log : {self.label_log}
                                    lock : {lock}
                                    self.current_tab : {self.current_tab}
                        """)
                        thread_smartphone = threading.Thread(target=RunSmartphones.main,
                                                             args=[smartphone_connected, self.user_id,
                                                                   self.list_tasksuser,
                                                                   self.label_log, lock, self.current_tab])
                        thread_smartphone.start()
                        list_thread_smartphone.append(thread_smartphone)
                    except ValueError:
                        logger.error("Error with thread RunSmartphone")
                try:
                    for each_thread_smartphone in list_thread_smartphone:
                        each_thread_smartphone.join()
                except ValueError:
                    logger.error("Error with each_thread_smartphone.join()")
            else:
                mymodules.DisplayMessageLogUI(self.label_log,
                                              "Phonebot couldn't start Appium server. Please contact support@phonebot.co")
                mymodules.PopupMessage('Error',
                                       "Phonebot couldn't start Appium server. Please contact support@phonebot.co")

        if self.automation_with_computer and not self.automation_with_smartphones:
            logger.info("========================= AUTOMATION WITH DESKTOP ONLY V0.003 ==========================")
            # WE ARE RUNNING AS MUCH ACCOUNTS AS POSSIBLE, WE NEED MAX BROWSERS
            # PHONEBOT WILL RUN THE SAME TASKS FOR EACH PROFILE FOUND IN PLATFORMS

            if self.checkBox_Chrome.isChecked() and mymodules.CheckBrowserProfile('Chrome'):
                automate_Chrome = True
            else:
                automate_Chrome = False

            if self.checkBox_Firefox.isChecked() and mymodules.CheckBrowserProfile('Firefox'):
                automate_Firefox = True
            else:
                automate_Firefox = False

            self.current_tab = "run"
            RunBrowser.main(automate_Chrome, automate_Firefox, self.list_tasksuser, self.label_log, lock,
                            self.current_tab)

        try:
            sqlite_cursor.close()
            sqlite_connection.close()
        except Exception as ex:
            logger.error(f"Error closing sqlite : {ex}")
        return "PhoneBot finish the job"

    def RunOneTaskComputerOrSmartphone(self, progress_callback):
        logger.info("DEF ========== RunOneTaskComputerOrSmartphone ==============")

        if self.tab_run_one_task_mode == 'computer':
            try:

                logger.info(f"""self.id_task:{self.id_task}
                            self.taskuser_id:{self.taskuser_id}
                            """)
                lock = threading.Lock()
                print(f"""
                label_log_run_one_task Enable : {self.label_log_run_one_task.isEnabled()}
                label_log_run_one_task Hidden : {self.label_log_run_one_task.isHidden()}
                """)
                self.current_tab = "run_one_task"
                # ==========================================================================================
                # ==========================================================================================
                # ==========================================================================================
                # EXECUTION OF THE TASK ====================================================================
                RunBrowser.StartBrowser(self.id_task, self.taskuser_id, self.browser, self.label_log_run_one_task, lock,
                                        self.current_tab)

                # ==========================================================================================
                # ==========================================================================================
                # ==========================================================================================

                if self.user_id is not None and self.user_id != "":
                    # FINAL PART => OPEN REPORT PAGE
                    mymodules.DisplayMessageLogUI(self.label_log_run_one_task,
                                                  f"Congratulations!!! The task was accomplished succesfully! PhoneBot will open the report in your browser.",
                                                  "Green", self.current_tab)
                    # mymodules.PopupMessage("Congratulations!",
                    #                      "The task was accomplished succesfully! PhoneBot will open the report in your browser.")
                    mymodules.UpdateMysqlDB(self.user_id)
                    # webbrowser.open(f'https://dashboard.phonebot.co/task_user_report/{self.taskuser_id}/view', new=2)

                else:
                    mymodules.PopupMessage("Error",
                                           "You need first to activate your PhoneBot with your email and your license key in the 'Settings' tab.")
                    self.label_log.setText(
                        "You need first to activate your PhoneBot with your email and your license key in the 'Settings' tab.")
                return "Task is done"
            except Exception as ex:
                logger.error(f"Error RunOneTaskComputerOrSmartphone : {ex}")
        elif self.tab_run_one_task_mode == 'smartphone':

            lock = threading.Lock()
            self.current_tab = "run_one_task"
            appium_server_started = self.StartAppiumServer()
            if appium_server_started:

                result = RunSmartphones.StartSmartphone(
                    self.comboBox_select_browser_smartphone_tab_run_one_task.currentText(),
                    self.id_task, self.taskuser_id, self.label_log_run_one_task, lock, self.current_tab)

                return "Task is done"
            else:
                mymodules.DisplayMessageLogUI(self.label_log_run_one_task,
                                              "Phonebot couldn't start Appium server. Please contact support@phonebot.co")
                mymodules.PopupMessage('Error',
                                       "Phonebot couldn't start Appium server. Please contact support@phonebot.co")
                return "Task is done"

    # ====================================== BUTTONS ========================================
    def CheckBoxControlSmartphones(self):

        # WE CHECK IF USER SELECTED A CAMPAIGN OR NOT
        if self.current_campaign_id == "" or self.current_campaign_id == None or not self.current_campaign_id or self.current_campaign_id == "0":
            mymodules.PopupMessage("Error!",
                                   "You have to select a campaign. If you don't see any campaign in the list, please go to your dashboard https://dashboard.phonebot.co and create or enable a campaign.")
            logger.error("You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

            self.label_4_Title.setStyleSheet(f"color: Red")
            self.label_info_campaign.setStyleSheet(f"color: Red")
            self.label_info_campaign.setText("Please select a campaign")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR CAMPAIGN:</b>You have to select a campaign.<br>If you don't see any campaign in the list, please go to your dashboard <a href='https://dashboard.phonebot.co'>https://dashboard.phonebot.co</a> and create or enable a campaign.")
            print(self.checkBox_smartphones.isChecked())
            self.checkBox_smartphones.setChecked(False)
        else:
            # USER SELECTED A CAMPAIGN, DID HE CHECK SMARTPHONES?
            if self.checkBox_smartphones.isChecked():
                print(self.checkBox_smartphones.isChecked())
                # WE SHOW THE LOADING ANIMATION BECAUSE TI WILL TAKE LONG TIME TO SCAN SMARTPHONES
                # WE SHOW ANIMATED GIF OF SCANNING SMARTPHONE
                # === Play animated gif ================
                self.label_loading_scan_smartphones.setHidden(False)
                self.gif_loading_smartphones = QMovie(
                    mymodules.LoadFile("gui/img/loading_scan_smartphones_V0003.gif"))
                self.label_loading_scan_smartphones.setMovie(self.gif_loading_smartphones)
                self.gif_loading_smartphones.start()
                self.HideAllQElements(True)
                self.label_logo.setHidden(True)

                self.line.setHidden(True)
                self.button_OpenLogFile.setHidden(True)

                # WE SET UP THE FUNCTION
                worker = Worker(
                    self.scan_details_smartphones_tab_run)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)
                # WE Execute
                self.threadpool.start(worker)



            else:
                print(self.checkBox_smartphones.isChecked())
                self.checkBox_smartphones.setChecked(False)

    def ButtonStartPhoneBot(self):  # <=== This method works perfectly by showing the loading gif.
        # Pass the function to execute
        # === 1rst we need to check if user select a campaign
        self.current_campaign_name = str(self.comboBox_select_campaign.currentText())
        self.current_campaign_id = self.GetCurrentCampaignID(self.current_campaign_name)

        logger.info(f"self.current_campaign_id : {self.current_campaign_id}")
        if self.current_campaign_id == "" or self.current_campaign_id is None or self.current_campaign_id == 'None' or not self.current_campaign_id or self.current_campaign_id == "0":
            mymodules.PopupMessage("Error!",
                                   "You have to select a campaign. If you don't see any campaign in the list, please go to your dashboard https://dashboard.phonebot.co and create or enable a campaign.")
            logger.error("You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

            self.label_4_Title.setStyleSheet(f"color: Red")
            self.label_info_campaign.setStyleSheet(f"color: Red")
            self.label_info_campaign.setText("Please select a campaign")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR CAMPAIGN:</b>You have to select a campaign.<br>If you don't see any campaign in the list, please go to your dashboard <a href='https://dashboard.phonebot.co'>https://dashboard.phonebot.co</a> and create or enable a campaign.")
        else:
            # === 2nd GOOGLE SPREADSHEET ==================================
            # Let's empty the Google sheet report
            mymodules.GoogleSheetClearValues('11jJvq12zM5q0VhkZS3RjttqhlQ61mtBmavkox0symZQ')
            # ===================================== CREATE SQLITE3 CONNECTION ==============================================
            sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
            sqlite_cursor = sqlite_connection.cursor()
            # ===================================== CREATE MYSQL CONNECTION ==============================================
            mysql_connection, mysql_cursor = mymodules.get_mysql_connection()
            # LET'S GEt ALL THE TASKS
            self.list_tasksuser = mymodules.GetAllTasksDetails(self.current_campaign_id)
            print(f"self.list_tasksuser : {self.list_tasksuser}")

            self.label_4_Title.setStyleSheet(f"color: Black")
            self.label_info_campaign.setStyleSheet(f"color: Green")
            self.label_info_campaign.setText("Campaign selected")

            print(f"current_campaign_name : {self.current_campaign_name}")
            print(f"current_campaign_data : {self.current_campaign_id}")

            # === 3rd WHICH DEVICES ==================================
            # === we need to check if user select computer or smartphones or both
            if not self.checkBox_Chrome.isChecked() and not self.checkBox_Firefox.isChecked() and not self.checkBox_smartphones.isChecked():
                mymodules.PopupMessage("Error!",
                                       "You have to select at least one device: computer or smartphone(s). You can select both if you like.")
                logger.error(
                    "You have to select at least one device: computer or smartphone(s). You can select both if you like.")

                self.label_4_Title_2.setStyleSheet(f"color: Red")
                self.label_info_devices.setStyleSheet(f"color: Red")
                self.label_log.setStyleSheet(f"color: Red")
                self.label_log.setText(
                    f"<b>ERROR DEVICES:</b>You have to select at least one device.<br>You can automate your computer and/or some Android smartphones connected to your computer with USB cable.")

            else:
                # === 4th ENABLE TRUE THE FLAGS ==================================

                self.label_4_Title_2.setStyleSheet(f"color: Blacked")
                self.label_info_devices.setStyleSheet(f"color: Green")
                self.label_info_devices.setText("Device(s) selected")

                print("# get the checkboxes values")
                if self.checkBox_Chrome.isChecked() or self.checkBox_Firefox.isChecked():
                    self.automation_with_computer = True
                else:
                    self.automation_with_computer = False

                if self.checkBox_smartphones.isChecked():
                    self.automation_with_smartphones = True
                else:
                    self.automation_with_smartphones = False

                # === If user select computer, we need to check if browsers are ok
                self.is_computer_ok = True
                self.are_smartphones_ok = True

                print(f"""
                        self.automation_with_smartphones : {self.automation_with_smartphones}
                        self.automation_with_computer : {self.automation_with_computer}
                """)

                # === 5th CHECK BROWSER PROFILES ==================================
                if self.automation_with_computer:
                    print("Automation computer is active")
                    self.is_profile_browser_ok = self.is_profile_chrome_browser_ok + self.is_profile_firefox_browser_ok
                    print(f"""
                            is_profile_browser_ok : {self.is_profile_browser_ok}
                            is_profile_firefox_browser_ok : {self.is_profile_firefox_browser_ok}
                            is_profile_chrome_browser_ok : {self.is_profile_chrome_browser_ok}
                            """)

                    if not self.is_profile_browser_ok:
                        mymodules.PopupMessage("Error!",
                                               f"PhoneBot didn't find the profile of one of your browser.\nThat means you didn't install it on your computer or your browser didn't save any credentials.")
                        self.label_4_Title_2.setStyleSheet(f"color: Red")
                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(
                            f"<b>ERROR DEVICES:</b>You have to select at least one device.<br>You can automate your computer and/or some Android smartphones connected to your computer with USB cable.")
                        self.is_computer_ok = False

                # === 6th ARE SMARTPHONES CONNECTED ==================================
                # === If user select smartphones, we need to check if smartphones are connected
                if self.automation_with_smartphones:
                    logger.info(
                        "Automation smartphones is active. Se we need to check if smartphone softwares are installed, to make list of necessary app, scan the smartphones")

                    # 1rst - We need to check the necessary softwares installed or not?
                    # 2nd - We get the list of tasks
                    # 3rd - We check if everything is completed correctly
                    # 4th - We check which smartphones are connected
                    # 5th - We check if each smartphones are the appropriate app

                    # 1rst - We need to check the necessary softwares
                    if not mymodules.CheckSoftwareInstalled():
                        mymodules.PopupMessage("Error!",
                                               "You try to automate smartphones but you didn't install all the necessary softwares!")
                        logger.error(
                            "You try to automatesmartphones but you didn't install all the necessary softwares!")

                        self.checkBox_smartphones.setStyleSheet(f"color: Red")
                        self.checkBox_smartphones.setChecked(False)
                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(
                            f"<b>ERROR SMARTPHONES:</b>You try to automate smartphones but you didn't install all the necessary softwares!<br>Please go to the tab 'Settings' and click on 'Install SmartPhone Automation' button.<br>You can skip this part by running automation on your computer only. You will have to check only the option 'Your computer'  and uncheck the option 'Your smartphone(s).")
                        self.are_smartphones_ok = False
                        self.checkBox_smartphones.setChecked(False)


                    else:
                        # 2nd - We get the list of tasks and # 3rd - We check if everything is completed correctly
                        self.MakeListNecessaryApp()
                        # 4th - We check which smartphones are connected and # 5th - We check if each smartphones are the appropriate app
                        self.are_smartphones_ok = self.sub_process_scan_details_smartphones()

                print(f"""
                        self.is_computer_ok = {self.is_computer_ok}
                        self.are_smartphones_ok = {self.are_smartphones_ok} 
                        self.automation_with_smartphones = {self.automation_with_smartphones}
                        """)

                # === 7th IF EVERYTHING IS OK ==================================

                if self.is_computer_ok or (self.are_smartphones_ok and self.automation_with_smartphones):
                    # 5th, we collect all the details of all the tasks of selected campaign and we save it in SQLITE3 DB

                    self.button_Run.setEnabled(False)
                    self.button_Run.setText('Running...')
                    self.button_Run.setStyleSheet("background-color: #ffcc00;")
                    self.label_logo.setHidden(True)
                    self.label_running.setHidden(False)
                    # Let's disable all the fields
                    self.EnableTabRun(False)

                    # === Play animated gif ================
                    self.gif = QMovie("gui/img/animated_gif_logo_UI_.gif")  # ('gui/img/animated_gif_logo_UI_.gif') !!!
                    self.label_running.setMovie(self.gif)
                    self.gif.start()

                    worker = Worker(self.StartPhoneBot)  # Any other args, kwargs are passed to the run function
                    worker.signals.result.connect(self.print_output)
                    worker.signals.finished.connect(self.thread_complete)
                    worker.signals.progress.connect(self.progress_fn)
                    print(f" comboBox_select_campaign is Enable ? : {self.comboBox_select_campaign.isEnabled()}")

                    # Execute
                    logger.info(
                        f"self. Before to run ButtonStartPhoneBot : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
                    self.threadpool.start(worker)
                    logger.info(
                        f"self. After to run ButtonStartPhoneBot : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

                else:
                    # === 8th IF SOMETHING IS WRONG ==================================

                    if self.automation_with_computer and not self.is_computer_ok:
                        mymodules.PopupMessage("Error!",
                                               "You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

                        logger.error(
                            "You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

                        self.label_3.setStyleSheet(f"color: Red")
                        self.label_3_Title.setStyleSheet(f"color: Red")

                        self.label_info3.setStyleSheet(f"color: Red")
                        self.label_info3.setText("You enable 'Computer' automation but it failed.")

                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(f"<b>ERROR BROWSER:</b>PhoneBot couldn't find your browser profile.")

                    if self.automation_with_smartphones and not self.are_smartphones_ok:
                        mymodules.PopupMessage("Error!",
                                               "You enable 'Smartphone' automation but there is an issue with your smartphone(s).")

                        logger.error(
                            "You enable 'Smartphone' automation but there is an issue with your smartphone(s).")

                        self.label_3.setStyleSheet(f"color: Red")
                        self.label_3_Title.setStyleSheet(f"color: Red")

                        self.label_info3.setStyleSheet(f"color: Red")
                        self.label_info3.setText("You enable 'Smartphone' automation but it failed.")

                        self.label_log.setStyleSheet(f"color: Red")
                        self.label_log.setText(f"<b>ERROR BROWSER:</b>PhoneBot couldn't find your browser profile.")

        try:
            sqlite_cursor.close()
            sqlite_connection.close()
        except Exception as ex:
            logger.error(f"Error closing sqlite : {ex}")
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

    def ButtonSaveLicense(self):
        self.HideAllQElements(True)
        self.label_1_Title.setHidden(True)
        self.lineEdit_Email.setHidden(True)
        self.label_loading_settings_usb_debugging.setHidden(True)
        self.label_loading_txt_settings.setHidden(True)
        self.label_loading_settings.setHidden(False)
        self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_settings.setMovie(self.gif_loading)

        self.gif_loading.start()
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(3, False)

        # Pass the function to execute
        worker = Worker(self.SaveLicense)  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        logger.info(
            f"self. Before to run ButtonSaveLicense : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

        self.threadpool.start(worker)
        logger.info(
            f"self. After to run ButtonSaveLicense : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    def ButtonStartPhoneBotReport(self):
        self.current_tab = "run"
        self.label_loading_txt_run.setHidden(False)

        self.label_loading_run.setHidden(False)
        self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_run.setMovie(self.gif_loading)
        self.gif_loading.start()
        self.HideAllQElements(True)
        self.line.setHidden(True)

        # Pass the function to execute
        worker = Worker(self.StartPhoneBotReport)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        logger.info(
            f"self. Before to run ButtonSaveLicense : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

        self.threadpool.start(worker)
        logger.info(
            f"self. After to run ButtonSaveLicense : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    def ButtonStartPhoneBotReport_2(self):
        self.current_tab = "run_one_task"
        self.label_loading_txt_run.setHidden(False)
        self.label_log_run_one_task.setText(
            "Please wait... PhoneBot is updating your data on your dashboard in order to show you an updated report.")
        self.label_loading_run.setHidden(False)
        self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_run.setMovie(self.gif_loading)
        self.gif_loading.start()

        self.HideAllQElements(True)
        self.line.setHidden(True)

        # Pass the function to execute
        worker = Worker(self.StartPhoneBotReport)  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        logger.info(
            f"self. Before to run ButtonReport : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

        self.threadpool.start(worker)
        logger.info(
            f"self. After to run ButtonReport : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    def ButtonOpenLogFile(self):
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        # if platform.system() == 'Darwin':

        # elif platform.system() == 'Windows':
        from shutil import copyfile
        copyfile(mymodules.LoadFile('log.log'), 'tmplog.log')
        os.system("start " + mymodules.LoadFile('tmplog.log'))

    def ButtonInstallSmartphoneAutomation(self):

        # === Play animated gif ================

        self.label_loading_txt_settings.setHidden(False)
        self.gif_loading_txt = QMovie(
            mymodules.LoadFile("gui/img/loading_txt_settings.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_txt_settings.setMovie(self.gif_loading_txt)
        self.gif_loading_txt.start()

        self.label_loading_settings.setHidden(False)
        self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_settings.setMovie(self.gif_loading)
        self.gif_loading.start()

        self.HideAllQElements(True)
        self.line.setHidden(True)

        # Pass the function to execute
        worker = Worker(self.InstallSmartphoneAutomation)  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        logger.info(
            f"self. Before to run ButtonInstallSmartphoneAutomation : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

        self.threadpool.start(worker)
        logger.info(
            f"self. After to run ButtonInstallSmartphoneAutomation : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    def ButtonStartScaningSmartphones(self):

        # === Play animated gif ================
        self.label_loading_scan_smartphones.setHidden(False)
        self.gif_loading_scan = QMovie(
            mymodules.LoadFile("gui/img/loading_scan_smartphones_V0003.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_scan_smartphones.setMovie(self.gif_loading_scan)
        self.gif_loading_scan.start()
        self.label_loading_settings.setHidden(False)
        self.gif_loading = QMovie(mymodules.LoadFile("gui/img/loading.gif"))  # ('gui/img/loading.gif') !!!
        self.label_loading_settings.setMovie(self.gif_loading)
        self.gif_loading.start()
        self.HideAllQElements(True)
        self.line.setHidden(True)
        self.label_loading_txt_settings.setHidden(True)
        self.label_loading_settings_usb_debugging.setHidden(True)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(3, False)
        # Pass the function to execute
        worker = Worker(self.scan_details_smartphones)  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        logger.info(
            f"self. Before to run ButtonStartScaningSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")
        self.threadpool.start(worker)
        logger.info(
            f"self. After to run ButtonStartScaningSmartphones : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

    def ClickCheckBoxBrowserChrome(self):
        self.current_campaign_name = str(self.comboBox_select_campaign.currentText())
        self.current_campaign_id = self.GetCurrentCampaignID(self.current_campaign_name)
        if self.current_campaign_id == "" or self.current_campaign_id == None or self.current_campaign_id == 'None' or not self.current_campaign_id or self.current_campaign_id == "0":
            mymodules.PopupMessage("Error!",
                                   "You have to select a campaign. If you don't see any campaign in the list, please go to your dashboard https://dashboard.phonebot.co and create or enable a campaign.")
            logger.error("You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

            self.label_4_Title.setStyleSheet(f"color: Red")
            self.label_info_campaign.setStyleSheet(f"color: Red")
            self.label_info_campaign.setText("Please select a campaign")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR CAMPAIGN:</b>You have to select a campaign.<br>If you don't see any campaign in the list, please go to your dashboard <a href='https://dashboard.phonebot.co'>https://dashboard.phonebot.co</a> and create or enable a campaign.")

            self.is_profile_chrome_browser_ok = False
            self.checkBox_Chrome.setCheckState(0)
            self.checkBox_Firefox.setCheckState(0)

        else:
            self.label_4_Title.setStyleSheet(f"color: Green")
            self.label_info_campaign.setStyleSheet(f"color: Green")
            self.label_info_campaign.setText("Campaign selected")
            self.label_log.setStyleSheet(f"color: Green")
            self.label_log.setText("<b>CAMPAIGN SELECTED</b>")

            print("# === Play animated gif Check Browser Chrome ================")
            try:
                # === Play animated gif ================

                self.gif_loading_browsers = QMovie(
                    mymodules.LoadFile("gui/img/scan_chrome_gif.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_run.setMovie(self.gif_loading_browsers)
                self.gif_loading_browsers.start()
                self.HideAllQElements(True)
                self.label_loading_run.setHidden(False)
                self.label_logo.setHidden(True)
                self.line.setHidden(True)
                self.button_OpenLogFile.setHidden(True)
                # Pass the function to execute
                worker = Worker(self.CheckProfileBrowserChrome)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)
                # Execute
                logger.info(
                    f"self. Before to run ClickCheckBoxBrowserChrome : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

                self.threadpool.start(worker)
                logger.info(
                    f"self. After to run ClickCheckBoxBrowserChrome : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

                print(" ==== Finish CheckProfileBrowser =================================================")
            except Exception as ex:
                print(f"Error Play animated gif Chrome : {ex}")

    def ClickCheckBoxBrowserFirefox(self):
        self.current_campaign_name = str(self.comboBox_select_campaign.currentText())
        self.current_campaign_id = self.GetCurrentCampaignID(self.current_campaign_name)
        if self.current_campaign_id == "" or self.current_campaign_id == None or self.current_campaign_id == 'None' or not self.current_campaign_id or self.current_campaign_id == "0":
            mymodules.PopupMessage("Error!",
                                   "You have to select a campaign. If you don't see any campaign in the list, please go to your dashboard https://dashboard.phonebot.co and create or enable a campaign.")
            logger.error("You enable 'Computer' automation but PhoneBot couldn't find your browser profile.")

            self.label_4_Title.setStyleSheet(f"color: Red")
            self.label_info_campaign.setStyleSheet(f"color: Red")
            self.label_info_campaign.setText("Please select a campaign")
            self.label_log.setStyleSheet(f"color: Red")
            self.label_log.setText(
                f"<b>ERROR CAMPAIGN:</b>You have to select a campaign.<br>If you don't see any campaign in the list, please go to your dashboard <a href='https://dashboard.phonebot.co'>https://dashboard.phonebot.co</a> and create or enable a campaign.")
            self.is_profile_chrome_browser_ok = False
            self.checkBox_Chrome.setCheckState(0)
            self.checkBox_Firefox.setCheckState(0)

        else:

            self.label_4_Title.setStyleSheet(f"color: Green")
            self.label_info_campaign.setStyleSheet(f"color: Green")
            self.label_info_campaign.setText("Campaign selected")
            self.label_log.setStyleSheet(f"color: Green")
            self.label_log.setText("<b>CAMPAIGN SELECTED</b>")

            print("# === Play animated gif Check Browser Firefox ================")
            try:
                # === Play animated gif ================

                self.gif_loading_browsers = QMovie(
                    mymodules.LoadFile("gui/img/scan_firefox_gif.gif"))  # ('gui/img/loading.gif') !!!
                self.label_loading_run.setMovie(self.gif_loading_browsers)
                self.gif_loading_browsers.start()
                self.HideAllQElements(True)
                self.label_loading_run.setHidden(False)
                self.label_logo.setHidden(True)

                self.line.setHidden(True)
                self.button_OpenLogFile.setHidden(True)
                # Pass the function to execute
                worker = Worker(
                    self.CheckProfileBrowserFirefox)  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.print_output)
                worker.signals.finished.connect(self.thread_complete)
                worker.signals.progress.connect(self.progress_fn)
                # Execute
                logger.info(
                    f"self. Before to run ClickCheckBoxBrowserFirefox : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

                self.threadpool.start(worker)
                logger.info(
                    f"self. After to run ClickCheckBoxBrowserFirefox : {self.threadpool.activeThreadCount()}/{self.threadpool.maxThreadCount()}")

                print(" ==== Finish CheckProfileBrowser =================================================")
            except Exception as ex:
                print(f"Error Play animated gif Firefox : {ex}")

    # ====================================== AUTRES ========================================

    def ButtonOpenSupport(self):
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        webbrowser.open('https://phonebot.co/community/', new=2)

    def ButtonOpenDoc(self):
        print(f"self.tabWidget.currentIndex() : {self.tabWidget.currentIndex()}")
        print(f"self.tabWidget.currentWidget() : {self.tabWidget.currentWidget()}")
        webbrowser.open('https://phonebot.co/manual-guide/', new=2)

    def ButtonOpenVideoKnowledge(self):
        webbrowser.open('https://phonebot.co/knowledge-base/', new=2)

    def ButtonOpenTutorials(self):
        webbrowser.open('https://phonebot.co/blog/', new=2)

    def ButtonOpenConfig(self):
        webbrowser.open('https://phonebot.co/my-account/edit-account/#configuration_page', new=2)

    def ButtonQuit(self):
        mymodules.KillPhoneBotUI()

    # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def print_output(self, obj):
        logger.info(f'def print_output(self, obj): {obj}')
        if obj == "Preparing PhoneBot Done":
            logger.info("FINISHED => Preparing PhoneBot Done")
            self.gif_loading.stop()  # <---- +++
            self.HideAllQElements(False)

            self.label_loading_settings.setHidden(True)  # <---- +++
            self.gif_loading_txt.stop()  # <---- +++
            self.label_loading_txt_settings.setHidden(True)  # <---- +++
            self.line.setHidden(False)
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)

        if obj == "The scan of smartphones is done.":
            logger.info("FINISHED => We enter in the condition if obj=='The scan of smartphones is done.'")
            self.gif_loading.stop()  # <---- +++
            self.HideAllQElements(False)
            self.label_loading_settings.setHidden(True)  # <---- +++
            self.gif_loading_scan.stop()  # <---- +++
            self.label_loading_scan_smartphones.setHidden(True)  # <---- +++
            self.line.setHidden(False)

            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)

            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(3, True)

        if obj == "Saving License Done":
            logger.info("FINISHED => We enter in the condition if obj=='Saving License Done'")
            self.gif_loading.stop()  # <---- +++
            self.HideAllQElements(False)
            self.label_loading_txt_settings.setHidden(True)
            self.label_loading_settings.setHidden(True)
            self.label_loading_scan_smartphones.setHidden(True)
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)

            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(3, True)

        if obj == "Build Report Done":
            logger.info("FINISHED => We enter in the condition if obj=='Build Report Done'")
            self.HideAllQElements(False)
            self.gif_loading.stop()  # <---- +++
            self.label_loading_run.setHidden(True)  # <---- +++
            self.label_loading_txt_run.setHidden(True)
            self.line.setHidden(False)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            # We have a problem on Tab One Task where all the buttons are displayed and fields
            # self.PrepareTabRunOneTask(True)
            self.TabRunOneTask_HideSelectSmartphoneBrowser(True)
            self.TabRunOneTask_ShowHideTasksButtons('hide')
            self.HideSelectDeviceAndBrowser(True)
            self.label_log_run_one_task.setText("Please select a campaign and a device")
            self.radioButton_Computer.setChecked(False)
            self.radioButton_Smartphone.setChecked(False)

        if obj == "Build Report Done Tab Run One Task":
            logger.info("FINISHED => We enter in the condition if obj=='Build Report Done Tab Run One Task'")
            self.HideAllQElements(False)
            self.gif_loading.stop()  # <---- +++
            self.label_loading_run.setHidden(True)  # <---- +++
            self.label_loading_txt_run.setHidden(True)
            self.line.setHidden(False)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.pushButton_youtube_2.setHidden(False)
            self.label_log_run_one_task.setHidden(True)
            self.comboBox_select_campaign_tab_run_one_task.setHidden(False)
            self.pushButton_youtube_2.setHidden(False)
            # We have a problem on Tab One Task where all the buttons are displayed and fields
            # self.PrepareTabRunOneTask(True)

        if obj == "Check configuration done":
            logger.info("FINISHED => We enter in the condition if obj=='Check configuration done'")
            self.HideAllQElements(False)
            self.gif_loading.stop()  # <---- +++
            self.label_loading_settings.setHidden(True)  # <---- +++
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)

            self.line.setHidden(False)

        if obj == "PhoneBot finish the job":
            logger.info("FINISHED => We enter in the condition if obj=='PhoneBot finish the job'")
            self.gif_loading.stop()  # <---- +++
            self.HideAllQElements(False)
            self.label_running.setHidden(True)
            self.gif.stop()
            self.label_loading_settings.setHidden(True)  # <---- +++

            self.line.setHidden(False)

            # Let's enable all the fields
            self.EnableTabRun(True)
            self.label_logo.setHidden(False)

        if obj == "Checking browser Chrome is finished":
            logger.info("FINISHED => We enter in the condition if obj=='Checking browser Chrome is finished'")
            self.gif_loading_browsers.stop()  # <---- +++
            self.HideAllQElements(False)
            self.label_loading_run.setHidden(True)  # <---- +++
            self.line.setHidden(False)
            self.label_logo.setHidden(False)

            self.button_OpenLogFile.setHidden(False)
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.label_logo.setHidden(False)

        if obj == "Checking browser Firefox is finished":
            logger.info("FINISHED => We enter in the condition if obj=='Checking browser Firefox is finished'")
            self.gif_loading_browsers.stop()  # <---- +++
            self.HideAllQElements(False)
            self.label_loading_run.setHidden(True)  # <---- +++
            self.line.setHidden(False)
            self.label_logo.setHidden(False)

            self.button_OpenLogFile.setHidden(False)
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.label_logo.setHidden(False)

        if obj == "The scan of smartphones is done from tab 'Run one Task'TRUE.":
            logger.info("FINISHED => The scan of smartphones is done from tab 'Run one Task'TRUE.")

            self.TabRunOneTask_Enable_1_2(True)
            self.label_loading_searching_tasks.setHidden(True)
            # self.label_log_run_one_task.setText("")
            self.label_loading_scan_smartphones_2.setHidden(True)
            self.gif_loading_scan.stop()
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.HideLoadingsTabRunCampaign(True)
            self.HideButtonsRunOneTask(False)
            self.label_log_run_one_task.setHidden(True)

        if obj == "The Checking of browser's profiles Firefox & Chrome is finished.":
            logger.info("FINISHED => The Checking of browser's profiles Firefox & Chrome is finished.")
            self.gif_loading_searching_tasks.stop()
            self.label_loading_searching_tasks.setHidden(True)
            self.label_loading_scan_smartphones_2.setHidden(True)

            self.TabRunOneTask_Enable_1_2(True)
            self.label_log_run_one_task.setHidden(False)
            # self.label_log_run_one_task.setText("")

            # self.HideSelectDeviceAndBrowser(False)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.HideLoadingsTabRunCampaign(True)
            self.label_log_run_one_task.setHidden(True)
            self.label_logo.setHidden(False)
            self.HideButtonsRunOneTask(False)

        if obj == "The scan of smartphones is done from tab 'Run one Task'FALSE.":
            logger.info("FINISHED => The scan of smartphones is done from tab 'Run one Task'FALSE.")

            self.TabRunOneTask_PrepareListTasksButtons('hide', 'smartphones')
            self.HideAllQElements(False)
            self.TabRunOneTask_Enable_1_2(True)
            self.label_loading_scan_smartphones_2.setHidden(True)
            self.label_loading_searching_tasks.setHidden(True)
            self.gif_loading_scan.stop()
            self.label_log_run_one_task.setHidden(False)
            mymodules.DisplayMessageLogUI(self.label_log_run_one_task,
                                          f"No smartphones detected!!! PhoneBot didn't detect any smartphones connected to your computer.",
                                          "Red", self.current_tab)

            mymodules.PopupMessage("ERROR : No smartphones detected!!!",
                                   "PhoneBot didn't detect any smartphones connected to your computer.")

            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.HideLoadingsTabRunCampaign(True)
            self.TabRunOneTask_HideSelectSmartphoneBrowser(True)
            self.HideButtonsRunOneTask(True)

        if obj == "The scan of smartphones is done from tab 'Run'.":
            logger.info("FINISHED => The scan of smartphones is done from tab 'Run'.")
            self.gif_loading_smartphones.stop()  # <---- +++
            # <---- +++
            self.HideAllQElements(False)
            self.label_loading_scan_smartphones.setHidden(True)
            """
            self.line.setHidden(False)
            self.label_logo.setHidden(False)

            self.button_OpenLogFile.setHidden(False)
            """

            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.HideLoadingsTabRunCampaign(True)

        if obj == "The Tab Settings is ready":
            logger.info("FINISHED => The Tab Settings is ready")
            self.gif_loading.stop()
            self.gif_loading_settings_usb_debugging.stop()
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(3, True)
            self.ChangeColorsNecessarySoftwares(self.java, self.node, self.android, self.appium, self.tesseract, \
                                                self.sdkmanager, self.build_tools)
            # <---- +++
            self.HideAllQElements(False)
            self.label_loading_scan_smartphones.setHidden(True)
            self.label_loading_settings_usb_debugging.setHidden(True)
            self.HideLoadingsTabRunOneTask(True)
            self.HideLoadingsTabSettings(True)
            self.HideButtonsRunOneTask(True)
            self.HideSelectDeviceAndBrowser(True)
            self.TabRunOneTask_HideSelectSmartphoneBrowser(True)
            self.tabWidget.setCurrentIndex(2)

        if obj == "Task is done":
            logger.info("FINISHED => Task is done")
            self.HideButtonsRunOneTask(False)

            self.TabRunOneTask_Enable_1_2(True)
            self.label_log_run_one_task.setHidden(True)
            self.label_4_see_results_tab_run_one_task.setHidden(False)
            self.button_Report_2.setHidden(False)
            self.button_OpenLogFile_2.setHidden(False)
            # FINAL PART => OPEN REPORT PAGE
            mymodules.DisplayMessageLogUI(self.label_log_run_one_task,
                                          f"Congratulations!!! The task was accomplished succesfully! PhoneBot will open the report in your browser.",
                                          "Green", self.current_tab)
            """
            mymodules.PopupMessage("Congratulations!",
                                   "The task was accomplished succesfully! PhoneBot will open the report in your browser.")
            mymodules.UpdateMysqlDB(self.user_id)
            webbrowser.open(f'https://dashboard.phonebot.co/task_user_report/{self.taskuser_id}/view', new=2)
            """
            self.HideLoadingsTabRunCampaign(True)
            self.HideLoadingsTabSettings(True)
            self.TabRunOneTask_Enable_1_2(True)
            self.TabRunOneTask_ShowHideTasksButtons('show')

    def thread_complete(self, val='finished'):
        logger.info(f'def thread_complete(self, obj): {val}')

    def progress_fn(self, val):
        logger.info(f'def progress_fn(self, obj): {val}')
    # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == '__main__':
    mymodules.CheckUpdates(__version__)

    # === We make the config file =======================================
    mymodules.MakeConfiginifile()

    # ============================================================================================================
    # ============================ CREATE THE DATABASE SQLITE IF NECESSARY =======================================
    # ============================================================================================================
    import os.path

    PATHSQLFILE = mymodules.LoadFile('create_db.sql')
    if not os.path.isfile(mymodules.LoadFile('db.db')):
        if os.path.isfile(mymodules.LoadFile('create_db.sql')):

            PATHDB = mymodules.LoadFile('db.db')
            logger.info(f"PATHDB : {PATHDB}")
            logger.info(f"PATHSQLFILE : {PATHSQLFILE}")
        else:
            logger.error("PhoneBot didn't find db.db and neither create_db.sql! It will stop.")
            mymodules.PopupMessage("Error db.db!",
                                   "PhoneBot didn't find db.db and neither create_db.sql! It will stop.")
            sys.exit(0, "Error db.db!")
    else:
        PATHDB = mymodules.LoadFile('db.db')
        logger.info(f"PATHDB : {PATHDB}")

    if os.path.isfile(PATHDB):
        # size of db
        size_db = os.path.getsize(mymodules.LoadFile('db.db'))
        print(size_db)

        if size_db != 0:
            logger.info("PhoneBot found your database 'db.db'. It will not create a new one.")
            # if os.path.isfile(mymodules.LoadFile(PATHSQLFILE)):
            # os.remove(mymodules.LoadFile(PATHSQLFILE))
            # logger.info(f"PhoneBot remove {PATHSQLFILE} file.")
        else:
            logger.info(f"PhoneBot found db.db but it was O Kb, so it will create the db from file {PATHSQLFILE}")
            if os.path.isfile(PATHSQLFILE) and os.access(PATHSQLFILE, os.R_OK):
                logger.info("PhoneBot will create new db now.")
                mymodules.ExecuteSQLFromFile(PATHSQLFILE)
                # os.remove(PATHSQLFILE)


    else:

        logger.info(f"PhoneBot will create the db from file {PATHSQLFILE}")
        if os.path.isfile(PATHSQLFILE) and os.access(PATHSQLFILE, os.R_OK):
            logger.info("PhoneBot will create new db now.")
            mymodules.ExecuteSQLFromFile(PATHSQLFILE)
            # os.remove(PATHSQLFILE)

        else:
            logger.info(
                "Either the file 'create_db.sql' is missing or not readable or it is not the first time you use PhoneBot.")

    # Create table if not exist
    # TABLE tasks_user
    sql_create_tasks_user = """
CREATE TABLE IF NOT EXISTS tasks_user (
    id                           INT (11)      NOT NULL
                                               PRIMARY KEY,
    enable                       INT (11)      DEFAULT NULL,
    id_task                      INT (11)      NOT NULL,
    id_campaign                  INT (11)      NOT NULL,
    url_keywords                 VARCHAR (300) DEFAULT NULL,
    minimum                      INT (12)      DEFAULT NULL,
    url_list                     VARCHAR (300) DEFAULT NULL,
    url_usernames                VARCHAR (300) DEFAULT NULL,
    message_txt_invitation_1B    TEXT,
    message_txt_1A               TEXT,
    message_txt_2A               TEXT,
    message_txt_3A               TEXT,
    message_txt_4A               TEXT,
    message_voice_1A             TEXT,
    message_voice_2A             TEXT,
    message_voice_3A             TEXT,
    message_voice_4A             TEXT,
    message_txt_invitation_1A    TEXT,
    message_txt_1B               TEXT,
    message_txt_2B               TEXT,
    message_txt_3B               TEXT,
    message_txt_4B               TEXT,
    message_voice_1B             TEXT,
    message_voice_2B             TEXT,
    message_voice_3B             TEXT,
    message_voice_4B             TEXT,
    date_counter_test_AB         DATETIME      DEFAULT NULL,
    time_delay_1A                INT (11)      DEFAULT NULL,
    time_delay_1A_type           VARCHAR (10)  DEFAULT NULL,
    time_delay_2A                INT (11)      DEFAULT NULL,
    time_delay_2A_type           VARCHAR (10)  DEFAULT NULL,
    time_delay_3A                INT (11)      DEFAULT NULL,
    time_delay_3A_type           VARCHAR (10)  DEFAULT NULL,
    time_delay_1B                INT (11)      DEFAULT NULL,
    time_delay_1B_type           VARCHAR (10)  DEFAULT NULL,
    time_delay_2B                INT (11)      DEFAULT NULL,
    time_delay_2B_type           VARCHAR (10)  DEFAULT NULL,
    time_delay_3B                INT (11)      DEFAULT NULL,
    time_delay_3B_type           VARCHAR (10)  DEFAULT NULL,
    message_1A_choice            VARCHAR (11)  DEFAULT NULL,
    message_2A_choice            VARCHAR (11)  DEFAULT NULL,
    message_3A_choice            VARCHAR (11)  DEFAULT NULL,
    message_4A_choice            VARCHAR (11)  DEFAULT NULL,
    message_1B_choice            VARCHAR (11)  DEFAULT NULL,
    message_2B_choice            VARCHAR (11)  DEFAULT NULL,
    message_3B_choice            VARCHAR (11)  DEFAULT NULL,
    message_4B_choice            VARCHAR (11)  DEFAULT NULL,
    AB_testing_enable            INT (11)      DEFAULT NULL,
    AB_testing_enable_invitation INT (11)      DEFAULT NULL,
    date_AB_testing              DATETIME      DEFAULT NULL,
    date_AB_testing_invitation   DATETIME      DEFAULT NULL,
    serie_type                   VARCHAR (20)  DEFAULT NULL,
    daily_limit                  INT (11)      DEFAULT NULL
);
"""
    mymodules.CreateTable(sql_create_tasks_user)
    # We need to create the new columns of version 0.003
    mymodules.AddColumn('sqlite', 'settings', 'java_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'node_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'android_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'appium_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'tesseract_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'sdkmanager_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'build_tools_ok', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'user_id', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'product_id', 'int(11)')
    mymodules.AddColumn('sqlite', 'settings', 'subscription_id', 'int(11)')
    mymodules.AddColumn('sqlite', 'smartphones', 'missing_packages', 'varchar(500)')

    mymodules.AddColumn('sqlite', 'settings', 'tracking_code_affiliate', 'varchar(50)')
    mymodules.AddColumn('sqlite', 'settings', 'coupon_affiliate', 'varchar(50)')
    mymodules.AddColumn('sqlite', 'settings', 'url_affiliate', 'varchar(200)')
    mymodules.AddColumn('sqlite', 'settings', 'user_email', 'varchar(75)')
    mymodules.AddColumn('sqlite', 'settings', 'license', 'varchar(30)')
    mymodules.AddColumn('sqlite', 'social_accounts', 'id_pc', 'varchar(30)')
    mymodules.AddColumn('sqlite', 'social_accounts', 'password', 'varchar(500)')
    mymodules.AddColumn('sqlite', 'social_accounts', 'browser', 'varchar(20)')
    mymodules.AddColumn('sqlite', 'social_accounts', 'status', 'int(11)')

    mymodules.AddColumn('sqlite', 'contacts', 'id_task_user', 'int(11)')

    mymodules.AddColumn('sqlite', 'actions', 'id_task_user', 'int(11)')
    mymodules.AddColumn('sqlite', 'contacts', 'replied', 'int(11)')
    mymodules.AddColumn('sqlite', 'contacts', 'replied_invitation', 'int(11)')
    mymodules.AddColumn('sqlite', 'actions', 'replied', 'int(11)')
    mymodules.AddColumn('sqlite', 'actions', 'replied_invitation', 'int(11)')
    mymodules.AddColumn('sqlite', 'actions', 'id_message', 'STRING')
    mymodules.AddColumn('sqlite', 'actions', 'date_created', 'DATETIME')
    mymodules.AddColumn('sqlite', 'contacts', 'date_created', 'DATETIME')
    mymodules.AddColumn('sqlite', 'actions', 'date_update', 'DATETIME')
    mymodules.AddColumn('sqlite', 'contacts', 'date_update', 'DATETIME')
    mymodules.AddColumn('sqlite', 'tasks_user', 'smartphone_allowed', 'int(1)')
    mymodules.AddColumn('sqlite', 'tasks_user', 'computer_allowed', 'int(1)')

    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'id_task_user', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'id_task_user', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_contacts', 'replied', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_contacts', 'replied_invitation', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'replied', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'replied_invitation', 'int(11)')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'id_message', 'STRING')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'date_created', 'DATETIME')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_contacts', 'date_created', 'DATETIME')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_actions', 'date_update', 'DATETIME')
    mymodules.AddColumn('mysql', 'W551je5v_phonebot_contacts', 'date_update', 'DATETIME')

    # AS MANY STAGIAIRES CREATED NEW COLUMNS IN TABLES actions & contacts, WE MAY NEED TO ADD NEW COLUMNS IN MYSQL TABLES
    mymodules.AddMissingColumnstoMysql()

    'sdkmanager_ok=?, build_tools_ok=?'

    # ============================================================================================================
    # ============================ We need to kill previous PhoneBot.exe opened. =================================
    # =========================== This can happen when we installed the software =================================
    # ============================================================================================================

    mymodules.KillPhoneBot()
    # ============================================================================================================

    # =============================================================================================================
    # ============================= SEND THE LOG TO OUR SUPPORT TEAM FOR DEBUGGING ================================
    # =============================================================================================================
    # === We send the log file to Admin =======================================
    # mymodules.SendLogFile()

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
