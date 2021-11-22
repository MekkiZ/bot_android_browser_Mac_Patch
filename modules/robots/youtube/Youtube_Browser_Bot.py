# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import mymodules
import logging



# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__Youtube_Browser_Bot__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)



def RunYoutubeBrowser(p_browser, p_function, p_taskuser_id,label_log,lock):
    logger.info(f"================================================ RunYoutubeBrowser {p_taskuser_id} ===================================================")

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
    driver.get('https://youtube.com')
    driver.implicitly_wait(10)

    # ======================= We need to refuse to login =================================
    try:
        # Find the iframe of login popup
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ("//iframe[@name='passive_signin']"))))
        driver.switch_to.frame(iframe)
        print("PhoneBot switch to iframe login")
    except:
        logger.error("No Iframe_Log_In found!")
    try:
        button_no_thanks = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='dismiss-button']//paper-button[@id='button']")))
        driver.execute_script("arguments[0].click();", button_no_thanks)
    except Exception as ex:
        logger.error("Phonebot didn't see any 'Cookies popup'! We carry on the job!")

    Youtube_username = "Desktop"
    # Let's get the quantity of actions possible
    logger.info("=== [3] GetQuantityActions =======================================")
    quantity_actions = mymodules.GetQuantityActions(p_taskuser_id, Youtube_username)
    if quantity_actions > 0:
        # ===================================================================================
        # WE WILL RUN THE TASK FOR THIS PROFILE =============================================
        # ===================================================================================
        p_function(p_browser,p_taskuser_id, driver, Youtube_username, quantity_actions,label_log,lock)
        # AT THE END OF THE TASK, WE LOGOUT AND TRY TO RUN THE TASK WITH OTHER PROFILE
        logger.info(f"Profile {Youtube_username} logout of Youtube .")
        return True
    else:
        logger.info(
            f"Profile {Youtube_username} couldn't execute task because quantity_actions doesn't allow' => {quantity_actions}' .")

        return False


    
    

def Influencers_Youtube_Influencers_16(p_browser,p_taskuser_id,p_driver,Youtube_username, p_quantity_actions,label_log,lock):
    logger.info(f"=================== Influencers_Youtube_Influencers_16 {p_taskuser_id} - {Youtube_username} - {p_quantity_actions} =======================")
    #mymodules.PopupMessage("ACTIONS", f"Youtube user {Youtube_username} can make {p_quantity_actions} actions now of Influencers_Youtube_Influencers_16!")
    mymodules.GoogleSheetAddValues('11jJvq12zM5q0VhkZS3RjttqhlQ61mtBmavkox0symZQ',
                                   [p_browser, p_taskuser_id, 'Influencers_Youtube_Influencers_16',
                                    Youtube_username, p_quantity_actions])
    # === 1 GET FULL DETAILS OF TASK
    details_taskuser = mymodules.GetDetailsTaskUser(p_taskuser_id)