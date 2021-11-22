# -*- coding: utf-8 -*-

import logging
import sqlite3

from modules.robots.facebook import Facebook_Smartphone_Bot

from modules import mymodules

# ================================ LOGGER ====================================

open (mymodules.LoadFile ('log.log'), 'w').close()
logger = logging.getLogger('__RunSmartphones__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)



def StartSmartphone(p_udid, id_task,p_taskuser_id, label_log, lock,current_tab):
    logger.info (f"# ==================== StartSmartphone {p_udid} {id_task} ==========================")
    
    """
    if id_task == 23 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the COMPUTER automation Craigslist_Smartphone_Bot.Scraping_Craigslist_Ads_23",
                                      "Black",current_tab)
        return Craigslist_Smartphone_Bot.RunCraigslistSmartphone(p_browser,
                                                       Craigslist_Smartphone_Bot.Scraping_Craigslist_Ads_23,
                                                       p_taskuser_id,label_log,lock)
    
    """
    if id_task == 3 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Facebook_Smartphone_Bot.Cold_Messaging_Facebook_Group_Members_3",
                                      "Black",current_tab)
        return Facebook_Smartphone_Bot.RunFaceBookApp(p_udid, Facebook_Smartphone_Bot.Smartphone_Cold_Messaging_Facebook_Group_Members_3, p_taskuser_id,label_log,lock)
    """
    if id_task == 13 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Facebook_Smartphone_Bot.Influencers_Facebook_Page_Admins_13",
                                      "Black",current_tab)
        return Facebook_Smartphone_Bot.RunFaceBookSmartphone(p_browser,
                                                       Facebook_Smartphone_Bot.Influencers_Facebook_Page_Admins_13,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 22 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Facebook_Smartphone_Bot.Influencers_Facebook_Group_Admins_22",
                                      "Black",current_tab)
        return Facebook_Smartphone_Bot.RunFaceBookSmartphone(p_browser,
                                                       Facebook_Smartphone_Bot.Influencers_Facebook_Group_Admins_22,
                                                       p_taskuser_id,label_log,lock)
    """
    if id_task == 24:
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Facebook_Smartphone_Bot.Scraping_Facebook_Group_Members_24",
                                      "Black",current_tab)

        return Facebook_Smartphone_Bot.RunFaceBookApp(p_udid,
                                                       Facebook_Smartphone_Bot.Smartphone_Scraping_Facebook_Group_members,
                                                       p_taskuser_id,label_log,lock)
    """
    if id_task == 33 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Facebook_Smartphone_Bot.Authority_Facebook_Add_Group_members_as_Friends_33",
                                      "Black",current_tab)

        return Facebook_Smartphone_Bot.RunFaceBookSmartphone(p_browser,
                                                       Facebook_Smartphone_Bot.Authority_Facebook_Add_Group_members_as_Friends_33,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 9 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Gmap_Smartphone_Bot.Cold_Messaging_Google_Map_Search_by_keyword_city_9",
                                      "Black",current_tab)

        return Gmap_Smartphone_Bot.RunGoogleMapSmartphone(p_browser,
                                                       Gmap_Smartphone_Bot.Cold_Messaging_Google_Map_Search_by_keyword_city_9,
                                                       p_taskuser_id,label_log,lock)

    if id_task == 26 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Gmap_Smartphone_Bot.Scraping_Google_Map_Search_by_keywords_city_26",
                                      "Black",current_tab)

        return Gmap_Smartphone_Bot.RunGmapSmartphone(p_browser,
                                                         Gmap_Smartphone_Bot.Scraping_Google_Map_Search_by_keywords_city_26,
                                                         p_taskuser_id,label_log,lock)
    if id_task == 4 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Instagram_Smartphone_Bot.Cold_Messaging_Instagram_Followers_of_accounts_4",
                                      "Black",current_tab)

        return Instagram_Smartphone_Bot.RunInstagramSmartphone(p_browser,
                                               Instagram_Smartphone_Bot.Cold_Messaging_Instagram_Followers_of_accounts_4,
                                               p_taskuser_id,label_log,lock)
    if id_task == 21 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Instagram_Smartphone_Bot.Influencers_Instagram_Influencers_21",
                                      "Black",current_tab)

        return Instagram_Smartphone_Bot.RunInstagramSmartphone(p_browser,
                                               Instagram_Smartphone_Bot.Influencers_Instagram_Influencers_21,
                                               p_taskuser_id,label_log,lock)
    if id_task == 25 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Instagram_Smartphone_Bot.Scraping_Instagram_Followers_of_accounts_25",
                                      "Black",current_tab)

        return Instagram_Smartphone_Bot.RunInstagramSmartphone(p_browser,
                                                       Instagram_Smartphone_Bot.Scraping_Instagram_Followers_of_accounts_25,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 34 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Instagram_Smartphone_Bot.Authority_Instagram_Auto_Follow_34",
                                      "Black",current_tab)

        return Instagram_Smartphone_Bot.RunInstagramSmartphone(p_browser,
                                                         Instagram_Smartphone_Bot.Authority_Instagram_Auto_Follow_34,
                                                         p_taskuser_id,label_log,lock)
    if id_task == 27 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Leboncoin_Smartphone_Bot.Scraping_Leboncoin_Ads_27",
                                      "Black",current_tab)

        return Leboncoin_Smartphone_Bot.RunLeboncoinSmartphone(p_browser,
                                                         Leboncoin_Smartphone_Bot.Scraping_Leboncoin_Ads_27,
                                                         p_taskuser_id,label_log,lock)
    if id_task == 7 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7",
                                      "Black",current_tab)

        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,
                                                       Linkedin_Smartphone_Bot.Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7,
                                                       p_taskuser_id,label_log,lock)

    if id_task == 8 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Cold_Messaging_Linkedin_Search_by_keywords_city_8",
                                      "Black",current_tab)

        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,
                                                       Linkedin_Smartphone_Bot.Cold_Messaging_Linkedin_Search_by_keywords_city_8,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 6 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Influencers_Linkedin_Group_Admins_6",
                                      "Black",current_tab)

        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,
                                                       Linkedin_Smartphone_Bot.Influencers_Linkedin_Group_Admins_6,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 17 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Influencers_Linkedin_Page_Admins_17",
                                      "Black",current_tab)

        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,
                                                       Linkedin_Smartphone_Bot.Influencers_Linkedin_Page_Admins_17,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 31 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Scraping_Linkedin_Search_by_keywords_city_31",
                                      "Black",current_tab)

        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,
                                                       Linkedin_Smartphone_Bot.Scraping_Linkedin_Search_by_keywords_city_31,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 32 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Linkedin_Smartphone_Bot.Scraping_Linkedin_Group_Members_32",
                                      "Black",current_tab)
        return Linkedin_Smartphone_Bot.RunLinkedinSmartphone(p_browser,Linkedin_Smartphone_Bot.Scraping_Linkedin_Group_Members_32,
                                                       p_taskuser_id,label_log,lock)

    if id_task == 28 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Pagesjaunes_Smartphone_Bot.Scraping_Pages_Jaunes_Search_by_keywords_city_28",
                                      "Black",current_tab)
        return Pagesjaunes_Smartphone_Bot.RunPagesjaunesSmartphone(p_browser,
                                                   Pagesjaunes_Smartphone_Bot.Scraping_Pages_Jaunes_Search_by_keywords_city_28,
                                                   p_taskuser_id,label_log,lock)
    if id_task == 15 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Reddit_Smartphone_Bot.Influencers_Reddit_Group_Admins_15",
                                      "Black",current_tab)
        return Reddit_Smartphone_Bot.RunRedditSmartphone(p_browser,
                                                     Reddit_Smartphone_Bot.Influencers_Reddit_Group_Admins_15,
                                                     p_taskuser_id,label_log,lock)

    if id_task == 10 :
        logger.error("Desktop computer can't automate task id N°10 because you need smartphone")

    if id_task == 18 :
        logger.error("Desktop computer can't automate task id N°18 because you need smartphone")
        
    if id_task == 20 :
        mymodules.DisplayMessageLogUI(label_log, "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20", "Black",current_tab)
        return Twitter_Smartphone_Bot.RunTwitterSmartphone(p_browser,
                                                     Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20,
                                                     p_taskuser_id,label_log,lock)
    if id_task == 5 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        return Twitter_Smartphone_Bot.RunTwitterSmartphone(p_browser,
                                                     Twitter_Smartphone_Bot.Influencers_Twitter_Influencers_5,
                                                     p_taskuser_id,label_log,lock)
    if id_task == 35 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        return Twitter_Smartphone_Bot.RunTwitterSmartphone(p_browser,
                                                       Twitter_Smartphone_Bot.Authority_Twitter_Auto_Follow_35,
                                                       p_taskuser_id,label_log,lock)
    if id_task == 11 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        logger.error("Desktop computer can't automate task id N°11 because you need smartphone")
    if id_task == 19 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        logger.error("Desktop computer can't automate task id N°19 because you need smartphone")
    if id_task == 29 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        return Yellowpages_Smartphone_Bot.RunYellowpagesSmartphone(p_browser,
                                                     Yellowpages_Smartphone_Bot.Scraping_YellowPages_Search_by_keywords_city_29,
                                                     p_taskuser_id,label_log,lock)
    if id_task == 16 :
        mymodules.DisplayMessageLogUI(label_log,
                                      "COMPUTER||| PhoneBot will run now the automation Twitter_Smartphone_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                      "Black",current_tab)

        return Youtube_Smartphone_Bot.RunYoutube_Smartphone_BotSmartphone(p_browser,
                                                             Youtube_Smartphone_Bot.Influencers_Youtube_Influencers_16,
                                                             p_taskuser_id,label_log,lock)


"""

def main(p_udid,p_user_id,p_list_tasksuser,label_log,lock,current_tab):
    """

    :param p_udid:
    :param p_taskuser:
    :return:
    """

    logger.info(f"SMARTPHONE||||{p_udid}||| main ==={p_user_id}============================")
    

    if p_udid == 'Computer':
        # === WE NEED TO GET DETAILS OF COMPUTER IN TABLE smartphones
        # ===================================== CREATE SQLITE3 CONNECTION ==============================================
        sqlite_connection = sqlite3.connect(mymodules.LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        is_chrome=sqlite_cursor.execute("SELECT * FROM smartphones WHERE udid=? AND devicename=?", ('Computer', 'Chrome')).fetchone()
        if is_chrome:
            automate_Chrome=True
        else:
            automate_Chrome=False

        is_firefox = sqlite_cursor.execute("SELECT * FROM smartphones WHERE udid=? AND devicename=?",
                                          ('Computer', 'Firefox')).fetchone()
        if is_firefox:
            automate_Firefox = True
        else:
            automate_Firefox = False
        print(f"automate_Chrome: {automate_Chrome}")
        print(f"automate_Firefox: {automate_Firefox}")
        # === RUN COMPUTER AUTOMATION
        RunSmartphone.main(automate_Chrome, automate_Firefox, p_list_tasksuser,label_log,lock,current_tab)
    else:
        logger.info(f"SMARTPHONE||||{p_udid}||| RunSmartphone ")
        mymodules.DisplayMessageLogUI(label_log,
                                      f"SMARTPHONE||| ====START==={p_udid}====",
                                      "Black",current_tab)

        try:
            
            while True:
                # Get the Tasks of campaign
                print(f"p_list_tasksuser : {p_list_tasksuser}")
                print(f"len(p_list_tasksuser) : {len(p_list_tasksuser)}")
                result = True
                
                for taskuser in p_list_tasksuser:


                    logger.info(f"SMARTPHONE||||{p_udid}||| AUTOMATION TASK N° {taskuser['id']} =============================")
                    print(f"taskuser : {taskuser}")
                    try:
                        #print("# ==================== GET id_task ==========================")
                        id_task = int(mymodules.GetIDTask(taskuser['id']))
                        # print("# Get details of task")
                        name_task, daily_limit, hourly_limit, id_type_task, id_platform = mymodules.GetDetailsTask(
                            taskuser['id'])
                        name_type_task = mymodules.GetDetailsTypeTask(id_type_task)
                        platform_name = mymodules.GetPlatformName(id_platform)
                        # print("#Display details on UI")
                        logger.info(f"SMARTPHONE||||{p_udid}||| Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}")
                        # self.DisplayFields()
                        mymodules.DisplayMessageLogUI(label_log,
                                                      f"SMARTPHONE||| {p_udid} STARTS THE TASK N°{id_task} - taskuser N° {taskuser['id']}",
                                                      "Black",current_tab)
                        mymodules.DisplayMessageLogUI(label_log,
                                                      f"SMARTPHONE||| Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}",
                                                      "Black",current_tab)

                        result = StartSmartphone(p_udid,id_task,taskuser['id'],label_log,lock,current_tab)
                        # print("Execute Chrome_Bot.StartChrome")
                    except Exception as ex:
                        logger.error(f"Error GET id_task : {ex}")


                break
        except Exception as ex:
            logger.error(f"Error when automation_with_smartphone {ex}")

