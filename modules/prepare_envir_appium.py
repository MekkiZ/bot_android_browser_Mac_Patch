# encoding: utf-8

"""
This script was reviewed by Alexis Lafaye
contact : lafaye.alexis@gmail.com
"""

import configparser
import distutils.spawn
import glob
import logging
import pdb
import shutil
import sqlite3
import time
from ftplib import FTP
import os
import sys
import wget
from os import path
from os.path import expanduser
import platform
import zipfile
import subprocess
from subprocess import PIPE, STDOUT
import modules.mymodulesteam as mymodules

# --- We prepare the logging --- #####################################################################
# from pathtub import ensure, clean, add_to_path

logger = logging.getLogger('__prepare_env_appium__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


#####################################++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''):  # b'\n'-separated lines
        logging.info('got line from subprocess: %r', line)


def ChangePathInDB(name, value):
    sqliteConnection = sqlite3.connect(mymodules.LoadFile('db.db'))
    cursor = sqliteConnection.cursor()

    cursor.execute("UPDATE settings set " + name + "=?", (value,))
    sqliteConnection.commit()
    logger.info(f"PhoneBot added '{name} = {value}' in local database.")

    if cursor:
        cursor.close()
    if sqliteConnection:
        sqliteConnection.close()


# https://stackoverflow.com/questions/21138014/how-to-add-to-and-remove-from-systems-environment-variable-path
import ctypes
import os
import sys

unicode = str

if platform.system() == 'Windows':
    print(f"platform.system() : {platform.system()}")
    print('We enter in Windows system algorithm')
    from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPVOID

    LRESULT = LPARAM  # synonymous
    import winreg


    class Environment(object):
        path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        hklm = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(hklm, path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
        SendMessage = ctypes.windll.user32.SendMessageW
        SendMessage.argtypes = HWND, UINT, WPARAM, LPVOID
        SendMessage.restype = LRESULT
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        NO_DEFAULT_PROVIDED = object()

        def get(self, name, default=NO_DEFAULT_PROVIDED):
            try:
                value = winreg.QueryValueEx(self.key, name)[0]
            except WindowsError:
                if default is self.NO_DEFAULT_PROVIDED:
                    raise ValueError("No such registry key", name)
                value = default
            return value

        def set(self, name, value):
            if value:
                winreg.SetValueEx(self.key, name, 0, winreg.REG_EXPAND_SZ, value)
            else:
                winreg.DeleteValue(self.key, name)
            self.notify()

        def notify(self):
            self.SendMessage(self.HWND_BROADCAST, self.WM_SETTINGCHANGE, 0, u'Environment')


    class EnvironmentUser(object):
        path = r'Environment'
        hklm = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(hklm, path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
        SendMessage = ctypes.windll.user32.SendMessageW
        SendMessage.argtypes = HWND, UINT, WPARAM, LPVOID
        SendMessage.restype = LRESULT
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        NO_DEFAULT_PROVIDED = object()

        def get(self, name, default=NO_DEFAULT_PROVIDED):
            try:
                value = winreg.QueryValueEx(self.key, name)[0]
            except WindowsError:
                if default is self.NO_DEFAULT_PROVIDED:
                    raise ValueError("No such registry key", name)
                value = default
            return value

        def set(self, name, value):
            if value:
                winreg.SetValueEx(self.key, name, 0, winreg.REG_EXPAND_SZ, value)
            else:
                winreg.DeleteValue(self.key, name)
            self.notify()

        def notify(self):
            self.SendMessage(self.HWND_BROADCAST, self.WM_SETTINGCHANGE, 0, u'Environment')


    Environment = Environment()  # singletion - create instance
    EnvironmentUser = EnvironmentUser()
    PATH_VAR = 'PATH'


    def append_path_envvar(addpath):
        def canonical(path):
            path = unicode(path.upper().rstrip(os.sep))
            return winreg.ExpandEnvironmentStrings(path)  # Requires Python 2.6+

        canpath = canonical(addpath)

        curpath = Environment.get(PATH_VAR, '')

        if not any(canpath == subpath
                   for subpath in canonical(curpath).split(os.pathsep)):
            Environment.set(PATH_VAR, os.pathsep.join((curpath, addpath)))


    def remove_envvar_path(folder):
        """ Remove *all* paths in PATH_VAR that contain the folder path. """

        curpath = Environment.get(PATH_VAR, '')

        folder = folder.upper()
        keepers = [subpath for subpath in curpath.split(os.pathsep)
                   if folder not in subpath.upper()]
        print(f"Set system: {folder}, {os.pathsep.join(keepers)}")
        #Environment.set(PATH_VAR, os.pathsep.join(keepers))
        ChangeEnvVarSys(PATH_VAR, os.pathsep.join(keepers))


    def remove_envvar_path_user(folder):
        """ Remove *all* paths in PATH_VAR that contain the folder path. """

        curpath = EnvironmentUser.get(PATH_VAR, '')

        folder = folder.upper()
        keepers = [subpath for subpath in curpath.split(os.pathsep)
                   if folder not in subpath.upper()]
        print(f"Set user: {folder}, {os.pathsep.join(keepers)}")
        #EnvironmentUser.set(PATH_VAR, os.pathsep.join(keepers))
        ChangeEnvVarUser(PATH_VAR, os.pathsep.join(keepers))


    def ChangePathInDB(name, value):
        sqliteConnection = sqlite3.connect(mymodules.LoadFile('db.db'))
        cursor = sqliteConnection.cursor()

        cursor.execute("UPDATE settings set " + name + "=?", (value,))
        sqliteConnection.commit()
        logger.info(f"PhoneBot added '{name} = {value}' in local database.")

        if cursor:
            cursor.close()
        if sqliteConnection:
            sqliteConnection.close()


    def RemoveFilesandFolder():
        logger.info(
            "=====================================================================================================")
        logger.info(
            "================================ Start RemoveFilesandFolder =========================================")
        logger.info(
            "=====================================================================================================")
        if path.isdir('android_tools_folder'):
            shutil.rmtree('android_tools_folder')
        if path.isfile('android_tool.zip'):
            os.remove("android_tool.zip")
        if path.isfile('java_install.exe'):
            os.remove("java_install.exe")
        if path.isfile('tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe'):
            os.remove("tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe")
        if path.isfile('node_install.msi'):
            os.remove("node_install.msi")
        if path.isfile('commandlinetools-win-6200805_latest.zip'):
            os.remove("commandlinetools-win-6200805_latest.zip")


    def ChangeEnvVarSys(name, value):
        logger.info(
            f"========================== START ChangeEnvVarSys {name} - {value}===================================================")
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"System\CurrentControlSet\Control\Session Manager\Environment")
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                          r"System\CurrentControlSet\Control\Session Manager\Environment", 0,
                                          winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False


    def GetEnvVarSys(name):
        logger.info(
            f"========================== START GetEnvVarSys {name} ===================================================")
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                          r"System\CurrentControlSet\Control\Session Manager\Environment", 0,
                                          winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            logger.info(
                f"========================== value: {value} ===================================================")
            return value
        except WindowsError:
            return None


    def ChangeEnvVarUser(name, value):
        logger.info(
            f"========================== START ChangeEnvVarUser {name} - {value}===================================================")
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0,
                                          winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False


    def GetEnvVarUser(name):
        logger.info(
            f"========================== START GetEnvVarUser {name} ===================================================")
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0,
                                          winreg.KEY_READ)
            value, regtype = winreg.QueryValueEx(registry_key, name)
            winreg.CloseKey(registry_key)
            logger.info(
                f"========================== value: {value} ===================================================")
            return value
        except WindowsError:
            return None


    def check_envrionment(java, node, android, appium, tesseract, sdkmanager, build_tools, version_build_tools):
        logger.info(
            "=====================================================================================================")
        logger.info(
            "================================== Start check_envrionment ==========================================")
        logger.info(
            "=====================================================================================================")

        logger.info("First of all, PhoneBot will check the PATHEXT values.")
        pathtext_sys = str(GetEnvVarSys('PATHEXT'))
        logger.info(f"pathtext_sys : {pathtext_sys}")

        pathtext_user = str(GetEnvVarUser('PATHEXT'))
        logger.info(f"pathtext_user : {pathtext_user}")

        if pathtext_sys.find('.CMD') == -1:
            pathtext_sys += ';.CMD'
            ChangeEnvVarSys('PATHEXT', pathtext_sys)

        if pathtext_user.find('.CMD') == -1:
            pathtext_user += ';.CMD'
            ChangeEnvVarUser('PATHEXT', pathtext_user)

        if pathtext_sys.find('.EXE') == -1:
            pathtext_sys += ';.EXE'
            ChangeEnvVarSys('PATHEXT', pathtext_sys)

        if pathtext_user.find('.EXE') == -1:
            pathtext_user += ';.EXE'
            ChangeEnvVarUser('PATHEXT', pathtext_user)

        if pathtext_sys.find('.BAT') == -1:
            pathtext_sys += ';.BAT'
            ChangeEnvVarSys('PATHEXT', pathtext_sys)

        if pathtext_user.find('.BAT') == -1:
            pathtext_user += ';.BAT'
            ChangeEnvVarUser('PATHEXT', pathtext_user)

        if pathtext_sys.find('.JS') == -1:
            pathtext_sys += ';.JS'
            ChangeEnvVarSys('PATHEXT', pathtext_sys)

        if pathtext_user.find('.JS') == -1:
            pathtext_user += ';.JS'
            ChangeEnvVarUser('PATHEXT', pathtext_user)

        logger.info("*" * 100)
        pathtext_sys = str(GetEnvVarSys('PATHEXT'))
        logger.info(f"pathtext_sys : {pathtext_sys}")

        pathtext_user = str(GetEnvVarUser('PATHEXT'))
        logger.info(f"pathtext_user : {pathtext_user}")

        # ===============================================================================================================

        C_program_folder = os.environ['PROGRAMFILES']
        common_files_folder = os.environ['COMMONPROGRAMFILES']
        home_user = expanduser("~")
        home_user_mac=os.path.expanduser('~')
        AppData_Local_folder = home_user + '\\AppData\\Local'
        AppData_Local_folder_Android = AppData_Local_folder + "\\Android"
        Folder_abd_osx = home_user_mac + "/Android/platform-tools/" #rajout

        platform_architecture = platform.architecture()[0]
        Path = os.getenv('Path')
        env_var_changed = False

        # =====================================================================================
        #                                     ANDROID_HOME
        # We will imediatly check existencce or create the folder C:\Users\your_username\AppData\Local\Android\cmdline-tools
        # and add the environment variable ANDROID_HOME
        # =====================================================================================
        logger.info("Checking ANDROID_HOME. Please wait..................")
        ANDROID_HOME_VALUE = home_user + '\\AppData\\Local\\Android'
        if os.path.isdir(ANDROID_HOME_VALUE):
            logger.info(f"PhoneBot found the folder {ANDROID_HOME_VALUE}.")
            logger.info(f" ==> ANDROID_HOME_VALUE : {ANDROID_HOME_VALUE} <==")
            if GetEnvVarUser("ANDROID_HOME") != ANDROID_HOME_VALUE:
                logger.info("PhoneBot will change ANDROID_HOME user.")
                ChangeEnvVarUser("ANDROID_HOME", ANDROID_HOME_VALUE)
                os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                env_var_changed = True
            else:
                logger.info("ANDROID_HOME user is fine.")

            if GetEnvVarSys("ANDROID_HOME") != ANDROID_HOME_VALUE:
                logger.info("PhoneBot will change ANDROID_HOME system.")
                ChangeEnvVarSys("ANDROID_HOME", ANDROID_HOME_VALUE)
                os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                env_var_changed = True
            else:
                logger.info("ANDROID_HOME system is fine.")
        else:
            logger.info(f"The folder {ANDROID_HOME_VALUE} doesn't exist. PhoneBot will create it.")
            os.mkdir(ANDROID_HOME_VALUE)
            if os.path.isdir(ANDROID_HOME_VALUE):
                logger.info(f"PhoneBot found the folder {ANDROID_HOME_VALUE}.")
                logger.info(f" ==> ANDROID_HOME_VALUE : {ANDROID_HOME_VALUE} <==")
                if GetEnvVarUser("ANDROID_HOME") != ANDROID_HOME_VALUE:
                    logger.info("PhoneBot will change ANDROID_HOME user.")
                    ChangeEnvVarUser("ANDROID_HOME", ANDROID_HOME_VALUE)
                    os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                    env_var_changed = True
                else:
                    logger.info("ANDROID_HOME user is fine.")

                if GetEnvVarSys("ANDROID_HOME") != ANDROID_HOME_VALUE:
                    logger.info("PhoneBot will change ANDROID_HOME system.")
                    ChangeEnvVarSys("ANDROID_HOME", ANDROID_HOME_VALUE)
                    os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                    env_var_changed = True
                else:
                    logger.info("ANDROID_HOME system is fine.")

        print('\n' * 2)

        # =====================================================================================
        #                                     JAVA
        # java.exe
        # C:\Program Files\Java\jre1.8.0_241
        # C:\Program Files (x86)\Java\jre1.8.0_241
        # =====================================================================================
        # JAVA_HOME = C:\Program Files\Java\jre1.8.0_241
        logger.info("Checking Java. Please wait..................")
        print(f"home_user : {home_user}")

        if mymodules.TestIfInstalled("java --version"):
            logger.info("Java is installed!")
            java = True
        else:
            java_exist = os.path.isdir(C_program_folder + "\\Java") or os.path.isdir(common_files_folder + "\\Oracle\\Java\\javapath")
            java_folder_found = False
            if java_exist:
                if os.path.isdir(C_program_folder + "\\Java"):
                    java_folder_tmp = C_program_folder + "\\Java"
                    logger.info(
                        f"PhoneBot found the folder {java_folder_tmp}. It will search for 'java.exe' from {java_folder_tmp}. Please be patient......")
                    java_file = glob.glob(java_folder_tmp + "\\**\\java.exe", recursive=True)
                    if java_file:
                        ChangePathInDB('java', java_file[0])
                        java_folder = str(java_file[0]).replace('java.exe', '')
                        if java_folder[len(java_folder) - 1] == '\\':
                            java_folder = java_folder[0:len(java_folder) - 1]
                            print(f"New java_folder without the '\\' : {java_folder}")
                        # We need to be sure it is Java8 minimum
                        # position of jre folder:
                        pos_jre1 = java_folder.find('jre1.')
                        pos_jre = java_folder.find('jre-')
                        pos_jdk = java_folder.find('jdk-')
                        print(f"pos_jre : {pos_jre1}")
                        if pos_jre1 != -1:
                            tmp_string = java_folder[pos_jre1 + 5:]

                        elif pos_jre != -1:
                            tmp_string = java_folder[pos_jre + 4:]

                        elif pos_jdk != -1:
                            tmp_string = java_folder[pos_jdk + 4:]

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
                        if int(first_digit) > 3:
                            version_java = first_digit
                            print(f"version_java : {version_java}")
                        else:
                            version_java = numbers[0:2]
                            print(f"version_java : {version_java}")
                        if int(version_java) < 8:
                            java_folder_found = False
                            logger.critical("ERROR : Your version of Java is too old. Please update your Java.")
                            mymodules.PopupMessage("Error Java!",
                                                   "Your version of Java is too old. Please update your Java.")
                            sys.exit()

                        else:
                            java_folder_found = True




                    else:
                        logger.info(f"PhoneBot couldn't find 'java.exe' in {java_folder_tmp}.")
                        java_folder_found = False
                elif os.path.isdir(common_files_folder + "\\Oracle\\Java\\javapath") and os.path.isfile(f"{common_files_folder}\\Oracle\\Java\\javapath\\java.exe"):
                    if mymodules.TestIfInstalled(f"{common_files_folder}\\Oracle\\Java\\javapath\\java.exe --version"):
                        java_folder = common_files_folder + "\\Oracle\\Java\\javapath"
                        java_folder_found = True
                        ChangePathInDB('java', f"{common_files_folder}\\Oracle\\Java\\javapath\\java.exe")
            else:
                logger.info(f"PhoneBot couldn't find the folder '{C_program_folder}\\Java'.")
                java_folder_found = False

            if java_folder_found:
                logger.info(f"java_folder : {java_folder}")
                print(f"java_folder : {java_folder}")
                JAVA_HOME_VALUE = java_folder.replace('\\bin\\', '')
                JAVA_HOME_VALUE = java_folder.replace(r'\bin\\', '')
                JAVA_HOME_VALUE = java_folder.replace(r'\bin', '')
                JAVA_HOME_VALUE = java_folder.replace('\\bin', '')

                logger.info(f"JAVA_HOME_VALUE = {JAVA_HOME_VALUE}")
                logger.info(f"We found java.exe in folder {java_folder}. Let's check now the environment variable!")

                print(f"GetEnvVarUser('JAVA_HOME') : {GetEnvVarUser('JAVA_HOME')} =? {JAVA_HOME_VALUE} : JAVA_HOME_VALUE")
                if GetEnvVarUser("JAVA_HOME") != JAVA_HOME_VALUE:
                    logger.info("PhoneBot will change JAVA_HOME user.")
                    ChangeEnvVarUser("JAVA_HOME", JAVA_HOME_VALUE)
                    os.environ['JAVA_HOME'] = JAVA_HOME_VALUE

                    env_var_changed = True
                else:
                    logger.info("JAVA_HOME user is fine.")
                print(f"GetEnvVarSys('JAVA_HOME') : {GetEnvVarSys('JAVA_HOME')} =? {JAVA_HOME_VALUE} : JAVA_HOME_VALUE")
                if GetEnvVarSys("JAVA_HOME") != JAVA_HOME_VALUE:
                    logger.info("PhoneBot will change JAVA_HOME system.")
                    ChangeEnvVarSys("JAVA_HOME", JAVA_HOME_VALUE)
                    os.environ['JAVA_HOME'] = JAVA_HOME_VALUE
                    env_var_changed = True
                else:
                    logger.info("JAVA_HOME system is fine.")

                PATH_USER = str(GetEnvVarUser("PATH"))
                PATH_USER_list = PATH_USER.split(';')
                for each_path_user in PATH_USER_list:
                    # each_path_user= str(each_path_user).lower()
                    print(f"each_path_user : {each_path_user}")
                    if each_path_user.find('Java') != -1 and each_path_user != JAVA_HOME_VALUE:
                        remove_envvar_path_user(each_path_user)
                        logger.info(f"PhoneBot remove the environment variable '{each_path_user}'.")

                PATH_USER = str(GetEnvVarUser("PATH"))

                if PATH_USER.find(f"{JAVA_HOME_VALUE}\\bin") == -1:
                    logger.info("PhoneBot will change PATH user for JAVA.")
                    PATH_TO_ADD = str(PATH_USER + ';' + JAVA_HOME_VALUE + "\\bin").replace('PATH=', '').replace('Path=', '').replace(
                        'path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    os.environ['PATH'] = PATH_TO_ADD
                    env_var_changed = True

                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    PATH_SYS_list = PATH_SYS.split(';')
                    for each_path_sys in PATH_SYS_list:
                        # each_path_user= str(each_path_user).lower()
                        print(f"each_path_sys : {each_path_sys}")
                        if each_path_sys.find('Java') != -1 and each_path_sys != JAVA_HOME_VALUE:
                            remove_envvar_path(each_path_sys)
                            logger.info(f"PhoneBot remove the environment variable '{each_path_sys}'.")

                    PATH_SYS = str(GetEnvVarSys("PATH"))

                    if PATH_SYS.find(JAVA_HOME_VALUE + "\\bin") == -1:
                        logger.info("PhoneBot will change PATH system for JAVA.")
                        PATH_TO_ADD = str(PATH_USER + ';' + JAVA_HOME_VALUE + "\\bin").replace('PATH=', '').replace('Path=',
                                                                                                          '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD
                        env_var_changed = True
                        java = True
                    else:
                        logger.info("PATH system for JAVA is fine.")
                        java = True

                else:
                    logger.info("PATH user for JAVA is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(JAVA_HOME_VALUE + "\\bin") == -1:
                        logger.info("PhoneBot will change PATH system for JAVA.")
                        PATH_TO_ADD = str(PATH_USER + ';' + JAVA_HOME_VALUE + "\\bin").replace('PATH=', '').replace('Path=',
                                                                                                          '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD

                        env_var_changed = True
                        java = True
                    else:
                        logger.info("PATH system for JAVA is fine.")
                        java = True


            else:
                logger.critical(
                    "We didn't find java.exe. PhoneBot will try to install it. If it fails, you will have to install it yourself. Nothing complicated, you'll just have to download the appropriate program and install it. PhoneBot will guide you. But first, let PhoneBot try to install it itself please..")
                java = False

        print('\n' * 2)
        # =====================================================================================
        #                                NODE.js
        # node.exe
        # C:\Program Files\nodejs
        # C:\Program Files (x86)\nodejs
        # =====================================================================================
        logger.info("Checking NodeJS. Please wait..................")
        if mymodules.TestIfInstalled("node --version"):
            logger.info("Node is installed!")
            node = True
        else:
            node_exist = str(mymodules.GetPathFromDB('node'))
            if node_exist.find('nodejs') == -1:
                print("We didn't find node.exe in DB.")
                if os.path.isdir(C_program_folder + "\\nodejs"):
                    print("We found nodejs folder --------")
                    node_path_folder = C_program_folder + "\\nodejs"
                    logger.info(
                        f"PhoneBot didn't find node.exe. It will search from {node_path_folder}. Please be patient......")
                    node_file = glob.glob(node_path_folder + "\\**\\node.exe", recursive=True)

                    if node_file:
                        ChangePathInDB('node', node_file[0])
                        print("We found node.exe method 1.1")
                        node_folder = str(node_file[0]).replace('node.exe', '')
                        node_folder_found = True
                        if node_folder[len(node_folder) - 1] == '\\':
                            node_folder = node_folder[0:len(node_folder) - 1]
                            print(f"New node_folder without the '\\' : {node_folder}")
                    else:
                        if str(C_program_folder).find('86') == -1:
                            C_program_folder = 'C:\Program Files'
                        else:
                            C_program_folder = 'C:\Program Files (x86)'

                        node_file = glob.glob(C_program_folder + "\\**\\node.exe", recursive=True)
                        if node_file:
                            if str(node_file).find('nodejs') != -1:
                                ChangePathInDB('node', node_file)
                                node_folder = str(node_file).replace('node.exe', '')
                                node_folder_found = True
                                if node_folder[len(node_folder) - 1] == '\\':
                                    node_folder = node_folder[0:len(node_folder) - 1]
                                    print(f"New node_folder without the '\\' : {node_folder}")
                            else:
                                print("We didn't find node.exe method 2")
                                node_folder_found = False
                        else:
                            print("We didn't find node.exe method 2")
                            node_folder_found = False
                else:
                    if str(C_program_folder).find('86') == -1:
                        C_program_folder = 'C:\Program Files'
                    else:
                        C_program_folder = 'C:\Program Files (x86)'
                    node_path_folder = C_program_folder + "\\nodejs"
                    logger.info(
                        f"PhoneBot didn't find node.exe. It will search from {C_program_folder}. Please be patient......")
                    node_file = glob.glob(C_program_folder + "\\**\\node.exe", recursive=True)
                    if node_file:
                        if str(node_file).find('nodejs') != -1:
                            ChangePathInDB('node', node_file[0])
                            print("We found node.exe method 2")
                            node_folder = str(node_file[0]).replace('node.exe', '')
                            node_folder_found = True
                            if node_folder[len(node_folder) - 1] == '\\':
                                node_folder = node_folder[0:len(node_folder) - 1]
                                print(f"New node_folder without the '\\' : {node_folder}")
                        else:
                            print("We didn't find node.exe method 3")
                            node_folder_found = False
                    else:
                        print("We didn't find node.exe method 3")
                        node_folder_found = False
            else:
                node_folder = str(node_exist).replace(r'\node.exe', '')
                node_folder_found = True

            if node_folder_found:
                logger.info(f"node_folder : {node_folder}")
                logger.info(f"We found node.exe in folder {node_folder}. Let's check now the environment variable!")
                NODE_FOLDER_VALUE = node_folder

                PATH_USER = str(GetEnvVarUser("PATH"))
                if PATH_USER.find(NODE_FOLDER_VALUE) == -1:
                    logger.info("PhoneBot will change PATH user for NODE.")
                    PATH_TO_ADD = str(PATH_USER + ';' + NODE_FOLDER_VALUE).replace('PATH=', '').replace('Path=',
                                                                                                        '').replace(
                        'path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    env_var_changed = True

                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(NODE_FOLDER_VALUE) == -1:
                        logger.info("PhoneBot will change PATH system for NODE.")
                        PATH_TO_ADD = str(PATH_USER + ';' + NODE_FOLDER_VALUE).replace('PATH=', '').replace('Path=',
                                                                                                            '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        env_var_changed = True
                        node = True
                    else:
                        logger.info("PATH system for NODE is fine.")
                        node = True

                else:
                    logger.info("PATH user for NODE is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(NODE_FOLDER_VALUE) == -1:
                        logger.info("PhoneBot will change PATH system for NODE.")
                        PATH_TO_ADD = str(PATH_USER + ';' + NODE_FOLDER_VALUE).replace('PATH=', '').replace('Path=',
                                                                                                            '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        env_var_changed = True
                        node = True
                    else:
                        logger.info("PATH system for NODE is fine.")
                        node = True






            else:
                logger.critical(
                    "We didn't find node.exe. PhoneBot will try to install it. If it fails, you will have to install it yourself. Nothing complicated, you'll just have to download the appropriate program and install it. PhoneBot will guide you. But first, let PhoneBot try to install it itself please..")
                node = False

        print('\n' * 2)
        # =====================================================================================
        #                                ANDROID SDK MANAGER(sdkmanager.bat)
        # =====================================================================================

        # --- To know the path of sdkmanager.bat folder

        logger.info("Checking Sdkmanager. Please wait..................")

        if mymodules.TestIfInstalled("sdkmanager --version"):
            logger.info("sdkmanager is installed!")
            sdkmanager = True
        else:
            sdkmanager_exist = mymodules.GetPathFromDB('sdkmanager')
            if not sdkmanager_exist:

                if os.path.isdir(AppData_Local_folder_Android):
                    logger.info(f"Good news! PhoneBot find {AppData_Local_folder_Android}")
                    logger.info(
                        f"PhoneBot will search sdkmanager.bat from {AppData_Local_folder_Android}. Please be patient......")
                    sdkmanager_file = glob.glob(AppData_Local_folder_Android + "\\**\\latest\\bin\\sdkmanager.bat",
                                                recursive=True)

                    if sdkmanager_file:
                        ChangePathInDB('sdkmanager', sdkmanager_file[0])
                        logger.info("PhoneBot found sdkmanager.bat")
                        sdkmanager_folder = str(sdkmanager_file[0]).replace('sdkmanager.bat', '')
                        sdkmanager_folder_found = True
                        if sdkmanager_folder[len(sdkmanager_folder) - 1] == '\\':
                            sdkmanager_folder = sdkmanager_folder[0:len(sdkmanager_folder) - 1]
                            logger.info(f"New sdkmanager_folder without the '\\' : {sdkmanager_folder}")
                    else:
                        sdkmanager_file = glob.glob(AppData_Local_folder_Android + "\\**\\tools\\sdkmanager.bat",
                                                    recursive=True)

                        if sdkmanager_file:
                            ChangePathInDB('sdkmanager', sdkmanager_file[0])
                            logger.info("PhoneBot found sdkmanager.bat")
                            sdkmanager_folder = str(sdkmanager_file[0]).replace('sdkmanager.bat', '')
                            sdkmanager_folder_found = True
                            if sdkmanager_folder[len(sdkmanager_folder) - 1] == '\\':
                                sdkmanager_folder = sdkmanager_folder[0:len(sdkmanager_folder) - 1]
                                logger.info(f"New sdkmanager_folder without the '\\' : {sdkmanager_folder}")



                        else:

                            sdkmanager_file = glob.glob(AppData_Local_folder_Android + "\\**\\sdkmanager.bat",
                                                        recursive=True)

                            if sdkmanager_file:
                                ChangePathInDB('sdkmanager', sdkmanager_file[0])
                                logger.info("PhoneBot found sdkmanager.bat")
                                sdkmanager_folder = str(sdkmanager_file[0]).replace('sdkmanager.bat', '')
                                sdkmanager_folder_found = True
                                if sdkmanager_folder[len(sdkmanager_folder) - 1] == '\\':
                                    sdkmanager_folder = sdkmanager_folder[0:len(sdkmanager_folder) - 1]
                                    logger.info(f"New sdkmanager_folder without the '\\' : {sdkmanager_folder}")

                            else:
                                sdkmanager_folder_found = False
                                logger.info("PhoneBot didn't find sdkmanager.bat")
                else:
                    sdkmanager_folder_found = False
                    logger.info(
                        f"PhoneBot didn't find  {AppData_Local_folder_Android}. So it is useless to go further. PhoneBot will try to install sdkmanager.")

            else:
                sdkmanager_folder = str(sdkmanager_exist).replace(r'\sdkmanager.bat', '')
                sdkmanager_folder_found = True

            if sdkmanager_folder_found:
                logger.info(f"sdkmanager_folder : {sdkmanager_folder}")

                sdkmanager_folder = sdkmanager_folder.replace('\\sdkmanager.bat\\', '')
                sdkmanager_folder = sdkmanager_folder.replace(r'\sdkmanager.bat\\', '')
                sdkmanager_folder = sdkmanager_folder.replace(r'\sdkmanager.bat', '')
                sdkmanager_folder = sdkmanager_folder.replace('\\sdkmanager.bat', '')
                logger.info(f" ==> sdkmanager_folder : {sdkmanager_folder} <==")

                PATH_USER = str(GetEnvVarUser("PATH"))
                if PATH_USER.find(sdkmanager_folder) == -1:
                    logger.info("PhoneBot will change PATH user for SDKMANAGER.")
                    PATH_TO_ADD = str(PATH_USER + ';' + sdkmanager_folder).replace('PATH=', '').replace('Path=',
                                                                                                        '').replace(
                        'path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    env_var_changed = True

                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(sdkmanager_folder) == -1:
                        logger.info("PhoneBot will change PATH system for SDKMANAGER.")
                        PATH_TO_ADD = str(PATH_USER + ';' + sdkmanager_folder).replace('PATH=', '').replace('Path=',
                                                                                                            '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        env_var_changed = True
                        sdkmanager = True
                    else:
                        logger.info("PATH system for SDKMANAGER is fine.")
                        sdkmanager = True

                else:
                    logger.info("PATH user for SDKMANAGER is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(sdkmanager_folder) == -1:
                        logger.info("PhoneBot will change PATH system for SDKMANAGER.")
                        PATH_TO_ADD = str(PATH_USER + ';' + sdkmanager_folder).replace('PATH=', '').replace('Path=',
                                                                                                            '').replace(
                            'path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        env_var_changed = True
                        sdkmanager = True
                    else:
                        logger.info("PATH system for SDKMANAGER is fine.")
                        sdkmanager = True

            else:
                logger.critical(
                    "We didn't find sdkmanager.bat. PhoneBot will try to install it. If it fails, you will have to install it yourself. But first, let PhoneBot try to install it itself please..")
                sdkmanager = False

        print('\n' * 2)

        # =====================================================================================
        #                                ANDROID build-tools folder
        # =====================================================================================

        # --- To know the path of build-tools folder
        logger.info("Checking SDK build-tools. Please wait..................")

        build_tools_exist = mymodules.GetPathFromDB('build_tools')
        if not build_tools_exist:
            if os.path.isdir(AppData_Local_folder_Android):
                logger.info(f"Good news! PhoneBot find {AppData_Local_folder_Android}")
                logger.info(
                    f"PhoneBot will search SDK build-tools from {AppData_Local_folder_Android}. Please be patient......")
                build_tools_folder = glob.glob(AppData_Local_folder_Android + "\\**\\build-tools", recursive=True)
                if build_tools_folder:
                    ChangePathInDB('build_tools', build_tools_folder[0])
                    build_tools_folder = build_tools_folder[0]
                    print(f"build_tools_folder : {build_tools_folder}")
                    build_tools_folder_found = True
                else:
                    logger.info(f"PhoneBot couldn't find 'build-tools' folder in {AppData_Local_folder_Android}")
                    build_tools_folder_found = False
            else:
                build_tools_folder_found = False
                logger.info(
                    f"PhoneBot didn't find sdkmanager in {AppData_Local_folder_Android}. So it is useless to go further. PhoneBot will try to install sdkmanager.")
        else:
            build_tools_folder = build_tools_exist
            build_tools_folder_found = True

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!BE CAREFULL HERE, WE HAVE THE SUBFOLDER 30.0.0-rc2 WHICH DEPENDS!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!OF BUILD-TOOLS VERSION !!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        build_tools_folder_to_be_added_in_path = build_tools_folder
        if build_tools_folder_found:
            logger.info(f" ==> build_tools_folder : {build_tools_folder} <==")

            build_tools_folder_30_0_0_rc2 = build_tools_folder + '\\' + version_build_tools
            PATH_USER = str(GetEnvVarUser("PATH"))
            if os.path.isdir(build_tools_folder_30_0_0_rc2):
                logger.info(f"PhoneBot found the folder '{build_tools_folder_30_0_0_rc2}'")
                build_tools_folder_to_be_added_in_path = build_tools_folder_30_0_0_rc2
            else:
                logger.info(f"PhoneBot didn't find the folder '{build_tools_folder_30_0_0_rc2}'")
                build_tools_folder_to_be_added_in_path = build_tools_folder

            if PATH_USER.find(build_tools_folder_to_be_added_in_path) == -1:
                logger.info("PhoneBot will change PATH user for build_tools_folder_to_be_added_in_path.")
                PATH_TO_ADD = str(PATH_USER + ';' + build_tools_folder_to_be_added_in_path).replace('PATH=',
                                                                                                    '').replace(
                    'Path=', '').replace(
                    'path=', '')
                ChangeEnvVarUser("PATH", PATH_TO_ADD)
                env_var_changed = True

                PATH_SYS = str(GetEnvVarSys("PATH"))
                if PATH_SYS.find(build_tools_folder_to_be_added_in_path) == -1:
                    logger.info(f"PhoneBot will change PATH system for {build_tools_folder_to_be_added_in_path}.")
                    PATH_TO_ADD = str(PATH_USER + ';' + build_tools_folder_to_be_added_in_path).replace('PATH=',
                                                                                                        '').replace(
                        'Path=',
                        '').replace(
                        'path=', '')
                    ChangeEnvVarSys("PATH", PATH_TO_ADD)
                    env_var_changed = True
                    build_tools = True
                else:
                    logger.info(f"PATH system for {build_tools_folder_to_be_added_in_path} is fine.")
                    build_tools = True
            else:
                logger.info(f"PATH user for {build_tools_folder_to_be_added_in_path} is fine.")
                PATH_SYS = str(GetEnvVarSys("PATH"))
                if PATH_SYS.find(build_tools_folder_to_be_added_in_path) == -1:
                    logger.info(f"PhoneBot will change PATH system for {build_tools_folder_to_be_added_in_path}.")
                    PATH_TO_ADD = str(PATH_USER + ';' + build_tools_folder_to_be_added_in_path).replace('PATH=',
                                                                                                        '').replace(
                        'Path=',
                        '').replace(
                        'path=', '')
                    ChangeEnvVarSys("PATH", PATH_TO_ADD)
                    env_var_changed = True
                    build_tools = True
                else:
                    logger.info(f"PATH system for {build_tools_folder_to_be_added_in_path} is fine.")
                    build_tools = True
        else:
            logger.critical(
                f"We didn't find {build_tools_folder_to_be_added_in_path}. PhoneBot will try to install it. If it fails, you will have to install it yourself. Nothing complicated, you'll just have to download the appropriate program and install it. PhoneBot will guide you. But first, let PhoneBot try to install it itself please..")
            build_tools = False

        print('\n' * 2)

        # =====================================================================================
        #                                ANDROID (adb.exe)
        # =====================================================================================
        logger.info("Checking adb.exe. Please wait..................")
        # --- To know the path of adb.exe folder

        if mymodules.TestIfInstalled("adb --version"):
            logger.info("adb is installed!")
            android = True
        else:
            adb_tools_exist = mymodules.GetPathFromDB('adb')
            if not adb_tools_exist:
                if os.path.isdir(AppData_Local_folder_Android):
                    logger.info(f"Good news! PhoneBot find {AppData_Local_folder_Android}")
                    logger.info(
                        f"PhoneBot will search adb.exe from {AppData_Local_folder_Android}. Please be patient......")
                    adb_folder = glob.glob(AppData_Local_folder_Android + "\\**\\adb.exe", recursive=True)
                    if adb_folder:
                        ChangePathInDB('adb', adb_folder[0])
                        adb_folder = adb_folder[0]
                        print(f"build_tools_folder : {adb_folder}")
                        adb_folder_found = True
                        logger.info(f"PhoneBot found {adb_folder}")
                    else:
                        #adb_folder = C_program_folder + r"\Android\platform-tools"
                        adb_folder = Folder_abd_osx #rajout
                        logger.info(
                            f"PhoneBot couldn't find 'adb.exe'  in {AppData_Local_folder_Android}. It will search from {adb_folder}")
                        if shutil.which('adb.exe', path=str(adb_folder)):
                            ChangePathInDB('adb', adb_folder + r'\adb.exe')
                            logger.info(f"PhoneBot found 'adb.exe' in {adb_folder}.")
                            adb_folder_found = True
                            print(f"adb_folder : {adb_folder}")
                        else:
                            logger.info(f"PhoneBot couldn't find 'adb.exe'  in {adb_folder}. It will search from 'C:\\'")
                            adb_file = distutils.spawn.find_executable('adb.exe')
                            if adb_file:
                                ChangePathInDB('adb', adb_file)
                                adb_folder = str(adb_file).replace('adb.exe', '')
                                logger.info(f"PhoneBot found 'adb.exe' in {adb_folder}.")
                                adb_folder_found = True
                                print(f"adb_folder : {adb_folder}")
                                if adb_folder[len(adb_folder) - 1] == '\\':
                                    adb_folder = adb_folder[0:len(adb_folder) - 1]
                                    print(f"New adb_folder without the '\\' : {adb_folder}")
                            else:
                                logger.info(f"PhoneBot couldn't find 'adb.exe' from 'C:\\'")
                                adb_folder_found = False
            else:
                adb_folder = str(adb_tools_exist).replace(r'\adb.exe', '')
                adb_folder_found = True

            if adb_folder_found:
                logger.info(f"adb_folder : {adb_folder}")
                adb_folder = adb_folder.replace('\\adb.exe\\', '')
                adb_folder = adb_folder.replace(r'\adb.exe\\', '')
                adb_folder = adb_folder.replace(r'\adb.exe', '')
                adb_folder = adb_folder.replace('\\adb.exe', '')
                logger.info(f" ==> adb_folder : {adb_folder} <==")
                PATH_USER = str(GetEnvVarUser("PATH"))
                if PATH_USER.find(adb_folder) == -1:
                    logger.info("PhoneBot will change PATH user for adb_folder.")
                    PATH_TO_ADD = str(PATH_USER + ';' + adb_folder).replace('PATH=', '').replace(
                        'Path=', '').replace('path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    env_var_changed = True

                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(adb_folder) == -1:
                        logger.info("PhoneBot will change PATH system for adb_folder.")
                        PATH_TO_ADD = str(PATH_USER + ';' + adb_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        env_var_changed = True
                        android = True
                    else:
                        logger.info("PATH system for ANDROID is fine.")
                        android = True
                        android = True

                else:
                    logger.info("PATH user for adb_folder is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(adb_folder) == -1:
                        logger.info("PhoneBot will change PATH system for adb_folder.")
                        PATH_TO_ADD = str(PATH_USER + ';' + adb_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD

                        env_var_changed = True
                        android = True
                    else:
                        logger.info("PATH system for adb_folder is fine.")
                        android = True

            else:
                logger.critical(
                    "We didn't find adb.exe. PhoneBot will try to install it. If it fails, you will have to install it yourself. Nothing complicated, you'll just have to download the appropriate program and install it. PhoneBot will guide you. But first, let PhoneBot try to install it itself please..")
                android = False

        print('\n' * 2)
        # =====================================================================================
        #                                Appium server (appium.cmd)
        # =====================================================================================
        # --- We get the HOME user folder in order to find the path of appium
        # ---  which suppose to be in C:\Users\USERNAME\AppData\Roaming\npm
        logger.info("Checking Appium.cmd. Please wait..................")

        if mymodules.TestIfInstalled("appium --version"):
            logger.info("Appium is installed!")
            appium = True
        else:
            appium_exist = mymodules.GetPathFromDB('appium')
            if not appium_exist:

                logger.info(f"home_user : {home_user}")
                appium_folder = home_user + r"\AppData\Roaming\npm"
                appium_exe = appium_folder + r"\appium.cmd"
                logger.info(f"appium_folder : {appium_folder}")
                logger.info(f"appium_exe : {appium_exe}")

                logger.info(f"Appium suppose to be located in this folder  : {appium_exe}")
                if os.path.isfile(appium_exe):
                    logger.info(
                        f"PhoneBot found appium.cmd in folder {appium_folder}. PhoneBot check now the environment variable!")
                    appium_folder_found = True
                    ChangePathInDB('appium', appium_exe)
                else:
                    logger.info(
                        f"PhoneBot didn't find appium.cmd. It will search from {appium_folder}. Please be patient......")
                    appium_file = glob.glob(appium_folder + "\\**\\appium.cmd", recursive=True)

                    if appium_file:
                        ChangePathInDB('appium', appium_file[0])
                        print("PhoneBot found appium.cmd")
                        appium_folder = str(appium_file[0]).replace('appium.cmd', '')
                        appium_folder_found = True
                        if appium_folder[len(appium_folder) - 1] == '\\':
                            appium_folder = appium_folder[0:len(appium_folder) - 1]
                            print(f"New appium_folder without the '\\' : {appium_folder}")
                    else:
                        logger.info(
                            f"PhoneBot didn't find appium.cmd from {appium_folder}. It will search from {home_user}. Please be patient......")
                        appium_file = glob.glob(home_user + "\\**\\appium.cmd", recursive=True)

                        if appium_file:
                            ChangePathInDB('appium', appium_file[0])
                            print("PhoneBot found appium.cmd")
                            appium_folder = str(appium_file[0]).replace('appium.cmd', '')
                            appium_folder_found = True
                            if appium_folder[len(appium_folder) - 1] == '\\':
                                appium_folder = appium_folder[0:len(appium_folder) - 1]
                                print(f"New appium_folder without the '\\' : {appium_folder}")
                        else:
                            logger.info(
                                f"PhoneBot didn't find appium.cmd from {home_user}. It will search from {C_program_folder}. Please be patient....")
                            appium_file = glob.glob(C_program_folder + "\\**\\appium.cmd", recursive=True)
                            if appium_file:
                                ChangePathInDB('appium', appium_file[0])
                                print("We found appium.cmd")
                                appium_folder = str(appium_file[0]).replace('appium.cmd', '')
                                appium_folder_found = True
                                if appium_folder[len(appium_folder) - 1] == '\\':
                                    appium_folder = appium_folder[0:len(appium_folder) - 1]
                                    print(f"New appium_folder without the '\\' : {appium_folder}")
                            else:
                                appium_folder_found = False
                                logger.critical(
                                    f"We didn't find appium.cmd from {C_program_folder}. We will try to install it.")

            else:
                appium_folder = str(appium_exist).replace(r'\appium.cmd', '')
                appium_folder_found = True

            if appium_folder_found:

                PATH_USER = str(GetEnvVarUser("PATH"))
                if PATH_USER.find(appium_folder) == -1:
                    logger.info("PhoneBot will change PATH user for APPIUM.")
                    PATH_TO_ADD = str(PATH_USER + ';' + appium_folder).replace('PATH=', '').replace(
                        'Path=', '').replace('path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    os.environ['PATH'] = PATH_TO_ADD
                    env_var_changed = True

                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(appium_folder) == -1:
                        logger.info("PhoneBot will change PATH system for APPIUM.")
                        PATH_TO_ADD = str(PATH_USER + ';' + appium_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD
                        env_var_changed = True
                        appium = True
                    else:
                        logger.info("PATH system for APPIUM is fine.")
                        appium = True

                else:
                    logger.info("PATH user for APPIUM is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if PATH_SYS.find(appium_folder) == -1:
                        logger.info("PhoneBot will change PATH system for APPIUM.")
                        PATH_TO_ADD = str(PATH_USER + ';' + appium_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD
                        env_var_changed = True
                        appium = True
                    else:
                        logger.info("PATH system for APPIUM is fine.")
                        appium = True
            else:
                logger.critical(
                    "We didn't find appium.cmd. PhoneBot will try to install it. If it fails, you will have to install it yourself. Nothing complicated, you'll just have to download the appropriate program and install it. PhoneBot will guide you. But first, let PhoneBot try to install it itself please..")
                appium = False

        print('\n' * 2)
        # =====================================================================================
        #                                Tesseract (C:\Program Files\Tesseract-OCR\tesseract.exe)
        # =====================================================================================

        logger.info("Checking Tesseract. Please wait..................")

        if mymodules.TestIfInstalled("tesseract --list-langs"):
            logger.info("Tesseract is installed!")
            tesseract = True
        else:
            tesseract_exist = mymodules.GetPathFromDB('tesseract')
            if not tesseract_exist:
                tesseract_folder = C_program_folder + "\\Tesseract-OCR"
                tesseract_exe = tesseract_folder + "\\tesseract.exe"
                logger.info(f"tesseract_folder : {tesseract_folder} - tesseract_exe {tesseract_exe}")
                if os.path.isfile(tesseract_exe):
                    ChangePathInDB('tesseract', tesseract_exe)
                    logger.info(
                        f"We found tesseract.exe in folder {tesseract_folder}. Let's check now the environment variable!")
                    tesseract_folder_found = True
                else:
                    tesseract_folder = "C:\\Program Files (x86)\\Tesseract-OCR"
                    tesseract_exe = tesseract_folder + "\\tesseract.exe"
                    logger.info(f"tesseract_folder : {tesseract_folder} - tesseract_exe {tesseract_exe}")
                    if os.path.isfile(tesseract_exe):
                        ChangePathInDB('tesseract', tesseract_exe)
                        logger.info(
                            f"We found tesseract.exe in folder {tesseract_folder}. Let's check now the environment variable!")
                        tesseract_folder_found = True

                    else:
                        logger.critical("We didn't find tesseract.exe in architecture 32 & 64. We will try to install it.")
                        tesseract_folder_found = False
            else:
                tesseract_folder = str(tesseract_exist).replace(r'\tesseract.exe', '')
                tesseract_folder_found = True

            if tesseract_folder_found:
                # ==========================================================================================================
                # ==========================================================================================================

                # We move the fra.traineddata file in the tesseract installation folder
                # first we check than folder C:\Program Files\Tesseract-OCR\tessdata exist
                tesseract_folder_data = tesseract_folder + "\\tessdata"
                tesseract_FR_file_destination = tesseract_folder_data + "\\fra.traineddata"
                if path.isdir(tesseract_folder_data):
                    if path.isfile(tesseract_FR_file_destination):
                        logger.info(
                            f"PhoneBot found the 'fra.traineddata' file in {tesseract_folder_data}. It doesn't need to copy it there.")

                        # We need to be sure the path of tesseract_data is in environment variable PATH

                        PATH_USER = str(GetEnvVarUser("PATH"))
                        if PATH_USER.find(tesseract_folder_data) == -1:
                            logger.info("PhoneBot will change PATH user for TESSERACT.")
                            PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=', '').replace(
                                'Path=', '').replace('path=', '')
                            ChangeEnvVarUser("PATH", PATH_TO_ADD)
                            os.environ['PATH'] = PATH_TO_ADD
                            env_var_changed = True
                            PATH_SYS = str(GetEnvVarSys("PATH"))
                            if PATH_SYS.find(tesseract_folder_data) == -1:
                                logger.info("PhoneBot will change PATH system for TESSERACT.")
                                PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=', '').replace(
                                    'Path=', '').replace('path=', '')
                                ChangeEnvVarSys("PATH", PATH_TO_ADD)
                                os.environ['PATH'] = PATH_TO_ADD
                                env_var_changed = True
                                tesseract = True
                            else:
                                logger.info("PATH system for TESSERACT is fine.")
                                tesseract = True

                        else:
                            logger.info("PATH user for TESSERACT is fine.")
                            PATH_SYS = str(GetEnvVarSys("PATH"))
                            if PATH_SYS.find(tesseract_folder_data) == -1:
                                logger.info("PhoneBot will change PATH system for TESSERACT.")
                                PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=', '').replace(
                                    'Path=', '').replace('path=', '')
                                ChangeEnvVarSys("PATH", PATH_TO_ADD)
                                os.environ['PATH'] = PATH_TO_ADD
                                env_var_changed = True
                                tesseract = True
                            else:
                                logger.info("PATH system for TESSERACT is fine.")
                                tesseract = True


                    # ========================= END OF ADDING ENV VAR FOR TESSERACT_DATA =================================
                    # ====================================================================================================

                    else:
                        logger.info(
                            f"The folder {tesseract_folder_data} exist. PhoneBot will copy the French Tesseract data.")
                        if not path.isfile("fra.traineddata"):
                            logger.info(
                                "It miss the file 'fra.traineddata' in PhoneBot installation folder. PhoneBot will try to re-download it, please wait...")
                            wget.download("https://github.com/tesseract-ocr/tessdata/raw/master/fra.traineddata", "fra.traineddata")
                        if path.isfile("fra.traineddata"):
                            shutil.move("fra.traineddata", tesseract_FR_file_destination)

                            # We need to be sure the path of tesseract_data is in environment variable PATH

                            PATH_USER = str(GetEnvVarUser("PATH"))
                            if PATH_USER.find(tesseract_folder_data) == -1:
                                logger.info("PhoneBot will change PATH user for TESSERACT.")
                                PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=', '').replace(
                                    'Path=', '').replace('path=', '')
                                ChangeEnvVarUser("PATH", PATH_TO_ADD)
                                os.environ['PATH'] = PATH_TO_ADD
                                env_var_changed = True
                                PATH_SYS = str(GetEnvVarSys("PATH"))
                                if PATH_SYS.find(tesseract_folder_data) == -1:
                                    logger.info("PhoneBot will change PATH system for TESSERACT.")
                                    PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=',
                                                                                                       '').replace(
                                        'Path=', '').replace('path=', '')
                                    ChangeEnvVarSys("PATH", PATH_TO_ADD)
                                    os.environ['PATH'] = PATH_TO_ADD
                                    env_var_changed = True
                                    tesseract = True
                                else:
                                    logger.info("PATH system for TESSERACT is fine.")
                                    tesseract = True

                            else:
                                logger.info("PATH user for TESSERACT is fine.")
                                PATH_SYS = str(GetEnvVarSys("PATH"))
                                if PATH_SYS.find(tesseract_folder_data) == -1:
                                    logger.info("PhoneBot will change PATH system for TESSERACT.")
                                    PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder_data).replace('PATH=',
                                                                                                       '').replace(
                                        'Path=', '').replace('path=', '')
                                    ChangeEnvVarSys("PATH", PATH_TO_ADD)
                                    os.environ['PATH'] = PATH_TO_ADD
                                    env_var_changed = True
                                    tesseract = True
                                else:
                                    logger.info("PATH system for TESSERACT is fine.")
                                    tesseract = True
                            # ======================= ENDING ADDING TESSERACTDATA IN ENV VAR =============================
                            # ============================================================================================



                        else:
                            logger.critical(
                                "It miss the file 'fra.traineddata' in PhoneBot installation folder. Aborting.")
                            sys.exit(-1)
                else:
                    if path.isfile(tesseract_FR_file_destination):
                        logger.info(
                            f"PhoneBot found the 'fra.traineddata' file in {tesseract_folder_data}. It doesn't need to copy it there.")
                    else:
                        if path.isfile("fra.traineddata"):
                            logger.info(
                                f"The folder {tesseract_folder_data} doesn't exist. PhoneBot will create the 'tessdata' folder and copy the French Tesseract data.")
                            os.replace("fra.traineddata", tesseract_FR_file_destination)
                        else:
                            logger.critical(
                                "It miss the file 'fra.traineddata' in PhoneBot installation folder. Aborting.")
                            sys.exit(-1)

                # ==========================================================================================================
                # ==========================================================================================================

                tesseract_folder_path = False
                PATH_USER = str(GetEnvVarUser("PATH"))

                if PATH_USER.find(tesseract_folder) == -1:
                    try:
                        if PATH_USER[PATH_USER.find(tesseract_folder) + len(tesseract_folder)] == ';':
                            tesseract_folder_path = True
                        elif PATH_USER[PATH_USER.find(tesseract_folder) + len(tesseract_folder)] == '\\':
                            if PATH_USER[PATH_USER.find(tesseract_folder) + len(tesseract_folder) + 1] == ';':
                                tesseract_folder_path = True
                    except:  # Exception = index out of range = it's the last element in path
                        tesseract_folder_path = True

                tesseract_folder_path_sys = False
                PATH_SYS = str(GetEnvVarSys("PATH"))

                if PATH_SYS.find(tesseract_folder) == -1:
                    try:
                        if PATH_SYS[PATH_SYS.find(tesseract_folder) + len(tesseract_folder)] == ';':
                            tesseract_folder_path_sys = True
                        elif PATH_SYS[PATH_SYS.find(tesseract_folder) + len(tesseract_folder)] == '\\':
                            if PATH_SYS[PATH_SYS.find(tesseract_folder) + len(tesseract_folder) + 1] == ';':
                                tesseract_folder_path_sys = True
                    except:  # Exception = index out of range = it's the last element in path
                        tesseract_folder_path_sys = True

                if not tesseract_folder_path:
                    logger.info("PhoneBot will change PATH user for TESSERACT.")
                    PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder).replace('PATH=', '').replace(
                        'Path=', '').replace('path=', '')
                    ChangeEnvVarUser("PATH", PATH_TO_ADD)
                    os.environ['PATH'] = PATH_TO_ADD
                    env_var_changed = True
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if not tesseract_folder_path_sys:
                        logger.info("PhoneBot will change PATH system for TESSERACT.")
                        PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD
                        env_var_changed = True
                        tesseract = True
                    else:
                        logger.info("PATH system for TESSERACT is fine.")
                        tesseract = True

                else:
                    logger.info("PATH user for TESSERACT is fine.")
                    PATH_SYS = str(GetEnvVarSys("PATH"))
                    if not tesseract_folder_path_sys:
                        logger.info("PhoneBot will change PATH system for TESSERACT.")
                        PATH_TO_ADD = str(PATH_USER + ';' + tesseract_folder).replace('PATH=', '').replace(
                            'Path=', '').replace('path=', '')
                        ChangeEnvVarSys("PATH", PATH_TO_ADD)
                        os.environ['PATH'] = PATH_TO_ADD
                        env_var_changed = True
                        tesseract = True
                    else:
                        logger.info("PATH system for TESSERACT is fine.")
                        tesseract = True
            else:
                logger.critical("We didn't find tesseract.exe in architecture. We will try to install it.")
                tesseract = False

        java_instruction = ''
        NodeJS_instruction = ''
        Android_Tools_instruction = ''
        Appium_instruction = ''
        Tesseract_instruction = ''
        Sdkmanager_instruction = ''
        Build_tools_instruction = ''

        print('\n' * 2)
        if not java:
            java_instruction = "Please download and install Java : https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241536_1f5b5a70bf22433b84d0e960903adac8 or from https://www.java.com/fr/download/"
        if not node:
            platform_architecture = platform.architecture()[0]
            if platform_architecture == "64bit":
                NodeJS_instruction = "Please download and install Node : https://nodejs.org/dist/v12.15.0/node-v12.15.0-x64.msi"
            else:
                NodeJS_instruction = "Please download and install Node : https://nodejs.org/dist/v12.15.0/node-v12.15.0-x86.msi"

        if not android:
            Android_Tools_instruction = "Please download and install Android Tools : https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

        if not sdkmanager:
            Sdkmanager_instruction = r"Please download and unzip this file in your folder 'C:\Program Files\Android\' or 'C:\Program Files (x86)\Android\' : https://dl.google.com/android/repository/commandlinetools-win-6200805_latest.zip"

        if not build_tools:
            # build_tools_name_program = '"build-tools;' + str(version_build_tools) + '"'
            build_tools_name_program = '"build-tools;28.0.3"'

            end_of_sentence = ". Execute 'cmd.exe' in your Windows search in order to open your terminal."
            Build_tools_instruction = "Please install SDK build-tools : You need to run this command in your terminal 'sdkmanager " + build_tools_name_program + end_of_sentence
        if not appium:
            Appium_instruction = "Please install Appium : You need to run this command in your terminal 'npm install -g appium'. Execute 'cmd.exe' in your Windows search in order to open your terminal."
        if not tesseract:
            Tesseract_instruction = "Please download and install Tesseract : https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe"

        logger.info("================= REPORT ===================")
        logger.info(f"Is Java Ready? => {java}. {java_instruction}")
        logger.info(f"Is NodeJS Ready? => {node}. {NodeJS_instruction}")
        logger.info(f"Is Android Tools Ready? => {android}. {Android_Tools_instruction}")
        logger.info(f"Is sdkmanager Ready? => {sdkmanager}. {Sdkmanager_instruction}")
        logger.info(f"Is build-tools Ready? => {build_tools}. {Build_tools_instruction}")
        logger.info(f"Is Appium Ready? => {appium}. {Appium_instruction}")
        logger.info(f"Is Tesseract Ready? => {tesseract}. {Tesseract_instruction}")
        logger.info("=============================================")

        # We clean the environment variable
        # clean(sort=True, remove_non_existent=True, remove_user_duplicates=True)
        print('\n' * 2)
        # ====================================================================================================
        # ============================================================================================================
        logger.info("PhoneBot finish by cleaning the path of double")

        # First we will clean the actual path by removing double
        path_sys = GetEnvVarSys('PATH')
        path_user = GetEnvVarUser('PATH')

        list_path_sys = path_sys.split(';')
        list_path_user = path_user.split(';')
        print(f"BEFORE len(list_path_sys) : {len(list_path_sys)}")
        print(f"BEFORE len(list_path_user) : {len(list_path_user)}")

        # remove the duplicate
        list_path_sys = list(dict.fromkeys(list_path_sys))
        list_path_user = list(dict.fromkeys(list_path_user))
        print(f"AFTER len(list_path_sys) : {len(list_path_sys)}")
        print(f"AFTER len(list_path_user) : {len(list_path_user)}")

        new_path_sys = ''
        new_path_user = ''

        for element_sys in list_path_sys:
            if element_sys != '':
                new_path_sys += element_sys + ';'

        if new_path_sys[len(new_path_sys) - 1] == ';':
            new_path_sys = new_path_sys[0:len(new_path_sys) - 1]

        for element_user in list_path_user:
            if element_user != '':
                new_path_user += element_user + ';'

        if new_path_user[len(new_path_user) - 1] == ';':
            new_path_user = new_path_user[0:len(new_path_user) - 1]

        new_path_sys = new_path_sys.replace('PATH=', '').replace('Path=', '').replace('path=', '')
        new_path_user = new_path_user.replace('PATH=', '').replace('Path=', '').replace('path=', '')
        ChangeEnvVarSys('PATH', new_path_sys)
        ChangeEnvVarUser('PATH', new_path_user)

        # ====================================================================================================
        # ====================================================================================================
        # ====================================================================================================

        return java, node, android, appium, tesseract, sdkmanager, build_tools, env_var_changed


    def install_environment(java, node, android, appium, tesseract, sdkmanager, build_tools):
        logger.info(
            "=====================================================================================================")
        logger.info(
            f"============== Start install_environment {java}-{node}-{android}-{appium}-{tesseract} - {sdkmanager} - {build_tools} ================")
        logger.info(
            "=====================================================================================================")

        platform_architecture = platform.architecture()[0]
        home_user = expanduser("~")
        C_program_folder = os.environ['PROGRAMFILES']
        AppData_Local_folder = home_user + '\\AppData\\Local'
        AppData_Local_folder_Android = AppData_Local_folder + "\\Android"
        version_build_tools = None
        logger.info("We will try to install the missing software and add the environment variable.")
        logger.info("If something goes wrong, please contact our support at support@phonebot.co.")

        print('\n' * 2)
        # =====================================================================================
        #                                INSTALLATION
        # =====================================================================================
        # JAVA => https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241536_1f5b5a70bf22433b84d0e960903adac8
        if not java:
            logger.info(
                "==================================== INSTALLATION JAVA ===========================================")
            try:
                logger.info("We will try now to download Java.")
                wget.download(
                    'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241536_1f5b5a70bf22433b84d0e960903adac8',
                    'java_install.exe')
                logger.info(
                    "We will try now to install Java. Please wait a few seconds, a window will pop up and follow the installation process.")
                proc = subprocess.check_call(['java_install.exe'], shell=True)

                # proc.wait()
            except Exception as ex:
                logger.critical(f"{ex} --> We tried to download and install Java on your computer, but something went wrong.\n \
                      Please download and install Java manually from https://www.java.com/fr/download/ \
                      Once it is done, re-start phonebot.exe")

        if not node:
            logger.info(
                "==================================== INSTALLATION NODE ===========================================")

            try:
                logger.info("We will try now to download NodeJS.")

                print(f"platform.architecture()[0]{platform.architecture()[0]} - {type(platform.architecture()[0])}")

                if platform_architecture == "64bit":
                    wget.download('https://nodejs.org/dist/v12.15.0/node-v12.15.0-x64.msi', 'node_install.msi')
                    logger.info(
                        "We will try now to install NodeJS 64Bits. Wait a few seconds, the installation program will start very soon. Please follow the installation process.")
                    logger.info(
                        "It is super easy! Just accept the T&C's and click always on 'Next' button. :-)")

                    proc = subprocess.Popen('node_install.msi',
                                            shell=True,
                                            # stdin=None, stdout=True, stderr=None, close_fds=True)
                                            stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True)

                    with proc.stdout:
                        log_subprocess_output(proc.stdout)
                    proc.wait()





                else:
                    wget.download('https://nodejs.org/dist/v12.15.0/node-v12.15.0-x86.msi', 'node_install.msi')
                    logger.info(
                        "We will try now to install NodeJS 32Bits. Wait a few seconds, the installation program will start very soon. Please follow the installation process.")
                    logger.info(
                        "It is super easy! Just accept the T&C's and click always on 'Next' button. :-)")
                    proc = subprocess.Popen('node_install.msi',
                                            shell=True,
                                            stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True)
                    with proc.stdout:
                        log_subprocess_output(proc.stdout)
                    proc.wait()


            except Exception as ex:
                logger.critical(f"{ex} --> We tried to download and install NodeJS on your computer, but something went wrong.\n \
                      Please download and install NodeJS manually from https://nodejs.org/en/download/\n \
                      Once it is done, re-start phonebot.exe")

        print('\n' * 2)
        if not sdkmanager:
            logger.info(
                "================================= INSTALLATION sdkmanager ========================================")

            sdkmanager_tools_folder = home_user + '\\AppData\\Local\\Android\\cmdline-tools'
            if not os.path.isdir(sdkmanager_tools_folder):
                logger.info(f"The folder {sdkmanager_tools_folder} doesn't exist. PhoneBot will create it.")
                os.mkdir(sdkmanager_tools_folder)

            print(f"sdkmanager_tools_folder : {sdkmanager_tools_folder}")
            try:
                logger.info("We will try now to download sdkmanager.")
                wget.download('https://dl.google.com/android/repository/commandlinetools-win-6609375_latest.zip',
                              'commandlinetools-win-6609375_latest.zip')
                logger.info("Downloaded! We will try now to unzip the Sdkmanager Tools.")
                with zipfile.ZipFile('commandlinetools-win-6609375_latest.zip', 'r') as zip_ref:
                    zip_ref.extractall(sdkmanager_tools_folder)
                sdkmanager_tools_folder_extracted = sdkmanager_tools_folder + '\\tools'
                sdkmanager_tools_folder_extracted_renamed = sdkmanager_tools_folder + '\\latest'
                if os.path.isdir(sdkmanager_tools_folder_extracted):
                    os.rename(sdkmanager_tools_folder_extracted, sdkmanager_tools_folder_extracted_renamed)
            except Exception as ex:
                logger.info(f"{ex} --> We tried to download and unzip sdkmanager on your computer, but something went wrong.\n \
                              Please download sdkmanager manually from https://dl.google.com/android/repository/commandlinetools-win-6200805_latest.zip\n  \
                              And unzip all the files in {sdkmanager_tools_folder} \n  \
                              Once it is done, restart phonebot.exe")

        print('\n' * 2)

        if not android:
            logger.info(
                "==================================== INSTALLATION ANDROID ===========================================")

            android_tools_folder = home_user + '\\AppData\\Local\\Android'
            print(f"android_tools_folder : {android_tools_folder}")
            try:
                logger.info("We will try now to download Android Tools.")
                wget.download('https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
                              'android_tool.zip')
                logger.info("Downloaded! We will try now to unzip the Android Tools.")
                with zipfile.ZipFile('android_tool.zip', 'r') as zip_ref:
                    zip_ref.extractall(android_tools_folder)
                    # if platform_architecture == "64bit":


            except Exception as ex:
                logger.info(f"{ex} --> We tried to download and unzip Android tools on your computer, but something went wrong.\n \
                      Please download Android tools manually from https://dl.google.com/android/repository/platform-tools-latest-windows.zip\n  \
                      And unzip all the files in {android_tools_folder} \n  \
                      Once it is done, restart phonebot.exe")

        print('\n' * 2)

        if not build_tools:
            logger.info(
                "==================================== INSTALLATION build-tools ===========================================")

            try:
                logger.info(
                    "We will try now to install SDK build_tools. Wait a few seconds, the installation program will start very soon.")
                sdkmanager_file = glob.glob(AppData_Local_folder_Android + "\\**\\latest\\bin\\sdkmanager.bat",
                                            recursive=True)
                logger.info(f"sdkmanager_file : {sdkmanager_file}")
                command_build_tools_final = sdkmanager_file[0] + ' "build-tools;28.0.3"'
                logger.info(f"command_build_tools_final : {command_build_tools_final}")
                proc = subprocess.Popen(command_build_tools_final, shell=True, stdout=True, stdin=PIPE, stderr=STDOUT)
                grep_stdout = proc.communicate(input=b'y')
                proc.wait()

                '''
                sdkmanager_list_command = sdkmanager_file[0] + " --list"
                logger.info(f"sdkmanager_list_command : {sdkmanager_list_command}")


                result_sdkmanager_list = str(os.popen(sdkmanager_list_command).read())
                logger.info(result_sdkmanager_list)

                if len(result_sdkmanager_list) == 0:
                    logger.info(
                        "PhoneBot couldn't execute the 'sdkmanager --list' command line. It is certainly a problem of environment variable. It will try on next turn.")
                else:
                    logger.info("We extract the last version number of build-tools")
                    result_build_tools_list = result_sdkmanager_list.split('\n')
                    list_build_tools_final = []
                    for build_tools in result_build_tools_list:
                        if str(build_tools).find('build-tools') != -1:
                            small_list_build_tools = build_tools.split('|')
                            for element in small_list_build_tools:
                                if str(element).find('build-tools') != -1:
                                    list_build_tools_final.append(element.strip())
                    command_build_tools = list_build_tools_final[len(list_build_tools_final) - 1]
                    version_build_tools_list = command_build_tools.split(';')
                    version_build_tools = version_build_tools_list[1]

                    command_build_tools_final = sdkmanager_file[0] + ' "' + str(command_build_tools) + '"'
                    logger.info(f"command_build_tools_final : {command_build_tools_final}")
                    proc = subprocess.Popen(command_build_tools_final, shell=True, stdout=True, stdin=PIPE, stderr=STDOUT)
                    grep_stdout = proc.communicate(input=b'y')
                    proc.wait()
                '''

            except Exception as ex:
                logger.critical(f"""{ex} --> We tried to download and install SDK build-tools on your computer, but something went wrong.\n \
                                      We will try again by forcing the path ANDROID_HOME to sdkmanager : sdkmanager --sdk_root=${{ANDROID_HOME}} "build-tools;28.0.3" """)

                try:
                    sdkmanager_file = glob.glob(AppData_Local_folder_Android + "\\**\\latest\\bin\\sdkmanager.bat",
                                                recursive=True)
                    logger.info(f"sdkmanager_file : {sdkmanager_file}")
                    command_build_tools_final = sdkmanager_file[
                                                    0] + " --sdk_root=${ANDROID_HOME}" + ' "build-tools;28.0.3"'
                    logger.info(f"command_build_tools_final : {command_build_tools_final}")
                    proc = subprocess.Popen(command_build_tools_final, shell=True, stdout=True, stdin=PIPE,
                                            stderr=STDOUT)
                    grep_stdout = proc.communicate(input=b'y')
                    proc.wait()
                except Exception as ex:

                    logger.critical(f"{ex} --> We tried to download and install SDK build-tools on your computer, but something went wrong.\n \
                          It may be a problem of environment variable. PhoneBot should restart in a few minutes.\nIf the problem persist, please download and install SDK build-tools manually\nOnce it is done, re-start phonebot.exe")

        print('\n' * 2)
        if not appium:
            logger.info(
                "==================================== INSTALLATION APPIUM ===========================================")

            try:
                logger.info(
                    "We will try now to install Appium. Wait a few seconds, the installation program will start very soon.")
                # command_install_npm =  '"' + C_program_folder + '\\nodejs\\npm install -g appium"'
                proc = subprocess.Popen('npm install -g appium',
                                        shell=True,
                                        stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True)

                # === This command is to

                with proc.stdout:
                    log_subprocess_output(proc.stdout)

                proc.wait()

            except Exception as ex:
                logger.critical(f"{ex} --> We tried to download and install NodeJS on your computer, but something went wrong.\n \
                      Please download and install NodeJS manually by typing in your Windows command terminal 'npm install -g appium'\n \
                      Once it is done, re-start phonebot.exe")

        print('\n' * 2)
        if not tesseract:
            logger.info(
                "==================================== INSTALLATION TESSERACT ===========================================")

            tesseract_folder = C_program_folder + 'Tesseract-OCR'
            try:
                logger.info("We will try now to download Tesseract.")
                wget.download(
                    'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe',
                    'tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe')

                logger.info(
                    "We will try now to install tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe.Wait a few seconds, the installation program will start very soon. A window will pop up, please follow the installation porcess.")
                proc = subprocess.check_call(["tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe"], shell=True)
                # proc.wait()
            except Exception as ex:
                logger.error(f"{ex} --> We tried to download and install Tesseract, but something went wrong.\n \
                      Please download Tesseract tools manually from https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe\n  \
                      Once it is done, restart phonebot.exe")

        RemoveFilesandFolder()

        if not version_build_tools:
            AppData_Local_folder_Android = home_user + '\\AppData\\Local\\Android'
            build_tools_folders = glob.glob(AppData_Local_folder_Android + "\\**\\build-tools", recursive=True)
            if len(build_tools_folders) != 0:
                logger.info(f"PhoneBot found {build_tools_folders[0]}")
                build_tools_folder = build_tools_folders[0]
                print(build_tools_folder)
                list_subfolders_with_paths = [f.name for f in os.scandir(build_tools_folder) if f.is_dir()]
                print(list_subfolders_with_paths[0])
                version_build_tools = list_subfolders_with_paths[0]

        logger.info(f"version_build_tools : {version_build_tools}")
        return version_build_tools


    def start_checking_env_appium():
        try:
            logger.info(
                "=====================================================================================================")
            logger.info(
                "============================ Start start_checking_env_appium ========================================")
            logger.info(
                "=====================================================================================================")
            RemoveFilesandFolder()
            java = False
            node = False
            android = False
            appium = False
            tesseract = False
            build_tools = False
            sdkmanager = False
            C_program_folder = os.environ['PROGRAMFILES']
            version_build_tools = ''
            java, node, android, appium, tesseract, sdkmanager, build_tools, env_var_changed = check_envrionment(java,
                                                                                                                 node,
                                                                                                                 android,
                                                                                                                 appium,
                                                                                                                 tesseract,
                                                                                                                 sdkmanager,
                                                                                                                 build_tools,
                                                                                                                 version_build_tools)
            print(
                "++++++++++++++++++++++++++++++ Final report Appium environment ++++++++++++++++++++++++++++++++++++++++++")
            print(f"java : {java}")
            print(f"node : {node}")
            print(f"android : {android}")
            print(f"appium : {appium}")
            print(f"tesseract : {tesseract}")
            print(f"sdkmanager : {sdkmanager}")
            print(f"build_tools : {build_tools}")
            print(f"env_var_changed : {env_var_changed}")
            print(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            cpt = 0
            while java != True or node != True or android != True or appium != True or tesseract != True or sdkmanager != True or build_tools != True:
                cpt += 1
                if java == True and node == True and android == True and appium == True and tesseract == True and sdkmanager == True and build_tools == True:
                    logger.info(
                        "Everything seems to be fine. When you will run the phonebot.exe, please send us the log file to support@phonebot.co if something goes wrong!")
                    mymodules.PopupMessage("How to enable USB DEBUG?",
                                           "\nAll necessary software has been installed successfully. Your computer is able now to automate smartphones through a USB cable.\n- 1 You need to enable Developer options on your Android smartphone.\n\n- 2 Then you will be able to enable USB Debugging \n\n- 3 Finally, you will plug your smartphone into your computer with a USB cable.\n\nAfter steps 1,2, and 3 are done, PhoneBot has the Scan Smartphones button in the tab Settings to help you to recognize your smartphone.\n\nWould you like to know how to enable Developer options?")
                    import webbrowser
                    webbrowser.open('https://www.youtube.com/watch?v=VcbDvsveqEs?t=19&hl=en&cc_lang_pref=en&cc=1')
                    break
                else:
                    version_build_tools = install_environment(java, node, android, appium, tesseract, sdkmanager,
                                                              build_tools)
                    java, node, android, appium, tesseract, sdkmanager, build_tools, env_var_changed = check_envrionment(
                        java,
                        node,
                        android,
                        appium,
                        tesseract,
                        sdkmanager,
                        build_tools,
                        version_build_tools)

                    if env_var_changed:

                        logger.info("""
    =====================================================================
    ||                                                                 ||                                                                                  
    ||                        _.-'''''-._                              ||
    ||                      .'  _     _  '.                            ||
    ||                     /   (_)   (_)   \                           ||
    ||                    |  ,           ,  |                          ||
    ||                    |  \`.       .`/  |                          ||
    ||                     \  '.`'""'"`.'  /                           ||
    ||                      '.  `'---'`  .'                            ||
    ||                        '-._____.-'                              ||
    ||                                                                 ||
    ||          CONGRATULATIONS! PhoneBot finished installing          ||
    ||                   all the necessary programs.                   ||
    ||                                                                 ||
    ||             PhoneBot will restart right now in order            ||
    ||              to enjoy the new environment variables.            ||
    ||                                                                 ||
    ||                                                                 ||
    =====================================================================
    """)

                        for remaining in range(5, 0, -1):
                            sys.stdout.write("\r")
                            sys.stdout.write("{:2d} seconds remaining before PhoneBot restarts.".format(remaining))
                            sys.stdout.flush()
                            time.sleep(1)

                        # proc = os.popen("start cmd /c PhoneBot.exe")
                        os.startfile('PhoneBot.exe')
                        sys.exit()
                        break


                    else:
                        logger.info("PhoneBot did't change any environment variables.")
                        logger.info("Before to run the tasks, it will load these environment variables:")
                        ANDROID_HOME = GetEnvVarSys("ANDROID_HOME")
                        JAVA_HOME = GetEnvVarSys("JAVA_HOME")
                        PATH = GetEnvVarSys("PATH")
                        logger.info(f"ANDROID_HOME : {ANDROID_HOME}")
                        logger.info(f"JAVA_HOME : {JAVA_HOME}")
                        logger.info(f"PATH : {PATH}")

                        os.environ['ANDROID_HOME'] = ANDROID_HOME
                        os.environ['JAVA_HOME'] = JAVA_HOME
                        os.environ['PATH'] = PATH

                        break




        except Exception as e:
            logger.critical(f"{e} ||| PhoneBot has an issue while it was installing the necessary programs.")
            return java, node, android, appium, tesseract, sdkmanager, build_tools

        return java, node, android, appium, tesseract, sdkmanager, build_tools

    # except ValueError:
    # print("ERROR prepare_env")

# ===============================================================================================================
# ====================================== WE EXECUTE CODE FOR MAC OS =============================================
# ===============================================================================================================
elif platform.system() == 'Darwin':
    print(f"platform.system() : {platform.system()}")


    def RemoveFilesandFolderMac():
        logger.info(
            "=====================================================================================================")
        logger.info(
            "================================ Start RemoveFilesandFolderMac =========================================")
        logger.info(
            "=====================================================================================================")
        if path.isdir('tools'):
            shutil.rmtree('tools')
        if path.isdir('platform-tools'):
            shutil.rmtree('platform-tools')
        if path.isfile('node-v12.18.3.pkg'):
            os.remove("node-v12.18.3.pkg")
        if path.isfile('jdk-14.0.2_osx-x64_bin.dmg'):
            os.remove("jdk-14.0.2_osx-x64_bin.dmg")


    def LoadPathEnvVar():
        """
        THis method will load the env variable path

        :return:
        """
        logger.info("========================= LoadPathEnvVar =================================")
        # WE NEED TO LOAD THE PATH FROM PROFILE FILE IN ENV VAR
        BASH_PROFILE_FILE = GetProfileFile()
        # WE WILL LOOP THE PROFILE FILE AND SEARCH FOR THE LINE PATH
        with open(mymodules.LoadFile(BASH_PROFILE_FILE)) as BP_file:
            cnt = 0
            for line in BP_file:
                if str(line).find("PATH =") != -1 or str(line).find("PATH=") != -1:
                    # WE ARE IN LINE PATH, WE NEED TO GET THE VALUE
                    pos_eq = str(line).find("=")
                    tmp_value = line[pos_eq + 1:]
                    tmp_value = str(tmp_value).replace("\"", "").replace("'", "")
                    os.environ['PATH'] = tmp_value
                    logger.info(f" ENV VARIABLE os.environ['PATH'] has been loaded: {tmp_value}")


    def GetEnvVarMAC(name):
        logger.info(
            f"========================== START GetEnvVarMAC {name} ===================================================")
        try:
            print(f"name : {name}")
            echo_arg = os.environ[name]
            print(f" : {echo_arg}")
            process_mac = subprocess.run(['echo', echo_arg], stdout=subprocess.PIPE, text=True)
            value = process_mac.stdout
            value = value.rstrip("\n")
            return value
        except Exception as ex:
            logger.error(f"PhoneBot didn't find the environment variable {name}")
            return None


    def ChangeEnvVarMAC(name, value):
        logger.info(
            f"========================== START ChangeEnvVarMAC {name} - {value}===================================================")
        try:

            bash_profile_path = GetProfileFile()
            print(f" : {bash_profile_path}")
            with open(bash_profile_path) as my_file:
                string_list = my_file.readlines()
                line_changed = False
            my_file.close()
            print(f"string_list : {string_list}")
            for i in range(0, len(string_list) - 1):
                print(f"string_list[i] : {string_list[i]}")

                if string_list[i].find(name + '="') != -1:
                    print(f"There is {name} in it ?")
                    print(f"PhoneBot found {name} in {string_list[i]}")
                    print(f"It will change for {value}")
                    string_list[i] = name + '="' + value + '"\n'
                    line_changed = True
                if string_list[i].find('::') != -1:
                    string_list[i].replace('::', ':')
            if line_changed:
                my_file = open(mymodules.LoadFile(bash_profile_path), "w")
                new_file_contents = "".join(string_list)
                print(f"PhoneBot will now write {bash_profile_path} file to add string_list : {string_list}")
                my_file.write(mymodules.LoadFile(new_file_contents))
                my_file.close()

                readable_file = open(mymodules.LoadFile(bash_profile_path))
                read_file = readable_file.read()
                print(f"read_file : {read_file}")
            else:
                string_to_add_1 = '\n' + name + '="' + value + '"\n'
                string_to_add_2 = 'export ' + name + '\n'
                with open(mymodules.LoadFile(bash_profile_path), 'a') as file:
                    file.write(string_to_add_1)
                    file.write(string_to_add_2)

            file = open(mymodules.LoadFile(bash_profile_path))
            print(100 * '>')
            print(file.read())
            file.close()
            print(100 * '<')

            return True
        except Exception as ex:
            logger.error(f"{ex} => PhoneBot couldn't add '{value}' to environment variable '{name}'")
            return False


    def GetProfileFile():
        """
        This function will return the path access to the correct profile file
        :return:
        """
        #home_path = str(GetEnvVarMAC('HOME'))
        home_path = os.path.expanduser('~')#rajout pour mac
        os_ver = str(platform.mac_ver()[0])
        if os_ver.find("10.13") != -1:
            print("macOS High Sierra")
            MAC_OS_VERSION = "High Sierra"
            BASH_PROFILE_FILE = f"{home_path}/.bash_profile"

        elif os_ver.find("10.12") != -1:
            print("macOS Sierra")
            MAC_OS_VERSION = "Sierra"
            BASH_PROFILE_FILE = f"{home_path}/.bash_profile"
        elif os_ver.find("10.15") != -1:
            print("macOS Catalina")
            MAC_OS_VERSION = "Catalina"
            BASH_PROFILE_FILE = f"{home_path}/.zshrc"
        elif os_ver.find("10.14") != -1:
            print("macOS Mojave")
            MAC_OS_VERSION = "Mojave"
            BASH_PROFILE_FILE = f"{home_path}/.bash_profile"
            print("(Mac) OS X something")
            MAC_OS_VERSION = "Else"
            BASH_PROFILE_FILE = f"{home_path}/.bash_profile"
        return BASH_PROFILE_FILE


    def remove_envvar_path_user_MAC(folder):

        """ Remove *all* paths in PATH_VAR that contain the folder path. """

        BASH_PROFILE_FILE = GetProfileFile()

        my_file = open(mymodules.LoadFile(BASH_PROFILE_FILE))
        string_list = my_file.readlines()
        my_file.close()
        print(string_list)
        for i in range(0, len(string_list) - 1):
            if string_list[i].find(folder) != -1:
                string_list[i].replace(folder, '')
            if string_list[i].find('::') != -1:
                string_list[i].replace('::', ':')
        my_file = open(mymodules.LoadFile(BASH_PROFILE_FILE), "w")
        new_file_contents = "".join(string_list)

        my_file.write(new_file_contents)
        my_file.close()

        readable_file = open(mymodules.LoadFile(BASH_PROFILE_FILE))
        read_file = readable_file.read()
        print(read_file)


    def check_envrionment(java, node, android, appium, tesseract, sdkmanager, build_tools, version_build_tools):
        logger.info(
            "=====================================================================================================")
        logger.info(
            "================================== Start check_envrionment MAC OS X ==========================================")
        logger.info(
            "=====================================================================================================")
        # We need to load environment variables from $PATH
        LoadPathEnvVar()
        # ===============================================================================================================
        # echo_arg = os.environ['PATH']
        # process_mac = subprocess.run(['/bin/bash','echo', echo_arg], stdout=subprocess.PIPE, text=True)
        # Path = process_mac.stdout
        # ===============================================================================================================
        C_program_folder = '/Applications'
        home_user = os.environ['HOME']
        AppData_Local_folder_Android = home_user + '/Android'

        # OUR SCRIPT PhoneBot_Install.sh store the path of environment variable in config.ini file
        # LET'S LOAD ALL THE ENVIRONMENT VARIABLE FROM THE CONFIG.INI

        config = configparser.ConfigParser()
        config.read(mymodules.LoadFile('config.ini'), encoding='utf-8')

        # =====================================================================================
        #                                     ANDROID_HOME
        # We will imediatly check existencce or create the folder C:\Users\your_username\AppData\Local\Android\cmdline-tools
        # and add the environment variable ANDROID_HOME
        # =====================================================================================
        logger.info("Checking ANDROID_HOME. Please wait..................")
        ANDROID_HOME_VALUE = AppData_Local_folder_Android
        if os.path.isdir(ANDROID_HOME_VALUE):
            logger.info(f"PhoneBot found the folder {ANDROID_HOME_VALUE}.")
            logger.info(f" ==> ANDROID_HOME_VALUE : {ANDROID_HOME_VALUE} <==")
            if GetEnvVarMAC("ANDROID_HOME") != ANDROID_HOME_VALUE:
                # logger.info("PhoneBot will change ANDROID_HOME user.")
                # ChangeEnvVarMAC("ANDROID_HOME", ANDROID_HOME_VALUE)
                os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                android = True
            else:
                logger.info("ANDROID_HOME user is fine.")
                android = True
        else:
            logger.info(f"The folder {ANDROID_HOME_VALUE} doesn't exist. PhoneBot will create it.")
            os.mkdir(ANDROID_HOME_VALUE)
            if os.path.isdir(ANDROID_HOME_VALUE):
                logger.info(f"PhoneBot found the folder {ANDROID_HOME_VALUE}.")
                logger.info(f" ==> ANDROID_HOME_VALUE : {ANDROID_HOME_VALUE} <==")
                if GetEnvVarMAC("ANDROID_HOME") != ANDROID_HOME_VALUE:
                    # logger.info("PhoneBot will change ANDROID_HOME user.")
                    # ChangeEnvVarMAC("ANDROID_HOME", ANDROID_HOME_VALUE)
                    os.environ['ANDROID_HOME'] = ANDROID_HOME_VALUE
                    android = True
                else:
                    logger.info("ANDROID_HOME user is fine.")
                    android = True

        print('\n' * 2)

        # =====================================================================================
        #                                     JAVA
        # =====================================================================================
        logger.info("Checking Java. Please wait..................")
        print(f"home_user : {home_user}")
        # C_program_folder_java='/System/Library/Frameworks/JavaVM.framework/Versions/A/Commands/'
        java = mymodules.TestIfInstalled('java -version')
        if not java:
            java = mymodules.TestIfInstalled('java -version')

        print('\n' * 2)
        # =====================================================================================
        #                                NODE.js
        # =====================================================================================
        node = mymodules.TestIfInstalled('node --version')
        print('\n' * 2)
        # =====================================================================================
        #                                ANDROID SDK MANAGER(sdkmanager)
        # =====================================================================================
        sdkmanager = mymodules.TestIfInstalled('sdkmanager --version')
        print('\n' * 2)

        # =====================================================================================
        #                                ANDROID build-tools folder
        # =====================================================================================
        # --- To know the path of build-tools folder
        logger.info("Checking SDK build-tools. Please wait..................")
        if sdkmanager:
            build_tools = True
        else:
            build_tools = False
        print('\n' * 2)

        # =====================================================================================
        #                                ANDROID (adb)
        # =====================================================================================
        logger.info("Checking adb. Please wait..................")
        android = mymodules.TestIfInstalled('adb --version')
        print('\n' * 2)
        # =====================================================================================
        #                                Appium server (appium)
        # =====================================================================================
        logger.info("Checking appium. Please wait..................")
        appium = mymodules.TestIfInstalled('appium -v')
        print('\n' * 2)
        # =====================================================================================
        #                                Tesseract (/usr/local/bin/tesseract)
        # =====================================================================================
        tesseract = mymodules.TestIfInstalled('tesseract --version')
        if tesseract:
            logger.info("Checking Tesseract. Please wait..................")
            print(f"PhoneBot didn't find tesseract folder in database!")

            if os.path.isdir(mymodules.LoadFile("/usr/local/Cellar/tesseract")):
                TESSERACT_FOLDER = mymodules.LoadFile("/usr/local/Cellar/tesseract")
                TESSERACT_FOLDER_FOUND = True
            elif os.path.isdir(mymodules.LoadFile("/opt/local/share/tessdata/")):
                TESSERACT_FOLDER = mymodules.LoadFile("/opt/local/share/tessdata/")
                try:
                    TESSDATA_PREFIX_VARIABLE = os.environ["TESSDATA_PREFIX"]
                    if TESSDATA_PREFIX_VARIABLE == "" or TESSDATA_PREFIX_VARIABLE is None:
                        TESSERACT_FOLDER_FOUND = False
                    else:
                        TESSERACT_FOLDER_FOUND = True
                except:
                    TESSERACT_FOLDER_FOUND = False


            elif os.path.isdir(mymodules.LoadFile(f"{home_user}/tesseract-ocr/tessdata")):
                TESSERACT_FOLDER = mymodules.LoadFile(f"{home_user}/tesseract-ocr/tessdata")
                TESSERACT_FOLDER_FOUND = True

            else:
                # IF WE DON'T FIND TESSERACT DATA FOLDER, WE SEARCH FOR IT
                logger.error("ERROR : There is a problem. We didn't find Tesseract folder!")
                logger.error("We will search for it everywhere")
                tesseract = False
            if TESSERACT_FOLDER_FOUND:
                if os.path.isfile(mymodules.LoadFile(f"{TESSERACT_FOLDER}/fra.traineddata")):
                    tesseract = True
                else:
                    tesseract = False
        else:
            tesseract = False

        java_instruction = ''
        NodeJS_instruction = ''
        Android_Tools_instruction = ''
        Appium_instruction = ''
        Tesseract_instruction = ''
        Sdkmanager_instruction = ''
        Build_tools_instruction = ''

        print('\n' * 2)
        if not java:
            java_instruction = "Please download and install Java : https://javadl.oracle.com/webapps/download/AutoDL?xd_co_f=MjVjODA5MjMtZWM2MC00OWM5LThkMTctMWJhMjI0YzhkYmE1&BundleId=242981_a4634525489241b9a9e1aa73d9e118e6 or from https://www.java.com/fr/download/"
        if not node:
            NodeJS_instruction = "Please download and install Node : https://nodejs.org/dist/v12.18.3/node-v12.18.3.pkg"

        if not android:
            Android_Tools_instruction = "Please download and install Android Tools : https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"

        if not sdkmanager:
            Sdkmanager_instruction = r"Please download and unzip this file in your folder " + home_user + r"/Android : https://dl.google.com/android/repository/commandlinetools-mac-6609375_latest.zip"

        if not build_tools:
            # build_tools_name_program = '"build-tools;' + str(version_build_tools) + '"'
            build_tools_name_program = '"build-tools;28.0.3"'
            end_of_sentence = ". Execute 'cmd.exe' in your Windows search in order to open your terminal."
            Build_tools_instruction = "Please install SDK build-tools : You need to run this command in your terminal 'sdkmanager " + build_tools_name_program + end_of_sentence
        if not appium:
            Appium_instruction = "Please install Appium : You need to run this command in your terminal 'sudo npm install -g appium --unsafe-perm=true --allow-root'. Execute 'cmd.exe' in your Windows search in order to open your terminal."
        if not tesseract:
            Tesseract_instruction = "Please download and install Tesseract with the command line  'brew install tesseract'"

        logger.info("================= REPORT ===================")
        logger.info(f"Is Java Ready? => {java}. {java_instruction}")
        logger.info(f"Is NodeJS Ready? => {node}. {NodeJS_instruction}")
        logger.info(f"Is Android Tools Ready? => {android}. {Android_Tools_instruction}")
        logger.info(f"Is sdkmanager Ready? => {sdkmanager}. {Sdkmanager_instruction}")
        logger.info(f"Is build-tools Ready? => {build_tools}. {Build_tools_instruction}")
        logger.info(f"Is Appium Ready? => {appium}. {Appium_instruction}")
        logger.info(f"Is Tesseract Ready? => {tesseract}. {Tesseract_instruction}")
        logger.info("=============================================")

        # We clean the environment variable
        # clean(sort=True, remove_non_existent=True, remove_user_duplicates=True)
        print('\n' * 2)
        # ====================================================================================================
        # ============================================================================================================
        logger.info("PhoneBot finish by cleaning the path of double")

        return java, node, android, appium, tesseract, sdkmanager, build_tools


    def install_environment():
        logger.info(
            "=====================================================================================================")
        logger.info(
            f"============== Start install_environment ================")
        logger.info(
            "=====================================================================================================")
        if not os.path.isfile(mymodules.LoadFile('PhoneBot_Install.sh')):
            logger.info("PhoneBot didn't find the script PhoneBot_Install.sh. It will download it.")
            wget.download('https://phonebot.co/dist/PhoneBot_Install.sh', 'PhoneBot_Install.sh')

        shell_script_install_PhoneBot = mymodules.LoadFile('PhoneBot_Install.sh')
        print(f"shell_script_install_PhoneBot:{shell_script_install_PhoneBot}")
        command_install_phonebot = f"""/usr/bin/osascript -e 'do shell script "/bin/bash {shell_script_install_PhoneBot} >> {os.environ['HOME']}/PhoneBot/log.log" with prompt "PhoneBot need to install some programs." with administrator privileges'"""
        proc = subprocess.Popen(command_install_phonebot, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = proc.communicate()
        logger.info(output.decode("utf8"))
        logger.info(err.decode("utf8"))
        returncode_command_install_phonebot = proc.wait()
        logger.info(f"returncode_command_install_phonebot : {returncode_command_install_phonebot}")


    def start_checking_env_appium():
        try:

            logger.info(
                "=====================================================================================================")
            logger.info(
                "============================ Start start_checking_env_appium ========================================")
            logger.info(
                "=====================================================================================================")

            # We initialize config.ini file
            config = configparser.ConfigParser()
            RemoveFilesandFolderMac()
            java = False
            node = False
            android = False
            appium = False
            tesseract = False
            build_tools = False
            sdkmanager = False

            version_build_tools = "28.0.3"
            java, node, android, appium, tesseract, sdkmanager, build_tools = check_envrionment(java, node, android,
                                                                                                appium, tesseract,
                                                                                                sdkmanager, build_tools,
                                                                                                version_build_tools)
            print(
                "++++++++++++++++++++++++++++++ Final report Appium environment ++++++++++++++++++++++++++++++++++++++++++")
            print(f"java : {java}")
            print(f"node : {node}")
            print(f"android : {android}")
            print(f"appium : {appium}")
            print(f"tesseract : {tesseract}")
            print(f"sdkmanager : {sdkmanager}")
            print(f"build_tools : {build_tools}")
            print(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            cpt = 0
            while java != True or node != True or android != True or appium != True or tesseract != True or sdkmanager != True or build_tools != True:

                cpt += 1
                if java == True and node == True and android == True and appium == True and tesseract == True and sdkmanager == True and build_tools == True:
                    logger.info(
                        "Everything seems to be fine. When you will run the PhoneBot executable, please send us the log file to support@phonebot.co if something goes wrong!")
                    mymodules.PopupMessage("How to enable USB DEBUG?",
                                           "\nAll necessary software has been installed successfully. Your computer is able now to automate smartphones through a USB cable.\n- 1 You need to enable Developer options on your Android smartphone.\n\n- 2 Then you will be able to enable USB Debugging \n\n- 3 Finally, you will plug your smartphone into your computer with a USB cable.\n\nAfter steps 1,2, and 3 are done, PhoneBot has the Scan Smartphones button in the tab Settings to help you to recognize your smartphone.\n\nWould you like to know how to enable Developer options?")
                    import webbrowser
                    webbrowser.open('https://www.youtube.com/watch?v=VcbDvsveqEs?t=19&hl=en&cc_lang_pref=en&cc=1')
                    break
                else:
                    install_environment()

                    # os.environ['PATH']=
                    version_build_tools = "28.0.3"
                    java, node, android, appium, tesseract, sdkmanager, build_tools = check_envrionment(java, node,
                                                                                                        android, appium,
                                                                                                        tesseract,
                                                                                                        sdkmanager,
                                                                                                        build_tools,
                                                                                                        version_build_tools)

                    # We will check the values of variables from the config.file which have been added by the PhoneBot_Install.sh script
                    # If they are all true, it means we installed successfully everything and PhoneBOt need to reboot
                    config.read(mymodules.LoadFile('config.ini'), encoding='utf-8')
                    try:
                        appium_config_ini = config.get('Settings', 'appium')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        appium_config_ini = 0
                    try:
                        java_config_ini = config.get('Settings', 'java')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        java_config_ini = 0
                    try:
                        node_config_ini = config.get('Settings', 'node')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        node_config_ini = 0
                    try:
                        android_config_ini = config.get('Settings', 'android')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        android_config_ini = 0
                    try:
                        sdkmanager_config_ini = config.get('Settings', 'sdkmanager')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        sdkmanager_config_ini = 0
                    try:
                        build_tools_config_ini = config.get('Settings', 'build_tools')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        build_tools_config_ini = 0
                    try:
                        tesseract_config_ini = config.get('Settings', 'tesseract')
                    except Exception as ex:
                        logger.error(f"{ex}")
                        tesseract_config_ini = 0

                    if appium_config_ini == 1 and java_config_ini == 1 and node_config_ini == 1 \
                            and android_config_ini == 1 and sdkmanager_config_ini == 1 \
                            and build_tools_config_ini == 1 and tesseract_config_ini == 1:
                        logger.info(
                            "The script PhoneBot_Install.sh installed correctly everything. We need to restart Phonebot??")
                        # proc = os.popen("start cmd /c PhoneBot.exe")
                        # os.startfile(mymodules.LoadFile('/Applications/PhoneBot.app/Contents/MacOS/PhoneBot'))
                        # sys.exit()
                        logger.info(
                            "Everything seems to be fine. When you will run the PhoneBot executable, please send us the log file to support@phonebot.co if something goes wrong!")
                        mymodules.PopupMessage("How to enable USB DEBUG?",
                                               "\nAll necessary software has been installed successfully. Your computer is able now to automate smartphones through a USB cable.\n- 1 You need to enable Developer options on your Android smartphone.\n\n- 2 Then you will be able to enable USB Debugging \n\n- 3 Finally, you will plug your smartphone into your computer with a USB cable.\n\nAfter steps 1,2, and 3 are done, PhoneBot has the Scan Smartphones button in the tab Settings to help you to recognize your smartphone.\n\nWould you like to know how to enable Developer options?")
                        import webbrowser
                        webbrowser.open('https://www.youtube.com/watch?v=VcbDvsveqEs?t=19&hl=en&cc_lang_pref=en&cc=1')
                        break
                if cpt > 2:
                    break
            return java, node, android, appium, tesseract, sdkmanager, build_tools
        # except Exception as e:
        # logger.critical(f"{e} ||| PhoneBot has an issue while it was installing the necessary programs.")
        # return java, node, android, appium, tesseract, sdkmanager, build_tools
        except ValueError:
            print("error")

        # except ValueError:

elif platform.system() == 'Linux':
    logger.info("Linux System")

    script = os.getcwd() + "/install_linux_tmp/phonebot_install_script_linux.sh"  # Path to the generated script


    def RemoveFilesandFolderLinux():
        logger.info(
            "\n=====================================================================================================")
        logger.info(
            "================================ Start RemoveFilesandFolderLinux =========================================")
        logger.info(
            "=====================================================================================================\n")
        if path.isdir('install_linux_tmp'):
            shutil.rmtree('install_linux_tmp')
        os.mkdir('install_linux_tmp')


    def GetEnvVarLinux(name):
        logger.info(
            f"========================== START GetEnvVarLinux {name} ===================================================")
        try:
            return os.environ[name]
        except Exception as ex:
            logger.error(f"PhoneBot didn't find the environment variable {name}")
            return None


    def ChangeEnvVarCommand(var, value):
        logger.info(
            f"========================== [QUEUE] Add {value} to var {var} ====================================")
        if var == 'PATH':
            echo = f"echo -e '\\nexport PATH=$PATH:\"{value}\"'"
        else:
            echo = f"echo -e '\\nexport {var}=\"{value}\"'"

        return echo + " >> \"/etc/profile.d/phonebot_sdks.sh\""


    def AddToInstallScript(command):
        """
        Adds a command to our custom install script.

        :param command: Command to add
        :return:
        """

        new = False

        if not path.isfile(script):
            new = True

        with open(script, 'a') as script_file:
            if new:
                script_file.write(f"#!/bin/bash\n")
                if not path.isfile("/etc/profile.d/phonebot_sdks.sh"):
                    setup = open("install_linux_tmp/setup_lock", 'w')
                    setup.write(f"if [[ -f \"{os.environ['HOME']}/.phonebot.lock\" ]]; then\n"
                                f"    rm \"{os.environ['HOME']}/.phonebot.lock\"\n"
                                f"fi\n")
                    setup.close()
                    script_file.write(
                        f"cat {os.getcwd()}/install_linux_tmp/setup_lock >> \"/etc/profile.d/phonebot_sdks.sh\"")
            script_file.write(f"\n{command}")


    def chmod(file):
        """
        Make a file executable
        :param file:
        :return:
        """

        proc = subprocess.Popen(f"chmod +x {file}", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT, close_fds=True)
        if proc.wait() != 0:
            logger.critical(f"There was an error while making {file} executable.")
            return False
        else:
            logger.info(f"Made {file} executable.")


    def RunInstallScript():
        """
        Run the generated install script as Super-User
        :return:
        """

        # Make our script executable

        chmod(script)

        commands = [f"pkexec bash {script}", "gksudo bash " + script, "kdesudo bash " + script,
                    "sudo bash " + script]  # Different methods to get super-user rights

        for command in commands:
            try:
                print(f"Trying command: {command}")
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, close_fds=True)
                returncode = proc.wait()
                output = proc.stdout.read()
                output = output.decode('utf-8')
                # print(f'returncode : {returncode}')
                logger.info("Script output:\n" +
                            output)
                if returncode == 0:
                    if not path.isfile(f"{os.environ['HOME']}/.phonebot.lock"):
                        open(f"{os.environ['HOME']}/.phonebot.lock", 'w')
                    return True
                elif command.startswith("sudo"):
                    logger.critical(f"PhoneBot couldn't run install script with super-user rights. Aborting.")
                    return False
                else:
                    logger.error("Bad return code, trying again with another method.")
            except Exception as ex:
                if command.startswith("sudo"):
                    logger.critical(f"{ex}: PhoneBot couldn't run install script with super-user rights. Aborting.")
                    return False
                else:
                    pass


    def ExtractArchive_Linux(file):
        logger.info(f"\nExtracting {file} ...\n")

        extension = file.split('.')
        returncode = -1

        if extension[-2] == "tar":
            logger.info("Using tar")
            proc = subprocess.Popen(f"tar -xf {file}", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, close_fds=True, cwd=f"{os.getcwd()}/install_linux_tmp")
            returncode = proc.wait()

        elif extension[-1] == "zip":
            logger.info("Using zipfile")
            try:
                with zipfile.ZipFile(file, "r") as zip_ref:
                    zip_ref.extractall(path=f"{os.getcwd()}/install_linux_tmp")
                returncode = 0
            except:
                returncode = -1

        else:
            logger.error("Unsupported archive type.")

        if returncode != 0:
            logger.error(f"\nERROR WHILE EXTRACTING ARCHIVE\n")
            return False
        else:
            logger.info(f"\n- Done unzipping {file} -\n")
            return True

    def is_in_profile_file(string):
        if path.isfile("/etc/profile.d/phonebot_sdks.sh"):
            with open("/etc/profile.d/phonebot_sdks.sh", 'r') as f:
                lines = f.read()
                if string in lines:
                    return True
                else:
                    return False
        else:
            return False



    def check_envrionment():
        if path.isfile(f"{os.environ['HOME']}/.phonebot.lock"):
            logger.error("\nA previous install of phonebot is waiting for a reboot.\n"
                         "Please reboot or logout to complete this install.\n")
            mymodules.PopupMessage("PhoneBot installation",
                                   "\nA previous install of phonebot is waiting for a reboot.\n"
                                   "Please reboot or logout to complete this install.\n"
                                   )
            sys.exit(0)

        logger.info("\n"
                    "=====================================================================================\n"
                    "======================== Begin check environment Linux ==============================\n"
                    "=====================================================================================\n")

        # Check if a previous installation is pending for reboot

        # =====================================================================================
        #                                     ANDROID_HOME
        # We will imediatly check existencce or create the folder /home/username/Android
        # and add the environment variable ANDROID_HOME
        # =====================================================================================

        java, node, android, appium, tesseract, sdkmanager, build_tools = None, None, None, None, None, None, None

        android_folder = None  # used to check directly the folder /home/username/Android
        android_home = GetEnvVarLinux("ANDROID_HOME")
        if not android_home:
            android_folder = path.isdir(os.environ['HOME'] + "/Android")

        if android_home or android_folder:
            if android_home:
                logger.info("We found ANDROID_HOME. We'll now check if the required tools are working ...")
            else:
                logger.info("PhoneBot found an Android folder which is not setup in environment variables. "
                            "We'll try to check and repair it.")
                android_home = os.environ['HOME'] + "/Android"
                AddToInstallScript(ChangeEnvVarCommand("ANDROID_HOME", android_home))

            if android_home[-1] == "/":
                android_home = android_home[:-1]  # Remove last '/'
            logger.info(f"android_home: {android_home}")
            # =====================================================================================
            #                           Check for adb
            # =====================================================================================

            logger.info("\n----- Checking for adb ... -----\n")
            android = mymodules.TestIfInstalled("adb --version")

            if android:
                logger.info("Found adb!")
            elif path.isdir(android_home + "/platform-tools"):
                if path.isfile(android_home + "/platform-tools/adb"):
                    logger.warning("PhoneBot found an installation of adb which is not in PATH. We'll add it.")
                    AddToInstallScript(ChangeEnvVarCommand("PATH", android_home + "/platform-tools"))
                    android = True
                else:
                    logger.warning("PhoneBot found a platform-tools folder, but it does not contain adb\n"
                                   "platform-tools will be re-installed")
                    AddToInstallScript(
                        f"mv {android_home}/platform-tools {android_home}/platform-tools-old")  # Rename corrupted platform-tools to platform-tools-old
            else:
                logger.info("!! adb needs to be installed !!")

            # =====================================================================================
            #                           Check for sdkmanager
            # =====================================================================================

            logger.info("\n----- Checking for sdkmanager ... -----\n")
            sdkmanager = mymodules.TestIfInstalled("sdkmanager --version")

            if sdkmanager:
                logger.info("Found sdkmanager!")
            elif path.isdir(android_home + "/cmdline-tools/tools/bin"):
                if path.isfile(android_home + "/cmdline-tools/tools/bin/sdkmanager"):
                    logger.warning("PhoneBot found an installation of sdkmanager which is not in PATH. We'll add it.")
                    AddToInstallScript(ChangeEnvVarCommand("PATH", android_home + "/cmdline-tools/tools/bin"))
                    sdkmanager = True
                else:
                    logger.warning("PhoneBot found a cmdline-tools/tools folder, but it does not contain sdkmanager\n"
                                   "android-tools will be re-installed")
                    AddToInstallScript(
                        f"mv {android_home}/cmdline-tools {android_home}/cmdline-tools-old")  # Rename corrupted cmdline-tools to platform-tools-old
            else:
                logger.info("!! sdkmanager needs to be installed !!")

            # =====================================================================================
            #                           Check for BUILD TOOLS
            # =====================================================================================

            logger.info("\n----- Checking for build-tools ... -----\n")
            if path.isdir(f"{android_home}/build-tools"):
                if path.isdir(f"{android_home}/build-tools/28.0.3"):
                    logger.info("Found build-tools 28.0.3!")
                    build_tools = True
                elif len(mymodules.all_subdirs_of(f"{android_home}/build-tools")) > 0:
                    logger.warning(
                        "Found a different version of build-tools, PhoneBot will install v28.0.3 to ensure full compatibility.")
                    build_tools = False
                else:
                    logger.warning("!! build-tools need to be installed !!")
                    build_tools = False
            else:
                logger.info("!! build-tools need to be installed !!")
                build_tools = False

        # =====================================================================================

        else:  # No ANDROID_HOME
            logger.info(
                f"!! No ANDROID_HOME found. adb, sdk-manager and build-tools will be installed in {os.environ['HOME']}/Android !!")
            if not path.isdir(os.environ['HOME'] + "/Android"):
                os.mkdir(os.environ['HOME'] + "/Android")
            AddToInstallScript(ChangeEnvVarCommand("ANDROID_HOME", os.environ['HOME'] + "/Android"))
            android_home = os.environ['HOME'] + "/Android"
            android = False
            build_tools = False
            sdkmanager = False

        # =====================================================================================
        #                                    JAVA
        # =====================================================================================

        logger.info("\n----- Checking for java ... -----\n")
        java = mymodules.TestIfInstalled("java --version")

        if java:
            logger.info("Found java!")
        else:
            if mymodules.TestIfInstalled("java -version"):
                logger.info("Found java!")
                java = True
            else:
                logger.info("!! Java needs to be installed !!")

        # =====================================================================================
        #                                   Node.JS
        # =====================================================================================

        logger.info("\n----- Checking for Node.JS ... -----\n")
        node = mymodules.TestIfInstalled("node --version")

        if node:
            logger.info("Found node!")
        else:
            logger.info("!! Node needs to be installed !!")

        # =====================================================================================
        #                               Appium Server
        # =====================================================================================

        logger.info("\n----- Checking for Appium ... -----\n")
        appium = mymodules.TestIfInstalled("appium --version")

        if appium:
            logger.info("Found appium!")
        else:
            logger.info("!! Appium needs to be installed !!")

        # =====================================================================================
        #                               Tesseract
        # =====================================================================================

        logger.info("\n----- Checking for Tesseract ... -----\n")
        tesseract = mymodules.TestIfInstalled("tesseract --list-langs")

        if tesseract:
            logger.info("Found tesseract!")
        else:
            logger.info("!! Tesseract needs to be installed !!")

        logger.info("\n\n"
                    "================= REPORT ===================")
        logger.info(f"Is Java Ready? => {java}")
        logger.info(f"Is NodeJS Ready? => {node}")
        logger.info(f"Is Android Tools Ready? => {android}")
        logger.info(f"Is sdkmanager Ready? => {sdkmanager}")
        logger.info(f"Is build-tools Ready? => {build_tools}")
        logger.info(f"Is Appium Ready? => {appium}")
        logger.info(f"Is Tesseract Ready? => {tesseract}")
        logger.info("=============================================")

        logger.info("\n"
                    "=====================================================================================\n"
                    "======================== Finish check environment Linux =============================\n"
                    "=====================================================================================\n")

        return java, node, android, appium, tesseract, sdkmanager, build_tools, android_home


    def install_environment_linux(java, node, android, appium, tesseract, sdkmanager, build_tools, android_home):
        logger.info("\n"
                    "=====================================================================================\n"
                    "======================== Begin install environment Linux ============================\n"
                    "=====================================================================================\n")

        wd = os.getcwd() + "/install_linux_tmp"  # Get working directory

        if not path.isdir(wd):
            os.mkdir(wd)

        # =====================================================================================
        #                                    JAVA
        # =====================================================================================

        if not java:
            logger.info(
                "\n==================================== JAVA ===========================================\n")
            try:
                logger.info("Downloading java ...")
                wget.download(
                    'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=244575_d7fc238d0cbf4b0dac67be84580cfb4b',
                    f'{wd}/jre-8u291-linux-x64.tar.gz')
                ExtractArchive_Linux(f"{wd}/jre-8u291-linux-x64.tar.gz")
                AddToInstallScript(f"mv {wd}/jre1.8.0_291 /opt")
                if not is_in_profile_file("/opt/jre1.8.0_291"):
                    AddToInstallScript(ChangeEnvVarCommand("JAVA_HOME", "/opt/jre1.8.0_291"))
                if not is_in_profile_file("/opt/jre1.8.0_291/bin"):
                    AddToInstallScript(ChangeEnvVarCommand("PATH", "/opt/jre1.8.0_291/bin"))
                logger.info("\nJava installation will be completed after running the install script as super-user.")
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We tried to download and install Java on your computer, but something went wrong.")
            logger.info(
                "\n================================ JAVA FINISHED =======================================\n")

        if not node:
            logger.info(
                "\n==================================== NODE ===========================================\n")
            try:
                logger.info("Downloading node ...")
                wget.download(
                    'https://nodejs.org/dist/v14.17.1/node-v14.17.1-linux-x64.tar.xz',
                    'install_linux_tmp/node.tar.xz')
                ExtractArchive_Linux(f"{wd}/node.tar.xz")
                AddToInstallScript(f"mv {wd}/node-v14.17.1-linux-x64 /opt")
                if not is_in_profile_file("/opt/node-v14.17.1-linux-x64/bin"):
                    AddToInstallScript(ChangeEnvVarCommand("PATH", "/opt/node-v14.17.1-linux-x64/bin"))
                logger.info("\nNode installation will be completed after running the install script as super-user.")
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We tried to download and install NodeJS on your computer, but something went wrong.")
            logger.info(
                "\n================================ NODE FINISHED =======================================\n")

        if not android:
            logger.info(
                "\n==================================== ADB ===========================================\n")
            logger.info(f"Android Home: {android_home}")
            try:
                logger.info("Downloading Android platform-tools ...")
                wget.download(
                    'https://dl.google.com/android/repository/platform-tools_r31.0.2-linux.zip',
                    'install_linux_tmp/platform-tools.zip')
                ExtractArchive_Linux(f"{wd}/platform-tools.zip")  # gives a platform-tools folder

                for elem in os.listdir(f"{wd}/platform-tools"):
                    if path.isfile(f"{wd}/platform-tools/{elem}") and len(elem.split('.')) == 1:
                        chmod(f"{wd}/platform-tools/{elem}")

                if not path.isdir(f"{wd}/Android"):
                    os.mkdir(f"{wd}/Android")
                shutil.move(f"{wd}/platform-tools", f"{wd}/Android")
                if not is_in_profile_file(android_home + "/platform-tools"):
                    AddToInstallScript(ChangeEnvVarCommand("PATH", android_home + "/platform-tools"))
                logger.info("\nADB installation will be completed after running the install script as super-user.")
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We tried to download and install ADB on your computer, but something went wrong.")
            logger.info(
                "\n================================ ADB FINISHED =======================================\n")

        if not sdkmanager:
            logger.info(
                "\n==================================== SDKMANAGER ===========================================\n")
            logger.info(f"Android Home: {android_home}")
            try:
                logger.info("Downloading Android tools ...")
                wget.download(
                    'https://dl.google.com/android/repository/commandlinetools-linux-6609375_latest.zip',
                    'install_linux_tmp/commandlinetools.zip')
                ExtractArchive_Linux(f"{wd}/commandlinetools.zip")  # Gives us a 'tools' folder

                for elem in os.listdir(f"{wd}/tools/bin"):
                    chmod(f"{wd}/tools/bin/{elem}")

                os.mkdir(f"{wd}/cmdline-tools")
                shutil.move(f"{wd}/tools", f"{wd}/cmdline-tools")
                if not path.isdir(f"{wd}/Android"):
                    os.mkdir(f"{wd}/Android")
                shutil.move(f"{wd}/cmdline-tools", f"{wd}/Android")

                if not is_in_profile_file("/cmdline-tools/tools/bin"):
                    AddToInstallScript(ChangeEnvVarCommand("PATH", android_home + "/cmdline-tools/tools/bin"))
                logger.info(
                    "\nsdkmanager installation will be completed after running the install script as super-user.")
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We tried to download and install sdkmanager on your computer, but something went wrong.")
            logger.info(
                "\n================================ SDKMANAGER FINISHED =======================================\n")

        if not build_tools:
            logger.info(
                "\n==================================== BUILD TOOLS ===========================================\n")
            logger.info(f"Android Home: {android_home}")
            try:
                sdkmanager_path = None
                if path.isfile(android_home + "/cmdline-tools/tools/bin/sdkmanager"):
                    sdkmanager_path = android_home + "/cmdline-tools/tools/bin/sdkmanager"
                elif path.isfile(f"{wd}/Android/cmdline-tools/tools/bin/sdkmanager"):
                    sdkmanager_path = wd + "/Android/cmdline-tools/tools/bin/sdkmanager"
                else:
                    logger.error("PhoneBot didn't find sdkmanager to install build tools !")

                if sdkmanager_path:
                    java_str = ""
                    if not java:
                        java_str = f"export JAVA_HOME='{wd}/jre1.8.0_291' && "  # If java is not yet installed, use our temp java folder to run sdkmanager
                    logger.info("Installing build tools...")
                    if mymodules.TestIfInstalled(java_str + sdkmanager_path + " \"build-tools;28.0.3\""):
                        logger.info(
                            "\nBuild tools installation will be completed after running the install script as super-user.")
                    else:
                        logger.critical("Error while installing build tools!")
                else:
                    logger.critical("PhoneBot failed to find sdkmanager to install build tools.")
            except Exception as ex:
                logger.critical(
                    f"{ex} --> We tried to download and install build tools on your computer, but something went wrong.")
            logger.info(
                "\n================================ BUILD TOOLS FINISHED =======================================\n")

        if path.isdir(f"{wd}/Android"):
            if not path.isdir(android_home):
                try:
                    os.mkdir(android_home)
                except:
                    AddToInstallScript(f"mkdir {android_home}")
            for elem in os.listdir(f"{wd}/Android"):
                AddToInstallScript(f"mv {wd}/Android/{elem} {android_home}")

        if not appium:
            logger.info(
                "\n==================================== APPIUM ===========================================\n")
            if not node:
                logger.info("node not installed yet, using the node folder we just downloaded.")
                command = f"export PATH=$PATH:'{wd}/node-v14.17.1-linux-x64/bin' && '{wd}/node-v14.17.1-linux-x64/bin/npm' install -g appium"
                logger.info("Installing appium...")
                if mymodules.TestIfInstalled(command):
                    logger.info(
                        "\nAppium installation will be completed after running the install script as super-user.")
                else:
                    logger.critical("Error while installing appium!")
            else:
                command = "npm install -g appium"
                if mymodules.TestIfInstalled(command):
                    logger.info("\nAppium installed.")
                else:
                    logger.critical("Error while installing appium!")
            logger.info(
                "\n================================ APPIUM FINISHED =======================================\n")

        if not tesseract:
            logger.info(
                "\n==================================== TESSERACT ===========================================\n")
            logger.info("Downloading Tesseract...")

            """
            We download AppImage version, which contains following languages:
                deu - German
                eng - English
                fin - Finnish
                fra - French
                osd - Script and orientation
                por - Portuguese
                rus - Russian
                spa - Spanish
            This is a packaged installed, all we have to do is add it to PATH and it works on almost all systems.
            """

            wget.download(
                'https://github.com/AlexanderP/tesseract-appimage/releases/download/v5.0.0-alpha-20210401-130-g7a308/tesseract-5.0.0-alpha-20210401-130-g7a308-x86_64.AppImage',
                'install_linux_tmp/tesseract.AppImage')

            chmod(f"{wd}/tesseract.AppImage")

            if not path.isdir(f"{wd}/tesseract"):
                os.mkdir(f"{wd}/tesseract")

            shutil.move(f"{wd}/tesseract.AppImage", f"{wd}/tesseract/tesseract")

            AddToInstallScript(f"mv {wd}/tesseract /opt")
            if not is_in_profile_file("/opt/tesseract"):
                AddToInstallScript(ChangeEnvVarCommand("PATH", "/opt/tesseract"))

            logger.info("\nTesseract installation will be completed after running the install script as super-user.")
            logger.info(
                "\n================================ TESSERACT FINISHED =======================================\n")

        logger.info("\n"
                    "=====================================================================================\n"
                    "========================= Finish install environment Linux ==========================\n"
                    "=====================================================================================\n")

        return True


    def start_checking_env_appium():
        RemoveFilesandFolderLinux()


        p_java, p_node, p_android, p_appium, p_tesseract, p_sdkmanager, p_build_tools, p_android_home = check_envrionment()
        # ============ DEBUG =============

        # p_java = p_node = p_android = p_appium = p_tesseract = p_sdkmanager = p_build_tools = False

        # ================================
        is_script = path.isfile("install_linux_tmp/phonebot_install_script_linux.sh")
        if p_java and p_node and p_android and p_appium and p_tesseract and p_sdkmanager and p_build_tools and p_android_home:
            if is_script:
                if RunInstallScript():
                    logger.info("\n==================== REBOOT REQUIRED ====================\n"
                                "You need to reboot your system, or logout and log back in.\n"
                                "After that your system should be ready to run PhoneBot !")
                    mymodules.PopupMessage("PhoneBot Installation",
                                           "\n==================== REBOOT REQUIRED ====================\n"
                                           "You need to reboot your system, or logout and log back in.\n"
                                           "After that your system should be ready to run PhoneBot !"
                                           )
                else:
                    logger.critical("The install script failed.")
                    mymodules.PopupMessage("PhoneBot Install", "The install script failed.")
            else:
                logger.info("\nYour environment seems to be ready to run PhoneBot !\n")
                mymodules.PopupMessage("PhoneBot Installation",
                                       "\nYour environment seems to be ready to run PhoneBot !\n")
        elif install_environment_linux(p_java, p_node, p_android, p_appium, p_tesseract, p_sdkmanager, p_build_tools,
                                       p_android_home):
            if RunInstallScript():
                logger.info("\n==================== REBOOT REQUIRED ====================\n"
                            "You need to reboot your system, or logout and log back in.\n"
                            "After that your system should be ready to run PhoneBot !")
                mymodules.PopupMessage("PhoneBot Installation",
                                       "\n==================== REBOOT REQUIRED ====================\n"
                                       "You need to reboot your system, or logout and log back in.\n"
                                       "After that your system should be ready to run PhoneBot !"
                                       )
            else:
                logger.critical("The install script failed.")
                mymodules.PopupMessage("PhoneBot Install", "The install script failed.")


'''
if __name__ == '__main__':
    start_checking_env_appium()


#start_checking_env_appium()
'''
'''
if __name__ == '__main__':
    start_checking_env_appium()

'''
#start_checking_env_appium()
