 # -*- coding: utf-8 -*-
import sys

sys.path.append("..")
sys.path.append(".")

from modules import mymodules
import logging
from modules.robots.facebook import Facebook_Browser_Bot
from modules.robots.freelancer import Freelancer_Browser_Bot
from modules.robots.linkedin import Linkedin_Browser_Bot
from modules.robots.instagram import Instagram_Browser_Bot
from modules.robots.tiktok import Tiktok_Browser_Bot
from modules.robots.twitter import Twitter_Browser_Bot
from modules.robots.gmap import Gmap_Browser_Bot
from modules.robots.reddit import Reddit_Browser_Bot
from modules.robots.leboncoin import Leboncoin_Browser_Bot
from modules.robots.pagesjaunes import Pagesjaunes_Browser_Bot
from modules.robots.craigslist import Craigslist_Browser_Bot
from modules.robots.yellowpages import Yellowpages_Browser_Bot
from modules.robots.youtube import Youtube_Browser_Bot

# ================================ LOGGER ====================================

open(mymodules.LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__RunBrowser__')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(mymodules.LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def StartBrowser(id_task, p_taskuser_id, p_browser, label_log, lock, current_tab):
    logger.info(f"COMPUTER||||{p_browser}||| StartBrowser id task: {id_task} id task user: {p_taskuser_id} ==========================")

    try:

        if id_task == 3:
            try:
                mymodules.DisplayMessageLogUI(label_log,
                                              f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Cold_Messaging_Facebook_Group_Members_3",
                                              "Black", current_tab)
            except Exception as ex:
                logger.error(f"Error running id_task 3 DisplayMessageLogUI : {ex}")

            try:
                result,counter= Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                               Facebook_Browser_Bot.Cold_Messaging_Facebook_Group_Members_3,
                                                               p_taskuser_id, label_log, lock)
                mymodules.DisplayMessageLogUI(label_log,
                                              f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Facebook groups members.",
                                              "Black", current_tab)

                return result
            except Exception as ex:
                logger.error(f"Error running Facebook_Browser_Bot.RunFaceBookBrowser : {ex}")

        if id_task == 4:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Cold_Messaging_Instagram_Followers_of_accounts_4",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                             Instagram_Browser_Bot.Cold_Messaging_Instagram_Followers_of_accounts_4,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to followers of Instagram accounts",
                                          "Black", current_tab)
            return result

        if id_task == 5:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Twitter_Browser_Bot.Influencers_Twitter_Influencers_5",
                                          "Black", current_tab)
            result,counter=  Twitter_Browser_Bot.RunTwitterBrowser(p_browser,
                                                         Twitter_Browser_Bot.Influencers_Twitter_Influencers_5,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Twitter Influencers",
                                          "Black", current_tab)
            return result
        if id_task == 6:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Influencers_Linkedin_Group_Admins_6",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Influencers_Linkedin_Group_Admins_6,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Linkedin groups Admins",
                                          "Black", current_tab)
            return result
        if id_task == 7:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Cold_Messaging_Linkedin_Likers_and_Post_Commenters_7,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Likers and Commenters of some Linkedin posts",
                                          "Black", current_tab)
            return result

        if id_task == 8:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Cold_Messaging_Linkedin_Search_by_keywords_city_8",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Cold_Messaging_Linkedin_Search_by_keywords_city_8,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages/connections to Linkedin profiles from a search result",
                                          "Black", current_tab)
            return result
        if id_task == 9:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Gmap_Browser_Bot.Cold_Messaging_Google_Map_Search_by_keyword_city_9",
                                          "Black", current_tab)
            result,counter=  Gmap_Browser_Bot.RunGmapBrowser(p_browser,
                                                   Gmap_Browser_Bot.Cold_Messaging_Google_Map_Search_by_keyword_city_9,
                                                   p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Gmap businesses",
                                          "Black", current_tab)
            return result
        if id_task == 10:
            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Cold Message Telegram group members' because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Cold Message Telegram group members' because you need a smartphone!",
                                          "Red")


        if id_task == 11:
            # Whatsapp bulk message
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot can't automate task Whatsapp_Browser_Bot because you need a smartphone!",
                                          "Black", current_tab)
            logger.error(
                f"COMPUTER||||{p_browser}||| PhoneBot can't automate task Whatsapp_Browser_Bot because you need a smartphone!")
            #mymodules.DisplayMessageLogUI(label_log,
            #                              f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} businesses on YellowPages.com",
            #                              "Black", current_tab)
            return False
        if id_task == 12:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Cold Messaging SMS' because you need a smartphone!",
                                          "Black", current_tab)
            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Cold Messaging SMS' because you need a smartphone!",
                "Black", current_tab)

            return result

        if id_task == 13:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Influencers_Facebook_Page_Admins_13",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                           Facebook_Browser_Bot.Influencers_Facebook_Page_Admins_13,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Admins of Facebook pages",
                                          "Black", current_tab)
            return result

        if id_task == 15:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Reddit_Browser_Bot.Influencers_Reddit_Group_Admins_15",
                                          "Black", current_tab)
            result,counter=  Reddit_Browser_Bot.RunRedditBrowser(p_browser,
                                                       Reddit_Browser_Bot.Influencers_Reddit_Group_Admins_15,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to some Reddit Groups Admins",
                                          "Black", current_tab)
            return result
        if id_task == 16:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Youtube_Browser_Bot.Influencers_Youtube_Influencers_16",
                                          "Black", current_tab)
            result,counter=  Youtube_Browser_Bot.RunYoutubeBrowser(p_browser,
                                                         Youtube_Browser_Bot.Influencers_Youtube_Influencers_16,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped the contact details of {counter} influencers on Youtube.com",
                                          "Black", current_tab)
            return result

        if id_task == 17:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Influencers_Linkedin_Page_Admins_17",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Influencers_Linkedin_Page_Admins_17,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Linkedin Page Admins",
                                          "Black", current_tab)
            return result
        if id_task == 18:
            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task id N°18 because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Cold Message Telegram Admin' because you need a smartphone!",
                                          "Red")

            return False

        if id_task == 19:
            # Whatsapp Group Admins
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task 'Influencers Whatsapp Group Admins' because you need a smartphone!",
                                          "Black", current_tab)
            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task id N°19 because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} businesses on YellowPages.com",
                                          "Black", current_tab)
            return result

        if id_task == 20:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Twitter_Browser_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                          "Black")
            result,counter=  Twitter_Browser_Bot.RunTwitterBrowser(p_browser,
                                                         Twitter_Browser_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to followers of Twitter accounts.",
                                          "Black", current_tab)
            return result

        if id_task == 21:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Instagram_Influencers_21",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                             Instagram_Browser_Bot.Instagram_Influencers_21,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Instagram influencers.",
                                          "Black", current_tab)
            return result
        if id_task == 22:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Influencers_Facebook_Group_Admins_22",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                           Facebook_Browser_Bot.Influencers_Facebook_Group_Admins_22,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Facebook groups Admins.",
                                          "Black", current_tab)
            return result
        if id_task == 23:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the COMPUTER automation Craigslist_Browser_Bot.Scraping_Craigslist_Ads_23",
                                          "Black", current_tab)
            result,counter=  Craigslist_Browser_Bot.RunCraigslistBrowser(p_browser,
                                                               Craigslist_Browser_Bot.Scraping_Craigslist_Ads_23,
                                                               p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} Craigslist Ads.",
                                          "Black", current_tab)
            return result
        if id_task == 24:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Scraping_Facebook_Group_Members_24",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                           Facebook_Browser_Bot.Scraping_Facebook_Group_Members_24,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} members of Facebook groups.",
                                          "Black", current_tab)
            return result

        if id_task == 25:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Scraping_Instagram_Followers_of_accounts_25",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                             Instagram_Browser_Bot.Scraping_Instagram_Followers_of_accounts_25,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} followers of Instagram accounts.",
                                          "Black", current_tab)
            return result

        if id_task == 26:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Gmap_Browser_Bot.Scraping_Google_Map_Search_by_keywords_city_26",
                                          "Black", current_tab)
            result,counter=  Gmap_Browser_Bot.RunGmapBrowser(p_browser,
                                                   Gmap_Browser_Bot.Scraping_Google_Map_Search_by_keywords_city_26,
                                                   p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} businesses on Google Map.",
                                          "Black", current_tab)
            return result
        if id_task == 27:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Leboncoin_Browser_Bot.Scraping_Leboncoin_Ads_27",
                                          "Black", current_tab)
            result,counter=  Leboncoin_Browser_Bot.RunLeboncoinBrowser(p_browser,
                                                             Leboncoin_Browser_Bot.Scraping_Leboncoin_Ads_27,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} Leboncoin Ads.",
                                          "Black", current_tab)
            return result

        if id_task == 28:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Pagesjaunes_Browser_Bot.Scraping_Pages_Jaunes_Search_by_keywords_city_28",
                                          "Black", current_tab)
            result,counter= Pagesjaunes_Browser_Bot.RunPagesjaunesBrowser(p_browser,
                                                                 Pagesjaunes_Browser_Bot.Scraping_Pages_Jaunes_Search_by_keywords_city_28,
                                                                 p_taskuser_id, label_log, lock)

            mymodules.DisplayMessageLogUI(label_log,
                                       f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} businesses on PagesJaunes.fr","Black", current_tab)
            return result
        if id_task == 29:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Yellowpages_Browser_Bot.Scraping_YellowPages_Search_by_keywords_city_29",
                                          "Black", current_tab)
            result,counter= Yellowpages_Browser_Bot.RunYellowpagesBrowser(p_browser,Yellowpages_Browser_Bot.Scraping_YellowPages_Search_by_keywords_city_29,
                                                                 p_taskuser_id, label_log, lock)

            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} businesses on YellowPages.com",
                                          "Black", current_tab)
            return result, counter
        if id_task == 31:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Scraping_Linkedin_Search_by_keywords_city_31",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Scraping_Linkedin_Search_by_keywords_city_31,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} Linkedin profiles from some search results.",
                                          "Black", current_tab)
            return result
        if id_task == 32:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Scraping_Linkedin_Group_Members_32",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Scraping_Linkedin_Group_Members_32,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} Linkedin group members.",
                                          "Black", current_tab)
            return result
        if id_task == 33:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Authority_Facebook_Add_Group_members_as_Friends_33",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                           Facebook_Browser_Bot.Authority_Facebook_Add_Group_members_as_Friends_33,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot added {counter} Facebook group members as Friends.",
                                          "Black", current_tab)
            return result
        if id_task == 34:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Authority_Instagram_Auto_Follow_34",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                             Instagram_Browser_Bot.Authority_Instagram_Auto_Follow_34,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot auto-followed {counter} Instagram accounts.",
                                          "Black", current_tab)
            return result

        if id_task == 35:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Twitter_Browser_Bot.Cold_Messaging_Twitter_Followers_of_accounts_20",
                                          "Black", current_tab)
            result,counter=  Twitter_Browser_Bot.RunTwitterBrowser(p_browser,
                                                         Twitter_Browser_Bot.Authority_Twitter_Auto_Follow_35,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot auto-followed {counter} Twitter accounts.",
                                          "Black", current_tab)
            return result

        if id_task == 45:

            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task on TikTok because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task TikTok because you need a smartphone!",
                                          "Red")
            return False


        if id_task == 46:

            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task on TikTok because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task TikTok because you need a smartphone!",
                                          "Red")
            return False
        if id_task == 47:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Authority_Linkedin_Random_Like_47",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Authority_Linkedin_Random_Like_47,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot auto-liked randomly {counter} posts on Linkedin.",
                                          "Black", current_tab)
            return result
        if id_task == 48:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Authority_Instagram_Random_Like_48",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                             Instagram_Browser_Bot.Authority_Instagram_Random_Like_48,
                                                             p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot auto-liked randomly {counter} posts on Instagram.",
                                          "Black", current_tab)
            return result
        if id_task == 49:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Twitter_Browser_Bot.Authority_Twitter_Random_Like_49",
                                          "Black", current_tab)
            result,counter=  Twitter_Browser_Bot.RunTwitterBrowser(p_browser,
                                                         Twitter_Browser_Bot.Authority_Twitter_Random_Like_49,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot auto-liked randomly {counter} posts on Twitter.",
                                          "Black", current_tab)
            return result
        if id_task == 50:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Authority_Instagram_Unfollow_50",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunTwitterBrowser(p_browser,
                                                           Instagram_Browser_Bot.Authority_Instagram_Unfollow_50,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot unfollowed {counter} Instagram accounts.",
                                          "Black", current_tab)
            return result
        if id_task == 51:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Twitter_Browser_Bot.Authority_Twitter_Unfollow_51",
                                          "Black", current_tab)
            result,counter=  Twitter_Browser_Bot.RunTwitterBrowser(p_browser,
                                                         Twitter_Browser_Bot.Authority_Twitter_Unfollow_51,
                                                         p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot unfollowed {counter} Twitter accounts.",
                                          "Black", current_tab)
            return result
        # if id_task == 52 :
        #     mymodules.DisplayMessageLogUI(label_log,
        #                                   f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Freelancer_Browser_Bot.Freelancer_Freelancer_Reply_52",
        #                                   "Black",current_tab)
        #     return Freelancer_Browser_Bot.RunFreelancerBrowser(p_browser,
        #                                                    Freelancer_Browser_Bot.Freelancer_Freelancer_reply_52,
        #                                                    p_taskuser_id,label_log,lock)
        if id_task == 53:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Authority_Facebook_Share_Post_53",
                                          "Black", current_tab)
            result, counter = Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                                      Facebook_Browser_Bot.Authority_Facebook_share_post_53,
                                                                      p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot shared a post on {counter} Facebook groups.",
                                          "Black", current_tab)
            return result
        if id_task == 54:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Authority_Linkedin_Comment_Posts_54",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                           Linkedin_Browser_Bot.Authority_Linkedin_comment_posts_54,
                                                           p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot wrote a comment on {counter} Facebook posts.",
                                          "Black", current_tab)
            return result
        if id_task == 55:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Reddit_Browser_Bot.Cold_Messaging_Reddit_Group_Members_55",
                                          "Black", current_tab)
            result,counter=  Reddit_Browser_Bot.RunRedditBrowser(p_browser,
                                                       Reddit_Browser_Bot.Cold_Messaging_Reddit_Group_Members_55,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Reddit group members.",
                                          "Black", current_tab)
            return result

        if id_task == 56:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Authority_Facebook_Random_Like_56",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                       Facebook_Browser_Bot.Authority_Facebook_Random_Like_56,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot liked randomly {counter} posts on Facebook.",
                                          "Black", current_tab)
            return result
        if id_task == 57:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Cold_Messaging_Facebook_Likers_Commnenters_57",
                                          "Black", current_tab)
            result,counter=  Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                       Facebook_Browser_Bot.Cold_Messaging_Facebook_Likers_Commnenters_57,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Facebook Likers & Commenters of some posts.",
                                          "Black", current_tab)
            return result
        if id_task == 58:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Instagram_Browser_Bot.Browser_Instagram_send_message_likers_commenters",
                                          "Black", current_tab)
            result,counter=  Instagram_Browser_Bot.RunInstagramBrowser(p_browser,
                                                       Instagram_Browser_Bot.Cold_Messaging_Instagram_Likes_Commenters_58,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot sent {counter} messages to Likers & Commenters of some Instagram posts.",
                                          "Black", current_tab)
            return result
        if id_task == 59:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Facebook_Browser_Bot.Authority_Facebook_comment_some_posts_59",
                                          "Black", current_tab)
            result,counter= \
                Facebook_Browser_Bot.RunFacebookBrowser(p_browser,
                                                       Facebook_Browser_Bot.Authority_Facebook_comment_some_posts_59,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot wrote comments on {counter} Facebook posts.",
                                          "Black", current_tab)
            return result
        if id_task == 60:
            logger.error(
                f"COMPUTER||||{p_browser}||| Desktop computer can't automate task on TikTok because you need a smartphone!")
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| Desktop computer can't automate task TikTok because you need a smartphone!",
                                          "Red")
            return False
        if id_task == 61:
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot will run now the automation Linkedin_Browser_Bot.Browser_Linkedin_scraping_likers_commenters_61",
                                          "Black", current_tab)
            result,counter=  Linkedin_Browser_Bot.RunLinkedinBrowser(p_browser,
                                                       Linkedin_Browser_Bot.Browser_Linkedin_scraping_likers_commenters_61,
                                                       p_taskuser_id, label_log, lock)
            mymodules.DisplayMessageLogUI(label_log,
                                          f"COMPUTER||||{p_browser}||| PhoneBot scraped {counter} Linkedin profiles who liked or commented a post.",
                                          "Black", current_tab)
            return result

    except Exception as ex:
        logger.error(f"Error when display message in Label : {ex}")


# ======================================================================================================
# ==================================== RunComputer ===============================
# ======================================================================================================

def main(p_automate_Chrome, p_automate_Firefox, p_list_tasksuser, label_log, lock, current_tab):
    """
    This function will run the browser automation with the Main Tab Run Campaign. It needs 3 paramers
    :param p_automate_Chrome: Is Chrome ok?
    :param p_automate_Firefox: Is Firefox ok?
    :param p_list_tasksuser: list of tasks of user
    :return:
    """
    logger.info(
        f"============ RunComputer.main({p_automate_Chrome},{p_automate_Firefox}) ==============================")

    try:
        while True:
            # Get the Tasks of campaign
            # print(f"p_list_tasksuser : {p_list_tasksuser}")
            print(f"len(p_list_tasksuser) : {len(p_list_tasksuser)}")
            print(f"p_list_tasksuser : {p_list_tasksuser}")
            result = True
            for task in p_list_tasksuser:
                id_task = int(mymodules.GetIDTask(task['id']))
                # WE WILL LOOP IN ALL THE TASKS ENABLE AND EXECUTE THE ACTIONS
                # Each Chrome_Bot.StartChrome[task] and Firefox_Bot.StartFirefox[task] will return True or False if it did something or not.
                # By this way, at the end of the loop :
                #       if "result" = False:
                #           it means no Taskuser could have been executed. It means
                #           we reach the limits, so we can sleep for 45 minutes.
                #       else:
                #           it means some Taskuser has been executed
                #
                if p_automate_Chrome:
                    logger.info(f"========== CHROME AUTOMATION task {task} ===========")
                    try:
                        print(f"# ==================== GET id_task {id_task}======================")
                        # id_task = int(mymodules.GetIDTask(task['id']))

                        # print("# Get details of task")
                        name_task, daily_limit, hourly_limit, id_type_task, id_platform = mymodules.GetDetailsTask(
                            task['id'])
                        name_type_task = mymodules.GetDetailsTypeTask(id_type_task)
                        platform_name = mymodules.GetPlatformName(id_platform)
                        # print("#Display details on UI")
                        logger.info(
                            f"COMPUTER CHROME - Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}")
                        # self.DisplayFields()
                        print(f"============================================================================")
                        print(
                            f"================= CHROME START THE TASKUSER N° {task['id']} TASK N° {id_task} =======================")
                        print(f"============================================================================")
                        mymodules.DisplayMessageLogUI(label_log,
                                                      f"COMPUTER|||CHROME|| STARTS THE TASK N°{id_task} - taskuser N° {task['id']}",
                                                      "Black", current_tab)
                        mymodules.DisplayMessageLogUI(label_log,
                                                      f"COMPUTER|||CHROME|| Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}",
                                                      "Black", current_tab)

                        result = StartBrowser(id_task, task['id'], 'Chrome', label_log, lock, current_tab)
                        print(f"result of StartBrowser {id_task},{task['id']}, 'Chrome',")
                        # print("Execute Chrome_Bot.StartChrome")
                    except Exception as ex:
                        logger.error(f"Error GET id_task : {ex}")

                if p_automate_Firefox:
                    logger.info("=========================== FIREFOX AUTOMATION =============================")
                    print(f"# ==================== GET id_task {id_task} =========================")
                    #
                    print("# Get details of task")
                    name_task, daily_limit, hourly_limit, id_type_task, id_platform = mymodules.GetDetailsTask(
                        task['id'])
                    name_type_task = mymodules.GetDetailsTypeTask(id_type_task)
                    platform_name = mymodules.GetPlatformName(id_platform)
                    print("#Display details on UI")
                    logger.info(
                        f"COMPUTER FIREFOX - Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}")
                    # self.DisplayFields()
                    print(f"============================================================================")
                    print(
                        f"================= FIREFOX START THE TASKUSER N° {task['id']} TASK N° {id_task} =======================")
                    print(f"============================================================================")
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"COMPUTER|||FIREFOX|| STARTS THE TASK N°{id_task} - taskuser N° {task['id']}",
                                                  "Black", current_tab)
                    mymodules.DisplayMessageLogUI(label_log,
                                                  f"COMPUTER|||FIREFOX|| Execution of Task '{platform_name} {name_type_task} - {name_task} ' : daily_limit={daily_limit}, hourly_limit={hourly_limit}",
                                                  "Black", current_tab)

                    print(f"id_task : {id_task}")
                    print(f"task['id'] : {task['id']}")
                    print(f"'Firefox'")
                    print(f"label_log : {label_log}")
                    print(f"lock : {lock}")
                    print(f"current_tab : {current_tab}")

                    result = StartBrowser(id_task, task['id'], 'Firefox', label_log, lock, current_tab)
                    print(f"result of StartBrowser {id_task},{task['id']}, 'Firefox',")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%             %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%% END OF LOOP TASKS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%             %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            """
            if not result:
                # WE NEED HERE SLEEPING SYSTEM
                # We need to sleep 45 minutes as the previous loop didn't do anything
                forty_five_minutes = 45 * 60 * 60
                time.sleep(forty_five_minutes)
            """
            break

    except Exception as ex:
        logger.error(f"Error when automation_with_computer {ex}")

"""
id_task = 29
taskuser_id = 2177
browser = "Firefox"
label_log_run_one_task = ""
lock = ""
current_tab = ""

if __name__ == '__main__':
    StartBrowser(id_task, taskuser_id, browser, label_log_run_one_task, lock, current_tab)
"""