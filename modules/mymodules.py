# -*- coding: utf-8 -*-
from __future__ import print_function
import ctypes
import distutils
import pathlib
import pdb
import platform
import shutil
import ssl
import subprocess
import zipfile
import datetime
from datetime import datetime, timedelta
from datetime import time
from email import encoders
from email.header import Header
from email.utils import formataddr
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from modules import mymodulesteam

from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import configparser
import sys
import codecs
import hmac
import hashlib
import mysql
import time
import random
import psutil
from appium import webdriver
import logging
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import getmac
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from PIL import Image
import re
import io
import pytesseract
import os
import json
import base64
if platform.system() == 'Windows':
    import win32crypt
#from Crypto.Cipher import AES
# from Cryptodome.Cipher import AES
from Crypto.Cipher import AES
import sqlite3
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from progress.bar import Bar


#--- We prepare the logging --- #####################################################################
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
import requests
import webbrowser

from googleapiclient.discovery import build
from google.oauth2 import service_account




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
    
    #print(f"p_name :{p_name}")
    #print(f"p_ext :{p_ext}")
    if platform.system() == 'Darwin':
        from AppKit import NSBundle
        # FOR MAC WE NEED FULL PATH, SO LET's PREPARE IT
        HOME_DIR = os.environ['HOME']
        # If folder /PhoneBot in user's home doesn't exist
        if not os.path.isdir(HOME_DIR + '/PhoneBot'):
            os.mkdir(HOME_DIR + '/PhoneBot')
        HOME_PHONEBOT_DIR = HOME_DIR + '/PhoneBot'
        UI_DIR = HOME_PHONEBOT_DIR + '/ui'
        test_if_PhoneBot_app=NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
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
                    #shutil.move(os.path.join(curpath , 'ui.json'), os.path.join(HOME_DIR, 'ui.json'))
                    logger.info(f"ui.json file was copied from application folder to home folder")
                else:
                    logger.info(f"ui.json file from your home directory is more recent than the one in applications folder")







        if test_if_PhoneBot_app is None:
            # WE ARE NOT IN PHONEBOT APP
            # ALSO WE HAVE 2 KINDS OF FILES: THE ONES WE READ ONLY AND THE ONES WE WILL MODIFY
            # FOR THE ONES WE MODIFY OR CREATE, WE NEED TO CHANGE LOCATION TO HOME/PhoneBot
            if p_file == 'log.log' or p_file == 'db.db' or p_file == 'config.ini' or p_file == 'tmp.txt' or p_file == 'ui.txt' \
                    or p_file == 'appium.log'  or p_file == 'appium.zip'  or p_file == 'log.zip':
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
            if p_file == 'log.log' or p_file == 'db.db' or p_file == 'config.ini' or p_file == 'tmp.txt' or p_file == 'ui.txt'  \
                    or p_file == 'appium.log'  or p_file == 'appium.zip'  or p_file == 'log.zip':

                #print(f"p_file is : {p_file}")
                # WE NEED TO CHECK IF THE FOLDER HOME/PhoneBot
                result = NSBundle.mainBundle().pathForResource_ofType_(HOME_PHONEBOT_DIR + '/' + p_name, p_ext)
                #print(f"result for log,db,config: {result}")

            # elif p_file == 'ui.json':
            #     
            #     print(f"p_file is : {p_file}")
            #     #result = NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
            #     result = NSBundle.mainBundle().pathForResource_ofType_(HOME_PHONEBOT_DIR + '/' + p_name, p_ext)
            #     print(f"result for ui.json: {result}")
            else:
                #print(f"p_file is : {p_file}")
                result = NSBundle.mainBundle().pathForResource_ofType_(p_name, p_ext)
                #print(f"result for else : {result}")
    else:
        result=p_file




    #print(f"result : {result}")
    return result

open(LoadFile('log.log'), 'w').close()
logger = logging.getLogger('__mymodules__')
logger.setLevel(logging.INFO)
formatter=logging.Formatter('%(process)d:%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler(LoadFile('log.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(console_handler)




# =================================================================================================================
# ========================================== FUNCTION TO EXTRACT DOMAIN =============================================
# =================================================================================================================
def extract_domain(url):
    domain_name = str(url).lower()

    # === First cleanup =======================================================
    domain_name = domain_name.replace('www.', '').replace('www', '').replace('WWW.', '').replace('WWW', '').replace('/', '')
    domain_name = domain_name.replace('http','').replace('https','').replace(':','').replace('/','').replace('wwww','')


    # === We remove any utm strings ============================================
    pos_utm = domain_name.find('?utm')
    if pos_utm!=-1:
        domain_name = domain_name[0:pos_utm]

    list_extensions = [".AAA", ".AARP", ".ABARTH", ".ABB", ".ABBOTT", ".ABBVIE", ".ABC", ".ABLE", ".ABOGADO", ".ABUDHABI", ".AC", ".ACADEMY", ".ACCENTURE", ".ACCOUNTANT", ".ACCOUNTANTS", ".ACO", ".ACTOR", ".AD", ".ADAC", ".ADS", ".ADULT", ".AE", ".AEG", ".AERO", ".AETNA", ".AF", ".AFAMILYCOMPANY", ".AFL", ".AFRICA", ".AG", ".AGAKHAN", ".AGENCY", ".AI", ".AIG", ".AIGO", ".AIRBUS", ".AIRFORCE", ".AIRTEL", ".AKDN", ".AL", ".ALFAROMEO", ".ALIBABA", ".ALIPAY", ".ALLFINANZ", ".ALLSTATE", ".ALLY", ".ALSACE", ".ALSTOM", ".AM", ".AMERICANEXPRESS", ".AMERICANFAMILY", ".AMEX", ".AMFAM", ".AMICA", ".AMSTERDAM", ".ANALYTICS", ".ANDROID", ".ANQUAN", ".ANZ", ".AO", ".AOL", ".APARTMENTS", ".APP", ".APPLE", ".AQ", ".AQUARELLE", ".AR", ".ARAB", ".ARAMCO", ".ARCHI", ".ARMY", ".ARPA", ".ART", ".ARTE", ".AS", ".ASDA", ".ASIA", ".ASSOCIATES", ".AT", ".ATHLETA", ".ATTORNEY", ".AU", ".AUCTION", ".AUDI", ".AUDIBLE", ".AUDIO", ".AUSPOST", ".AUTHOR", ".AUTO", ".AUTOS", ".AVIANCA", ".AW", ".AWS", ".AX", ".AXA", ".AZ", ".AZURE", ".BA", ".BABY", ".BAIDU", ".BANAMEX", ".BANANAREPUBLIC", ".BAND", ".BANK", ".BAR", ".BARCELONA", ".BARCLAYCARD", ".BARCLAYS", ".BAREFOOT", ".BARGAINS", ".BASEBALL", ".BASKETBALL", ".BAUHAUS", ".BAYERN", ".BB", ".BBC", ".BBT", ".BBVA", ".BCG", ".BCN", ".BD", ".BE", ".BEATS", ".BEAUTY", ".BEER", ".BENTLEY", ".BERLIN", ".BEST", ".BESTBUY", ".BET", ".BF", ".BG", ".BH", ".BHARTI", ".BI", ".BIBLE", ".BID", ".BIKE", ".BING", ".BINGO", ".BIO", ".BIZ", ".BJ", ".BLACK", ".BLACKFRIDAY", ".BLOCKBUSTER", ".BLOG", ".BLOOMBERG", ".BLUE", ".BM", ".BMS", ".BMW", ".BN", ".BNPPARIBAS", ".BO", ".BOATS", ".BOEHRINGER", ".BOFA", ".BOM", ".BOND", ".BOO", ".BOOK", ".BOOKING", ".BOSCH", ".BOSTIK", ".BOSTON", ".BOT", ".BOUTIQUE", ".BOX", ".BR", ".BRADESCO", ".BRIDGESTONE", ".BROADWAY", ".BROKER", ".BROTHER", ".BRUSSELS", ".BS", ".BT", ".BUDAPEST", ".BUGATTI", ".BUILD", ".BUILDERS", ".BUSINESS", ".BUY", ".BUZZ", ".BV", ".BW", ".BY", ".BZ", ".BZH", ".CA", ".CAB", ".CAFE", ".CAL", ".CALL", ".CALVINKLEIN", ".CAM", ".CAMERA", ".CAMP", ".CANCERRESEARCH", ".CANON", ".CAPETOWN", ".CAPITAL", ".CAPITALONE", ".CAR", ".CARAVAN", ".CARDS", ".CARE", ".CAREER", ".CAREERS", ".CARS", ".CASA", ".CASE", ".CASEIH", ".CASH", ".CASINO", ".CAT", ".CATERING", ".CATHOLIC", ".CBA", ".CBN", ".CBRE", ".CBS", ".CC", ".CD", ".CEB", ".CENTER", ".CEO", ".CERN", ".CF", ".CFA", ".CFD", ".CG", ".CH", ".CHANEL", ".CHANNEL", ".CHARITY", ".CHASE", ".CHAT", ".CHEAP", ".CHINTAI", ".CHRISTMAS", ".CHROME", ".CHURCH", ".CI", ".CIPRIANI", ".CIRCLE", ".CISCO", ".CITADEL", ".CITI", ".CITIC", ".CITY", ".CITYEATS", ".CK", ".CL", ".CLAIMS", ".CLEANING", ".CLICK", ".CLINIC", ".CLINIQUE", ".CLOTHING", ".CLOUD", ".CLUB", ".CLUBMED", ".CM", ".CN", ".CO", ".COACH", ".CODES", ".COFFEE", ".COLLEGE", ".COLOGNE", ".COM", ".COMCAST", ".COMMBANK", ".COMMUNITY", ".COMPANY", ".COMPARE", ".COMPUTER", ".COMSEC", ".CONDOS", ".CONSTRUCTION", ".CONSULTING", ".CONTACT", ".CONTRACTORS", ".COOKING", ".COOKINGCHANNEL", ".COOL", ".COOP", ".CORSICA", ".COUNTRY", ".COUPON", ".COUPONS", ".COURSES", ".CPA", ".CR", ".CREDIT", ".CREDITCARD", ".CREDITUNION", ".CRICKET", ".CROWN", ".CRS", ".CRUISE", ".CRUISES", ".CSC", ".CU", ".CUISINELLA", ".CV", ".CW", ".CX", ".CY", ".CYMRU", ".CYOU", ".CZ", ".DABUR", ".DAD", ".DANCE", ".DATA", ".DATE", ".DATING", ".DATSUN", ".DAY", ".DCLK", ".DDS", ".DE", ".DEAL", ".DEALER", ".DEALS", ".DEGREE", ".DELIVERY", ".DELL", ".DELOITTE", ".DELTA", ".DEMOCRAT", ".DENTAL", ".DENTIST", ".DESI", ".DESIGN", ".DEV", ".DHL", ".DIAMONDS", ".DIET", ".DIGITAL", ".DIRECT", ".DIRECTORY", ".DISCOUNT", ".DISCOVER", ".DISH", ".DIY", ".DJ", ".DK", ".DM", ".DNP", ".DO", ".DOCS", ".DOCTOR", ".DOG", ".DOMAINS", ".DOT", ".DOWNLOAD", ".DRIVE", ".DTV", ".DUBAI", ".DUCK", ".DUNLOP", ".DUPONT", ".DURBAN", ".DVAG", ".DVR", ".DZ", ".EARTH", ".EAT", ".EC", ".ECO", ".EDEKA", ".EDU", ".EDUCATION", ".EE", ".EG", ".EMAIL", ".EMERCK", ".ENERGY", ".ENGINEER", ".ENGINEERING", ".ENTERPRISES", ".EPSON", ".EQUIPMENT", ".ER", ".ERICSSON", ".ERNI", ".ES", ".ESQ", ".ESTATE", ".ESURANCE", ".ET", ".ETISALAT", ".EU", ".EUROVISION", ".EUS", ".EVENTS", ".EXCHANGE", ".EXPERT", ".EXPOSED", ".EXPRESS", ".EXTRASPACE", ".FAGE", ".FAIL", ".FAIRWINDS", ".FAITH", ".FAMILY", ".FAN", ".FANS", ".FARM", ".FARMERS", ".FASHION", ".FAST", ".FEDEX", ".FEEDBACK", ".FERRARI", ".FERRERO", ".FI", ".FIAT", ".FIDELITY", ".FIDO", ".FILM", ".FINAL", ".FINANCE", ".FINANCIAL", ".FIRE", ".FIRESTONE", ".FIRMDALE", ".FISH", ".FISHING", ".FIT", ".FITNESS", ".FJ", ".FK", ".FLICKR", ".FLIGHTS", ".FLIR", ".FLORIST", ".FLOWERS", ".FLY", ".FM", ".FO", ".FOO", ".FOOD", ".FOODNETWORK", ".FOOTBALL", ".FORD", ".FOREX", ".FORSALE", ".FORUM", ".FOUNDATION", ".FOX", ".FR", ".FREE", ".FRESENIUS", ".FRL", ".FROGANS", ".FRONTDOOR", ".FRONTIER", ".FTR", ".FUJITSU", ".FUJIXEROX", ".FUN", ".FUND", ".FURNITURE", ".FUTBOL", ".FYI", ".GA", ".GAL", ".GALLERY", ".GALLO", ".GALLUP", ".GAME", ".GAMES", ".GAP", ".GARDEN", ".GAY", ".GB", ".GBIZ", ".GD", ".GDN", ".GE", ".GEA", ".GENT", ".GENTING", ".GEORGE", ".GF", ".GG", ".GGEE", ".GH", ".GI", ".GIFT", ".GIFTS", ".GIVES", ".GIVING", ".GL", ".GLADE", ".GLASS", ".GLE", ".GLOBAL", ".GLOBO", ".GM", ".GMAIL", ".GMBH", ".GMO", ".GMX", ".GN", ".GODADDY", ".GOLD", ".GOLDPOINT", ".GOLF", ".GOO", ".GOODYEAR", ".GOOG", ".GOOGLE", ".GOP", ".GOT", ".GOV", ".GP", ".GQ", ".GR", ".GRAINGER", ".GRAPHICS", ".GRATIS", ".GREEN", ".GRIPE", ".GROCERY", ".GROUP", ".GS", ".GT", ".GU", ".GUARDIAN", ".GUCCI", ".GUGE", ".GUIDE", ".GUITARS", ".GURU", ".GW", ".GY", ".HAIR", ".HAMBURG", ".HANGOUT", ".HAUS", ".HBO", ".HDFC", ".HDFCBANK", ".HEALTH", ".HEALTHCARE", ".HELP", ".HELSINKI", ".HERE", ".HERMES", ".HGTV", ".HIPHOP", ".HISAMITSU", ".HITACHI", ".HIV", ".HK", ".HKT", ".HM", ".HN", ".HOCKEY", ".HOLDINGS", ".HOLIDAY", ".HOMEDEPOT", ".HOMEGOODS", ".HOMES", ".HOMESENSE", ".HONDA", ".HORSE", ".HOSPITAL", ".HOST", ".HOSTING", ".HOT", ".HOTELES", ".HOTELS", ".HOTMAIL", ".HOUSE", ".HOW", ".HR", ".HSBC", ".HT", ".HU", ".HUGHES", ".HYATT", ".HYUNDAI", ".IBM", ".ICBC", ".ICE", ".ICU", ".ID", ".IE", ".IEEE", ".IFM", ".IKANO", ".IL", ".IM", ".IMAMAT", ".IMDB", ".IMMO", ".IMMOBILIEN", ".IN", ".INC", ".INDUSTRIES", ".INFINITI", ".INFO", ".ING", ".INK", ".INSTITUTE", ".INSURANCE", ".INSURE", ".INT", ".INTEL", ".INTERNATIONAL", ".INTUIT", ".INVESTMENTS", ".IO", ".IPIRANGA", ".IQ", ".IR", ".IRISH", ".IS", ".ISMAILI", ".IST", ".ISTANBUL", ".IT", ".ITAU", ".ITV", ".IVECO", ".JAGUAR", ".JAVA", ".JCB", ".JCP", ".JE", ".JEEP", ".JETZT", ".JEWELRY", ".JIO", ".JLL", ".JM", ".JMP", ".JNJ", ".JO", ".JOBS", ".JOBURG", ".JOT", ".JOY", ".JP", ".JPMORGAN", ".JPRS", ".JUEGOS", ".JUNIPER", ".KAUFEN", ".KDDI", ".KE", ".KERRYHOTELS", ".KERRYLOGISTICS", ".KERRYPROPERTIES", ".KFH", ".KG", ".KH", ".KI", ".KIA", ".KIM", ".KINDER", ".KINDLE", ".KITCHEN", ".KIWI", ".KM", ".KN", ".KOELN", ".KOMATSU", ".KOSHER", ".KP", ".KPMG", ".KPN", ".KR", ".KRD", ".KRED", ".KUOKGROUP", ".KW", ".KY", ".KYOTO", ".KZ", ".LA", ".LACAIXA", ".LAMBORGHINI", ".LAMER", ".LANCASTER", ".LANCIA", ".LAND", ".LANDROVER", ".LANXESS", ".LASALLE", ".LAT", ".LATINO", ".LATROBE", ".LAW", ".LAWYER", ".LB", ".LC", ".LDS", ".LEASE", ".LECLERC", ".LEFRAK", ".LEGAL", ".LEGO", ".LEXUS", ".LGBT", ".LI", ".LIDL", ".LIFE", ".LIFEINSURANCE", ".LIFESTYLE", ".LIGHTING", ".LIKE", ".LILLY", ".LIMITED", ".LIMO", ".LINCOLN", ".LINDE", ".LINK", ".LIPSY", ".LIVE", ".LIVING", ".LIXIL", ".LK", ".LLC", ".LLP", ".LOAN", ".LOANS", ".LOCKER", ".LOCUS", ".LOFT", ".LOL", ".LONDON", ".LOTTE", ".LOTTO", ".LOVE", ".LPL", ".LPLFINANCIAL", ".LR", ".LS", ".LT", ".LTD", ".LTDA", ".LU", ".LUNDBECK", ".LUPIN", ".LUXE", ".LUXURY", ".LV", ".LY", ".MA", ".MACYS", ".MADRID", ".MAIF", ".MAISON", ".MAKEUP", ".MAN", ".MANAGEMENT", ".MANGO", ".MAP", ".MARKET", ".MARKETING", ".MARKETS", ".MARRIOTT", ".MARSHALLS", ".MASERATI", ".MATTEL", ".MBA", ".MC", ".MCKINSEY", ".MD", ".ME", ".MED", ".MEDIA", ".MEET", ".MELBOURNE", ".MEME", ".MEMORIAL", ".MEN", ".MENU", ".MERCKMSD", ".METLIFE", ".MG", ".MH", ".MIAMI", ".MICROSOFT", ".MIL", ".MINI", ".MINT", ".MIT", ".MITSUBISHI", ".MK", ".ML", ".MLB", ".MLS", ".MM", ".MMA", ".MN", ".MO", ".MOBI", ".MOBILE", ".MODA", ".MOE", ".MOI", ".MOM", ".MONASH", ".MONEY", ".MONSTER", ".MORMON", ".MORTGAGE", ".MOSCOW", ".MOTO", ".MOTORCYCLES", ".MOV", ".MOVIE", ".MP", ".MQ", ".MR", ".MS", ".MSD", ".MT", ".MTN", ".MTR", ".MU", ".MUSEUM", ".MUTUAL", ".MV", ".MW", ".MX", ".MY", ".MZ", ".NA", ".NAB", ".NAGOYA", ".NAME", ".NATIONWIDE", ".NATURA", ".NAVY", ".NBA", ".NC", ".NE", ".NEC", ".NET", ".NETBANK", ".NETFLIX", ".NETWORK", ".NEUSTAR", ".NEW", ".NEWHOLLAND", ".NEWS", ".NEXT", ".NEXTDIRECT", ".NEXUS", ".NF", ".NFL", ".NG", ".NGO", ".NHK", ".NI", ".NICO", ".NIKE", ".NIKON", ".NINJA", ".NISSAN", ".NISSAY", ".NL", ".NO", ".NOKIA", ".NORTHWESTERNMUTUAL", ".NORTON", ".NOW", ".NOWRUZ", ".NOWTV", ".NP", ".NR", ".NRA", ".NRW", ".NTT", ".NU", ".NYC", ".NZ", ".OBI", ".OBSERVER", ".OFF", ".OFFICE", ".OKINAWA", ".OLAYAN", ".OLAYANGROUP", ".OLDNAVY", ".OLLO", ".OM", ".OMEGA", ".ONE", ".ONG", ".ONL", ".ONLINE", ".ONYOURSIDE", ".OOO", ".OPEN", ".ORACLE", ".ORANGE", ".ORG", ".ORGANIC", ".ORIGINS", ".OSAKA", ".OTSUKA", ".OTT", ".OVH", ".PA", ".PAGE", ".PANASONIC", ".PARIS", ".PARS", ".PARTNERS", ".PARTS", ".PARTY", ".PASSAGENS", ".PAY", ".PCCW", ".PE", ".PET", ".PF", ".PFIZER", ".PG", ".PH", ".PHARMACY", ".PHD", ".PHILIPS", ".PHONE", ".PHOTO", ".PHOTOGRAPHY", ".PHOTOS", ".PHYSIO", ".PICS", ".PICTET", ".PICTURES", ".PID", ".PIN", ".PING", ".PINK", ".PIONEER", ".PIZZA", ".PK", ".PL", ".PLACE", ".PLAY", ".PLAYSTATION", ".PLUMBING", ".PLUS", ".PM", ".PN", ".PNC", ".POHL", ".POKER", ".POLITIE", ".PORN", ".POST", ".PR", ".PRAMERICA", ".PRAXI", ".PRESS", ".PRIME", ".PRO", ".PROD", ".PRODUCTIONS", ".PROF", ".PROGRESSIVE", ".PROMO", ".PROPERTIES", ".PROPERTY", ".PROTECTION", ".PRU", ".PRUDENTIAL", ".PS", ".PT", ".PUB", ".PW", ".PWC", ".PY", ".QA", ".QPON", ".QUEBEC", ".QUEST", ".QVC", ".RACING", ".RADIO", ".RAID", ".RE", ".READ", ".REALESTATE", ".REALTOR", ".REALTY", ".RECIPES", ".RED", ".REDSTONE", ".REDUMBRELLA", ".REHAB", ".REISE", ".REISEN", ".REIT", ".RELIANCE", ".REN", ".RENT", ".RENTALS", ".REPAIR", ".REPORT", ".REPUBLICAN", ".REST", ".RESTAURANT", ".REVIEW", ".REVIEWS", ".REXROTH", ".RICH", ".RICHARDLI", ".RICOH", ".RIGHTATHOME", ".RIL", ".RIO", ".RIP", ".RMIT", ".RO", ".ROCHER", ".ROCKS", ".RODEO", ".ROGERS", ".ROOM", ".RS", ".RSVP", ".RU", ".RUGBY", ".RUHR", ".RUN", ".RW", ".RWE", ".RYUKYU", ".SA", ".SAARLAND", ".SAFE", ".SAFETY", ".SAKURA", ".SALE", ".SALON", ".SAMSCLUB", ".SAMSUNG", ".SANDVIK", ".SANDVIKCOROMANT", ".SANOFI", ".SAP", ".SARL", ".SAS", ".SAVE", ".SAXO", ".SB", ".SBI", ".SBS", ".SC", ".SCA", ".SCB", ".SCHAEFFLER", ".SCHMIDT", ".SCHOLARSHIPS", ".SCHOOL", ".SCHULE", ".SCHWARZ", ".SCIENCE", ".SCJOHNSON", ".SCOR", ".SCOT", ".SD", ".SE", ".SEARCH", ".SEAT", ".SECURE", ".SECURITY", ".SEEK", ".SELECT", ".SENER", ".SERVICES", ".SES", ".SEVEN", ".SEW", ".SEX", ".SEXY", ".SFR", ".SG", ".SH", ".SHANGRILA", ".SHARP", ".SHAW", ".SHELL", ".SHIA", ".SHIKSHA", ".SHOES", ".SHOP", ".SHOPPING", ".SHOUJI", ".SHOW", ".SHOWTIME", ".SHRIRAM", ".SI", ".SILK", ".SINA", ".SINGLES", ".SITE", ".SJ", ".SK", ".SKI", ".SKIN", ".SKY", ".SKYPE", ".SL", ".SLING", ".SM", ".SMART", ".SMILE", ".SN", ".SNCF", ".SO", ".SOCCER", ".SOCIAL", ".SOFTBANK", ".SOFTWARE", ".SOHU", ".SOLAR", ".SOLUTIONS", ".SONG", ".SONY", ".SOY", ".SPACE", ".SPORT", ".SPOT", ".SPREADBETTING", ".SR", ".SRL", ".SS", ".ST", ".STADA", ".STAPLES", ".STAR", ".STATEBANK", ".STATEFARM", ".STC", ".STCGROUP", ".STOCKHOLM", ".STORAGE", ".STORE", ".STREAM", ".STUDIO", ".STUDY", ".STYLE", ".SU", ".SUCKS", ".SUPPLIES", ".SUPPLY", ".SUPPORT", ".SURF", ".SURGERY", ".SUZUKI", ".SV", ".SWATCH", ".SWIFTCOVER", ".SWISS", ".SX", ".SY", ".SYDNEY", ".SYMANTEC", ".SYSTEMS", ".SZ", ".TAB", ".TAIPEI", ".TALK", ".TAOBAO", ".TARGET", ".TATAMOTORS", ".TATAR", ".TATTOO", ".TAX", ".TAXI", ".TC", ".TCI", ".TD", ".TDK", ".TEAM", ".TECH", ".TECHNOLOGY", ".TEL", ".TEMASEK", ".TENNIS", ".TEVA", ".TF", ".TG", ".TH", ".THD", ".THEATER", ".THEATRE", ".TIAA", ".TICKETS", ".TIENDA", ".TIFFANY", ".TIPS", ".TIRES", ".TIROL", ".TJ", ".TJMAXX", ".TJX", ".TK", ".TKMAXX", ".TL", ".TM", ".TMALL", ".TN", ".TO", ".TODAY", ".TOKYO", ".TOOLS", ".TOP", ".TORAY", ".TOSHIBA", ".TOTAL", ".TOURS", ".TOWN", ".TOYOTA", ".TOYS", ".TR", ".TRADE", ".TRADING", ".TRAINING", ".TRAVEL", ".TRAVELCHANNEL", ".TRAVELERS", ".TRAVELERSINSURANCE", ".TRUST", ".TRV", ".TT", ".TUBE", ".TUI", ".TUNES", ".TUSHU", ".TV", ".TVS", ".TW", ".TZ", ".UA", ".UBANK", ".UBS", ".UG", ".UK", ".UNICOM", ".UNIVERSITY", ".UNO", ".UOL", ".UPS", ".US", ".UY", ".UZ", ".VA", ".VACATIONS", ".VANA", ".VANGUARD", ".VC", ".VE", ".VEGAS", ".VENTURES", ".VERISIGN", ".VERSICHERUNG", ".VET", ".VG", ".VI", ".VIAJES", ".VIDEO", ".VIG", ".VIKING", ".VILLAS", ".VIN", ".VIP", ".VIRGIN", ".VISA", ".VISION", ".VIVA", ".VIVO", ".VLAANDEREN", ".VN", ".VODKA", ".VOLKSWAGEN", ".VOLVO", ".VOTE", ".VOTING", ".VOTO", ".VOYAGE", ".VU", ".VUELOS", ".WALES", ".WALMART", ".WALTER", ".WANG", ".WANGGOU", ".WATCH", ".WATCHES", ".WEATHER", ".WEATHERCHANNEL", ".WEBCAM", ".WEBER", ".WEBSITE", ".WED", ".WEDDING", ".WEIBO", ".WEIR", ".WF", ".WHOSWHO", ".WIEN", ".WIKI", ".WILLIAMHILL", ".WIN", ".WINDOWS", ".WINE", ".WINNERS", ".WME", ".WOLTERSKLUWER", ".WOODSIDE", ".WORK", ".WORKS", ".WORLD", ".WOW", ".WS", ".WTC", ".WTF", ".XBOX", ".XEROX", ".XFINITY", ".XIHUAN", ".XIN"]
    # === We remove anything after extension ==============================================================

    for extension in list_extensions:
        extension = str(extension).lower()
        pos_extension = domain_name.find(extension)
        if pos_extension != -1:
            domain_name = domain_name[0:pos_extension + len(extension)]

    return domain_name


def KillPhoneBot():
    logger.info("========================= Start KillPhoneBot ======================================")
    # === Initialisation of SQLITE DB ========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"BASE_DIR : {BASE_DIR}")
    #db_path = os.path.join(BASE_DIR, "db.db")
    db_path=LoadFile("db.db")
    sqlite_connection = sqlite3.connect(db_path)
    sqlite_cursor = sqlite_connection.cursor()

    if platform.system() == 'Windows':
        PROCNAME = "PhoneBot.exe"
        PROCNAME_ADB = "adb.exe"
        PROCNAME_NODE = "node.exe"

    elif platform.system() == 'Darwin':
        PROCNAME = "PhoneBot"
        PROCNAME_ADB = "adb"
        PROCNAME_NODE = "node"

    elif platform.system() == 'Linux':
        PROCNAME = "PhoneBot"
        PROCNAME_ADB = "adb"
        PROCNAME_NODE = "node"

    # === Let's know what is actual pid =======================
    mypid = os.getpid()
    print(f"PID of PhoneBot : {mypid}")

    # === 1rst we check if a row was created in table settings
    id_settings_tuple = sqlite_cursor.execute("SELECT id FROM settings").fetchall()
    print(f"id_settings_tuple : {id_settings_tuple} - {type(id_settings_tuple)}")
    if id_settings_tuple:
        id_settings = id_settings_tuple[0][0]
        print(f"id_settings : {id_settings} - {type(id_settings)}")

    # === 2nd we need to check in database if there is a PID ======
    open_pid_tuple = sqlite_cursor.execute("SELECT pid FROM settings").fetchone()
    print(f"open_pid_tuple : {open_pid_tuple} - {type(open_pid_tuple)}")
    # === 3rd, We kill the process if exist, Else we add actual process in database
    if open_pid_tuple:
        logger.info(
            "PhoneBot found a PID in local table. that means another instance of PhoneBot may be running... Let's KILL it.")
        open_pid = open_pid_tuple[0]
        print(f"Previous PID of previous PhoneBot  : {open_pid} - {type(open_pid)}")
        if mypid != open_pid:

            try:
                p = psutil.Process(open_pid)
                if p.name == PROCNAME:
                    p.terminate()
                if p.name == PROCNAME_ADB:
                    p.terminate()
                if p.name == PROCNAME_NODE:
                    p.terminate()
            except Exception as ex:
                logger.error(
                    f"{ex} --> PhoneBot failed to close another instance of PhoneBot N°{open_pid}. Maybe this instance was already killed.")

    # === This method sometimes failed, so to be sure, we will scroll all the process and kill all the phonebot.exe process which is not the current one.

    for proc in psutil.process_iter():
        # print(proc.name)
        # print(proc.name())
        # print(proc.pid)

        if(proc.name == PROCNAME or proc.name()==PROCNAME) :
            if proc.pid != mypid:
                print(f"PhoneBot will kill this process : {proc}")
                proc.kill()

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME_ADB or proc.name()==PROCNAME_ADB:
            print(f"PhoneBot will kill this process : {proc}")
            proc.kill()

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME_NODE or proc.name()==PROCNAME_NODE:
            print(f"PhoneBot will kill this process : {proc}")
            proc.kill()

    # === Now we need to update the lcoal database table settings with new PID wich is running =========================
    # === 2 scenarios:
    # === If it is first time the bot is running we need to INSERT
    # === If it NOT the first time the bot is running we need to UPDATE

    if id_settings_tuple:
        sqlite_cursor.execute("UPDATE settings set pid=? WHERE id=?",(mypid, id_settings))
        sqlite_connection.commit()
        logger.info("PhoneBot UPDATE PID in local database")
    else:
        sqlite_cursor.execute("INSERT INTO settings(pid) VALUES(?)",(mypid,))
        sqlite_connection.commit()
        logger.info("PhoneBot INSERT PID in local database as it is first time running.")



def KillPhoneBotUI():
    # === Initialisation of SQLITE DB ========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"BASE_DIR : {BASE_DIR}")
    db_path=LoadFile("db.db")

    if platform.system() == 'Windows':
        PROCNAME = "PhoneBot.exe"
        PROCNAME_ADB = "adb.exe"
        PROCNAME_NODE = "node.exe"

    elif platform.system() == 'Darwin':
        PROCNAME = "PhoneBot"
        PROCNAME_ADB = "adb"
        PROCNAME_NODE = "node"

    # === Let's know what is actual pid =======================
    mypid = os.getpid()
    print(f"PID of PhoneBot : {mypid}")

    try:
        for proc in psutil.process_iter():
            #print(proc.name)
            #print(proc.name())
            #print(proc.pid)
            if proc.name() == PROCNAME or proc.name()==PROCNAME:
                print(f"PhoneBot will kill this process : {proc}")
                proc.kill()
            if  proc.pid() == mypid:
                print(f"PhoneBot will kill this process : {proc}")
                proc.kill()

        for proc in psutil.process_iter():
            if proc.name() == PROCNAME_ADB or proc.name()==PROCNAME_ADB:
                print(f"PhoneBot will kill this process : {proc}")
                proc.kill()

        for proc in psutil.process_iter():
            if proc.name() == PROCNAME_NODE or proc.name()==PROCNAME_NODE:
                print(f"PhoneBot will kill this process : {proc}")
                proc.kill()
    except Exception as ex:
        logger.error(f"ERROR KillPhoneBotUI : {ex}")



def KillPhoneBot_During_Update():
    if platform.system() == 'Windows':
        PROCNAME = "PhoneBot.exe"
        PROCNAME_ADB = "adb.exe"
        PROCNAME_NODE = "node.exe"

    elif platform.system() == 'Darwin':
        PROCNAME = "PhoneBot"
        PROCNAME_ADB = "adb"
        PROCNAME_NODE = "node"

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            print(f"PhoneBot will kill this process : {proc}")
            try:
                proc.kill()
            except Exception as ex:
                logger.error(f"{ex} - PhoneBot couldn't kill the process")

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME_ADB:
            print(f"PhoneBot will kill this process : {proc}")
            try:
                proc.kill()
            except Exception as ex:
                logger.error(f"{ex} - PhoneBot couldn't kill the process")

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME_NODE:
            print(f"PhoneBot will kill this process : {proc}")
            try:
                proc.kill()
            except Exception as ex:
                logger.error(f"{ex} - PhoneBot couldn't kill the process")

    



def get_product_attributes(p_product_attribute, p_string_attribute):
    #--- this function extract the attribute value out from an attribute string
    #--- p_product_attribute = string which contains all the attributes values. It is a mess, that is why we need this function
    #--- result_attribute is the result attribute of the function which will be given to the variable which will store the value
    #--- p_string_attribute is the  string which will be search in p_product_attribute
    logger.info(f"----------- Starting get_product_attributes function for {p_string_attribute} ---")

    result_attribute = p_product_attribute[p_product_attribute.find(p_string_attribute) + len(
        p_string_attribute) + 19:p_product_attribute.find(p_string_attribute) + len(
        p_string_attribute) + 19 + 2]

    result_attribute=result_attribute.replace('"','')

    logger.info(p_string_attribute + " : " + result_attribute)
    return result_attribute


def verify_appPackage_present(p_platform,p_dico_smartphones):
    """
    This function check if the application is installed on smartphone and it return the dico smartphone updated
    
    """
    
    
    platform_package = p_platform + "_appPackage"
    p_platform=p_platform.replace('_','.')
    adb_command = "adb -s " + p_dico_smartphones['Smartphone_ID'] + " shell pm list packages -f " + p_platform.lower()
    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    print(f"adb_command : {adb_command}")
    result_app_installed = os.popen(adb_command).read()

    if result_app_installed:
        logger.info(f"{p_platform} is installed on Smartphone {p_dico_smartphones['Smartphone_ID']} \n {result_app_installed}")
        # We have special case with mms where it is not /base.apk in our put but /MtkMms.apk
        
        pos_appPackage = result_app_installed.find(".apk=") + len(".apk=")
        p_dico_smartphones[platform_package] = result_app_installed[pos_appPackage:].rstrip("\n")
        print(f"p_dico_smartphones[{platform_package}] : {p_dico_smartphones[platform_package]}")

    else:
        
        # We have an exception here with mms and message app. These apps depends of ANdroid version. So we should ignore them
       
        logger.error(f"There is not {p_platform} application installed on smartphone {p_dico_smartphones['Smartphone_ID']}")
        logger.error(f"If you plan to automate {p_platform}, don't be surprised if you see PhoneBot bugging!!!")

        p_dico_smartphones[platform_package] = ""
        # We add the missing package in key directory missing_packages
        p_dico_smartphones['missing_packages'] += platform_package + ','




        # I commendted the 2 lines below as I don't want to force users to install all these apps. So we will just warn him /her
        #p_dico_smartphones[platform_package] = ''
        #sys.exit()
    return p_dico_smartphones


# ======================================================================================
# ========================= FUNCTION TO GET ANDROID VERSION ============================
# ======================================================================================



# =================================================================================================================
# ============================== FUNCTION TO GET THE LIST OF DEVICES ==============================================
# =================================================================================================================

def adb_devices_list():
    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    devices = os.popen("adb devices -l").read()

    # logger.info(f"devices : {devices}")

    # --- store the result in tmp.txt file

    f = open(LoadFile('tmp.txt'), 'w')
    f.writelines(devices)
    f.close()



    # --- Count the number of connected phones(previous code 1 line per smartphone + the header title + empty footer.
    # --- So we need to count the lines of tmp.txt - 2
    global quantity_connected_phones

    quantity_connected_phones = len(open('tmp.txt').readlines()) - 2




# ===============================================================================
# =================== FUNCTION TO KNOW WHICH SMARTPHONES ARE CONNECTED ==========
# ===============================================================================
def NumberSmartphonesConnected():
    """
    This function will return the number of connected smartphones
    """

    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
        devices = os.popen("adb devices -l").read()
        print(f"NumberSmartphonesConnected => devices : {devices}")
    elif platform.system() == 'Windows':
        devices = os.popen("adb devices -l").read()


    # logger.info(f"devices : {devices}")

    # --- store the result in tmp.txt file

    f = open(LoadFile('tmp.txt'), 'w')
    f.writelines(devices)
    f.close()



    # --- Count the number of connected phones(previous code 1 line per smartphone + the header title + empty footer.
    # --- So we need to count the lines of tmp.txt - 2
    global quantity_connected_phones

    quantity_connected_phones = len(open(LoadFile('tmp.txt')).readlines()) - 2

    if quantity_connected_phones == 0:
        logger.info("PhoneBot can wait until you connect one or several smartphones to your computer throught USB.")
        #CountDown(20)
    else:
        logger.info(f"PhoneBot found these smartphones connected:\n{devices}")
    return quantity_connected_phones













#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------

def EmptyTablesmartphones():
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()

    cursor.execute("DELETE FROM smartphones")
    sqlite_connection.commit()
    logger.info("PhoneBot will empty the table 'smartphones'")

def get_details_smartphones():
    ############################################################################################
    #     I place here the apppackages as I will need it later
    # desired_caps['appActivity'] = ' com.instagram.android/com.instagram.android.activity.MainTabActivity'
    # desired_caps['appActivity'] = 'com.linkedin.android.authenticator.LaunchActivity'
    # desired_caps['appActivity'] = 'fr.leboncoin.ui.activities.MainActivity'
    # desired_caps['appActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'
    # desired_caps['appActivity'] = 'com.twitter.app.main.MainActivity'
    # --- We need to count the number of connected smartphones
    # --- We nitialize dictionnary in order to store all the details of smartphone for Appium
    dico_smartphones = {}  # => Will store the id of each smartphones and desired_caps
    list_smartphones = []  # => Will store the dico of smartphones

    # --- List the connected devices



    number_connected_phones = NumberSmartphonesConnected()
    with open(LoadFile('tmp.txt')) as f:
        lines = f.readlines()
    f.close()

    #logger.info(f"You have {number_connected_phones} smartphone(s) connected on your computer.")
    #logger.info(
    #    "If Phonebot didn't detect some smartphones connected, please be sure to have enabled 'USB debugging mode' => read https://developer.android.com/studio/debug/dev-options.")
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()

    cursor.execute("DELETE FROM smartphones")
    sqlite_connection.commit()
    logger.info("PhoneBot will empty the table 'smartphones'")


    Maximum_number_of_phones = cursor.execute("select value from limits where name_limit=?",('Maximum_number_of_phones',)).fetchone()[0]

    cursor.execute("UPDATE smartphones SET status=?",(0,))

    if number_connected_phones == 0:
        #logger.critical("No smartphoned was found! Please check the USB cable and 'USB debugging mode' is enable. ")
        return number_connected_phones
        #sys.exit()

    elif number_connected_phones > Maximum_number_of_phones:
        logger.critical(f"You don't have permission to connect so many smartphones. Your maximum capacity is {Maximum_number_of_phones} smartphone(s) Maximum! Please upgrate your license in order to get the possibility to connect more smartphones.")
        sys.exit()


    # --- So now we will extract the ID and the deviceName from tmp.txt
    # --- We start first to extract all the lines in a list
    


    # --- then we can extract the id  in a list of dictionnary
    # At the end, it should look something like this
    # list = [
    #    {'smartphone_ID': '41492968379078', 'deviceName': 'S6S5IN3G'},
    #    {'smartphone_ID': '53519716736397', 'deviceName': 'S6S5IN3G'}
    # ]
    i = 0
    print(f"number_connected_phones : {number_connected_phones}")
    while i <(number_connected_phones + 1):
        # --- We extract the ID If we are not reading the first line and the last line of tmp.txt
        try:
            if i != 0 and i !=(number_connected_phones + 1):
                if 'offline' in lines[i]:
                    logger.error(f"One smartphone is not connected to computer.")
                else:
                    first_space_pos = lines[i].find(
                        ' ')  # We try to find position of first space in order to find the ID of smartphone
                    smartphone_id = lines[i][0:first_space_pos]  # We extract the ID of smartphone
                    dico_smartphones["Smartphone_ID"] = smartphone_id  # We add the ID in dico
                    logger.info(f"Smartphone {i} id : {smartphone_id}")

                    device_product_pos = lines[i].find('device product:') + len('device product:')  # We try now to find position of deviceName
                    model_pos = lines[i].find(' model')  # and now the position of "model" in order to extract the deviceName in the middle of the line
                    while model_pos==-1:
                        if platform.system() == 'Darwin':
                            home_user = os.environ['HOME']
                            adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                            proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT)
                        devices = os.popen("adb devices -l").read()
                        
                        f = open(LoadFile('tmp.txt'), 'w')
                        f.writelines(devices)
                        f.close()
                        with open(LoadFile('tmp.txt')) as f:
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



                    dico_smartphones["deviceName"] = deviceName  # We add the deviceName in dico

                    # --- Now we need to check if the apps are installed in smartphone : Facebook, Instagram, Twitter, Linkedin, Leboncoin
                    # --- And we extract the appPackage -----------------------------------------------------------------------------------
                    # --- FACEBOOK -------------------------------------------------------------------------------------------------------
                    dico_smartphones=verify_appPackage_present("Facebook_Katana",dico_smartphones) #for facebook
                    dico_smartphones=verify_appPackage_present("Instagram", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Linkedin", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Leboncoin", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Twitter", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Pagesjaunes", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Reddit", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Facebook_Orca", dico_smartphones) # for messenger
                    dico_smartphones=verify_appPackage_present("android_apps_map", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("ProductHunt", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Meetup", dico_smartphones)
                    dico_smartphones=verify_appPackage_present("Telegram", dico_smartphones)


                    # --- And now the version of Android
                    # This paragraph of code below is necesssary when several smarptohnes have the same udid.
                    # If this is the case, the adb command will return an error message. So we will have to try to get
                    # the android version with another parameter than udid(ex: device, model, etc...)
                    # ==> see https://stackoverflow.com/questions/30214744/using-adb-with-multiple-devices-with-the-same-serial-number

                    adb_command = "adb -s " + dico_smartphones['Smartphone_ID'] + " shell getprop ro.build.version.release"
                    p = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    result_adb_command = str(p.communicate()[1])

                    if result_adb_command.find("error") != -1:
                        print(f"result_adb_command : {result_adb_command}")

                        adb_command = "adb -s model:" + modele_device + " shell getprop ro.build.version.release"
                        p = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        result_adb_command = str(p.communicate()[1])
                        if result_adb_command.find("error") != -1:
                            print(f"result_adb_command : {result_adb_command}")

                            adb_command = "adb -s device:" + device_string + " shell getprop ro.build.version.release"
                            p = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                        if platform.system() == 'Darwin':
                            home_user = os.environ['HOME']
                            adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                            proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT)

                        result_adb_command = str(os.popen(adb_command).read())
                        print(f"result_adb_command : {result_adb_command}")
                        version_android = str(result_adb_command).strip().split('\n\n')
                        print(f"version_android : {version_android}")

                        # --- I need to remove brackets from the string ['6.0'] ---------------------
                        new_version_android_1 = str(version_android).replace("['", "")
                        new_version_android_2 = str(new_version_android_1).replace("']", "")
                        print(f"new_version_android_2 : {new_version_android_2}")
                        # -- I also need to be sure there willl be .O after the digit of version
                        if new_version_android_2.find('.0')==-1:
                            logger.info(f"OS Version = {new_version_android_2}. It miss the '.0' in the version of OS of Smartphone {dico_smartphones['Smartphone_ID']}. ")
                            logger.info(f"We will add '.0' at the end.")
                            new_version_android_2 = new_version_android_2 + ".0"
                            logger.info(f"OS version = {new_version_android_2}")




                        dico_smartphones['version_android'] = str(new_version_android_2)
                        logger.info(f"dico_smartphones['version_android'] : {dico_smartphones['version_android']}")

                        list_smartphones.append(dico_smartphones.copy())  # We add the dico in our list
                        #logger.info(f"{p_udid}|||i=" + str(i) + " dico : " + str(dico_smartphones))
                        #logger.info(f"{p_udid}|||i=" + str(i) + " list : " + str(list_smartphones))

            i += 1
            print(f"i => {i}")
            print("-" * 100)
            print(f"i:{i}/{number_connected_phones}")
            print("-" * 100)
        #except ValueError:
        except Exception as ex:
            logger.critical(f"{ex} -> ERROR getting list of app installed on each smartphone!")
            #print("ERROR getting list of app installed on each smartphone!")

    logger.info("##############################")
    logger.info(f"Final dico : {dico_smartphones}")
    logger.info(f"Final list : {list_smartphones}")

    # --------------------------------------------------------------------------------------------------------------
    # --- So we have everything, we can now store everything in the table "smartphones" from our sqlight db.--------
    # --------------------------------------------------------------------------------------------------------------
    logger.info("------- Starting Saving smartphones details in SQLite local DB ----------")

    #logger.info(f"{p_udid}|||Successfully Connected to SQLite")



    # --- Now that we put status=0 to all the rows of table smartphones, we can check which smartphones is connected and update table
    # --- we loop each smartphones in our list in order to update our DB -----------------------------
    for smartphone in list_smartphones:
        #sql_test_exist_smartphone = "SELECT udid, COUNT(*) FROM smartphones WHERE udid = " + str(smartphone['Smartphone_ID']) + " GROUP BY udid"
        cursor.execute("SELECT udid, COUNT(*) FROM smartphones WHERE udid =? GROUP BY udid",(str(smartphone['Smartphone_ID']),))
        exist = cursor.fetchone()
        # check if it is empty and print error
        if not exist:

            logger.info(f"The smartphone {smartphone['Smartphone_ID']} DOES NOT exist. We add its values in DB")
            #sql_add_smartphone = "INSERT INTO smartphones(udid, devicename, Facebook.Katana_appPackage, Twitter_appPackage, Linkedin_appPackage, Instagram_appPackage,Leboncoin_appPackage, platformversion, status) VALUES('" + str(
            #    smartphone['Smartphone_ID']) + "', '" + str(smartphone['deviceName']) + "', '" + str(
            #    smartphone['Facebook.Katana_appPackage']) + "','" + str(smartphone['Twitter_appPackage']) + "','" + str(
            #    smartphone['Linkedin_appPackage']) + "','" + str(smartphone['Instagram_appPackage']) + "','" + str(
            #    smartphone['Leboncoin_appPackage']) + "','" + str(smartphone['version_android']) + "', 1)" # the int(connected) at the end is the boolean value true for status
            logger.info(f"smartphone['version_android']) : {str(smartphone['version_android'])}")
            cursor = sqlite_connection.cursor()
            cursor.execute("INSERT INTO smartphones(udid, devicename, Facebook_Katana_appPackage, Twitter_appPackage,  \
                        Linkedin_appPackage, Instagram_appPackage,Leboncoin_appPackage,Pagesjaunes_appPackage,  \
                        Facebook_Orca_appPackage,Reddit_appPackage, android_apps_map_appPackage, ProductHunt_appPackage,  \
                        Meetup_appPackage,  Telegram_appPackage, platformversion, OS_device, status)  \
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(str(smartphone['Smartphone_ID']),  str(smartphone['deviceName']),   \
                        str(smartphone['Facebook_Katana_appPackage']),str(smartphone['Twitter_appPackage']),   \
                        str(smartphone['Linkedin_appPackage']) ,str(smartphone['Instagram_appPackage']) ,  \
                        str(smartphone['Leboncoin_appPackage']) , str(smartphone['Pagesjaunes_appPackage']),  \
                        str(smartphone['Facebook_Orca_appPackage']),str(smartphone['Reddit_appPackage']),   \
                        str(smartphone['android_apps_map_appPackage']), str(smartphone['ProductHunt_appPackage']),  \
                        str(smartphone['Meetup_appPackage']),  str(smartphone['Telegram_appPackage']),
                        str(smartphone['version_android']),'Android', 1) # the int(connected) at the end is the boolean value true for status
            )
            sqlite_connection.commit()

        else:

            logger.info(f"str(smartphone['version_android']) : {str(smartphone['version_android'])}")
            logger.info(f"The smartphone " + str(
                smartphone['Smartphone_ID']) + " exist. We update values for this smartphone in DB.")
            values =(str(smartphone['deviceName']), str(smartphone['Facebook_Katana_appPackage']),
                 str(smartphone['Twitter_appPackage']), str(smartphone['Linkedin_appPackage']),
                 str(smartphone['Instagram_appPackage']), str(smartphone['Leboncoin_appPackage']),
                 str(smartphone['Pagesjaunes_appPackage']), str(smartphone['Facebook_Orca_appPackage']),  \
                 str(smartphone['Reddit_appPackage']), str(smartphone['android_apps_map_appPackage']), str(smartphone['ProductHunt_appPackage']), \
                 str(smartphone['Meetup_appPackage']), str(smartphone['Telegram_appPackage']),  \
                 str(smartphone['version_android']),'Android', "1", str(smartphone['Smartphone_ID']))
            #cursor.execute("UPDATE smartphones SET devicename=?, Facebook.Katana_appPackage=?, Twitter_appPackage=?, Linkedin_appPackage=?, Instagram_appPackage=?,Leboncoin_appPackage=?, platformversion=?, status=? WHERE id=? ",(str(smartphone['deviceName']), str(smartphone['Facebook.Katana_appPackage']), str(smartphone['Twitter_appPackage']), str(smartphone['Linkedin_appPackage']), str(smartphone['Instagram_appPackage']), str(smartphone['Leboncoin_appPackage']), str(smartphone['version_android']), "1", str(smartphone['Smartphone_ID'])))

            cursor.execute("UPDATE smartphones SET devicename=?, Facebook_Katana_appPackage=?, Twitter_appPackage=?, \
                        Linkedin_appPackage=?, Instagram_appPackage=?,Leboncoin_appPackage=?,Pagesjaunes_appPackage=?,  \
                        Facebook_Orca_appPackage=?,Reddit_appPackage=?, android_apps_map_appPackage=?, ProductHunt_appPackage=?,  \
                        Meetup_appPackage=?,  Telegram_appPackage=?, platformversion=?, \
                        OS_device=?, status=? WHERE udid=?", values)

            #exist = cursor.fetchall()
            #logger.info(f"{p_udid}|||The fetchall give " + str(exist))
            sqlite_connection.commit()

            logger.info(f"We added the bot details successfully in the DB :-)")
    cursor.close()
    sqlite_connection.close()
    return number_connected_phones


def CheckSoftwareInstalled():
    """
    This function will check is necessary softwares for smartphone automation are installed
    """
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()       
    tuple_softwares_status=sqlite_cursor.execute("SELECT java_ok, node_ok, android_ok, appium_ok, tesseract_ok,  \
        sdkmanager_ok, build_tools_ok FROM settings WHERE id=?",(1,)).fetchone()
    for software_status in tuple_softwares_status:
        print(software_status)
        if software_status == 0 or software_status is None:
            return False
    return True
    




#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
def check_license(p_license_config, p_hash,label_log=''):
    # --- Function to check if license in config.ini is the same than the hash stored in License manager woocommerce table ---
    logger.info(f"------------------- Starting check_license function ------------------------")
    secret = codecs.encode('2b14ceedbf1ad94002d8f9be9e35b744b397bda1dc167c0dbd742cbeddf3b054')
    bkey = p_license_config.encode('ascii')
    h = hmac.new(secret, bkey, hashlib.sha256)
    h = h.hexdigest()


    if h == p_hash:
        logger.info(f"Your license key is correct! :-)")
        label_log.setText("Your license key is correct! :-)")
        return True
    else:
        logger.info(f"Your license key is not correct! :-(")
        label_log.setText("Your license key is not correct! :-(")
        return False




#-------------------------------------------------------------------------------------
#------------------------1rst version of get_daily_mimit method-------------------------

def get_daily_limit(p_product_id):
    logger.info(f"-- We start to collect the daily limit based on product id ---------")
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")

            time.sleep(5)
    mycursor = mydb.cursor(buffered=True)
    sql_get_attribute = "select meta_value from W551je5v_postmeta where post_id = '" + str(
        p_product_id[0]) + "' and meta_key='_product_attributes'"
    mycursor.execute(sql_get_attribute)
    product_attribute = str(mycursor.fetchone())

    # logger.info(f"{p_udid}|||Attribute of product : " + str(product_attribute))

    # --- We need now to prepare sqlite db limits table and config.ini in order to update table limits

    config = configparser.ConfigParser()

    config.read(LoadFile('config.ini'),encoding='utf-8')



    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()
    cursor.execute("DELETE FROM limits")
    sqlite_connection.commit()


    # ---  let's now extract the values of attributes from this meta_value
    # --- Ok. We extract the atribute of product which is a big string full of useless stuff. We need to extract the values we need now!
    # --- NO panic :-) . The line below extract from pos1:pos2, so it is all about calculating the good position of what we need and making a string[pos1:pos2]

    Maximum_number_of_phones = get_product_attributes(product_attribute, "Maximum number of phones")#we get the daily limit
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Maximum_number_of_phones', \
                    Maximum_number_of_phones))

    # ================================ GET THE DAILY LIMITS ====================================================
    # We need to collect these limits from the Mysql table tasks_user

    Daily_limit_Facebook_Share_posts_in_groups = get_product_attributes(product_attribute,
                                                                        "Daily limit Facebook Share posts in groups")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Facebook_Share_posts_in_groups', \
                                                                             Daily_limit_Facebook_Share_posts_in_groups))

    Daily_limit_Facebook_Send_message_to_user = get_product_attributes(product_attribute,
                                                                       "Daily limit Facebook Send message to user")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Facebook_Send_message_to_user', \
                                                                             Daily_limit_Facebook_Send_message_to_user))

    Daily_Limit_Facebook_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                       "Daily Limit Facebook Scrap profil details")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_Limit_Facebook_Scrap_profil_details', \
                                                                             Daily_Limit_Facebook_Scrap_profil_details))


    Daily_limit_Instagram_Scrap_email = get_product_attributes(product_attribute,
                                                               "Daily limit Instagram Scrap email")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Instagram_Scrap_email', \
                                                                             Daily_limit_Instagram_Scrap_email))

    Daily_limit_Instagram_Send_mail = get_product_attributes(product_attribute,
                                                               "Daily limit Instagram Send mail")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Instagram_Send_mail', \
                                                                         Daily_limit_Instagram_Send_mail))

    Daily_limit_Instagram_Scrap_profile_details = get_product_attributes(product_attribute,
                                                               "Daily limit Instagram Scrap profile details")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Instagram_Scrap_profile_details', \
                                                                         Daily_limit_Instagram_Scrap_profile_details))

    Daily_limit_Instagram_Send_message = get_product_attributes(product_attribute,
                                                                "Daily limit Instagram Send message")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Instagram_Send_message', \
                                                                             Daily_limit_Instagram_Send_message))

    Daily_limit_Instagram_Like_pics_of_member = get_product_attributes(product_attribute,
                                                                       "Daily limit Instagram Like pics of member")

    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",('Daily_limit_Instagram_Like_pics_of_member', \
                                                                             Daily_limit_Instagram_Like_pics_of_member))

    Daily_limit_Instagram_Follow_members = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram Follow members")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Instagram_Follow_members', \
                    Daily_limit_Instagram_Follow_members))

    Daily_limit_Instagram_UnFollow = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram UnFollow")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Instagram_UnFollow', \
                    Daily_limit_Instagram_UnFollow))


    Daily_limit_Linkedin_Invite_1rst_connexion_and_message = get_product_attributes(product_attribute,
                                                                                    "Daily limit Linkedin Invite 1rst connexion and message")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Linkedin_Invite_1rst_connexion_and_message', \
                    Daily_limit_Linkedin_Invite_1rst_connexion_and_message ))


    Daily_limit_Linkedin_Send_direct_message_to_contacts = get_product_attributes(product_attribute,
                                                                                  "Daily limit Linkedin Send direct message to contacts")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Linkedin_Send_direct_message_to_contacts', \
                    Daily_limit_Linkedin_Send_direct_message_to_contacts))


    Daily_limit_Linkedin_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                       "Daily limit Linkedin Scrap profil details")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Linkedin_Scrap_profil_details', \
                    Daily_limit_Linkedin_Scrap_profil_details))


    Daily_limit_Leboncoin_Scrap_Phone_number = get_product_attributes(product_attribute,
                                                                      "Daily limit Leboncoin Scrap Phone number")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Leboncoin_Scrap_Phone_number', \
                    Daily_limit_Leboncoin_Scrap_Phone_number))

    Daily_limit_Leboncoin_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                        "Daily limit Leboncoin Scrap profil details")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Leboncoin_Scrap_profil_details', \
                    Daily_limit_Leboncoin_Scrap_profil_details))

    Daily_limit_Leboncoin_Send_direct_message_to_sellers = get_product_attributes(product_attribute,
                                                                                  "Daily limit Leboncoin Send direct message to sellers")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Leboncoin_Send_direct_message_to_sellers', \
                    Daily_limit_Leboncoin_Send_direct_message_to_sellers))

    Daily_limit_Send_SMS = get_product_attributes(product_attribute, "Daily limit Send SMS")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Send_SMS', \
                    Daily_limit_Send_SMS))


    Daily_limit_Twitter_Follow = get_product_attributes(product_attribute, "Daily limit Twitter Follow")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Twitter_Follow', \
                    Daily_limit_Twitter_Follow))

    Daily_limit_Twitter_UnFollow = get_product_attributes(product_attribute, "Daily limit Twitter UnFollow")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Twitter_UnFollow', \
                    Daily_limit_Twitter_UnFollow))

    Daily_limit_Facebook_Add_Friends = get_product_attributes(product_attribute, "Daily limit Facebook Add Friends")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Facebook_Add_Friends', \
                    Daily_limit_Facebook_Add_Friends))

    Daily_limit_Telegram_Send_Message = get_product_attributes(product_attribute, "Daily limit Telegram Send Message")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Telegram_Send_Message', \
                    Daily_limit_Telegram_Send_Message))

    Daily_limit_Gmap_Send_Message = get_product_attributes(product_attribute, "Daily limit Gmap Send Message")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Gmap_Send_Message', \
                    Daily_limit_Gmap_Send_Message))

    Daily_limit_Gmap_Scrap_Business = get_product_attributes(product_attribute, "Daily limit Gmap Scrap Business")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Gmap_Scrap_Business', \
                    Daily_limit_Gmap_Scrap_Business))

    Daily_limit_Twitter_Send_Message = get_product_attributes(product_attribute, "Daily limit Twitter Send Message")
    cursor.execute("INSERT INTO limits(name_limit,value) values(?,?)",
                  ('Daily_limit_Twitter_Send_Message', \
                    Daily_limit_Twitter_Send_Message))





    #--- We can now add these values in our SQLITE table limits -----
    #--- But first we will empty this table limits -----
    sqlite_connection.commit()

    try:
        if cursor:
            cursor.close()
        if sqlite_connection:
            sqlite_connection.close()

        if mycursor:
            mycursor.close()
        if mydb.is_connected():
            mydb.close()

    except:
        logger.error("PhoneBot failed to close Mysql DB and SQLITE connections.")




# ===============================================================================================================
# =========================== 2nde version of GetdailyLimit function ============================================
# ===============================================================================================================

def GetDailyLimit(p_product_id):
    logger.info(f"-- We start to collect the daily limit based on product id ---------")
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")

            time.sleep(5)
    mycursor = mydb.cursor(buffered=True)
    sql_get_attribute = "select meta_value from W551je5v_postmeta where post_id = '" + str(
        p_product_id[0]) + "' and meta_key='_product_attributes'"
    mycursor.execute(sql_get_attribute)
    product_attribute = str(mycursor.fetchone())
    print("*" * 100)
    print("*" * 100)
    print("*" * 100)
    print(f"product_attribute : {product_attribute}")
    print("*" * 100)
    print("*" * 100)
    print("*" * 100)
    # logger.info(f"{p_udid}|||Attribute of product : " + str(product_attribute))

    # --- We need now to prepare sqlite db limits table and config.ini in order to update table limits

    config = configparser.ConfigParser()

    config.read(LoadFile('config.ini'),encoding='utf-8')




    # ---  let's now extract the values of attributes from this meta_value
    # --- Ok. We extract the atribute of product which is a big string full of useless stuff. We need to extract the values we need now!
    # --- NO panic :-) . The line below extract from pos1:pos2, so it is all about calculating the good position of what we need and making a string[pos1:pos2]

    Maximum_number_of_phones = get_product_attributes(product_attribute, "Maximum number of phones")#we get the daily limit

    Daily_limit_Facebook_Share_posts_in_groups = get_product_attributes(product_attribute,
                                                                        "Daily limit Facebook Share posts in groups")
    Daily_limit_Facebook_Send_message_to_user = get_product_attributes(product_attribute,
                                                                       "Daily limit Facebook Send message to user")

    Daily_Limit_Facebook_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                       "Daily Limit Facebook Scrap profil details")

    Daily_limit_Instagram_Scrap_email = get_product_attributes(product_attribute,
                                                               "Daily limit Instagram Scrap email")

    Daily_limit_Instagram_Send_mail = get_product_attributes(product_attribute,
                                                               "Daily limit Instagram Send mail")
    Daily_limit_Instagram_Scrap_profile_details = get_product_attributes(product_attribute,
                                                                         "Daily limit Instagram Scrap profile details")

    Daily_limit_Instagram_Send_message = get_product_attributes(product_attribute,
                                                                "Daily limit Instagram Send message")

    Daily_limit_Instagram_Like_pics_of_member = get_product_attributes(product_attribute,
                                                                       "Daily limit Instagram Like pics of member")


    Daily_limit_Instagram_Follow_members = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram Follow members")
    Daily_limit_Instagram_Like_random_picture = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram Like random picture")
    Daily_limit_Instagram_Upload_pictures = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram Upload pictures")

    Daily_limit_Instagram_UnFollow = get_product_attributes(product_attribute,
                                                                  "Daily limit Instagram UnFollow")
    print(f"get product attributes Daily_limit_Instagram_UnFollow => {Daily_limit_Instagram_UnFollow}")

    Daily_limit_Linkedin_Invite_1rst_connexion_and_message = get_product_attributes(product_attribute,
                                                                                    "Daily limit Linkedin Invite 1rst connexion and message")

    Daily_limit_Linkedin_Send_direct_message_to_contacts = get_product_attributes(product_attribute,
                                                                                  "Daily limit Linkedin Send direct message to contacts")

    Daily_limit_Linkedin_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                       "Daily limit Linkedin Scrap profil details")

    Daily_limit_Leboncoin_Scrap_Phone_number = get_product_attributes(product_attribute,
                                                                      "Daily limit Leboncoin Scrap Phone number")

    Daily_limit_Leboncoin_Scrap_profil_details = get_product_attributes(product_attribute,
                                                                        "Daily limit Leboncoin Scrap profil details")

    Daily_limit_Leboncoin_Send_direct_message_to_sellers = get_product_attributes(product_attribute,
                                                                                  "Daily limit Leboncoin Send direct message to sellers")

    Daily_limit_Send_SMS = get_product_attributes(product_attribute, "Daily limit Send SMS")

    Daily_limit_Twitter_Follow = get_product_attributes(product_attribute, "Daily limit Twitter Follow")

    Daily_limit_Twitter_UnFollow = get_product_attributes(product_attribute, "Daily limit Twitter UnFollow")

    Daily_limit_Facebook_Add_Friends = get_product_attributes(product_attribute, "Daily limit Facebook Add Friends")

    Daily_limit_Telegram_Send_Message = get_product_attributes(product_attribute, "Daily limit Telegram Send Message")

    Daily_limit_Gmap_Send_Message = get_product_attributes(product_attribute, "Daily limit Gmap Send Message")

    Daily_limit_Gmap_Scrap_Business = get_product_attributes(product_attribute, "Daily limit Gmap Scrap Business")

    Daily_limit_Twitter_Send_Message = get_product_attributes(product_attribute, "Daily limit Twitter Send Message")

    #--- We can now add these values in our SQLITE table limits -----
    #--- But first we will empty this table limits -----


    try:
        if mydb.is_connected():
            mydb.close()
    except:
        logger.error("PhoneBot failed to close Mysql DB connection.")

    return Daily_limit_Facebook_Add_Friends,  \
            Daily_Limit_Facebook_Scrap_profil_details,  \
            Daily_limit_Facebook_Send_message_to_user,  \
            Daily_limit_Facebook_Share_posts_in_groups,  \
            Daily_limit_Gmap_Scrap_Business,  \
            Daily_limit_Gmap_Send_Message,  \
            Daily_limit_Instagram_Follow_members, \
            Daily_limit_Instagram_UnFollow, \
            Daily_limit_Instagram_Like_random_picture, \
            Daily_limit_Instagram_Upload_pictures, \
            Daily_limit_Instagram_Like_pics_of_member,  \
            Daily_limit_Instagram_Scrap_email, \
            Daily_limit_Instagram_Send_mail, \
            Daily_limit_Instagram_Scrap_profile_details,  \
            Daily_limit_Instagram_Send_message,  \
            Daily_limit_Leboncoin_Scrap_Phone_number,  \
            Daily_limit_Leboncoin_Scrap_profil_details,  \
            Daily_limit_Leboncoin_Send_direct_message_to_sellers,  \
            Daily_limit_Linkedin_Invite_1rst_connexion_and_message,  \
            Daily_limit_Linkedin_Scrap_profil_details,  \
            Daily_limit_Linkedin_Send_direct_message_to_contacts,  \
            Daily_limit_Send_SMS,  \
            Daily_limit_Telegram_Send_Message,  \
            Daily_limit_Twitter_Follow,  \
            Daily_limit_Twitter_UnFollow, \
            Daily_limit_Twitter_Send_Message
        #-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
def CheckProductID(license_key_config):
    """
    This function return True if product id is found or False if product id is not found
    """
    logger.info(f"---------------- Starting initialize_phonebot function ---------------------")

    plan_purchased = license_key_config[0:4]
    logger.info(f"You purchased the plan " + plan_purchased)
    # --- Let's now extract the meta_value of table postmeta of Woocommerce product
    #--- We connect to database of Phonebot
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")

            time.sleep(5)
    mycursor = mydb.cursor(buffered=True)
    
    sql_find_product_id = "SELECT ID from W551je5v_posts WHERE post_type LIKE 'product' AND post_title like '%" + plan_purchased + "%'"
    mycursor.execute(sql_find_product_id)
    product_id = mycursor.fetchone()
    # check if it is empty and print error
    if not product_id:
        # Let's check if it is affiliate plan(platinium plan)
        if license_key_config=="affiliate":
            product_id = 11271
            return True            

        else:


            logger.error(f"We didn't find the product ID. It means we don't know which plan you purchased on Phonebot.co :-( Please contact support@phonebot.co")
            PopupMessage("Problem with your License Key!","There is a problem with your License Key. Please check your License key on https://phonebot.co/my-account/view-license-keys/.\nIt needs to be the same than the one you typed here in the PhoneBot software('Settings' tab).")
            return False
            try:
                mydb.close
            except:
                logger.error("PhoneBot failed to close Mysql DB connection.")
            #sys.exit()
    else:
        logger.info(f"We found the product ID. :-)")        
        return True
        try:
            mydb.close
        except:
            logger.error("PhoneBot failed to close Mysql DB connection.")
def GetAllTasksDetailsInsertDB(p_campaign_id):
    """
    This function get the campaign ID and it will collect the daily limits,
    messages, targets, etc... of each task and update the table tasksuser
    """
    # Connect to MYSQL
    mysql_connection, mysql_cursor = get_mysql_connection()
    SQL_DETAILS_OF_TASKS = f"SELECT * FROM W551je5v_pb_tasks_users WHERE enable=1 AND id_campaign={p_campaign_id}"
    #print(f"SQL_DETAILS_OF_TASKS : {SQL_DETAILS_OF_TASKS}")
    # Connect to SQLITE
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    # Test if tasks_user table exist
    # We empty the table tasks_user
    sqlite_cursor.execute("DELETE FROM tasks_user")
    #sqlite_cursor.execute("VACUUM")
    sqlite_connection.commit()

    mysql_cursor.execute(SQL_DETAILS_OF_TASKS)
    tuple_all_tasks_user = mysql_cursor.fetchall()
    list_task_user=[]
    for task_user in tuple_all_tasks_user:
        print(task_user)
        mysql_cursor.execute(
            f"SELECT smartphone_allowed,computer_allowed FROM W551je5v_pb_tasks WHERE id={task_user['id_task']}")
        smartphone_computer_allowed_tuple = mysql_cursor.fetchone()
        #print(f"smartphone_computer_allowed_tuple : {smartphone_computer_allowed_tuple}")
    
        sqlite_cursor.execute("INSERT INTO tasks_user(id,enable,id_task,id_campaign,url_keywords,minimum,url_list,  \
            url_usernames,message_txt_invitation_1B,message_txt_1A,message_txt_2A,message_txt_3A,message_txt_4A,  \
            message_voice_1A,message_voice_2A,message_voice_3A,message_voice_4A,message_txt_invitation_1A,message_txt_1B,  \
            message_txt_2B,message_txt_3B,message_txt_4B,message_voice_1B,message_voice_2B,message_voice_3B,  \
            message_voice_4B,date_counter_test_AB,time_delay_1A,time_delay_1A_type,time_delay_2A,time_delay_2A_type,  \
            time_delay_3A,time_delay_3A_type,time_delay_1B,time_delay_1B_type,time_delay_2B,time_delay_2B_type,  \
            time_delay_3B,time_delay_3B_type,message_1A_choice,message_2A_choice,message_3A_choice,message_4A_choice,  \
            message_1B_choice,message_2B_choice,message_3B_choice,message_4B_choice,AB_testing_enable,AB_testing_enable_invitation,  \
            date_AB_testing,date_AB_testing_invitation,serie_type,daily_limit,smartphone_allowed,computer_allowed) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,  \
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",  \
           (task_user['id'],task_user['enable'],task_user['id_task'],task_user['id_campaign'],task_user['url_keywords'],task_user['minimum'],task_user['url_list'],  \
            task_user['url_usernames'],task_user['message_txt_invitation_1B'],task_user['message_txt_1A'],task_user['message_txt_2A'],task_user['message_txt_3A'],  \
                task_user['message_txt_4A'],task_user['message_voice_1A'],task_user['message_voice_2A'],task_user['message_voice_3A'],task_user['message_voice_4A'],task_user['message_txt_invitation_1A'],  \
                task_user['message_txt_1B'],task_user['message_txt_2B'],task_user['message_txt_3B'],task_user['message_txt_4B'],task_user['message_voice_1B'],task_user['message_voice_2B'],task_user['message_voice_3B'],  \
                task_user['message_voice_4B'],task_user['date_counter_test_AB'],task_user['time_delay_1A'],task_user['time_delay_1A_type'],task_user['time_delay_2A'],task_user['time_delay_2A_type'],  \
                task_user['time_delay_3A'],task_user['time_delay_3A_type'],task_user['time_delay_1B'],task_user['time_delay_1B_type'],task_user['time_delay_2B'],task_user['time_delay_2B_type'],  \
                task_user['time_delay_3B'],task_user['time_delay_3B_type'],task_user['message_1A_choice'],task_user['message_2A_choice'],task_user['message_3A_choice'],task_user['message_4A_choice'],  \
                task_user['message_1B_choice'],task_user['message_2B_choice'],task_user['message_3B_choice'],task_user['message_4B_choice'],task_user['AB_testing_enable'],task_user['AB_testing_enable_invitation'],  \
                task_user['date_AB_testing'],task_user['date_AB_testing_invitation'],task_user['serie_type'],task_user['daily_limit'],smartphone_computer_allowed_tuple['smartphone_allowed'],smartphone_computer_allowed_tuple['computer_allowed']))

        sqlite_connection.commit()


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


def GetAllTasksDetails(p_campaign_id,p_device=''):
    """
    This function get the campaign ID and it will collect the daily limits,
    messages, targets, etc... of each task and update the table tasksuser
    """
    # Connect to MYSQL
    mysql_connection, mysql_cursor = get_mysql_connection()
    if p_device == '':
        SQL_DETAILS_OF_TASKS = f"SELECT W551je5v_pb_tasks_users.id FROM W551je5v_pb_tasks_users INNER JOIN W551je5v_pb_tasks ON W551je5v_pb_tasks.id=W551je5v_pb_tasks_users.id_task WHERE W551je5v_pb_tasks_users.enable=1 AND W551je5v_pb_tasks_users.id_campaign={p_campaign_id} AND W551je5v_pb_tasks.enable=1"
    elif p_device == 'Computer':
        SQL_DETAILS_OF_TASKS = f"SELECT W551je5v_pb_tasks_users.id FROM W551je5v_pb_tasks_users INNER JOIN W551je5v_pb_tasks ON W551je5v_pb_tasks.id=W551je5v_pb_tasks_users.id_task WHERE W551je5v_pb_tasks_users.enable=1 AND W551je5v_pb_tasks_users.id_campaign={p_campaign_id} AND W551je5v_pb_tasks.computer_allowed=1 AND W551je5v_pb_tasks.enable=1"

    elif p_device == 'Smartphone':
        SQL_DETAILS_OF_TASKS = f"SELECT W551je5v_pb_tasks_users.id FROM W551je5v_pb_tasks_users INNER JOIN W551je5v_pb_tasks ON W551je5v_pb_tasks.id= W551je5v_pb_tasks_users.id_task WHERE W551je5v_pb_tasks_users.enable=1 AND W551je5v_pb_tasks_users.id_campaign={p_campaign_id} AND W551je5v_pb_tasks.smartphone_allowed=1 AND W551je5v_pb_tasks.enable=1"

    print(f"SQL_DETAILS_OF_TASKS : {SQL_DETAILS_OF_TASKS}")
    mysql_cursor.execute(SQL_DETAILS_OF_TASKS)
    tuple_all_tasks_user = mysql_cursor.fetchall()
    print(f"tuple_all_tasks_user : {tuple_all_tasks_user}")
    list_task_user = []

    try:
        mysql_cursor.close()
        mysql_connection.close()
    except Exception as ex:
        logger.error(f"Error closing mysql : {ex}")
    
    return tuple_all_tasks_user


def GetDetailsTaskUserBAK_SQLITE(p_taskuser_id):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate (cursor.description):
            d[col[0]] = row[idx]
        return d
    # Connect to SQLITE
    sqlite_connection = sqlite3.connect (LoadFile ('db.db'))
    sqlite_connection.row_factory = dict_factory
    sqlite_cursor = sqlite_connection.cursor ()
    taskuser_details_dico=sqlite_cursor.execute("SELECT id,enable,id_task,id_campaign,url_keywords,minimum,url_list,  \
            url_usernames,message_txt_invitation_1B,message_txt_1A,message_txt_2A,message_txt_3A,message_txt_4A,  \
            message_voice_1A,message_voice_2A,message_voice_3A,message_voice_4A,message_txt_invitation_1A,message_txt_1B,  \
            message_txt_2B,message_txt_3B,message_txt_4B,message_voice_1B,message_voice_2B,message_voice_3B,  \
            message_voice_4B,date_counter_test_AB,time_delay_1A,time_delay_1A_type,time_delay_2A,time_delay_2A_type,  \
            time_delay_3A,time_delay_3A_type,time_delay_1B,time_delay_1B_type,time_delay_2B,time_delay_2B_type,  \
            time_delay_3B,time_delay_3B_type,message_1A_choice,message_2A_choice,message_3A_choice,message_4A_choice,  \
            message_1B_choice,message_2B_choice,message_3B_choice,message_4B_choice,AB_testing_enable,AB_testing_enable_invitation,  \
            date_AB_testing,date_AB_testing_invitation,serie_type,daily_limit  \
            FROM tasks_user where id=?",(p_taskuser_id,)).fetchone()
    return taskuser_details_dico


def GetDetailsTaskUser(p_taskuser_id):
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


def find_row_csv_source_in_table_sources(p_platform='', p_type='', p_name='', p_url='', p_target_group=''):
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()
    if p_type=='share_post':
        result = cursor.execute("select * from sources where type=? and platform=? and  url=?",(p_type,p_platform,p_url)).fetchall()
        print(f"result : {result}")
        print(f"len(result : {len(result)}")
        if len(result)!=0:
            return True
        else:
            return False
    else:
        result = cursor.execute("select * from sources where type=? and platform=? and name=?",(p_type, p_platform, p_name)).fetchall()
        print(f"result : {result}")
        print(f"len(result : {len(result)}")
        if len(result)!=0:
            return True
        else:
            return False




def Task_Facebook_Share_posts_in_groups(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Facebook_Share_posts_in_groups for SMartphone N° {p_udid} --------------")

    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appWaitActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'
    desired_caps['autoGrantPermissions'] = 'true'
    desired_caps['appPackage'] = 'com.facebook.katana'
    desired_caps['appActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


    driver.start_activity("com.facebook.katana", "com.facebook.katana.activity.FbMainTabActivity")
    # inspect available log types

    logger.info(f"{p_udid}|||Let's do some Facebook share post stuff for smartphone N°{p_udid} :-)")

    driver.close()

    logger.info(f"{p_udid}|||Task Facebook share post will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Facebook_Share_posts_in_groups"


def Task_Facebook_Send_message_to_user(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Facebook_Send_message_to_user for SMartphone N° {p_udid}--------------")

    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appWaitActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'
    desired_caps['autoGrantPermissions'] = 'true'
    desired_caps['appPackage'] = 'com.facebook.katana'
    desired_caps['appActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.facebook.katana", "com.facebook.katana.activity.FbMainTabActivity")
    # inspect available log types

    logger.info(f"{p_udid}|||Let's do some Facebook share post stuff for smartphone N°{p_udid} :-)")

    driver.close()
    logger.info(f"{p_udid}|||Task Facebook send messages will wait a few seconds....")
    time.sleep(randint(1, 6))

    return "===> Done Task_Facebook_Send_message_to_user"


def Task_Instagram_Send_message(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    #--- Ok, I get answers and solution form here: https://stackoverflow.com/questions/60002957/how-to-pass-several-parameters-to-a-function-which-is-iterated-by-executor-map/60003870#60003870


    logger.info(f"{p_udid}|||---- Start Task_Instagram_Send_message for SMartphone N° {p_udid}-----------")

    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.instagram.android'
    desired_caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.instagram.android", "com.instagram.mainactivity.MainActivity")

    logger.info(f"{p_udid}|||Let's do some Instagram stuff for smartphone N°{p_udid} :-)")

    driver.close()
    logger.info(f"{p_udid}|||Task Instagram send messages will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Instagram_Send_message"


def Task_Instagram_Like_pics_of_member(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Instagram_Like_pics_of_member for SMartphone N° {p_udid} --------------")



    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.instagram.android'
    desired_caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.instagram.android", "com.instagram.mainactivity.MainActivity")

    logger.info(f"{p_udid}|||Let's do some Instagram stuff for smartphone N°{p_udid} :-)")

    driver.close()
    logger.info(f"{p_udid}|||Task will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Instagram_Like_pics_of_member"


def Task_Instagram_Follow_members(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Instagram_Follow_members : {p_udid} --------------")



    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.instagram.android'
    desired_caps['appActivity'] = 'com.instagram.mainactivity.MainActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.instagram.android", "com.instagram.mainactivity.MainActivity")

    logger.info(f"{p_udid}|||Let's do some Instagram stuff for smartphone N°{p_udid} :-)")

    driver.close()
    logger.info(f"{p_udid}|||Task Instagram Follow will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Instagram_Follow_members"


def Task_Linkedin_Invite_1rst_connexion_and_message(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Linkedin_Invite_1rst_connexion_and_message for SMartphone N° {p_udid} --------------")

    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.linkedin.android'
    desired_caps['appActivity'] = 'com.linkedin.android.authenticator.LaunchActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.linkedin.android", "com.linkedin.android.authenticator.LaunchActivity")

    logger.info(f"{p_udid}|||Let's do some Linkedin stuff for smartphone N°{p_udid} :-)")

    driver.close()


    logger.info(f"{p_udid}|||Task Linkedin Invite 1rst connexion will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Linkedin_Invite_1rst_connexion_and_message"


def Task_Linkedin_Send_direct_message_to_contacts(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Linkedin_Send_direct_message_to_contacts  for SMartphone N° {p_udid} --------------")
    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.linkedin.android'
    desired_caps['appActivity'] = 'com.linkedin.android.authenticator.LaunchActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.linkedin.android", "com.linkedin.android.authenticator.LaunchActivity")

    logger.info(f"{p_udid}|||Let's do some Linkedin stuff for smartphone N°{p_udid} :-)")

    driver.close()

    logger.info(f"{p_udid}|||Task Linkedin Send Direct Messages will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Linkedin_Send_direct_message_to_contacts"


def Task_Send_SMS(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Send_SMS  for SMartphone N° {p_udid}--------------")
    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.android.messaging'
    desired_caps['appActivity'] = 'com.android.messaging.ui.conversationlist.ConversationListActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.android.messaging", "com.android.messaging.ui.conversationlist.ConversationListActivity")

    logger.info(f"{p_udid}|||Let's send some SMS smartphone N°{p_udid} :-)")

    driver.close()

    logger.info(f"{p_udid}|||Task SMS will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Send_SMS"


def Task_Twitter_Follow(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||--------- Start Task_Twitter_Follow  for SMartphone N° {p_udid} --------------")

    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'com.twitter.android'
    desired_caps['appActivity'] = 'com.twitter.app.main.MainActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("com.twitter.android", "com.twitter.app.main.MainActivity")

    logger.info(f"{p_udid}|||Let's do some Twitter stuff smartphone N°{p_udid} :-)")

    driver.close()

    logger.info(f"{p_udid}|||Task Twitter will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Twitter_Follow"


def Task_Leboncoin_Send_direct_message_to_sellers(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||----------- Start the action {p_name_action} ----------------------------")
    desired_caps = {}
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['appPackage'] = 'fr.leboncoin'
    desired_caps['appActivity'] = 'fr.leboncoin.ui.activities.MainActivity'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    driver.start_activity("fr.leboncoin", "fr.leboncoin.ui.activities.MainActivity")

    logger.info(f"{p_udid}|||Let's send some SMS smartphone N°{p_udid} :-)")

    driver.close()

    logger.info(f"{p_udid}|||Task Leboncoin will wait a few seconds....")
    time.sleep(randint(1, 6))
    return "===> Done Task_Leboncoin_Send_direct_message_to_sellers"


def start_action(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit):
    logger.info(f"{p_udid}|||----------- Start the action {p_name_action} ----------------------------")

    if p_name_action == 'Facebook_Share_posts_in_groups':
        Task_Facebook_Share_posts_in_groups(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Facebook_Send_message_to_user':
        Task_Facebook_Send_message_to_user(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Instagram_Send_message':
        Task_Instagram_Send_message(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Instagram_Like_pics_of_member':
        Task_Instagram_Like_pics_of_member(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Instagram_Follow_members':
        Task_Instagram_Follow_members(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Linkedin_Invite_1rst_connexion_and_message':
        Task_Linkedin_Invite_1rst_connexion_and_message(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Linkedin_Send_direct_message_to_contacts':
        Task_Linkedin_Send_direct_message_to_contacts(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Leboncoin_Send_direct_message_to_sellers':
        Task_Leboncoin_Send_direct_message_to_sellers(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Send_SMS':
        Task_Send_SMS(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)

    if p_name_action == 'Twitter_Follow':
        Task_Twitter_Follow(p_name_action,p_udid, p_systemPort, p_deviceName, p_version, p_os,quantity_tasks_per_hit)





# ================================================================================================================
# ====================================Old version of run_smartphone======================================
# ================================================================================================================

def run_smartphone(p_udid,lock):
    while True:
        try:
            logger.info(f"{p_udid}|||----------- We start to run the bots smartphone {p_udid} ---------------------")


            # --- Make total daily limit of activated activities
            # --- This total will help us to split and organise all the tasks of the smartphones
            # throught the differents applications
            # For this purpose, we have the table limits
            try:
                total_daily_tasks = 0
                total_activities_enable = 0

                sqlite_connection = sqlite3.connect(LoadFile('db.db'))
                cursor = sqlite_connection.cursor()
                for row in cursor.execute("SELECT * from limits"):
                    total_daily_tasks += int(row[1])
            except Exception as ex:
                print(f"{ex} --> ERROR runsmartphone get the limits")

            # ========================= WE NEED TO GET DETAILS OF SMARTPHONE FOR OPENING DRIVER ==============================
            # ============================== devicename, platformversion, systemPort, OS_device ==============================

            parameters_smartphone=cursor.execute("SELECT devicename, platformversion, systemPort, OS_device FROM smartphones WHERE udid=?",(p_udid,)).fetchone()
            logger.info(f"{p_udid}|||parameters_smartphone = {parameters_smartphone}")

            logger.info(f"{p_udid}|||total_daily_tasks for smartphone {p_udid} : {str(total_daily_tasks)}")


            # --- Now we have the total_daily_tasks, we need to calculate how many tasks need to be done for each hit
            # --- A hit is an action of the smartphone on the platform
            # --- The smartphone can't make 50 actions in a sequence without pause. It will look suspicious.
            # --- to calculate this quantity of tasks per hit, we need:
            # --- total_daily_tasks / 8 hours / quantity of activities enabled
            quantity_tasks_per_hit = round(total_daily_tasks / 16 / 8)


            logger.info(f"{p_udid}|||quantity_tasks_per_hit for smartphone {p_udid} : {str(quantity_tasks_per_hit)}")

            # --- Ok, now the most difficult is to calculate how long time the bot need to sleep after a queue of tasks.
            # --- The bot will execute for example 3 tasks for 15 activities=45. If the bot need 10 seconds for each tasks,
            # --- it will execute his 370 tasks for example, in 3700 seconds(around 1 hour).
            # --- The bot need to sleep between each hit in order to take 8 hours to accomplish his daily job
            # --- As we know we get quantity_tasks_per_hit for 8 hours, if we have 3 tasks(3 times the same activity) per hit and we have 15 activities,
            # --- our smartphone need to make 3*15/60=0,75 minute(45 seconds) of pause between each tasks

            cpt_daily_tasks = 0
            time_to_sleep =(quantity_tasks_per_hit * 16 / 60 * 60)

            # --- We create a loop WHILE cpt_task < total_tasks

            cursor2 = sqlite_connection.cursor()
            cursor3 = sqlite_connection.cursor()
            while True:
                logger.info("We are in run_smartphone method 1rst 'While True' loop")
                while cpt_daily_tasks < total_daily_tasks:
                    logger.info("We are in run_smartphone method 'While cpt_daily_tasks < total_daily_tasks' loop")
                    #devicename, platformversion, systemPort, OS_device
                    while True:
                        logger.info("We are in run_smartphone method 2nd 'While True' loop")
                        try:
                            logger.info("We run Instagram_bot.Start_Bot")
                            try :
                                logger.info(f"str(p_udid) : {str(p_udid)}")
                                logger.info(f"parameters_smartphone[2] : {parameters_smartphone[2]}")
                                logger.info(f"str(parameters_smartphone[0] : {str(parameters_smartphone[0])}")
                                logger.info(f"str(parameters_smartphone[1] {str(parameters_smartphone[1])}")
                                logger.info(f"str(parameters_smartphone[3]){str(parameters_smartphone[3])}")
                                logger.info(f"quantity_tasks_per_hit : {quantity_tasks_per_hit}")
                                Instagram_total_counter_tasks_of_hit=Instagram_bot.StartBot("Instagram ",str(p_udid),str(parameters_smartphone[2]),str(parameters_smartphone[0]),  \
                                                    str(parameters_smartphone[1]),str(parameters_smartphone[3]),  \
                                                    quantity_tasks_per_hit,quantity_tasks_per_hit,quantity_tasks_per_hit,  \
                                                    quantity_tasks_per_hit,quantity_tasks_per_hit,quantity_tasks_per_hit,  \
                                                    quantity_tasks_per_hit,lock)
                            except Exception as ex :
                                logger.error("ERROR WITH Instagram_bot")

                            logger.info(f"{p_udid}|||Instagram_total_counter_tasks_of_hit : {Instagram_total_counter_tasks_of_hit}")
                            cpt_daily_tasks += Instagram_total_counter_tasks_of_hit
                            break
                        except Exception as ex :
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||{ex} --> The method 'run_smartphone' failed. Let's try again!")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")
                            logger.error(f"{p_udid}|||*****************************************************")












                    logger.info(f"{p_udid}|||cpt_daily_tasks for smartphone {p_udid} : {str(cpt_daily_tasks)}/{total_daily_tasks}")

                logger.info(f"{p_udid}|||PhoneBot finished the task of the day. It will sleep {time_to_sleep} seconds.")
                time.sleep(time_to_sleep)


            sqlite_connection.close()
            cursor.close()
            id_process = os.getpid()
            logger.info(f"{p_udid}|||parent process: {os.getppid()}")
            logger.info(f"{p_udid}|||process id:{id_process}")
            break

        except Exception as ex :
            logger.error("ERROR We start to run the bots smartphone")




def give_systemPort_to_smartphones():
    # --- THis function will scroll all the smartphones of table and give a systemPort number to the ones who doesn't have a portnumber
    logger.info("------- Starting give_systemPort_to_smartphones ----------")
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()
    cursor2 = sqlite_connection.cursor()
    # --- First we need to make a list of all the systemport already set up in smarpthones table
    list_systemPort_tuple = cursor.execute("select systemPort from smartphones").fetchall()

    '''
    WE HAVE BIG ISSUE WITH THESE LINES OF CODE
    I DON'T SEE ANY PURPOSE TO KEEP THE PREVIOUS PORT
    SO WE CAN GIVE NEW PORT ON EACH SMARTPHONE EACH TIME PHONEBOT IS RUNNING
    logger.info(f"list_systemPort_tuple : {list_systemPort_tuple}")
    list_systemPort = [item[0] for item in list_systemPort_tuple]
    logger.info(f"list_systemPort : {list_systemPort}")

    max_systemPort = int(max(list_systemPort))
    if max_systemPort < 4724:
        max_systemPort = 4724
    logger.info(max_systemPort)
    '''
    max_systemPort = 4724
    for row in cursor.execute("select id, systemPort,udid from smartphones"):
        #As our computer is in list of smartphones in table smartphones, it is useless to give port number to computer
        if row[2]!="Computer":
            max_systemPort += 1
            cursor2.execute("Update smartphones set systemPort=? where id=?",(max_systemPort,row[0]))
            sqlite_connection.commit()


            max_systemPort=4724
            for row2 in cursor.execute("select * from smartphones WHERE udid!=?",('Computer',)):
                logger.info(max_systemPort)
                max_systemPort += 1
                cursor2.execute("Update smartphones set systemPort=? where id=?",(max_systemPort,row2[0]))
                sqlite_connection.commit()


    logger.info("We update table smartphones for adding the port for Appium")

    try:
        cursor.close()
    except:
        print("Error: PhoneBot couldn't close cursor")

    try:
        cursor2.close()
    except:
        print("Error: PhoneBot couldn't close cursor2")

    try:
        sqlite_connection.close()
    except:
        print("Error: PhoneBot couldn't close sqlite_connection")


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


#===========================================================================================================
#==================================== METHOD TO SCROLL DOWN =====================================================
#===========================================================================================================
def Scroll_Down(p_driver,p_udid,p_swap_times=1):
    # ============= WE prepare the scroll
    try:
        windows_size = p_driver.get_window_size()
        start_y = windows_size['height'] * 0.8
        end_y = windows_size['height'] * 0.2
        start_x = windows_size['width'] * 0.5
        end_x = windows_size['width'] * 0.5
        logger.info(f"{p_udid}|||start_y : {start_y}")
        logger.info(f"{p_udid}|||end_y : {end_y}")
        logger.info(f"{p_udid}|||start_x : {start_x}")
        logger.info(f"{p_udid}|||end_x : {end_x}")
        duration = random.uniform(800, 1200)
        # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
        action = TouchAction(p_driver)
        counter_swipe=0
        while counter_swipe < p_swap_times:
            # On swipe random times and we need to be sure there is a LIKE button before to stop
            action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

            logger.info(f"{p_udid}|||We swipe!")
            counter_swipe += 1
            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(1.9, 3.3))
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> {ex} --> ERROR Scroll_Down")


#===========================================================================================================
#==================================== METHOD TO SCROLL UP =====================================================
#===========================================================================================================
def Scroll_Up(p_driver,p_udid,p_swap_times=1):
    try:
        # ============= WE prepare the scroll
        windows_size = p_driver.get_window_size()
        start_y = windows_size['height'] * 0.2
        end_y = windows_size['height'] * 0.8
        start_x = windows_size['width'] * 0.5
        end_x = windows_size['width'] * 0.5
        logger.info(f"{p_udid}|||start_y : {start_y}")
        logger.info(f"{p_udid}|||end_y : {end_y}")
        logger.info(f"{p_udid}|||start_x : {start_x}")
        logger.info(f"{p_udid}|||end_x : {end_x}")
        duration = random.uniform(400, 800)
        # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
        action = TouchAction(p_driver)
        counter_swipe=0
        while counter_swipe < p_swap_times:
            # On swipe random times and we need to be sure there is a LIKE button before to stop
            action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

            logger.info(f"{p_udid}|||We swipe!")
            counter_swipe += 1
            logger.info(f"{p_udid}|||The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(0.9, 1.3))
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> {ex} --> ERROR Scroll_Down")




#===========================================================================================================
#==================================== METHOD TO SCROLL DOWN =====================================================
#===========================================================================================================
def Scroll_Down_small(p_driver,p_udid,p_swap_times=1):
    # ============= WE prepare the scroll
    windows_size = p_driver.get_window_size()
    start_y = windows_size['height'] * 0.6
    end_y = windows_size['height'] * 0.45
    start_x = windows_size['width'] * 0.5
    end_x = windows_size['width'] * 0.5
    logger.info(f"{p_udid}|||start_y : {start_y}")
    logger.info(f"{p_udid}|||end_y : {end_y}")
    logger.info(f"{p_udid}|||start_x : {start_x}")
    logger.info(f"{p_udid}|||end_x : {end_x}")
    duration = random.uniform(400, 800)
    # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
    action = TouchAction(p_driver)
    counter_swipe=0
    while counter_swipe < p_swap_times:
        # On swipe random times and we need to be sure there is a LIKE button before to stop
        action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

        logger.info(f"{p_udid}|||We swipe!")
        counter_swipe += 1



#===========================================================================================================
#==================================== METHOD TO SCROLL DOWN =====================================================
#===========================================================================================================
def Scroll_Down_medium(p_driver,p_udid,p_swap_times=1):
    # ============= WE prepare the scroll
    windows_size = p_driver.get_window_size()
    start_y = windows_size['height'] * 0.70
    end_y = windows_size['height'] * 0.3
    start_x = windows_size['width'] * 0.5
    end_x = windows_size['width'] * 0.5
    logger.info(f"{p_udid}|||start_y : {start_y}")
    logger.info(f"{p_udid}|||end_y : {end_y}")
    logger.info(f"{p_udid}|||start_x : {start_x}")
    logger.info(f"{p_udid}|||end_x : {end_x}")
    duration = random.uniform(400, 800)
    # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
    action = TouchAction(p_driver)
    counter_swipe=0
    while counter_swipe < p_swap_times:
        # On swipe random times and we need to be sure there is a LIKE button before to stop
        action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

        logger.info(f"{p_udid}|||We swipe!")
        counter_swipe += 1



#===========================================================================================================
#==================================== SMALL MEDIUM =====================================================
#===========================================================================================================
def Scroll_Down_Small_medium(p_driver,p_udid,p_swap_times=1):
    # ============= WE prepare the scroll
    windows_size = p_driver.get_window_size()
    start_y = windows_size['height'] * 0.60
    end_y = windows_size['height'] * 0.4
    start_x = windows_size['width'] * 0.5
    end_x = windows_size['width'] * 0.5
    logger.info(f"{p_udid}|||start_y : {start_y}")
    logger.info(f"{p_udid}|||end_y : {end_y}")
    logger.info(f"{p_udid}|||start_x : {start_x}")
    logger.info(f"{p_udid}|||end_x : {end_x}")
    duration = random.uniform(400, 800)
    # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
    action = TouchAction(p_driver)
    counter_swipe=0
    while counter_swipe < p_swap_times:
        # On swipe random times and we need to be sure there is a LIKE button before to stop
        action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

        logger.info(f"{p_udid}|||We swipe!")
        counter_swipe += 1





#===========================================================================================================
#==================================== METHOD TO SCROLL UP =====================================================
#===========================================================================================================
def Scroll_Up_small(p_driver,p_udid,p_swap_times=1):
    # ============= WE prepare the scroll
    windows_size = p_driver.get_window_size()
    start_y = windows_size['height'] * 0.45
    end_y = windows_size['height'] * 0.55
    start_x = windows_size['width'] * 0.5
    end_x = windows_size['width'] * 0.5
    logger.info(f"{p_udid}|||start_y : {start_y}")
    logger.info(f"{p_udid}|||end_y : {end_y}")
    logger.info(f"{p_udid}|||start_x : {start_x}")
    logger.info(f"{p_udid}|||end_x : {end_x}")
    duration = random.uniform(400, 800)
    # p_driver.swipe(start_x, start_y, end_x, end_y, duration)
    action = TouchAction(p_driver)
    counter_swipe=0
    while counter_swipe < p_swap_times:
        # On swipe random times and we need to be sure there is a LIKE button before to stop
        action.press(x=start_x, y=start_y).wait(duration).move_to(el=None, x=end_x, y=end_y).release().perform()

        logger.info(f"{p_udid}|||We swipe!")
        counter_swipe += 1






# ===============================================================================================================
# ============================== FUNCTION TO GET NECESSARY VALUES FOR SMS =========================
# ===============================================================================================================
def GetSMSValues(p_udid,p_id):
    # ---on lit le fichier config.ini
    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    # ================================== WE CONNECT TO MYSQL DATABASE ==============================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(
                f"{p_udid}|||{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!","PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")
            time.sleep(5)
        return

    logger.info(f"{p_udid}|||Connect to Phonebot Database successful!!")
    mycursor = mydb.cursor(buffered=True)

    # ============================== WE NOW NEED TO GET use_id FROM MYSQL DATABASE ==============================
    # Check for config file
    while not CheckConfigIni():
        logger.info("Your config.ini file is not ok.")

    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    email = config.get('Settings', 'email')
    license_key_config = config.get('Settings', 'license_key')

    # --- get the userID from WP database-----------------------------------------------------------------

    sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
    print(f"{sql_user_id}")
    mycursor.execute(sql_user_id)
    user_id = mycursor.fetchone()
    if user_id is None:
        logger.critical(
            f"{p_udid}||| --> There are no user id {email} in Phonebot.co Database! Check your config.ini. Try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
        sys.exit()
    else:
        user_id = str(user_id[0])
        logger.info(f"{p_udid}|||User ID found on Phonebot.co :-) :" + str(user_id))

    # ============================= LET'S EXTRACT IF SMS TASK IS ACTIVATED =============================
    sql_sms_send_message = "select meta_value from W551je5v_usermeta where meta_key= 'smartphone_" + str(p_id) + "_what_automate_" + str(p_id) + "' AND user_id=" + str(user_id)
    print(f"sql_find_application_enable : {sql_sms_send_message}")
    mycursor.execute(sql_sms_send_message)
    brut_value_application_enable_tuple = mycursor.fetchone()


    sms = False


    if not brut_value_application_enable_tuple:
        logger.error(
            f"{p_udid}|||ERROR! You didn't fill the SMS Send message in your account details on our website phonebot.co")
        result = ''
    else:
        brut_value_application_enable = brut_value_application_enable_tuple[0]
        logger.info(f"{p_udid}|||brut_value_application_enable : {brut_value_application_enable}")
        if str(brut_value_application_enable).find('sms') != -1:

            sms_send_message = 1
            logger.info(f"{p_udid}|||{sms_send_message}")


    # ============================= LET'S EXTRACT SMS MESSAGE =============================
    sql_sms_message = "SELECT meta_value FROM W551je5v_usermeta WHERE meta_key='smartphone_"+ str(p_id) + "_sms_message_"+ str(p_id) +"' AND user_id=" + str(user_id)
    print(f"sql_sms_message:{sql_sms_message}")
    mycursor.execute(sql_sms_message)
    sms_message_tuple = mycursor.fetchone()
    if not sms_message_tuple:
        logger.error(
            f"{p_udid}|||ERROR! You didn't fill the SMS message in your account details on our website phonebot.co")
        result = ''
    else:
        sms_message = str(sms_message_tuple[0])
        logger.info(f"{p_udid}|||{sms_message}")

    # ============================= LET'S EXTRACT SMS LIST OF PHONE NUMBER =============================
    sql_sms_list_phone_number = "SELECT meta_value FROM W551je5v_usermeta WHERE meta_key='smartphone_" + str(
        p_id) + "_sms_list_phone_number_" + str(p_id) + "' AND user_id=" + str(user_id)
    print(f"sql_sms_list_phone_number:{sql_sms_list_phone_number}")
    mycursor.execute(sql_sms_list_phone_number)
    sms_list_phone_number_tuple = mycursor.fetchone()
    if not sms_list_phone_number_tuple:
        logger.error(
            f"{p_udid}|||ERROR! You didn't fill the SMS list of phone numbers in your account details on our website phonebot.co")
        result = ''
    else:
        brut_list_phone_number = str(sms_list_phone_number_tuple).replace('\\r', '').replace('(', '').replace(')',
                                                                                                              '').replace(
            ',', '').replace("'", '')
        sms_list_phone_number = brut_list_phone_number.split('\\n')
        logger.info(f"{p_udid}|||sms_list_phone_number :{sms_list_phone_number}")
    try:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close
    except:
        logger.error("PhoneBot failed to close Mysql DB connection.")

    return sms_send_message,sms_message,sms_list_phone_number




#=================================================================================================================
#===================== FUNCTION TO COMPARE FACEBOOK USERNAME FROM APP TO Account details =========================
#=================================================================================================================
def CompareFBUsername(p_udid,p_platform,p_username,p_acf):
    print(f"CompareFBUsername : {p_username} &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(f"p_udid : {p_udid} &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    # ==============================================================================================================
    # ---on lit le fichier config.ini
    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    #================================== WE CONNECT TO MYSQL DATABASE ==============================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{p_udid}|||{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")
            time.sleep(5)
    logger.info(f"{p_udid}|||Connect to Phonebot Database successful!!")
    mycursor = mydb.cursor(buffered=True)

    # ============================== WE NOW NEED TO GET use_id FROM MYSQL DATABASE ====================================
    while not CheckConfigIni():
        logger.info("Your config.ini file is not ok.")

    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    email = config.get('Settings', 'email')
    license_key_config = config.get('Settings', 'license_key')


    # --- get the userID from WP database-----------------------------------------------------------------



    sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
    print(f"{sql_user_id}")
    mycursor.execute(sql_user_id)
    user_id = mycursor.fetchone()
    if user_id is None:
        logger.critical(f"{p_udid}||| --> There are no user id {email} in Phonebot.co Database! Check your config.ini. Try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
        sys.exit()
    else:
        user_id = str(user_id[0])
        logger.info(f"{p_udid}|||User ID found on Phonebot.co :-) :" + str(user_id))

    # ============================= LET'S IDENTIFY WHICH SMARTPHONE WE ARE RUNNING NOW =============================
    sql_query = "SELECT meta_key FROM W551je5v_usermeta WHERE meta_key LIKE '%" + p_platform + "%' AND meta_value= '" + p_username + "' AND user_id=" + str(user_id)
    print(f"sql_query:{sql_query}")
    mycursor.execute(sql_query)
    meta_key=mycursor.fetchone()
    if not meta_key:

        logger.error(f"{p_udid}|||ERROR! One of your smartphone is trying to automate {p_platform} with the account '{p_username}'. But PhoneBot didn't find '{p_username}' in the {p_platform} tab of your configuration in your 'Account details' on Phonebot.co. You certainly changed the linkedin username for this smartphone. Please login to https://phonebot.co and add this {p_platform} username '{p_username}' in your {p_platform} configuration.")
        result=False
        PopupMessage("Problem with your configuration!",
                     f"ERROR on smartphone {p_udid}! Your smartphone is trying to automate {p_platform} with the account '{p_username}'. But PhoneBot didn't find '{p_username}' in the {p_platform} tab of your configuration in your 'Account details' on Phonebot.co. You certainly changed the linkedin username for this smartphone. Please login to https://phonebot.co and add this {p_platform} username '{p_username}' in your {p_platform} configuration.")

    else:
        logger.error(
            f"{p_udid}|||GOOD USERNAME! One of your smartphone is trying to automate {p_platform} with the account '{p_username}'. PhoneBot found '{p_username}' in the {p_platform} tab of your configuration in your 'Account details' on Phonebot.co. You certainly changed the linkedin username for this smartphone. Please login to https://phonebot.co and add this {p_platform} username '{p_username}' in your {p_platform} configuration.")
        result = True
    return result


#=================================================================================================================
#=================================== FUNCTION TO GET ACF VAMUES OF A TASK ========================================
#=================================================================================================================
def GetValueFromCustomField(p_udid,p_platform,p_username,p_acf):
    print(f"p_username : {p_username} &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(f"p_udid : {p_udid} &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #==============================================================================================================
    # This function extract the value of a custom field necessary for making the automation.
    #
    '''
    List of the MYSQL fields from table ACF where 1 is the number of smartphone
    user_id, meta_key,meta_value
    ********** FACEBOOK ********
    smartphone_1_facebook_list_groups_scrap_message_1
    smartphone_1_facebook_list_groups_share_url_1
    smartphone_1_facebook_list_pages_scrap_message_1
    smartphone_1_facebook_list_urls_to_share_1
    smartphone_1_facebook_message_1
    smartphone_1_facebook_scrap_members_groups_pages_1
    smartphone_1_facebook_send_message_to_user_1
    smartphone_1_Facebook_Share_posts_in_groups_1
    smartphone_1_facebook_username_1

    ********** GOOGLEMAP ********
    smartphone_1_googlemap_category_location_1

    ********** INSTAGRAM ********
    smartphone_1_instagram_follow_1
    smartphone_1_Instagram_like_pictures_of_followers_1
    smartphone_1_instagram_like_random_pictures_1
    smartphone_1_instagram_list_hashtags_liking_pictures_1
    smartphone_1_instagram_mail_subject_1
    smartphone_1_instagram_message_1
    smartphone_1_instagram_publish_pictures_1
    smartphone_1_instagram_publish_pictures_facebook_1
    smartphone_1_instagram_publish_pictures_tumblr_1
    smartphone_1_instagram_publish_pictures_twitter_1
    smartphone_1_Instagram_scrap_email_1
    smartphone_1_Instagram_send_mail_1
    smartphone_1_Instagram_send_message_1
    smartphone_1_instagram_unfollow_1
    smartphone_1_instagram_username_1
    smartphone_1_list_hashtags_publish_pictures_1
    smartphone_1_list_of_instagram_influencers_or_competitors_1
    smartphone_1_list_of_labels_pictures_1


    ********** LEBONCOIN ********
    smartphone_1_leboncoin_category_location_1
    smartphone_1_leboncoin_personal_professional_1
    smartphone_1_leboncoin_scrap_1
    smartphone_1_leboncoin_send_message_1
    smartphone_1_leboncoin_username_1

    ********** LINKEDIN ********
    smartphone_1_linkedin_list_of_keywords_locations_1
    smartphone_1_linkedin_make_1rst_connection_1
    smartphone_1_linkedin_scrap_1
    smartphone_1_linkedin_send_message_1
    smartphone_1_linkedin_short_message_1
    smartphone_1_linkedin_username_1
    smartphone_1_list_of_twitter_influencers_or_competitors

    ********** SMS ********
    smartphone_1_sms_list_phone_number_1
    smartphone_1_sms_message_1

    ********** TWITTER ********
    smartphone_1_twitter_follow_1
    smartphone_1_twitter_unfollow_1
    smartphone_1_twitter_username_1
    smartphone_1_twitter_send_message_1
    smartphone_1_twitter_message_1

    :param p_platform: this parameters is to know from which social network we need to check the username
    :param p_username: this parameter is useful to know on which smartphone is running the phonebot
    :return:
    '''
    # ==============================================================================================================
    # ---on lit le fichier config.ini
    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    #================================== WE CONNECT TO MYSQL DATABASE ==============================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{p_udid}|||{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")
            time.sleep(5)
    logger.info(f"{p_udid}|||Connect to Phonebot Database successful!!")
    mycursor = mydb.cursor(buffered=True)

    # ============================== WE NOW NEED TO GET use_id FROM MYSQL DATABASE ====================================
    while not CheckConfigIni():
        logger.info("Your config.ini file is not ok.")

    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    email = config.get('Settings', 'email')
    license_key_config = config.get('Settings', 'license_key')

    # --- get the userID from WP database-----------------------------------------------------------------

    sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
    print(f"{sql_user_id}")
    mycursor.execute(sql_user_id)
    user_id = mycursor.fetchone()
    if user_id is None:
        logger.critical(f"{p_udid}||| --> There are no user id {email} in Phonebot.co Database! Check your config.ini. Try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
        sys.exit()
    else:
        user_id = str(user_id[0])
        logger.info(f"{p_udid}|||User ID found on Phonebot.co :-) :" + str(user_id))

    # ============================= LET'S IDENTIFY WHICH SMARTPHONE WE ARE RUNNING NOW =============================
    sql_query = "SELECT meta_key FROM W551je5v_usermeta WHERE meta_key LIKE '%" + p_platform + "%' AND meta_value= '" + p_username + "' AND user_id=" + str(user_id)
    print(f"sql_query:{sql_query}")
    mycursor.execute(sql_query)
    meta_key=mycursor.fetchone()
    if not meta_key:
        logger.error(f"{p_udid}|||ERROR! One of your smartphone is trying to automate {p_platform} with the account '{p_username}'. But PhoneBot didn't find '{p_username}' in the {p_platform} tab of your configuration in your 'Account details' on Phonebot.co. You certainly changed the linkedin username for this smartphone. Please login to https://phonebot.co and add this {p_platform} username '{p_username}' in your {p_platform} configuration.")
        result=''
    else:
        meta_key = str(meta_key[0])
        logger.info(f"{p_udid}|||{meta_key}")
        print(f"metakey : {meta_key}")
        pos_number_smartphone = meta_key.find("smartphone_") + len("smartphone_")
        number_smartphone= meta_key[pos_number_smartphone]
        logger.info(f"{p_udid}|||pos_number_smartphone : {pos_number_smartphone}")
        logger.info(f"{p_udid}|||number_smartphone : {number_smartphone}")

        # ============================= WE CAN NOW EXTRACT THE VALUE OF THE ACF FIELD REQUESTED =========================
        sql_query_result = "SELECT meta_value FROM W551je5v_usermeta WHERE meta_key LIKE 'smartphone_" + number_smartphone + "%" + p_acf + "%' AND user_id=" + str(user_id)
        print(f"{sql_query_result}")
        mycursor.execute(sql_query_result)
        result_sql = mycursor.fetchone()
        print(f"result_sql : {result_sql}")
        result = str(result_sql).replace("('","").replace("',)","").replace("\\r","").replace("\\'","'").replace('("','').replace(',)','').replace('"','')
        print(f"result : {result}")
        try:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close
        except:
            logger.error("PhoneBot failed to close Lysql DB connection.")

    return result



# ==============================================================================================================
# ================ METHOD TO COLLECT ALL THE USERNAMES FROM ALL THE PLATFORM AND STORE THEM IN DB.db ================
# ==============================================================================================================
def CollectUsernames(p_platform,lock):
    # ---on lit le fichier config.ini
    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    # ================================== WE CONNECT TO MYSQL DATABASE ==============================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            logger.info(f"DESKTOP|||Connect to Phonebot Database successful!!")
            mycursor = mydb.cursor(buffered=True)
            break

        except Exception as ex:
            logger.critical(f"DESKTOP|||Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            sys.exit()



    # ============================== WE NOW NEED TO GET use_id FROM MYSQL DATABASE ====================================
    while not CheckConfigIni():
        logger.info("Your config.ini file is not ok.")

    config = configparser.ConfigParser()
    config.read(LoadFile('config.ini'))
    email = config.get('Settings', 'email')
    license_key_config = config.get('Settings', 'license_key')

    # --- get the userID from WP database-----------------------------------------------------------------

    sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
    #print(f"{sql_user_id}")
    mycursor.execute(sql_user_id)
    user_id = mycursor.fetchone()
    if user_id is None:
        logger.critical(
            f"DESKTOP|||There are no user id {email} in Phonebot.co Database! Check your config.ini. Try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
        sys.exit()
    else:
        user_id = str(user_id[0])
        logger.info(f"DESKTOP|||User ID found on Phonebot.co :-) :" + str(user_id))

    # ==============================================================================================================
    # ============================= WE CAN NOW EXTRACT THE VALUE OF THE ACF FIELD REQUESTED =========================
    sql_query = "SELECT meta_value FROM W551je5v_usermeta WHERE meta_key LIKE 'smartphone_%" + p_platform + "_username%' AND user_id=" + str(user_id)
    print(f"{sql_query}")
    mycursor.execute(sql_query)
    tuple_of_usernames = mycursor.fetchall()
    print(f"tuple_of_usernames : {tuple_of_usernames}")
    list_of_usernames = [item[0] for item in tuple_of_usernames]

    # ============================== NOW WE ADD THE USERNAMES IN THE TABLE 'social_accounts' ========================
    for username in tuple_of_usernames:
        print(f"username = {username[0]}")
        if p_cursor1.execute("SELECT * FROM social_accounts WHERE username=? AND platform=?",(str(username[0]),p_platform)).fetchone():
            logger.info(f"DESKTOP|||{str(username[0])} for {p_platform} already exists in local database!")

        else:
            logger.info(f"DESKTOP|||{str(username[0])} for {p_platform} doesn't exists in local database. We will add it.")
            with lock:
                p_cursor1.execute("INSERT INTO social_accounts(username,platform) VALUES(?,?)",(str(username[0]),p_platform))
                sqlite_connection.commit()


    # ================ NOW WE NEED TO REMOVE NON EXISITNG usernames FROM table 'social_accounts' ======================
    # First we need to loop all the rows of table 'social_accounts'
    print('''
    # ================ NOW WE NEED TO REMOVE NON EXISITNG usernames FROM table 'social_accounts' ======================
    # First we need to loop all the rows of table 'social_accounts'
    
    ''')
    results=p_cursor1.execute("SELECT username FROM social_accounts WHERE platform=?",(p_platform,)).fetchall()
    print(f"results : {results}")
    print(f"len(results) : {len(results)}")
    print(f"list_of_usernames : {list_of_usernames}")
    for row in results:
        # We are in a row. Let's compare
        print(f"row : {row}")
        if row[0] in list_of_usernames:
            print(f"{row[0]} is in 'Account details'. It is fine!")
        else:
            print(f"{row[0]} is NOT in 'Account details'. We need to remove it!")
            with lock:
                p_cursor1.execute("DELETE FROM social_accounts WHERE username =? AND platform=?",(row[0],p_platform))
                sqlite_connection.commit()

    print("# ====================== WE CAN NOW EXTRACT AND RETURN THE LIST OF USERNAMES FOR p_platform =======================")
    tuple_usernames = p_cursor1.execute("SELECT username FROM social_accounts WHERE platform=?",
                                      (p_platform,)).fetchall()
    list_usernames = [item[0] for item in tuple_usernames]

    print("# ====================== WE CLOSE EVERYTHING =======================")
    try:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close

        if p_cursor1:
            p_cursor1.close()
        if sqlite_connection:
            sqlite_connection.close()
    except:
        logger.error("PhoneBot failed to close Mysql DB and SQLIte connections.")
    print(f"CollectUsernames() => list_usernames : {list_usernames}")
    return list_usernames



# ===============================================================================================================
# ================================ FUNCTION TO CALCULATE NUMBER OF ACTIONS IN THE LAST 24H ======================
# ===============================================================================================================


def HowManyActions_Last24H(p_myprofile, p_platform, p_type_action):
    # ===================== Let's make the list of dates order by most recent date =============================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    list_of_dates_of_post_picture = p_cursor1.execute(
        "SELECT date FROM actions WHERE id_social_account=? AND platform=? and type_action=?",
       (p_myprofile, p_platform, p_type_action)).fetchall()

    list_date = []
    for date_picture in list_of_dates_of_post_picture:
        date = datetime.strptime(date_picture[0], "%d/%m/%Y %H:%M:%S")
        print(f"date : {date}")
        list_date.append(date)

    list_sorted = sorted(list_date, reverse=True)

    cpt = 0
    # ======================= let's loop in the list and count how many dates are in less than 24h ===============
    for one_date in list_sorted:

        now = datetime.now()
        date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
        difference_between_most_recent_and_now = now - one_date

        print(f"hours = {difference_between_most_recent_and_now.total_seconds() / 3600}")
        number_of_hours = difference_between_most_recent_and_now.total_seconds() / 3600
        if float(str(number_of_hours)) < 24.0:
            cpt += 1

    if p_cursor1:
        p_cursor1.close()

    if sqlite_connection:
        sqlite_connection.close()
    return cpt
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


# ================================ FUNCTION TO CALCULATE HOW MANY HOURS AGO WAS LAST PUBLISH PIC ================

def NumberHoursLastAction(p_myprofile,p_platform,p_type_action):

    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    list_of_dates_of_post_picture = p_cursor1.execute("SELECT date FROM actions WHERE id_social_account=? AND platform=? and type_action=?",(p_myprofile, p_platform, p_type_action)).fetchall()
    print(f"list_of_dates_of_post_picture : {list_of_dates_of_post_picture}")
    list_date=[]
    for date_picture in list_of_dates_of_post_picture:
        date= datetime.strptime(date_picture[0],"%d/%m/%Y %H:%M:%S")
        print(f"date : {date}")
        list_date.append(date)

    print(f"oldest date = {min(list_date)}")
    print(f"most recent date = {max(list_date)}")
    most_recent_date=max(list_date)

    now = datetime.now()
    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    difference_between_most_recent_and_now = now - most_recent_date
    print(f"difference_between_most_recent_and_now = {difference_between_most_recent_and_now}")
    print(f"hours = {difference_between_most_recent_and_now.total_seconds()/3600}")
    return difference_between_most_recent_and_now.total_seconds()/3600



def NumberHoursLastGoogleScrapLinkedin():

    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    p_cursor1.execute("SELECT id,date FROM linkedin_profiles ORDER BY id DESC LIMIT 1")
    result = p_cursor1.fetchone()
    print(result)
    if result is None:
        return 333
    # If it is first scraping, linkedin_profiles will be empty and it will create an issue.
    # So we give 333 hours to result in order to allow the scrap.
    most_recent_date = datetime.strptime(result[1],"%d/%m/%Y %H:%M:%S")


    now = datetime.now()
    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    difference_between_most_recent_and_now = now - most_recent_date
    print(f"difference_between_most_recent_and_now = {difference_between_most_recent_and_now}")
    print(f"hours = {difference_between_most_recent_and_now.total_seconds()/3600}")

    if p_cursor1:
        p_cursor1.close()

    if sqlite_connection:
        sqlite_connection.close()

    return round(difference_between_most_recent_and_now.total_seconds()/3600,1)


def GetSocialAccountLastGoogleScrapLinkedin():
    # ============================== INITIALISATION OF DB ==================================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()

    # ============================== WE EXTRACT FIRST ALL THE DATE==========================================

    p_cursor1.execute("SELECT id_social_account FROM linkedin_profiles ORDER BY id DESC LIMIT 1")
    result = p_cursor1.fetchone()
    print(result)
    if result is None:
        result='None'



    if p_cursor1:
        p_cursor1.close()

    if sqlite_connection:
        sqlite_connection.close()
    return result[0]






#==================================================================================================================



def NumberHoursLastBingScrapLinkedin():

    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()
    p_cursor1.execute("SELECT id,date FROM linkedin_profiles ORDER BY id DESC LIMIT 1")
    result = p_cursor1.fetchone()
    print(result)
    if result is None:
        return 333
    # If it is first scraping, linkedin_profiles will be empty and it will create an issue.
    # So we give 333 hours to result in order to allow the scrap.
    most_recent_date = datetime.strptime(result[1],"%d/%m/%Y %H:%M:%S")


    now = datetime.now()
    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    difference_between_most_recent_and_now = now - most_recent_date
    print(f"difference_between_most_recent_and_now = {difference_between_most_recent_and_now}")
    print(f"hours = {difference_between_most_recent_and_now.total_seconds()/3600}")

    if p_cursor1:
        p_cursor1.close()

    if sqlite_connection:
        sqlite_connection.close()

    return round(difference_between_most_recent_and_now.total_seconds()/3600,1)


def GetSocialAccountLastBingScrapLinkedin():
    # ============================== INITIALISATION OF DB ==================================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    p_cursor1 = sqlite_connection.cursor()

    # ============================== WE EXTRACT FIRST ALL THE DATE==========================================

    p_cursor1.execute("SELECT id_social_account FROM linkedin_profiles ORDER BY id DESC LIMIT 1")
    result = p_cursor1.fetchone()
    print(result)
    if result is None:
        result='None'



    if p_cursor1:
        p_cursor1.close()

    if sqlite_connection:
        sqlite_connection.close()
    return result[0]






#==================================================================================================================


def get_proxies():
    try:
        co = webdriver.ChromeOptions()
        co.add_argument("log-level=3")
        co.add_argument("--headless")
        # driver = webdriver.Chrome(chrome_options=co)
        driver = webdriver.Chrome(options=co)
        driver.get("0https://free-proxy-list.net/")
        driver.find_element_by_xpath("*//th[text()='Https']").click()
        print("The bot will sleep just a few seconds..............................")
        time.sleep(random.uniform(0.9, 2.3))
        driver.find_element_by_xpath("*//th[text()='Https']").click()
        PROXIES = []

        while True:
            proxies = driver.find_elements_by_css_selector("tr[role='row']")

            result = proxies[1].text.split(" ")
            print(f"proxies[1].text : {proxies[1].text}")
            print(f"result[-1] : {result[-1]}")

            if result[-1] != "yes":
                print(f"We scrapped all the https proxies. We can break the loop.")
                break

            for p in proxies:
                print(f"row : {p.text}")
                result = p.text.split(" ")

                if result[-1] == "yes":
                    PROXIES.append(result[0] + ":" + result[1])

            driver.find_element_by_xpath("*//a[text()='Next']").click()
            print("The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(0.9, 2.3))
    except Exception as ex:
        print(f"Something went wrong by scraping proxies from https://free-proxy-list.net/.")
        print(f"Let's try from http://free-proxy.cz/fr/proxylist/country/all/https/ping/all.")
        PROXIES = []
        try:
            # driver = webdriver.Chrome(chrome_options=co)
            driver = webdriver.Chrome(options=co)
            driver.get("http://free-proxy.cz/fr/proxylist/country/all/socks5/ping/all")
            print("The bot will sleep just a few seconds..............................")
            time.sleep(random.uniform(0.9, 2.3))
            proxies = driver.find_elements_by_xpath("*//table[@id='proxy_list']//tr")
            for p in proxies:
                print(f"row : {p.text}")
                print(f"len(row) : {len(p.text)}")
                if len(p.text) != 0:
                    result = p.text.split(" ")
                    PROXIES.append(result[0] + ":" + result[1])

            for i in range(2, 5):
                print(f"i = {i}")
                url = "http://free-proxy.cz/fr/proxylist/country/all/socks5/ping/all/" + str(i)
                driver.get(url)
                print("The bot will sleep just a few seconds..............................")
                time.sleep(random.uniform(0.9, 2.3))
                proxies = driver.find_elements_by_xpath("*//table[@id='proxy_list']//tr")

                for p in proxies:
                    list_row = str(p.text).split('\n')
                    print(f"row : {list_row[0]}")
                    if len(p.text) != 0:
                        result = p.text.split(" ")
                        PROXIES.append(result[0] + ":" + result[1])
        except Exception as ex:
            print(
                f"{ex} --> Something went wrong by scraping proxies from http://free-proxy.cz/fr/proxylist/country/all/https/ping/all.")
            print(f"Please contact support@phonebot.co")

    if driver:
        driver.close()
    return PROXIES

#=================================================================================================================
#=================================================================================================================
#=================================================================================================================

def proxy_driver(PROXIES):
    # ======================= DEFINE A RANDOM USER-AGENT ====================================================
    ua = UserAgent()
    useragent = ua.firefox
    print(f"useragent : {useragent}")

    # ======================= DEFINE A RANDOM PROXY =========================================================
    index_proxy = random.randint(0, len(PROXIES) - 1)
    proxy = str(PROXIES[index_proxy])
    proxy_split = str(proxy).split(':')
    print(proxy)

    # https://stackoverflow.com/questions/58873022/how-to-make-selenium-script-undetectable-using-geckodriver-and-firefox-through-p/58879076#58879076
    # profile = webdriver.FirefoxProfile('C:\\Users\\You\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\something.default-release')
    profile = webdriver.FirefoxProfile()
    PROXY_HOST = proxy_split[0]
    PROXY_PORT = proxy_split[1]
    USERNAME='centref'
    PASSWORD='lqU1x1d4eW'

    profile.set_preference("network.proxy.type", 1)
    #profile.set_preference("network.proxy.socks_username", USERNAME)
    #profile.set_preference("network.proxy.socks_password", PASSWORD)
    profile.set_preference("general.useragent.override", useragent)
    # profile.set_preference("network.proxy.http", PROXY_HOST)
    # profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.set_preference("network.cookie.cookieBehavior", 2)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "noProxy": [],
        "proxyType": "MANUAL"
    }

    options_proxy = {
        'proxy': {
            'http': 'http://centref:lqU1x1d4eW@' + proxy,
            'https': 'https://centref:lqU1x1d4eW@' + proxy,
            'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
        }
    }

    driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired,seleniumwire_options=options_proxy)
    time.sleep(10)

    return driver


def NoProxyDriver(headless=False):



    logger.info(" ======================= NoProxyDriver() ========================================")
    if platform.system() == 'Darwin':
        from webdriver_manager.chrome import ChromeDriverManager
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')


        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)



        logger.info(f"GOOGLE DESKTOP|||Chrome=>Google Search;NoProxyDriver; options : {str(options)}")
        # driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired)
        if headless:
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
            '''
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get:() => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
            print(driver.execute_script("return navigator.userAgent;"))
            '''

        else:
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
            '''
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get:() => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
            print(driver.execute_script("return navigator.userAgent;"))
            '''


    elif platform.system() == 'Windows':
        from webdriver_manager.firefox import GeckoDriverManager
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        #profile.set_preference('network.proxy.Kind', 'Direct')
        profile.set_preference('network.proxy.type',0)
        profile.update_preferences()
        from selenium.webdriver.firefox.options import Options
        #desired = DesiredCapabilities.FIREFOX
        logger.info(f"GOOGLE DESKTOP|||Firefox>Google Search;NoProxyDriver; profile : {str(profile)}")
        #driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired)
        if headless:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=profile,options=options)
        else:
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=profile)


    time.sleep(3)

    return driver
#=================================================================================================================

#==========================================================================================================
#==============================     FUNCTION GET ID FROM TABLE 'contacts'   ===============================
#==========================================================================================================
def Get_ID_from_Username(p_username,p_udid,p_platform):
    try:
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
        p_cursor1 = sqlite_connection.cursor()
        id_contact_tuple = p_cursor1.execute("SELECT id FROM contacts WHERE username=? AND platform=?",
                                                          (p_username, p_platform)).fetchone()
        id_contact = int(id_contact_tuple[0])  # We transform the id_contact in integer in order to store it in table
        sqlite_connection.commit()
        return id_contact
    except Exception as ex:
        logger.critical(f"{p_udid}|||{ex} --> ERROR Get_ID_from_Username")

#=================================================================================================================




# ========================================================================================================
# ==================  FUNCTION TO GET THE TEXT DISPLAYED IN SCREEN  =====================================
# ========================================================================================================
def GetTextfromScreenshot(p_driver='driver',p_udid='nophone_id',p_element='',p_mode=''):
    try:
        logger.info(f"{p_udid}|||# ================= Make Screenshot and get text with GetFacebookTextfromScreenshot =============")
        if p_element is None:
            imagestring=p_driver.get_screenshot_as_base64()
        else:
            imagestring=p_element.screenshot_as_base64

        if p_mode=='username_from_list':
            # Size of the image in pixels(size of orginal image)
            #(This is not mandatory)
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
            #(It will not change orginal image)
            image = im.crop((left, top, right, bottom))
        else:
            #pic = io.StringIO()
            image_string = io.BytesIO(base64.b64decode(imagestring))
            image = Image.open(image_string)
            #image.show()
        #print(pytesseract.image_to_string(image, lang='fra'))
        #tessdata_dir_config=r'--tessdata-dir "' + os.environ["TESSDATA_PREFIX"] + '"'
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        tesseract_command = sqlite_cursor.execute("SELECT tesseract FROM settings").fetchone()

        pytesseract.pytesseract.tesseract_cmd = tesseract_command[0]
        return pytesseract.image_to_string(image)
        #return pytesseract.image_to_string(image, lang='fra')
    #except ValueError:
        #print("error")
    except Exception as ex:

        logger.critical(
            f'''{p_udid}|||{ex} --> #ERROR! Something went wrong while making screenshot and OCR. Please check :\n
                                - you installed 'tesseract' for Windows => https://tesseract-ocr.github.io/tessdoc/4.0-with-LSTM.html#400-alpha-for-windows\n
                                - you download the french training file data => https://github.com/tesseract-ocr/tessdata/blob/master/fra.traineddata
                                - you place this french language data in the 'tessdata' folder(ex: C:\Program Files\Tesseract-OCR\\tessdata)\n
                                - you add the 'tesseract' folder in your environment variables.                        
                        ''')

#=============================================================================================================

def CleanOCRText(p_string):
    list_p_string = p_string.split("\n")
    print(f"list_p_string : {list_p_string}")
    p_string = ' '.join(list_p_string)
    p_string = p_string.lstrip()
    p_string = p_string.rstrip()
    print(f"p_string : {p_string}")

    return p_string



# ========================================================================================================
# ==================  FUNCTION TO GET THE TEXT DISPLAYED IN SCREEN  =====================================
# ========================================================================================================
def GetFacebookFullnameAndHeaderfromListMember(p_element,p_label):
    print(
        f"====================== GetFacebookFullnameAndHeaderfromListMemeber for {p_element} ============================")
    # === 1rst === We crop the image which contain the text
    imagestring = p_element.screenshot_as_base64

    print(f"p_label : {p_label}")

    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(imagestring))
    img = Image.open(image_string)
    #img.show()



    width, height = img.size
    # Setting the points for cropped image
    if p_label=='ADD FRIEND':
        left = width * 0.225
        right = width * 0.71
    elif p_label=='MESSAGE':
        left = width * 0.225
        right = width * 0.76
    elif p_label=='AJOUTER':
        left = width * 0.225
        right = width * 0.79
    elif p_label=='ENVOYER UN MESSAGE':
        left = width * 0.225
        right = width * 0.553
    else:
        left = width * 0.225
        right = width * 0.847

    print(f"left : {left/width}")
    print(f"right : {right/width}")
    top = 0
    bottom = height
    print(f"{left}, {top}, {right}, {bottom}")
    # Cropped image of above dimension
    #(It will not change orginal image)
    img_crop = img.crop((left, top, right, bottom))


    # ==============================================================
    # === 2nd === We extract the data text and string_text

    data_text = pytesseract.image_to_data(img_crop, lang='fra')
    print(data_text)
    string_text = pytesseract.image_to_string(img_crop, lang='fra')
    print(f"string_text : {string_text}")
    if string_text == '':
        print("PhoneBOt didn't succeed to OCR the text fullname. It will return empty string!")
        firstline=''
        secondline=''
        return firstline, secondline

    # ==============================================================
    # === 3rd === We will try first to get fullname and header byt the 'New member' method
    # === If there is the string 'New member', we can easily identify fullname and header

    # METHOD 1 WITH 'New member ' string
    list_brut_text_username_from_list = string_text.split('\n')
    index_user = 0
    print(f"list_brut_text_username_from_list : {list_brut_text_username_from_list}")
    print(f"len(list_brut_text_username_from_list) : {len(list_brut_text_username_from_list)}")

    list_fullname = []
    list_header = []
    new_member_detected = False
    for user in list_brut_text_username_from_list:
        if str(user).find("Nouveau membre") != -1 or str(user).find("New Member") != -1:
            new_member_detected = True

        if not new_member_detected:
            list_fullname.append(user)
        else:
            list_header.append(user)

    print(f"list_fullname : {list_fullname}")
    print(f"list_header : {list_header}")

    firstline = ''
    secondline = ''
    if new_member_detected:
        clean_list_fullname = []
        for user in list_fullname:
            if(user != "") and str(user).find("recent post") == -1 and str(user).find("récente") == -1 and str(
                    user).find("Modérateur") == -1 and str(user).find("Moderator") and str(user).find(
                    "publication") == -1:
                clean_list_fullname.append(user)

        for user in list_fullname:
            if str(user).find("Nouveau membre") != -1:
                clean_list_fullname.remove(user)
        for user in list_fullname:
            if str(user).find("New member") != -1:
                clean_list_fullname.remove(user)

        clean_list_header = []
        for user in list_header:
            if(user != "") and str(user).find("recent post") == -1 and str(user).find("récente") == -1 and str(
                    user).find("Nouveau membre") == -1 and str(user).find("New Member") == -1 and str(user).find(
                    "publication") == -1:
                clean_list_header.append(user)

        print(f"clean_list_fullname : {clean_list_fullname}")
        print(f"clean_list_header : {clean_list_header}")
        if clean_list_fullname:
            firstline = clean_list_fullname[0]
        if clean_list_header:
            for element in clean_list_header:
                secondline += element + ' '



    else:  # METHOD 2 WITHOUT 'New member ' string
        table_data_brut = str(data_text).split("\n")
        table_data_line = []
        final_table_data = []

        print(f"final_table_data ==============================================================")
        for line in table_data_brut:
            table_data_line = str(line).split("	")
            final_table_data.append(table_data_line)

        clean_final_table_data = []

        for line in final_table_data:
            print(line)
            try:
                #sometime we get a list index out of range because the table can produce lines which doesn't have 11 elements
                tmp_line_eleven=line[11]
                if line[11] != '' and line[11] != ' ' and line[11] != 'text' and line[11] is not None and  \
                        str(line[11]).find("recent post") == -1 \
                        and str(line[11]).find("récente") == -1 and str(line[11]).find("Modérateur") == -1 and \
                        str(line[11]).find("Moderator") == -1 and str(line[11]).find("publication") == -1 \
                        and str(line[11])[0] != '+' and str(line[11]).find('©') == -1:
                    clean_final_table_data.append([line[7], line[9], line[11]])
            except:
                logger.info(f"line[11] doesn't exist for line : {line}")


        print(f"clean_final_table_data ==============================================================")
        # for line in clean_final_table_data:
        print(line)

        clean2_final_table_data = []
        cpt = 1

        top = ''
        we_are_secondline = False
        for line2 in clean_final_table_data:
            print(f"{cpt} => {line2}")

            if cpt > 1:

                print(f"top : {top} - {type(top)}")
                print(f"line2[0] : {line2[0]} - {type(line2[0])}")
                difftop = abs(int(top) - int(line2[0]))
                print(f"diff top : {int(top)}-{int(line2[0])} = {difftop}")
                if difftop <= 1:
                    if not we_are_secondline:
                        firstline += line2[2] + ' '
                else:
                    if difftop <=(int(height) + int(line2[1])):
                        diffheight = abs(int(height) - int(line2[1]))
                        print(f"diff top : {int(height)}-{int(line2[1])} = {diffheight}")
                        if diffheight <= 1:
                            firstline += line2[2] + ' '
                        else:
                            we_are_secondline = True

                            secondline += line2[2] + ' '
                    else:
                        we_are_secondline = True
                        secondline += line2[2] + ' '


            else:
                top = line2[0]
                height = line2[1]
                firstline = line2[2] + ' '

            cpt += 1
            if cpt == len(final_table_data):
                break

    print(f"firstline : {firstline}")
    print(f"secondline : {secondline}")

    return firstline, secondline


# ========================================================================================================
# ==================  FUNCTION TO GET INDEX ELEMENT OF A LIST  =====================================
# ========================================================================================================
def index_of(val, in_list):
    try:
        return in_list.index(val)
    except Exception as ex:
        return -1


# ====================================================================================================================
# ============================ FONCTION TO CALCULATE THE DIFFERENCE BETWEEN 2 DATES ==================================
# ====================================================================================================================
def DifferenceBetween2Dates(date1,date2):
    difference = date1 - date2
    days, seconds = difference.days, difference.seconds
    hours = abs(days * 24 + seconds // 3600)
    minutes = abs((seconds % 3600) // 60)
    seconds = abs(seconds % 60)

    return hours,minutes,seconds




# ====================================================================================================================
# ============================ START APPIUM INSTANCE ================================================================
# ====================================================================================================================
def StartAppiumInstance(p_udid,p_systemPort,p_deviceName, p_version,p_os):

    # ======================== INITIALISATION OF DRIVER ================================
    logger.info(
        f"{p_udid}|||============== INITIALISATION OF DRIVER for Smartphone {p_udid}")
    logger.info(f"{p_udid}|||p_udid : {p_udid}")
    logger.info(f"{p_udid}|||p_systemPort : {p_systemPort}")
    logger.info(f"{p_udid}|||p_deviceName : {p_deviceName}")
    logger.info(f"{p_udid}|||p_version : {p_version}")
    logger.info(f"{p_udid}|||p_os : {p_os}")
    logger.info(
        f"{p_udid}|||===============================================================================================")

    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'
    desired_caps['platformName'] = p_os
    desired_caps['platformVersion'] = p_version
    desired_caps['deviceName'] = p_deviceName
    desired_caps['udid'] = p_udid
    desired_caps['noReset'] = 'true'
    desired_caps['systemPort'] = p_systemPort
    desired_caps['chromeDriverPort'] = p_systemPort
    desired_caps['appWaitDuration'] = 100000
    desired_caps['newCommandTimeout'] = 0
    desired_caps['wdaStartupRetries'] = 4
    desired_caps['wdaStartupRetryInterval'] = 20000
    desired_caps['uiautomator2ServerLaunchTimeout'] = 100000

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver

# ====================================================================================================================
# ============================ METHOD TO SEND A MAIL =================================================================
# ====================================================================================================================
def SendMail(p_from,p_name,p_password,p_subject,p_message_txt,p_message_html,p_to):
    msg = MIMEMultipart('alternative')


    # setup the parameters of the message
    password = p_password
    msg['From'] = p_name + "<" + p_from + ">"
    msg['To'] = p_to
    msg['Subject'] = p_subject

    # Create the body of the message(a plain-text and an HTML version).
    text = p_message_txt
    html = p_message_html
    '''
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
    '''

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    smtp_server = 'smtp.ionos.fr'
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(p_from, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    # create server









# ===================================================================================================================
# =================================== METHOD TO CLOSSE ALL THE DB AND CURSOR ========================================
# ===================================================================================================================
def CloseAllDB(mysql_db='',mysql_cursor='',sqlite_db='',sqlite_cursor=''):
    try:
        if sqlite_cursor:
            sqlite_cursor.close()
    except:
        logger.info("Error when closing 'cursor'.")

    try:
        if mysql_cursor:
            mysql_cursor.close()
    except:
        logger.info("Error when closing 'mycursor'.")
    try:
        if sqlite_db:
            sqlite_db.close()
    except:
        logger.info("Error when closing 'sqlite_connection'.")
    try:
        if mysql_db:
            mysql_db.close()
    except:
        logger.info("Error when closing 'mydb'.")




# === Function to get all the mac addresses ================================================
def get_mac_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield(interface,(snic.address))


# ===================================================================================================================
# ============================= FUNCTION TO CHECK THE MAC ADDRESS OF USER IN OUR SYSTEM =============================
# ===================================================================================================================
def CheckMacAddress(p_subscription_id):
    # ===============================================================================================================
    # ==================================== CONNECTION TO MYSQL AND READ config.ini ==================================
    # ===============================================================================================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            mycursor = mydb.cursor()
            break
        except:
            logger.info("Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            sys.exit()


    # ================================================================================================
    # =============================== let's check for MAC address ====================================
    # ================================================================================================
    # ==================================== EXTRACT MAC ADDRESS =======================================
    # ================================================================================================
    # --- extract the MAC address of local computer -------------------------------------------------
    # mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    #                        for ele in range(0, 8 * 6, 8)][::-1])
    mac_address = getmac.get_mac_address()
    logger.info("MAC Address of PC : " + mac_address)
    # ====================================================================================================
    # --- extract the MAC address from WP Database -------------------------------------------------
    sql_mac_address = "SELECT meta_value from  W551je5v_postmeta where meta_key = 'mac' AND post_id = '" + str(p_subscription_id) + "'"
    print(f"sql_mac_address : {sql_mac_address}")
    mycursor.execute(sql_mac_address)
    wp_mac_address = mycursor.fetchone()
    #print(f"wp_mac_address : {wp_mac_address}")

    if wp_mac_address is None or wp_mac_address[0] == '':
        # ================================================================================================
        # ====================IF MAC ADDRESS IS NOT FOUND IN TABLE post_meta , WE ADD IT==================
        # ================================================================================================
        logger.info("1rst installation on this device. We update database")
        sql_mac_address_add = "INSERT INTO W551je5v_postmeta(meta_value,meta_key,post_id) VALUES('" + mac_address + "','mac','" + str(p_subscription_id) + "')"
        print(f"sql_mac_address_add : {sql_mac_address_add}")
        mycursor.execute(sql_mac_address_add)
        mydb.commit()
        logger.info("We just added your new MAC Address")
        # --- We test if Sqlite DB is there or not
        # --- otherwise we compare both Mac address
        return True
    elif str(wp_mac_address[0]) == mac_address:
        # ================================================================================================
        # =======================IF MAC ADDRESS WAS FOUND IN TABLE post_meta, IT IS PERFECT ==============
        # ================================================================================================
        logger.info("MAC Address was already saved in our system and it is correct. Let's carry on....")
        CloseAllDB(mydb, mycursor)
        return True


    else:

        macs = dict(get_mac_addresses(psutil.AF_LINK))
        list_mac_adress = []

        # User can sometimes use ethernet or wifi connection which are 2 differents MAC Address
        # SO we make the list of local Mac Address and check
        for mac in macs:
            list_mac_adress.append(str(macs.get(mac)).lower().replace('-',':'))
        print(f"wp_mac_address[0] : {wp_mac_address[0]}")
        print(f"mac_address : {mac_address}")
        print(f"list_mac_adress : {list_mac_adress}")
        if str(wp_mac_address[0]).lower() in list_mac_adress and str(mac_address).lower() in list_mac_adress:
            logger.info("PhoneBot think you are using another internet connection on your device. It should be ok.")
            return True

        # User can start to use PhoneBot with Free license and then subscribe for pay license
        # So We will check that the actual License is not 'trialXXXXXX'. Because if it is a pay license, we will
        # change the mac address for this license.
        # We need also to be sure user cannot install this license on another computer(so another mac)

        '''
        # we extract the 5 first letters of license to check if it is trial
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))
        license_key_config = config.get('Settings', 'license_key')
        first_part_license = license_key_config[:5]


        # we extract the product name attached to this MAC address : is it Gold? Silver? Bronze? License? or Trial?
        sql_product_name = "SELECT meta_value from  W551je5v_postmeta where meta_key = 'product_name' AND post_id = '" + str(
            p_subscription_id) + "'"
        mycursor.execute(sql_product_name)
        sql_product_name = mycursor.fetchone()

        if first_part_license != 'trial':
            sql_update_mac_address = "UPDATE W551je5v_postmeta set meta_value='" + str(mac_address) + "' where meta_key = 'mac' AND post_id = '" + str(
                p_subscription_id) + "'"
        '''
        # ================================================================================================
        # ================IF MAC ADDRESS WAS FOUND IN TABLE post_meta AND DOESN'T CORRESPOND =============
        # ================================================================================================
        logger.error(
            "PhoneBot is already installed on another device. Please contact support@phonebot.co to reset it and allow you to install Phonebot on this new computer.")
        logger.error(
            "Maybe you use an ethernet cable to connect to internet the previous time and now you are using your wifi connexion?")
        logger.error(
            "You can't change the way you connect your computer to the internet. We are sorry for the inconvenience but this is the way it is to protect PhoneBot from scammers!")
        logger.error(
            "Please contact support@phonebot.co to reset it and allow you to install Phonebot on this new computer.")
        CloseAllDB(mydb, mycursor)
        logger.error(
            "PhoneBot is already installed on another device. Please contact support@phonebot.co to reset it and allow you to install Phonebot on this new computer.")
        return False

# ===================================================================================================================
# ============================= FUNCTION TO CHECK config.ini file ======================================
# =================================================================
# ===================================================================================================================

def CheckConfigIni():
    # =================================================================================================================
    # =============================== CHECK IF LICENSE KEY AND EMAIL ARE FILLED =======================================
    # =================================================================================================================
    # [1] We check immediatly if license key and email client are filled in the config.ini
    # --- We use configparser to extract from config.ini the license_key ------------------------------------
    try:
        # ---on lit le fichier config.ini
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))
        license_key_ok = False
        license_key_config = config.get('Settings', 'license_key')
        if license_key_config == '':

            logger.error(f"ERROR : PhoneBot couldn't find your license key in LoadFile('config.ini') file!")
            logger.error(
                "You can find your license key on PhoneBot website:https://phonebot.co/my-account/view-license-keys/")
            #logger.error("Please open with notepad your config.ini file located in your PhoneBot installation folder.")
            answer=''
            while answer!='y' or answer!='n':
                answer = input("Would you like to edit your config.ini file now?(y/n):")
                if answer=='y':
                    #config_ini_path = str(phonebot_folder[0]) + '\config.ini'
                    config_ini_path = LoadFile('config.ini')

                    proc = subprocess.Popen(config_ini_path,
                                            shell=True,
                                            stdin=None, stdout=True, stderr=None, close_fds=True)
                    proc.wait()
                    break

                elif answer =='n':
                    logger.error("As you didn't add your license key, PhoneBot may bug in a few seconds. You'll have to restart PhoneBot.")

                    break
                else:
                    logger.error("Please answer by 'y' or 'n'!")
        else:
            license_key_ok=True


        config.read(LoadFile('config.ini'))
        email = config.get('Settings', 'email')
        email_ok = False
        if email == '':



            logger.error("ERROR : PhoneBot couldn't find your email in LoadFile('config.ini') file!")
            logger.error("You can find your email on PhoneBot website:https://phonebot.co/my-account/")
            # logger.error("Please open with notepad your config.ini file located in your PhoneBot installation folder.")
            answer = ''
            while answer != 'y' or answer != 'n':
                answer = input("Would you like to edit your config.ini file now?(y/n):")
                if answer == 'y':
                    # config_ini_path = str(phonebot_folder[0]) + '\config.ini'
                    config_ini_path = LoadFile('config.ini')

                    proc = subprocess.Popen(config_ini_path,
                                            shell=True,
                                            stdin=None, stdout=True, stderr=None, close_fds=True)
                    proc.wait()
                    break

                elif answer == 'n':
                    config.read(LoadFile('config.ini'))
                    email = config.get('Settings', 'email')
                    if email == '':
                        logger.error(
                            "As you didn't add your license key, PhoneBot may bug in a few seconds. You'll have to restart PhoneBot.")


                    break
                else:
                    logger.error("Please answer by 'y' or 'n'!")
        else:
            email_ok = True


        if license_key_ok and email_ok:
            logger.info("Your config.ini file is OK.")
            result_config_ini=True
        else:
            result_config_ini=False
        return result_config_ini

    except Exception as e:
        logger.critical(f"Problem with config.ini => {e}. Please have a look at your config.ini file.")
        CountDown(15)
    #except ValueError:
        #print("ERROR")





def ExecuteSQLFromFile(filename):
    '''
    logger.info("PhoneBot will update Database db.db")
    conn = sqlite3.connect(LoadFile('db.db'))
    c = conn.cursor()
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    '''
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect(LoadFile('db.db'))
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()









# ===================================================================================================================
# ============================= FUNCTION TO CHECK THE PAYMENT OF SUBSCRIPTION, ======================================
# ============================= THE LICENSE KEY, EXPIRATION DATE AND MAC ADDRESS ====================================
# ===================================================================================================================
def CheckSubscription():
    try:

        # ===================================================================================================================
        # ==================================== CONNECTION TO MYSQL AND READ config.ini ======================================
        # ===================================================================================================================
        while True:
            try:
                mydb = mysql.connector.connect(
                    host="217.160.43.98",
                    port=3306,
                    user="reader",
                    passwd="Arina@221204",
                    database="wp_fi1lb"
                )
                mycursor = mydb.cursor()
                break
            except:
                logger.info("Problem with Mysql Database! It is certainly a problem of Internet connexion.")
                sys.exit()



        # ---on lit le fichier config.ini
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))
        # =========================================================================================================
        # Check for config file
        while not CheckConfigIni():
            logger.info("Your config.ini file is not ok.")
        # ---on lit le fichier config.ini
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))
        # =========================================================================================================
        if Path(LoadFile('db.db')).is_file():
            logger.info("Database LoadFile('db.db') File exist")
            sqlite_connection = sqlite3.connect(LoadFile('db.db'))
            cursor = sqlite_connection.cursor()
        else:
            logger.critical(
                f"We couldn't find your local database. Please check that the file LoadFile('db.db') is in the folder of Phonebot.\nIf LoadFile('db.db') is not then, reinstall PhoneBot.")
            CloseAllDB(mydb, mycursor)
            sys.exit(
                f"We couldn't find your local database. Please check that the file LoadFile('db.db') is in the folder of Phonebot.\nIf LoadFile('db.db') is not then, reinstall PhoneBot.")

        # --- First of all, we will update the "status" column to 0 to all the smartphones in order to make them all disconnected
        # ---- and then the Loop below will update startus=1 for the smartphones connected
        cursor = sqlite_connection.cursor()
        # ===================================================================================================================
        # === Get the date of today from online server -----------------------------------------------------------
        res = urlopen('http://just-the-time.appspot.com/')
        date_now_online = res.read().strip()
        date_now_online_str = date_now_online.decode('utf-8')
        date_now_online_DATE = datetime.strptime(date_now_online_str, '%Y-%m-%d %H:%M:%S')
        print(f"date_now_online_DATE : {date_now_online_DATE}-{type(date_now_online_DATE)}")
        # ===================================================================================================================
        # ==================================== GET THE USER ID FROM WP DATABASE =============================================
        # ===================================================================================================================
        email = config.get('Settings', 'email')
        license_key_config = config.get('Settings', 'license_key')
        logger.info(f"Your email in config.ini is '{email}")
        logger.info(f"Your license_key in config.ini is '{license_key_config}")
        sql_user_id = "SELECT ID from W551je5v_users WHERE user_email = '" + str(email) + "'"
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sql_user_id)
        user_id = mycursor.fetchone()
        if user_id is None:
            logger.critical("There are no user id in Phonebot.co Database! Check your config.ini. Maybe you didn't pay your subscription or your trial period has expired.\nIf your subscription is active, try to restart PhoneBot. if the problem persists please contact support@phonebot.co")
            CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
            sys.exit()
        else:
            user_id = str(user_id[0])
            logger.info("User ID found on Phonebot.co :-) :" + str(user_id))
        # ===================================================================================================================




        sql_find_licenses = f"SELECT hash,user_id,CAST(expires_at AS CHAR),order_id,product_id,id from W551je5v_lmfwc_licenses WHERE user_id='{user_id}'"

        print(f"sql_find_licenses : {sql_find_licenses}")

        logger.info(f"You filled your license key in configi.ini.")
        mycursor.execute(sql_find_licenses)

        tuple_hash_license_key = mycursor.fetchall()
        list_hash_license_key = [item for item in tuple_hash_license_key]

        license_key_found = False
        for hash_license_key in list_hash_license_key:
            if check_license(license_key_config, hash_license_key[0]):
                logger.info("License key found in PhoneBot.co.")

                order_id_of_license = hash_license_key[0]
                date_expire_str = hash_license_key[2]
                product_id = hash_license_key[4]
                order_id = hash_license_key[3]
                license_id = hash_license_key[5]

                license_key_found = True
                break
            else:
                logger.info("PhoneBot didn't match your License key.")



        # === If we found a correct license key in MYSQL PhoneBot, we can start to check the expiration date and the mac address
        if license_key_found:
            logger.info("You filled your license key in config.ini and PhoneBot checked it correctly.")

            # === Let's get imediatly the subscription ID as we will need it for the rest
            # === 1rst we need to get all the subscription of user in relation with the product in order to get the list of orders
            sql_subscription_list_of_user_for_a_product = f"select W551je5v_postmeta.post_id FROM W551je5v_postmeta INNER JOIN W551je5v_posts ON W551je5v_postmeta.post_id = W551je5v_posts.ID WHERE W551je5v_postmeta.meta_value='{order_id}' and W551je5v_posts.post_author = '{user_id}' and W551je5v_posts.post_type = 'subscription'"
            print(f"sql_subscription_list_of_user_for_a_product : {sql_subscription_list_of_user_for_a_product}")
            mycursor.execute(sql_subscription_list_of_user_for_a_product)
            tuple_subscription = mycursor.fetchall()
            if tuple_subscription:
                list_subscription = [item[0] for item in tuple_subscription]
                print(f"list_subscription : {list_subscription}")

                subscription_id=list_subscription[0]
            else:
                logger.error("PhoneBot didn't find your subscritpion in our system. Please contact support@phonebot.co")
                CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                sys.exit()
            # === let's check for expiration date ================================================================

            # =============================================================================================================
            # ===================== IF date_expire EXIST, IT MEANS IT IS A TRIAL LICENSE ==================================
            # =============================================================================================================
            if date_expire_str is not None and date_expire_str != '':
                date_expire = datetime.strptime(date_expire_str, "%Y-%m-%d %H:%M:%S")
                print(f"date_expire : {date_expire}-{type(date_expire)}")
                logger.info("Your Trial License is still valid.")
                if date_expire < date_now_online_DATE:
                    logger.info("Your Trial License expired. You need to buy a license in order to use PhoneBot. We gave you for free during 2 weeks our PhoneBot. Did it help you to growth?")
                    logger.info("We gave you for free during 2 weeks our PhoneBot. Did it help you to growth? If yes, why not to invest in a license?")
                    logger.info("Please visit https://phonebot.co/prices/ in order to purchase a PhoneBot license.")
                    message_txt = f'Hi,\n\Your Free trial License expired. You need to buy a pay plan in order to use PhoneBot\n\nPlease visit https://phonebot.co/prices/ in order to purchase a PhoneBot license.\n\nKind regards.\n\nPhoneBot.co\'s team\n\nhttps://phonebot.co'
                    message_html = f"""
                                                        <html>
                                                          <head></head>
                                                          <body>
                                                            <p>Hi,<br><br>
                                                            Your Free trial License expired. You need to buy a pay plan in order to use PhoneBot<br><br>
                                                            Please visit <a href='https://phonebot.co/prices/'>https://phonebot.co/prices/</a> in order to purchase a PhoneBot license.<br><br>
                                                            If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                                            Kind regards.<br><br>
                                                            PhoneBot.co\'s team<br>
                                                            https://phonebot.co
                                                            </p>
                                                          </body>
                                                        </html>
                                        """
                    try:
                        SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                           'ALERT: Your Free trial License expired', message_txt, message_html, email)
                    except Exception as ex:
                        logger.error(f"{ex} => Error sending mail reminder about payment.")

                    CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                    sys.exit()
                else:
                    logger.info("Your Trial license seems to be valid for the moment.")
                    logger.info("PhoneBot check now if you run the bot on correct computer...")
                    mac_address_ok=CheckMacAddress(subscription_id)
                    if mac_address_ok:
                        logger.info("Your MAC Address is ok. PhoneBot tested everything regarding your subscription. It can run the bots.")
                        CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                        return user_id,license_key_config
                    else:
                        logger.info(
                            "Your MAC Address is not ok.")
                        CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                        sys.exit()
            else:
                # ========================================================================================================
                # ===================== THERE ISN'T date_expire, IT MEANS IT IS A PAID LICENSE ===========================
                # ========================================================================================================
                # === We need to get all the orders from product_id and check if the last order was paid


                # === We just get all the subscriptions of user for the product connected to his license, now
                # === we need to get the list of orders
                for subscription_id in list_subscription:
                    sql_order_list_of_user_for_a_subscription=f"SELECT meta_value FROM W551je5v_postmeta WHERE W551je5v_postmeta.post_id='{subscription_id}' and meta_key='order_id'"
                    mycursor.execute(sql_order_list_of_user_for_a_subscription)
                    tuple_orders = mycursor.fetchall()
                    list_orders = [item[0] for item in tuple_orders]
                    print(f"list_orders : {list_orders}")

                # === Now we have the list of orders connected to the subscription in relation of the product
                # === connected to his license,, we need to get the last order ID as it will be the most recent
                # === then we'll be able to check the status of this order if it is complete or not
                order_found = False

                print(f"product_id : {product_id} - {type(product_id)}")
                # === We add these lines of code to handle the Lifetime license issue =========================
                if product_id != 6005:

                # ==============================================================================================

                    if list_orders is None or list_orders == '' or len(list_orders) == 0:
                        logger.error(f"There are no order id for subscription N° {subscription_id} - product N° {product_id} - user N° {user_id} in Phonebot.co Database!:-( Please contact support@phonebot.co")
                        logger.info(f"PhoneBot didn't find order...Mmmmm... So PhoneBot will try to search for last_order_id.")
                        sql_last_order_id = f"SELECT meta_value from W551je5v_postmeta WHERE meta_key='last_order_id' AND post_id='{subscription_id}'"
                        print(f"sql_last_order_id : {sql_last_order_id}")
                        mycursor.execute(sql_last_order_id)
                        tuple_sql_last_order_id = mycursor.fetchall()

                        if tuple_sql_last_order_id:

                            list_orders = [item[0] for item in tuple_sql_last_order_id]
                            print(f"list_orders : {list_orders}")
                            order_found=True
                        else:
                            logger.error(f"There are DEFININITLY not order id for subscription N° {subscription_id} - product N° {product_id} - user N° {user_id} in Phonebot.co Database!:-( Please contact support@phonebot.co")
                            sys.exit("There are no order id in Phonebot.co Database!:-( Please contact support@phonebot.co")
                    else:
                        order_found = True




                    if order_found:
                        last_order = max(list_orders)
                        print(f"last_order : {last_order}")
                        sql_status_and_date_of_last_order=f"SELECT post_status, CAST(post_modified AS CHAR) FROM W551je5v_posts WHERE ID='{last_order}'"
                        print(f"sql_status_and_date_of_last_order : {sql_status_and_date_of_last_order}")
                        mycursor.execute(sql_status_and_date_of_last_order)
                        status_and_date = mycursor.fetchall()
                        print(f"status_and_date : {status_and_date}")
                        order_status = status_and_date[0][0]
                        order_date = status_and_date[0][1]
                        print(f"order_date : {order_date}/type : {type(order_date)}")

                        # order_id = str(order_id[0]) We don't need this line as we already transform the order_id tuple in list
                        logger.info(f"Order id found on Phonebot.co :-) => {last_order} - Status: {order_status} - Date : {order_date}")
                        order_found = True



                        # =================================================================================================
                        # ============================= WE NEED TO CHECK THE STATUS OF THE ORDER ==========================
                        # =================================================================================================
                        # ==== IF status is not completed ------------------------------------------------------------------------
                        if order_status != 'wc-completed':
                            logger.error(f"The status of your order is not 'complete'.")
                            print(f"order_status : {order_status}")

                            hours, minutes, seconds = DifferenceBetween2Dates(date_now_online_DATE, datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S"))
                            print(f"hours : {hours}")
                            # I don't know why I choose >48. So I'll put >0
                            #if hours > 48:
                            if hours > 24:
                                logger.info(f"Payment of subscription has not been done for the moment.")
                                message_txt = f'Hi,\n\nYour subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.\n\nWould you please update your payment method on https://phonebot.co/my-account/payment-methods/.\n\nYour PhoneBot will be blocked in 24h if you don\'t pay your subscription.\n\nIf you think this is a mistake, please contact us as soon as possible at support@phonebot.co.\n\nKind regards.\n\nPhoneBot.co\'s team\n\nhttps://phonebot.co'
                                message_html = f"""
                                                        <html>
                                                          <head></head>
                                                          <body>
                                                            <p>Hi,<br><br>
                                                            Your subscription to PhoneBot suppose to be paid the {order_date}. We are the {date_now_online_DATE} and obviously no payment was done.<br><br>
                                                            Would you please update your payment method on <a href='https://phonebot.co/my-account/payment-methods/'>https://phonebot.co/my-account/payment-methods/</a>.<br><br>
                                                            Your PhoneBot is blocked because you don't pay your subscription.<br><br>
                                                            If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                                            Kind regards.<br><br>
                                                            PhoneBot.co\'s team<br>
                                                            https://phonebot.co
                                                            </p>
                                                          </body>
                                                        </html>
                                        """
                                try:
                                    SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                                       'ALERT: You have to pay your subscription', message_txt,
                                                       message_html, email)
                                except Exception as ex:
                                    print(f"{ex} => Error sending mail reminder about payment.")

                                CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                                sys.exit("There are no order id in Phonebot.co Database!:-( Please contact support@phonebot.co")
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
                                                                                        Your PhoneBot will be blocked very soon if you don't pay your subscription.<br><br>
                                                                                        If you think this is a mistake, please contact us as soon as possible at support@phonebot.co.<br><br>
                                                                                        Kind regards.<br><br>
                                                                                        PhoneBot.co\'s team<br>
                                                                                        https://phonebot.co
                                                                                        </p>
                                                                                      </body>
                                                                                    </html>
                                                                    """
                                try:
                                    SendMail('noreply@phonebot.co', 'PhoneBot.co', 'Lormont@33310',
                                             'ALERT: You have to pay your subscription', message_txt,
                                             message_html, email)
                                except Exception as ex:
                                    print(f"{ex} => Error sending mail reminder about payment.")
                                return user_id, license_key_config


                        else:
                            # ==== IF status is completed ------------------------------------------------------------------------
                            logger.info(f"Payment of subscription is ok.")
                            logger.info(f"PhoneBot will check now your MAC Address.")
                            mac_address_ok = CheckMacAddress(subscription_id)
                            if mac_address_ok:
                                logger.info(
                                    "Your MAC Address is ok. PhoneBot tested everything regarding your subscription. It can run the bots.")
                                CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                                return user_id,license_key_config
                            else:
                                logger.error("Your MAC Address is not ok.")
                                CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
                                sys.exit()
                    else:
                        logger.error("PhoneBot couldn't find your order ID. Please contact support@phonebot.co")
                        CloseAllDB(mydb, mycursor, sqlite_connection, cursor)
                        sys.exit()
                else:
                    logger.info("You're lucky guy! You have the lifetime license! :-) Enjoy!!!")

        else:
            logger.info("You filled your license key in config.ini but PhoneBot couldn't find it in our server. Please edit your config.ini file.")

        CloseAllDB(mydb, mycursor,sqlite_connection,cursor)
        return False,False
    except ValueError:
        "Error check check subscription"



# =============================================================================================================
# ============================ FUNCTION TO PLAY,STOP_PAUSE THE BOTS =============================================
# =============================================================================================================

def PlayStopPause(p_udid,p_action):
    # === Initialisation of SQLITE DB ========================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    if p_udid=='':
        p_udid='SYSTEM'

    what_to_do=sqlite_cursor.execute("SELECT play_stop_pause FROM settings").fetchone()
    if what_to_do:
        if what_to_do[0]==1:
            # STOP
            logger.info(f"{p_udid}|||PhoneBot has been STOPPED {p_action}.")
            sqlite_cursor.close()
            sqlite_connection.close()
            sys.exit()
        elif what_to_do[0]==2:
            # PAUSE
            logger.info(f"{p_udid}|||PhoneBot is on PAUSE {p_action}.")
            while True:
                time.sleep(10)
                what_to_do = sqlite_cursor.execute("SELECT play_stop_pause FROM settings").fetchone()
                if what_to_do[0]==0:
                    # PLAY
                    sqlite_cursor.close()
                    sqlite_connection.close()
                    break
                elif what_to_do[0]==1:
                    # STOP
                    logger.info(f"{p_udid}|||PhoneBot STOP {p_action}.")
                    sqlite_cursor.close()
                    sqlite_connection.close()
                    sys.exit()
                    while True:
                        PROCNAME = "python.exe"
                        PROCNAME_ADB = "adb.exe"
                        PROCNAME_NODE = "node.exe"
                        for proc in psutil.process_iter():
                            if proc.name() == PROCNAME:
                                # print(f"PhoneBot stop : {proc}")
                                print(f"PhoneBot stop. Thanks for using PhoneBot.")
                                try:
                                    proc.kill()
                                except:
                                    sys.exit()

                            if proc.name() == PROCNAME_ADB:
                                # print(f"PhoneBot stop : {proc}")
                                print(f"Adb stop. Thanks for using PhoneBot.")
                                try:
                                    proc.kill()
                                except:
                                    sys.exit()
                            if proc.name() == PROCNAME_NODE:
                                # print(f"PhoneBot stop : {proc}")
                                print(f"Node stop. Thanks for using PhoneBot.")
                                try:
                                    proc.kill()
                                except:
                                    sys.exit()
                    break





# =============================================================================================================
# ============================ METHOD TO KILL ALL THE APPS RUNNING EXCEPT THE ONE WE NEED =====================
# =============================================================================================================
def KillApps(p_udid,p_exception):
    table_of_applications=[
        "com.google.android.apps.maps",
        "com.facebook.katana",
        "com.twitter.android",
        "com.linkedin.android",
        "com.instagram.android",
        "com.facebook.orca",
        "com.reddit.frontpage",
        "com.producthuntmobile",
        "com.meetup",
        "org.telegram.messenger",
        "com.android.mms",
        "com.google.android.apps.messaging"
    ]
    adb_command_list_process = "adb -s " + p_udid + " shell ps"
    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result_app_running = os.popen(adb_command_list_process).read()
    #print(result_app_running)
    result_app_running_lines=str(result_app_running).split('\n')
    #print(result_app_running_lines)
    for line in result_app_running_lines:
        if line.find(p_exception)==-1:
            for application in table_of_applications:
                if line.find(application)!=-1:
                    logger.info(f"PhoneBot found {application} Running. It will kill it in order to avoid any issue.")
                    line_table=line.split(" ")
                    thread_table=[]
                    for element in line_table:
                        if element!=" " and element!="" and element is not None:
                            thread_table.append(element)
                    #for thread in thread_table:
                        #pass
                        #print(f"{thread}")
                    print(f"The thread ID N°{thread_table[1]} of {application} : {thread_table[8]}")
                    application_in_ps=str(thread_table[8])
                    pos_two_points=application_in_ps.find(':')
                    if pos_two_points!=-1:
                        application_in_ps = application_in_ps[0:pos_two_points]
                        print(f"application_in_ps : {application_in_ps}")
                    adb_command_kill_a_process = "adb -s " + p_udid + " shell am force-stop " + application_in_ps
                    print(adb_command_kill_a_process)
                    if platform.system() == 'Darwin':
                        home_user = os.environ['HOME']
                        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
                        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                                stderr=subprocess.STDOUT)
                    os.popen(adb_command_kill_a_process)


# ==================================================================================================================
# ========================= FUNCTION TO GET THE ID NUMBER(Between 1 and 10) OF THE PHONE ==========================
# ==================================================================================================================
def GetSmartphoneIDFromSerialSmartphone(p_udid,p_user_id):
    p_udid = str(p_udid)
    # ==================================================================================
    # ===================== Get the product ID =========================================
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )


            break

        except Exception as ex:
            logger.critical(f"{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")

            time.sleep(5)

    mycursor = mydb.cursor(buffered=True)

    sql_find_serial = "select meta_key from W551je5v_usermeta where meta_value= '" + p_udid + "' AND meta_key like '%smartphone_%_serial_number%' AND user_id=" + p_user_id
    mycursor.execute(sql_find_serial)
    serial_smartphone_tuple = mycursor.fetchall()

    if serial_smartphone_tuple:

        if len(serial_smartphone_tuple) > 1:
            logger.critical(
                f"{p_udid}||| ERROR. PhoneBot found several times the serial number N° {p_udid} in your 'Account details' on our website https://phonebot.co.")
            logger.critical(
                f"{p_udid}||| Please edit the configuration of your bot in order to remove these duplicate serial number => https://phonebot.co/my-account/edit-account/#configuration_page")
            return 0
        else:
            logger.info(f"{p_udid}|||serial_smartphone_tuple : {serial_smartphone_tuple}")
            serial_smartphone = serial_smartphone_tuple[0][0]
            smartphone_id = serial_smartphone[len(serial_smartphone) - 1:]
            logger.info(f"{p_udid}|||smartphone id for {p_udid} : {smartphone_id}")
            return int(smartphone_id)
    else:
        logger.critical(
            f"{p_udid}||| ERROR. PhoneBot couldn't find the serial number N° {p_udid} in your 'Account details' on our website https://phonebot.co.")
        logger.critical(
            f"{p_udid}||| Please edit the configuration of your bot in order to add the serial number of your smartphone => https://phonebot.co/my-account/edit-account/#configuration_page")
        return 0



# ==================================================================================================================
# ================ FUNCTION TO  WHICH APPLICATION ARE ENABLE IN THE 'My account details' of USER ===================
# ==================================================================================================================
def GetApplicationsEnableFromSmartphoneID(p_id, p_udid,p_user_id):
    p_id = str(p_id)
    while True:
        try:
            mydb = mysql.connector.connect(
                host="217.160.43.98",
                port=3306,
                user="reader",
                passwd="Arina@221204",
                database="wp_fi1lb"
            )
            break

        except Exception as ex:
            logger.critical(f"{ex} --> Problem with Mysql Database! It is certainly a problem of Internet connexion.")
            PopupMessage("Problem with Internet connection!",
                          "PhoneBot could not connect to Database! It is certainly a problem of Internet connexion.")

            time.sleep(5)
    mycursor = mydb.cursor(buffered=True)
    sql_find_application_enable = "select meta_value from W551je5v_usermeta where meta_key= 'smartphone_" + p_id + "_what_automate_" + p_id + "' AND user_id=" + p_user_id
    print(f"sql_find_application_enable : {sql_find_application_enable}")
    mycursor.execute(sql_find_application_enable)
    brut_value_application_enable_tuple = mycursor.fetchone()
    brut_value_application_enable = brut_value_application_enable_tuple[0]
    logger.info(f"{p_udid}|||brut_value_application_enable : {brut_value_application_enable}")
    facebook = False
    instagram = False
    linkedin = False
    twitter = False
    telegram = False
    gmap = False
    sms = False
    if str(brut_value_application_enable).find('facebook') != -1:
        facebook = True
    if str(brut_value_application_enable).find('instagram') != -1:
        instagram = True
    if str(brut_value_application_enable).find('linkedin') != -1:
        linkedin = True
    if str(brut_value_application_enable).find('twitter') != -1:
        twitter = True
    if str(brut_value_application_enable).find('telegram') != -1:
        telegram = True
    if str(brut_value_application_enable).find('gmap') != -1:
        gmap = True
    if str(brut_value_application_enable).find('sms') != -1:
        sms = True

    return facebook, instagram, linkedin, twitter, telegram, gmap, sms


# ===============================================================================================================
# ======================= FUNCTION TO KNOW WHICH SMS APP IS USING THE SMARTPHONE ================================
# ===============================================================================================================
def WhatIsMessageingApp(p_udid):
    android_messaging="com.google.android.apps.messaging"
    android_messaging_activity=".ui.ConversationListActivity"
    android_messaging_new = "com.google.android.apps.messaging:id/start_new_conversation_button"
    android_messaging_number_field = "com.google.android.apps.messaging:id/recipient_text_view"
    android_messaging_send_to_number="//android.widget.ListView/android.widget.FrameLayout"
    android_messaging_message_field = "com.google.android.apps.messaging:id/compose_message_text"
    android_messaging_send_button = "com.google.android.apps.messaging:id/send_message_button_icon"
    android_messaging_start_new_sms=".conversation.screen.ConversationActivity"
    android_messaging_back_FR=""
    android_messaging_back_EN = ""

    android_mms="com.android.mms"
    android_mms_activity="com.android.mms.ui.BootActivity"
    android_mms_new = "com.android.mms:id/action_compose_new"
    android_mms_number_field = "com.android.mms:id/recipients_editor"
    android_mms_send_to_number =""
    android_mms_message_field="com.android.mms:id/embedded_text_editor"
    android_mms_send_button="com.android.mms:id/send_button_sms"
    android_mms_start_new_sms = ".ui.ComposeMessageActivity"
    android_mms_back_FR = "//android.widget.ImageButton[@content-desc='Parcourir vers le haut']"
    android_mms_back_EN = "//android.widget.ImageButton[@content-desc='Navigate up']"
    # ===========================================================================================================
    # === Test if 'com.google.android.apps.messaging' is the SMS app

    adb_command = "adb -s " + p_udid + " shell pm list packages -f " + android_messaging
    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result_app_installed = os.popen(adb_command).read()

    print(f"result_app_installed android_messaging : {result_app_installed}")

    if result_app_installed:
        logger.info(f"'{android_messaging}' is installed on Smartphone '{p_udid}' \n {result_app_installed}")
        adb_command = "adb -s " + p_udid + " shell pm clear " + android_messaging
        return android_messaging,android_messaging_activity,android_messaging_new,android_messaging_number_field,android_messaging_send_to_number,android_messaging_message_field,android_messaging_send_button,android_messaging_start_new_sms
    else:
        logger.error(f"There is not '{android_messaging}' application installed on smartphone '{p_udid}'")

    # ===========================================================================================================
    # === Test if 'com.android.mms' is the SMS app

    adb_command = "adb -s " + p_udid + " shell pm list packages -f " + android_mms
    if platform.system() == 'Darwin':
        home_user = os.environ['HOME']
        adb_command_line = "sudo chmod 755 " + home_user + '/Android/platform-tools/adb'
        proc = subprocess.Popen(adb_command_line, shell=True, stdout=True, stdin=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    result_app_installed = os.popen(adb_command).read()

    print(f"result_app_installed android_mms : {result_app_installed}")

    if result_app_installed:
        logger.info(f"'{android_mms}' is installed on Smartphone '{p_udid}' \n {result_app_installed}")
        adb_command = "adb -s " + p_udid + " shell pm clear " + android_mms
        return android_mms,android_mms_activity,android_mms_new,android_mms_number_field,android_mms_send_to_number,android_mms_message_field,android_mms_send_button,android_mms_start_new_sms
    else:
        logger.error(f"There is not '{android_mms}' application installed on smartphone '{p_udid}'")

def CountDown(p_seconds=15):
    for remaining in range(p_seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining before PhoneBot resumes.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
















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


# =======================================================================================================
# ============================ Method to add a column ===================================================
# =======================================================================================================
def AddColumn(p_db,p_table,p_new_column,p_type):
    if p_db=="sqlite":
        # === Let's add the missing columns:
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()
        try:
            sqlite_cursor.execute(f'ALTER TABLE {p_table} ADD COLUMN {p_new_column} {p_type};')
            sqlite_connection.commit()
            logger.info(f"PhoneBot add successfully the missing column {p_new_column} in table {p_table}.")
        except Exception as er:
            logger.error(f"{er} -> SQLITE -> PhoneBot couldn't add the missing column {p_new_column} in table {p_table}.")

        sqlite_cursor.close ()
        sqlite_connection.close ()
    elif p_db=="mysql":
        # === Let's add the missing columns:
        mysql_connection,mysql_curosr=get_mysql_connection()
        try:
            mysql_curosr.execute(f'ALTER TABLE {p_table} ADD COLUMN {p_new_column} {p_type};')
            mysql_connection.commit()
            logger.info(f"PhoneBot add successfully the missing column {p_new_column} in table {p_table}.")
        except Exception as er:
            logger.error(f"{er} -> MYSQL -> PhoneBot couldn't add the missing column {p_new_column} in table {p_table}.")

        mysql_curosr.close()
        mysql_connection.close()


def AddMissingColumnstoMysql():
    """
    This method will add the missing columns in the tables actions & contacts from Mysql DB
    :param p_table:
    :param p_new_column:
    :param p_type:
    :return:
    """
    mysql_connection, mysql_curosr = get_mysql_connection()
    sqlite_connection = sqlite3.connect(mymodulesteam.LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()

    # Let's start with table 'actions'
    p_tables=['actions','contacts']
    for p_table in p_tables:
        columns = sqlite_cursor.execute(f'PRAGMA TABLE_INFO({p_table})')
        for column in columns:
            if column[0] != 'id' and column[0] != 'ID':
                p_new_column = column[1]
                p_type = column[2]
                #print(f"p_new_column : {p_new_column} - type : {type(p_new_column)}")
                #print(f"p_type : {p_type} - type : {type(p_type)}")
                if p_type == 'STRING':
                    p_type='TEXT'
            try:

                mysql_curosr.execute(f'ALTER TABLE W551je5v_phonebot_{p_table} ADD COLUMN {p_new_column} {p_type};')
                mysql_connection.commit()
                logger.info(f"PhoneBot add successfully the missing column {p_new_column} in table {p_table}.")
            except Exception as er:
                logger.error(f"{er} -> MYSQL -> PhoneBot couldn't add the missing column {p_new_column} in table {p_table}.")

    mysql_curosr.close()
    mysql_connection.close()



def CreateTable(p_sql):
    print("add TABLE ****")
    try:
        sqlite_connection = sqlite3.connect (LoadFile ('db.db'))
        sqlite_cursor = sqlite_connection.cursor ()
        sqlite_cursor.execute(p_sql)
        sqlite_connection.commit()

        sqlite_cursor.close ()
        sqlite_connection.close ()
    except Exception as ex:
        logger.error(f"Error CreateTable {ex}")




def TestIfInstalled(p_command):
    # This function will run a shell command to test if program is installed
    # Very often, it will be a 'program --version' command
    proc = subprocess.Popen(p_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, close_fds=True)
    returncode = proc.wait()
    print(f'returncode : {returncode} - {type(returncode)}')
    output = proc.stdout.read()
    output = output.decode('utf-8')

    print(f"output : {output} returncode : {returncode}")
    if returncode != 0:
        return False
    else:
        if p_command.find("java")!=-1:
            # We need to be sure it is Java8 minimum
            # position of jre folder:
            pos_jre1 = output.find('java version "')
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
                if int(first_digit) ==1 :
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
        else:
            return True


#####################################################################################
#              METHOD TO DISPLAY A POPUP MESSAGE                                    #
#####################################################################################
def PopupMessage(p_title,p_message,link=''):
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
        if link!='':
            result=ctypes.windll.user32.MessageBoxW(0, p_message, p_title, 4)
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



#####################################################################################
#               FUNCTION WHICH GIVE THE LIST OF SMARTPHONE CONNECTED                #
#####################################################################################
def GetListDevicesForThread(lst):
    lst_id_clean= [t for t in (set(i[0] for i in lst))]
    print(f"lst_id_clean  : {lst_id_clean}")
    lst_clean=[]
    cpt_Computer=0
    for element in lst:
        if element[0] in lst_id_clean:
            if element[0]=='Computer':
                cpt_Computer+=1
                if cpt_Computer==1:
                    lst_clean.append(element)
            else:
                lst_clean.append(element)
    print(f"lst_clean : {lst_clean}")
    return lst_clean
def ListSmartPhonesConnected():
    """
    in V 0.002, this function suppose to return the list of smartphones with details from the DB.
    In V 0.003, we need to provide the details after when Smartphone is ready to run in the Facebook, Twitter...etc files

    :return:
    """
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    cursor = sqlite_connection.cursor()


    list_smartphones_connected_tuple = cursor.execute(
        'SELECT udid, systemPort, deviceName, platformversion, OS_device FROM smartphones where status=1').fetchall()

    # IF COMPUTER AUTOMATION IS ENABLE, WE ADD THE COMPUTER IN LIST OF DEVICES FOR MULTI THREAD

    print(f"list_smartphones_connected_tuple : {list_smartphones_connected_tuple}")
    list_smartphones_connected_tuple=GetListDevicesForThread(list_smartphones_connected_tuple)
    print(f"list_smartphones_connected_tuple : {list_smartphones_connected_tuple}")
    list_smartphones_connected = [item[0] for item in list_smartphones_connected_tuple]

    print(f"list_smartphones_connected : {list_smartphones_connected}")
    return list_smartphones_connected


# =====================================================================================================================
# =============================== FUNCTION TO CHANGE THE type_action OF A ROW IN table actions ========================
# =====================================================================================================================

def AddActionStatus(p_new_status,p_udid,p_platform,myprofile_username,fb_group,p_msg,p_lock):
    """
    This function add a row in table action to say if group is "pending" or "not found"
    The field is type_action
    If the row already exist, we update it.
    if type_actions is empty, we return actual status(we'll do that in other function GetGroupStatus
    :param p_status:
    :param p_udid:
    :param id_contact:
    :param fullname:
    :param myprofile_username:
    :param p_lock:
    :return:
    """
    print(f"""
    p_new_status : {p_new_status}
    p_udid : {p_udid}
    p_platform : {p_platform}
    myprofile_username : {myprofile_username}
    fb_group : {fb_group}
    p_msg : {p_msg}
    p_lock : {p_lock}
    """)
    logger.info(
        f"{p_udid}|||# ================= [2] INITIALISATION OF DATABASE db.db ChangeFBGroupStatus ==============")
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))  # we prepare db
    cursor1 = sqlite_connection.cursor()
    logger.info(f"{p_udid}|||INITIALISATION OF DATABASE db.db")

    now = datetime.now()
    date_n_time = str(now.strftime("%d/%m/%Y %H:%M:%S"))


    # ===============================================================================================
    # ================== 1rst we need to check if the group is already in table actions ===================
    with p_lock:

        row_group_tuple=cursor1.execute( "SELECT type_action FROM actions WHERE platform=? AND id_social_account=? AND message=? AND type_action=? AND fb_group_name=?",
               (p_platform, myprofile_username, p_msg, p_new_status,fb_group)).fetchone()
        print(f"row_group_tuple : {row_group_tuple}")
        # === IF GROUP EXIST IN TABLE ACTIONS ============================================
        # ================================================================================
        if row_group_tuple:
            logger.info(
                f"{p_udid}|||The group '{fb_group}' was found in table actions for profile '{myprofile_username}'!")
            # === IF STATUS IS NOT EMPTY, WE CHANGE STATUS ======================================================

            if p_new_status != '':
                cursor1.execute(
                    "UPDATE actions set type_action=?, date=? , message=? WHERE platform=? AND type_action=?",
                   (p_new_status, date_n_time,
                     p_msg,p_platform, p_new_status))
                sqlite_connection.commit()
                return p_new_status

            else:
            # ================================================================================
            # === ELSE IT MEANS WE JUST WANT TO GET THE STATUS WE RETURN p_old_status ====================================================================
                return row_group_tuple[0]

        else:
            if p_new_status != '':
                cursor1.execute("INSERT INTO actions(platform,id_smartphone,id_social_account, message,type_action,date,fb_group_name) VALUES(?,?,?,?,?,?,?)",
                   (p_platform, p_udid, myprofile_username, p_msg, p_new_status,
                     date_n_time, fb_group))
                sqlite_connection.commit()
                logger.info(
                    f"{p_udid}|||We added group status '{fb_group}' in table actions for profile '{myprofile_username}'!")
                logger.info(
                    f"{p_udid}|||This group '{fb_group}' was NOT found in table actions for profile '{myprofile_username}'!")
                sqlite_connection.commit()
                return p_new_status

            else:
                return  row_group_tuple[0]


        sqlite_connection.commit()



# ================================================= GLOBAL VARIABLES =================================================
def Save_email_license_user_id_subscription_id(email, license, user_id, subscription_id,product_id):
    print(f"email, license, user_id, subscription_id,product_id : {email, license, user_id, subscription_id,product_id}")



    # ====================== NEW CODE ADDED =======================================
    # WE WILL SAVE THE DATA email, license, user_id, subscription_id in local TABLE settings
    # ===================================== CREATE SQLITE3 CONNECTION ==============================================
    logger.info(
        " ******************** WILL SAVE THE DATA user_email, license, user_id, subscription_id in local TABLE settings")

    try:
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))
        cursor = sqlite_connection.cursor()
    except Exception as ex:
        print(f"Error sqlite_connection Save_email_license_user_id_subscription_id ============================ > {ex}")

    try:
        if email is not None:


            if email !="":
                email = str(email)
                cursor.execute("UPDATE settings SET user_email=? WHERE id=?",
                               (email, 1))
                sqlite_connection.commit()

        if license is not None:


            if license != "":
                license = str(license)
                cursor.execute("UPDATE settings SET license=? WHERE id=?",
                               ( license, 1))
                sqlite_connection.commit()

        if user_id is not None:


            if user_id != "":
                user_id = int(user_id)

                cursor.execute("UPDATE settings SET  user_id=? WHERE id=?",
                               ( user_id,  1))
                sqlite_connection.commit()

        if subscription_id is not None:


            if subscription_id != "":
                subscription_id = int(subscription_id)
                print("*************************   WE FOUND subscription_id ***************************************************************")
                print(f"subscription_id : {subscription_id}")

                try:
                    cursor.execute("UPDATE settings SET  subscription_id=? WHERE id=?",
                                   (subscription_id, 1))
                    sqlite_connection.commit()
                except Exception as ex:
                    logger.critical(f"Error when updating settings table : {ex}")

        if product_id is not None:
            if product_id != "":
                product_id = int(product_id)
                if product_id != 0:
                    cursor.execute("UPDATE settings SET product_id=? WHERE id=?",
                                   (product_id, 1))
                    sqlite_connection.commit()


    except Exception as ex:
        print(f"Error Save_email_license_user_id_subscription_id ============================ > {ex}")
    # ********************************************************************************
    # ********************************************************************************


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
            PopupMessage("Error Database!",f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

            logger.info(
                f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

    return  mysql_connection, mysql_cursor



# ==================================================================================================
# ===================== METHOD TO SEND THE LOG FILE ================================================
# ==================================================================================================
def SendLogFile():
    try:
        # ---on lit le fichier config.ini
        config = configparser.ConfigParser()
        config.read(LoadFile('config.ini'))

        license_key_config = config.get('Settings', 'license_key')
        email = config.get('Settings', 'email')

        can_upload = False

        log_file = LoadFile('log.log')

        appium_log_file = LoadFile('appium.log')
        zip_appium_log_file = LoadFile('appium.zip')
        zip_log_file = LoadFile('log.zip')
        try:
            with ZipFile(LoadFile('log.zip'), 'w', zipfile.ZIP_DEFLATED) as zip:
                zip.write(log_file)


                log_file_found = True
                size_log_file = os.stat(LoadFile('log.zip')).st_size
                logger.info(f"size_log_file : {size_log_file}")

        except ValueError:
            logger.info("Error with log.log file")
            log_file_found = False
            size_log_file = 0

        try:
            with ZipFile(LoadFile('appium.zip'), 'w', zipfile.ZIP_DEFLATED) as zip:
                zip.write(appium_log_file)
                appium_log_file_found = True
                size_appium_file = os.stat(LoadFile('appium.zip')).st_size
                logger.info(f"size_appium_file : {size_appium_file}")

        except ValueError:
            logger.info("Error with appium.log file")
            appium_log_file_found = False
            size_appium_file = 0

        files = []
        if size_appium_file + size_log_file > 4000000:
            logger.info(f"The log files are too big! PhoneBot ca not attach them to the mail.")
        else:

            can_upload = True
            if os.path.isfile(LoadFile(zip_log_file)) and os.access(LoadFile(zip_log_file), os.R_OK):
                logger.info("'log.zip' File exists and is readable")
                files.append(zip_log_file)
            else:
                logger.info("Either the file 'log.log' is missing or not readable")

            if os.path.isfile(LoadFile(zip_appium_log_file)) and os.access(LoadFile(zip_appium_log_file), os.R_OK):
                logger.info("'appium.zip' File exists and is readable")
                files.append(LoadFile(zip_appium_log_file))
            else:
                logger.info("Either the file 'appium.log' is missing or not readable")

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the subject
        msg['Subject'] = f"log user : {email} + {license_key_config}"
        sender_email = formataddr((str(Header(u'Log PhoneBot', 'utf-8')), "log@phonebot.co"))
        msg['From'] = sender_email

        # string to store the body of the mail
        body = f"""This message is sent from PhoneBot program.
        You'll find attach the log file of user {license_key_config} + {email}.
        log_file_found : {log_file_found}
        appium_log_file_found = {appium_log_file_found}"""

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        cpt = 0
        if can_upload:
            for a_file in files:
                attachment = open(LoadFile(a_file), 'rb')
                file_name = os.path.basename(LoadFile(a_file))
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                part.add_header('Content-Disposition',
                                 'attachment',
                                 filename=file_name)
                encoders.encode_base64(part)
                msg.attach(part)

            # attach the instance 'p' to instance 'msg'
            # msg.attach(part)

        if log_file_found or appium_log_file_found:
            text = msg.as_string()
            port = 465  # For SSL
            smtp_server = "smtp.ionos.fr"
            login_email = "log@phonebot.co"  # Enter your address

            receiver_email = "log@phonebot.co"  # Enter receiver address
            password = "Lormont@33310"

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(login_email, password)
                    server.sendmail(sender_email, receiver_email, text)
            except Exception as ex:
                logger.info(
                    f"{ex}. PhoneBot could not send your log files to server. It is certainly a problem of internet connection. Please check that your computer is connected to Internet.")
                # sys.exit()
            # except ValueError:
            # logger.info("ERROR")
        else:
            logger.info(
                f"PhoneBot will not send the log files because log_file_found : {log_file_found} and appium_log_file_found = {appium_log_file_found}")

    except Exception as ex:
        print(f"{ex} : Error while sending the log file!")


def CheckUpdates(p_version):
    from io import BytesIO
    from zipfile import ZipFile
    import urllib.request
    try:
        # -- Online Version File
        # -- Replace the url for your file online with the one below.
        url = "http://phonebot.co/dist/version.txt"
        file = requests.get(url)
        new_version = ''
        for line in file:
            new_version = line.decode("utf-8")
            logger.info(f"Last Version of PhoneBot : {new_version}")
        file.close()


        # -- Local Version File
        # f = open('version.txt','r')
        # data = f.read()
        # f.close()
        new_version_number = str(new_version).replace('.', '')
        now_version = str(p_version).replace('.', '')
        logger.info(f"now_version:{now_version} VS {new_version_number} : new_version")
        if float(new_version_number) > float(now_version):
            PopupMessage(f"Software Update - Update N°{new_version} Available!","PhoneBot detected a new version of software. It will download it and start the installation. The installation program will appear once the download is done.")
            try:
                # ===================== WINDOWS =============================
                if platform.system() == 'Windows':
                    zip_file=f"PBWin{new_version_number}.zip"
                    exe_file=f"PhoneBot_Install_{new_version_number}.exe"
                    # filename_install_exe = 'PhoneBot_Install_Windows_' + new_version_number + '.exe'
                    # new_sql_file = 'PhoneBot_New_DB_' + new_version_number + '.sql'
                    if os.path.isfile(LoadFile(zip_file)):
                        print("zip File exist")
                        # os.remove(zip_file)
                    else:
                        print("zip File doesn't exist")
                        url = f"http://www.phonebot.co/dist/{zip_file}"
                        urllib.request.urlretrieve(url, zip_file)
                    print("We unzip zip file for Windows")
                    with ZipFile(zip_file, 'r') as zipObj:
                        # Extract all the contents of zip file in current directory
                        zipObj.extractall()
                    if os.path.isfile(LoadFile(exe_file)):
                        logger.info("We will update PhoneBot.co.")
                        os.system(exe_file)
                    else:
                        print(f"PhoneBot didn't find the file {exe_file}")

                # ===================== MAC OS X =============================
                elif platform.system() == 'Darwin':
                    zip_file=f"PBMACOSX{new_version_number}.zip"
                    exe_file=f"PhoneBot_Mac_OS_X_{new_version_number}.pkg"
                    path_to_zip_file = os.environ['HOME'] + '/' + zip_file
                    path_to_exe_file = os.environ['HOME'] + '/' + exe_file
                    if os.path.isfile(LoadFile(path_to_zip_file)):
                        print("zip File exist")
                        # os.remove(zip_file)
                    else:
                        print("zip File doesn't exist")
                        url = f"http://www.phonebot.co/dist/{zip_file}"
                        urllib.request.urlretrieve(url, path_to_zip_file)
                    print("We unzip zip file for MAC OS")
                    try:
                        with ZipFile(path_to_zip_file, 'r') as zipObj:
                            # Extract all the contents of zip file in current directory
                            print("Unzipping....")
                            zipObj.extractall(path=os.environ['HOME'])
                    except Exception as ex:
                        print(f"Error Unziping ZIP file {ex}")
                    if os.path.isfile(LoadFile(path_to_exe_file)):
                        logger.info("We will update PhoneBot.co.")

                        shell_script_update_PhoneBot = LoadFile('PhoneBot_Update.sh')
                        print(f"shell_script_update_PhoneBot:{shell_script_update_PhoneBot}")
                        command_update_phonebot = f"""/usr/bin/osascript -e 'do shell script "/bin/bash {shell_script_update_PhoneBot} >> {os.environ['HOME']}/PhoneBot/log.log" with prompt "PhoneBot will update to the new version." with administrator privileges'"""
                        proc = subprocess.Popen(command_update_phonebot, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE, shell=True)
                        (output, err) = proc.communicate()
                        logger.info(output.decode("utf8"))
                        logger.info(err.decode("utf8"))
                        returncode_command_update_phonebot = proc.wait()
                        logger.info(f"returncode_command_update_phonebot : {returncode_command_update_phonebot}")

                else:
                        print(f"PhoneBot didn't find the file exe_file.")


                # subprocess.call(filename_install_exe)
                logger.info(f"PhoneBot is executing exe_file")
                # time.sleep(20)
                try:
                    KillPhoneBot_During_Update()

                except Exception as ex:
                    logger.error(f"{ex} - {exe_file} PhoneBot could not kill itself. It will try another way.")
                    sys.exit()

            except Exception as ex:
                PopupMessage(f"Update Error!",f"{ex} - PhoneBot could not download the new version : {zip_file}. Please contact support@phonebot.co")

                logger.critical(
                    f"{ex} - PhoneBot could not download the new version : {zip_file}. Please contact support@phonebot.co")

        else:
            logger.info("'Software Update - ', 'No Updates are Available.'")
    except Exception as e:
        logger.info('Unable to Check for Update, Error:' + str(e))


def FindTableSource(p_db, p_table_name):
    sqlite_connection = sqlite3.connect(p_db)
    sqlite_cursor = sqlite_connection.cursor()
    detail_table = sqlite_cursor.execute(f"PRAGMA table_info({p_table_name});").fetchall()
    for line in detail_table:
        if line[1] == 'source':
            logger.info(f"We found column source in table {p_table_name}")
            return True

    return False




def UpdateDB():
    original_db = 'db.db'
    backup_db = 'db_BAK.db'

    while True:
        try:
            if os.path.isfile(LoadFile('db.db')):
                logger.info(f"PhoneBot found your local database 'db.db' in forlder '{LoadFile(os.path.realpath('.'))}'")
                logger.info("It will make a copy 'db_BAK.db' before to update new version.")
                shutil.copyfile(LoadFile(original_db), LoadFile(backup_db))
                logger.info("PhoneBot made a backup of your local database 'db.db'.")

                if FindTableSource(LoadFile('db.db'), 'actions'):
                    AddColumn(LoadFile('db.db'), 'actions', 'source')
                if FindTableSource(LoadFile('db.db'), 'linkedin_profiles'):
                    AddColumn(LoadFile('db.db'), 'linkedin_profiles', 'source')
                if FindTableSource(LoadFile('db.db'), 'contacts'):
                    AddColumn(LoadFile('db.db'), 'contacts', 'source')
                # We need to check if the column 'source' in the tables actions, contacts, and linkedin_profiles

                break
            else:
                if platform.system() == 'Windows':
                    if os.path.isfile('C:\\Program Files(x86)\\PhoneBot-co\\db.db'):
                        C_program = 'C:\\Program Files(x86)\\PhoneBot-co\\'
                        original_db = C_program + 'db.db'
                        backup_db = C_program + 'db_BAK.db'
                        logger.info(
                            "PhoneBot found your local database 'db.db' in forlder 'C:\\Program Files(x86)\\PhoneBot-co\\'. It will make a copy 'db_BAK.db' before to update new version.")
                        shutil.copyfile(original_db, backup_db)
                        logger.info("PhoneBot made a backup of your local database 'db.db'.")
                        if FindTableSource(original_db, 'actions'):
                            AddColumn(original_db, 'actions', 'source')
                        if FindTableSource(original_db, 'linkedin_profiles'):
                            AddColumn(original_db, 'linkedin_profiles', 'source')
                        if FindTableSource(original_db, 'contacts'):
                            AddColumn(original_db, 'contacts', 'source')
                        break

                    elif os.path.isfile('C:\\C:\Program Files\\PhoneBot-co\\db.db'):
                        C_program = 'C:\\Program Files\\PhoneBot-co\\'
                        backup_db = C_program + 'db_BAK.db'
                        logger.info(
                            "PhoneBot found your local database 'db.db' in forlder 'C:\\Program Files(x86)\\PhoneBot-co\\'. It will make a copy 'db_BAK.db' before to update new version.")
                        shutil.copyfile(original_db, backup_db)
                        logger.info("PhoneBot made a backup of your local database 'db.db'.")
                        if FindTableSource(original_db, 'actions'):
                            AddColumn(original_db, 'actions', 'source')
                        if FindTableSource(original_db, 'linkedin_profiles'):
                            AddColumn(original_db, 'linkedin_profiles', 'source')
                        if FindTableSource(original_db, 'contacts'):
                            AddColumn(original_db, 'contacts', 'source')
                        break

                    else:
                        logger.info(
                            "PhoneBot could not find your local database 'db.db'. It will search for it in all your system. this can take a few minutes. Please be patient...")
                        original_db = distutils.spawn.find_executable('db.db')
                        if original_db:
                            C_program = str(original_db).replace('db.db', '')
                            logger.info(f"C_program : {C_program}")
                            backup_db = C_program + 'db_BAK.db'
                            logger.info(
                                "PhoneBot found your local database 'db.db' in forlder 'C:\\Program Files(x86)\\PhoneBot-co\\'. It will make a copy 'db_BAK.db' before to update new version.")
                            shutil.copyfile(original_db, backup_db)
                            logger.info("PhoneBot made a backup of your local database 'db.db'.")
                            if FindTableSource(original_db, 'actions'):
                                AddColumn(original_db, 'actions', 'source')
                            if FindTableSource(original_db, 'linkedin_profiles'):
                                AddColumn(original_db, 'linkedin_profiles', 'source')
                            if FindTableSource(original_db, 'contacts'):
                                AddColumn(original_db, 'contacts', 'source')
                            break
                        else:
                            logger.info(
                                "Unfortunately, PhoneBot could not find your local database. It will will not be able to update itself.")
                            break
                elif platform.system() == 'Darwin':
                    logger.info(
                        "Unfortunately, PhoneBot could not find your local database. It will will not be able to update itself.")
                    break


        except Exception as er:

            logger.info(
                f"{er} -> Unfortunately, PhoneBot could not find your local database. It will will not be able to update itself.")
            break




# ========================================================================================
# ========================================================================================
# ========================================================================================

def MakeConfiginifile(p_mode="default"):
    """
    This function will create config.ini and accept one argument : p_mode:
        - default: it will create config.ini if it doesn't exist
        - reset: it will create config.ini in any case

    """

    logger.info(
        f"========================================= Start MakeConfiginifile {p_mode} ================================================= ")
    content_file = """# -*- coding: utf-8 -*-
# Please add your email(the one you used to register in PhoneBot.co).
# And add your license key. You can find your license key on PhoneBot website:https://phonebot.co/my-account/view-license-keys/
# You do not need to add quotes "". Just type your email and your license key in front of 'email=' and 'license_key=' without anything else.
# Then save this file.
[Settings]
email=
license_key=

"""
    file_exist = os.path.isfile(LoadFile('config.ini'))
    if p_mode=="default" : #default case
        if not file_exist:
            with open(LoadFile('config.ini'), 'w', encoding='utf-8') as f:
                f.write(content_file)
            f.close()
    else: #reset case
        if not file_exist:
            with open(LoadFile('config.ini'), 'w', encoding='utf-8') as f:
                f.write(content_file)
            f.close()











def UpdateMysqlDB(p_user_id):
    """
    This function will update the Mysql tables actions and contacts in order to upload
    to our main database the user's data. By this way, he'll be able to get his scrapped data
    and report
    """
    logger.info(f"========================= UpdateMysqlDB {p_user_id}======================================")

    AddNewRowsInMysql(p_user_id,'contacts')
    AddNewRowsInMysql(p_user_id, 'actions')
    UpdateRowsInMysql(p_user_id,'contacts')
    UpdateRowsInMysql(p_user_id,'actions')



def CheckBrowserProfile(p_browser_name):
    logger.info(f"======================= CheckBrowserProfile {p_browser_name} ==============================")

    if platform.system() == 'Windows':
        if str(p_browser_name).lower() == "chrome":
            # Here comes the code to check if cookie exist for chrome in Windows
            chrome_profile_path= r"%LocalAppData%\Google\Chrome\User Data"
            chrome_profile_path = os.path.expandvars(chrome_profile_path)
            if os.path.isdir(chrome_profile_path):
                logger.info(f"Folder {chrome_profile_path} exists!")
                return True

            else:
                logger.info (f"Folder {chrome_profile_path} DOES NOT exist!")
                return False
        elif str(p_browser_name).lower() == "firefox":
            firefox_profile_path = os.environ['APPDATA'] + "\Mozilla\Firefox\Profiles"
            if os.path.isdir(firefox_profile_path):
                logger.info (f"Folder {firefox_profile_path} exists!")
                return True
            else:
                logger.info (f"Folder {firefox_profile_path} DOES NOT exist!")
                return False


    elif platform.system() == 'Darwin':
        HOME_DIR = os.environ['HOME']
        # Here comes the code to check if cookie exist for chrome in MAC OS
        # https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/
        # https://www.howtogeek.com/255587/how-to-find-your-firefox-profile-folder-on-windows-mac-and-linux/
        if str(p_browser_name).lower() == "chrome":
            # Here comes the code to check if cookie exist for chrome in Windows

            chrome_profile_path = HOME_DIR + r"/Library/Application Support/Google/Chrome/Default"
            chrome_profile_path = os.path.expandvars(chrome_profile_path)
            if os.path.isdir(chrome_profile_path):
                logger.info(f"Folder {chrome_profile_path} exists!")
                return True

            else:
                logger.info(f"Folder {chrome_profile_path} DOES NOT exist!")
                return False
        elif str(p_browser_name).lower() == "firefox":
            firefox_profile_path = HOME_DIR + "/Library/Application Support/Firefox/Profiles"
            if os.path.isdir(firefox_profile_path):
                logger.info(f"Folder {firefox_profile_path} exists!")
                return True
            else:
                logger.info(f"Folder {firefox_profile_path} DOES NOT exist!")
                return False
    else:
        HOME_DIR = os.environ['HOME']
        # Here comes the code to check if cookie exist for chrome in MAC OS
        # https://www.howtogeek.com/255653/how-to-find-your-chrome-profile-folder-on-windows-mac-and-linux/
        # https://www.howtogeek.com/255587/how-to-find-your-firefox-profile-folder-on-windows-mac-and-linux/
        if str(p_browser_name).lower() == "chrome":
            # Here comes the code to check if cookie exist for chrome in Windows

            chrome_profile_path = "/bin/chrome"
            chrome_profile_path = os.path.expandvars(chrome_profile_path)
            if os.path.isdir(chrome_profile_path):
                logger.info(f"Folder {chrome_profile_path} exists!")
                return True

            else:
                logger.info(f"Folder {chrome_profile_path} DOES NOT exist!")
                return False
        elif str(p_browser_name).lower() == "firefox":
            firefox_profile_path = "/bin/firefox"
            if os.path.isdir(firefox_profile_path):
                logger.info(f"Folder {firefox_profile_path} exists!")
                return True
            else:
                logger.info(f"Folder {firefox_profile_path} DOES NOT exist!")
                return False

def ChromeCookie(p_website):
    """
    This function will return the list of Chrome Cookies for Desktop automation
    #https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies

    """


    path = r'%LocalAppData%\Google\Chrome\User Data\Local State'
    path = os.path.expandvars(path)
    with open(path, 'r') as file:
        encrypted_key = json.loads(file.read())['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key)                                       # Base64 decoding
    encrypted_key = encrypted_key[5:]                                                     # Remove DPAPI
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]  # Decrypt key

    from os.path import expanduser
    path_home_user = expanduser("~")
    cookie_path = path_home_user + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"
    sqlite_connection = sqlite3.connect(cookie_path)
    sqlite_cursor = sqlite_connection.cursor()

    #values=sqlite_cursor.execute("SELECT name, encrypted_value, host_key FROM cookies WHERE host_key=?",(".indeed.com",)).fetchall()
    #values=sqlite_cursor.execute("SELECT name, encrypted_value, host_key FROM cookies").fetchall()
    values=sqlite_cursor.execute("SELECT name, encrypted_value, host_key FROM cookies WHERE host_key LIKE ?",(f"%{p_website}%",)).fetchall()

    list_cookie=[]
    for value in values:




        """ 
        data = bytes.fromhex('76 31 30 7b 6e eb 7e 7c 1c 91 20 07 ac c6 0c 56 \
        23 a4 1c 5b b7 c5 9a 8b 58 45 cb a4 6d db f1 0d \
        81 a9 da 8d dd 55 07 b2 d0') # the encrypted cookie 
        """


        data=value[1]
        nonce = data[3:3+12]
        ciphertext = data[3+12:-16]
        tag = data[-16:]
        cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode() # the decrypted cookie
        #p_cookie[value[0]]= plaintext.strip().decode()
        tuple_cookie =(value[0],plaintext,value[2])
        list_cookie.append(tuple_cookie)


    return list_cookie






def get_daily_limit_actions(p_taskuser_id):
    """
    New version V0.003 for getting the daily limits from task_user id
    """
    # ======================================================================================
    # =============================== DATABASES ==========================================


    mysql_connection, mysql_cursor = get_mysql_connection()

    sql_get_daily_limit_task_user = f"SELECT daily_limit FROM W551je5v_pb_tasks_users WHERE id={p_taskuser_id}"
    mysql_cursor.execute(sql_get_daily_limit_task_user)
    daily_limit_task_user=mysql_cursor.fetchone()
    print(f"daily_limit_task_user : {daily_limit_task_user}")

    try:
        mysql_cursor.close()
        mysql_connection.close()
    except Exception as ex:
        logger.error(f"Error closing mysql : {ex}")


    return daily_limit_task_user['daily_limit']



    pass




def return_text_color_software(p_software):
    """
    This function will return the correct colors for necessary softwares labels
    """

    if p_software:
        p_value = "Installed"
        p_color = "Green"
    else:
        p_value = "Not Installed"
        p_color = "Red"
    return p_value,p_software



def AddNewRowsInMysql(p_user_id,p_table):
    logger.info(f"# ================== ADD NEW ROWS IN TABLE '{p_table}' =================")
    # ====================================================================================
    # =============================== DATABASES ==========================================
    # 1 === Intialisation Database =======================================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    # Get name of columns from SQLITE DB (see https://itheo.tech/get-column-names-from-slqite-python)
    sqlite_connection.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_connection.cursor()
    mysql_connection, mysql_cursor = get_mysql_connection()

    # 2 ===  WE NEED THE LAST ID_ROW FROM MYSQL IN ORDER TO ADD ONLY THE LAST ROWS FROM SQLITE3 DB
    sql_get_last_row_p_table=f"SELECT id_row FROM W551je5v_phonebot_{p_table} WHERE id_client={p_user_id} ORDER BY id_row DESC LIMIT 1;"
    mysql_cursor.execute(sql_get_last_row_p_table)
    last_id_row_dico_contact=mysql_cursor.fetchall()
    print(f"last_id_row_dico_contact : {last_id_row_dico_contact}")

       #print(last_id_row_dico_contact)
    #print(last_id_row_dico_contact['id_row'])
    last_id_row=last_id_row_dico_contact[0]['id_row']

    # 3 ===  WE need to get all the columns names of table "{p_table}" because Stagiaires may have been added new columns we ignore
    columns = sqlite_cursor.execute(f'PRAGMA TABLE_INFO({p_table})')
    column_names=""
    for column in columns:
        p_new_column = column[1]
        column_names+=p_new_column + ','
        #print(f"p_new_column : {p_new_column} - type : {type(p_new_column)}")

    print(f"column_names : {column_names}")
    print(f"column_names[len(column_names)-1:] : {column_names[len(column_names) - 1:]}")
    # 5 ===  WE Can now get build the string names of columns =================
    if column_names[len(column_names) - 1:] == ',':
        print("There is a comma in column_names")
        column_names = column_names[:len(column_names) - 1]
        print(f"column_names : {column_names}")
    else:
        print("no comma in column_names")
    list_column_names = column_names.split(',')
    qty_columns= len(list_column_names)

    str_values = (qty_columns+1)*"%s,"

    # 7 ===  We build the SQL query to get values from SQLITE DB ========================
    sql_get_all_new_rows_p_table="SELECT " + column_names + f" FROM {p_table} WHERE id >{last_id_row}"

    sqlite_cursor.execute(sql_get_all_new_rows_p_table)
    data_p_table = sqlite_cursor.fetchall()
    qty_rows_data_p_table = len(data_p_table)
    # 8 ===  WE CAN LOOP THE data_p_table FROM SQLITE AND INSERT THE ROWS
    if data_p_table:
        bar = Bar('Processing', max=qty_rows_data_p_table)

        for data_table in data_p_table:
            data_table = dict(data_table)
            sql_test_if_exist_table = f"SELECT * FROM W551je5v_phonebot_{p_table} WHERE id_client=" + str(p_user_id) + " AND id_row=" + str(data_table['id'])
            #print(f"sql_test_if_exist_table : {sql_test_if_exist_table}")
            mysql_cursor.execute(sql_test_if_exist_table)

            if not mysql_cursor.fetchone():
                print(f"data_table : {data_table}")
                logger.info(f"id_row : {data_table['id']} - client :{p_user_id}")

                # We need to check if there aren't NULL values as we can't INSERT Null values
                args_insert_row_table = (p_user_id,)
                columns_to_insert = ""
                str_values = "%s,"
                for key in data_table:
                    print(f"{key} -> {data_table[key]}")

                    columns_to_insert+=key + ","
                    args_insert_row_table += (data_table[key],)
                    str_values+="%s,"


                # We need to remove the last comma of columns_to_insert
                if columns_to_insert[len(columns_to_insert) - 1:] == ',':
                    print("There is a comma in columns_to_insert")
                    columns_to_insert = columns_to_insert[:len(columns_to_insert) - 1]
                    print(f"columns_to_insert : {columns_to_insert}")
                else:
                    print("no comma in columns_to_insert")
                list_columns_to_insert = columns_to_insert.split(',')
                qty_columns = len(list_columns_to_insert)

                # We need to remove the last comma of str_values
                if str_values[len(str_values) - 1:] == ',':
                    print("There is a comma in str_values")
                    str_values = str_values[:len(str_values) - 1]
                    print(f"str_values : {str_values}")
                else:
                    print("no comma in str_values")
                list_str_values = str_values.split(',')
                qty_columns = len(list_str_values)
                columns_to_insert=columns_to_insert.replace('id,','id_row,')
                print(f"columns_to_insert AFTER replace id by id_row : {columns_to_insert}")
                sql_insert_row_p_table = f"INSERT INTO W551je5v_phonebot_{p_table} (id_client," + columns_to_insert + \
                                ") VALUES("+ str_values + ")"

                print(f"sql_insert_row_p_table : {sql_insert_row_p_table}")
                #args_insert_row_table +=(data_table)
                print(f"args_insert_row_table : {args_insert_row_table}")
                mysql_cursor.execute(sql_insert_row_p_table,args_insert_row_table)
                mysql_connection.commit()
            else:
                #print("This row 'contact' already exist!")
                pass

            bar.next()
        bar.finish()
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


def UpdateRowsInMysql(p_user_id,p_table):
    logger.info(f"# ================== UPDATE ROWS IN TABLE '{p_table}' ==================")
    # ======================================================================================
    # =============================== DATABASES ==========================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    sqlite_connection.row_factory = sqlite3.Row
    mysql_connection, mysql_cursor = get_mysql_connection()
    # ========================== UPDATE THE contacts ROWS WHICH date_update SQLITE3> date_update MYSQL ================

    # WE NEED TO GET ALL ROWS FROM user_id FROM MYSQL =================================================================
    sql_get_row_MYSQL=f"SELECT id_row,date_update FROM W551je5v_phonebot_{p_table} WHERE id_client={p_user_id} ;"
    mysql_cursor.execute(sql_get_row_MYSQL)
    rows_MYSQL=mysql_cursor.fetchall()
    qty_rows_MYSQL=len(rows_MYSQL)
    logger.info(f"PhoneBot will check {qty_rows_MYSQL} rows in MYSQL table {p_table}...")
    bar = Bar('Processing', max=len(rows_MYSQL))

    # We need to make the list of column names of sqlite table
    columns = sqlite_cursor.execute(f'PRAGMA TABLE_INFO({p_table})')
    column_names_sqlite = ""
    for column in columns:
        p_new_column = column[1]
        column_names_sqlite += p_new_column + ','
        #print(f"p_new_column : {p_new_column} - type : {type(p_new_column)}")
    #print(f"column_names_sqlite : {column_names_sqlite}")

    # Let's built immediately the string for the Mysql UPDATE query
    # Let's prepare the values string
    str_values = column_names_sqlite.replace(',','=%s,')
    # We need to remove the last comma of str_values
    if str_values[len(str_values) - 1:] == ',':
        print("There is a comma in str_values")
        str_values = str_values[:len(str_values) - 1]
        #print(f"str_values : {str_values}")
    else:
        print("no comma in str_values")

    # We can finaly remove the comma ',' from column_names_sqlite
    if column_names_sqlite[len(column_names_sqlite) - 1:] == ',':
        print("There is a comma in column_names_sqlite")
        column_names_sqlite = column_names_sqlite[:len(column_names_sqlite) - 1]
        #print(f"column_names_sqlite : {column_names_sqlite}")
    else:
        print("no comma in column_names_sqlite")

    str_values = str_values.replace('id=%s,', 'id_row=%s,')
    #print(f"column_names_sqlite : {column_names_sqlite}")
    #print(f"str_values : {str_values}")
    list_str_values = str_values.split(',')
    #print(f"list_str_values : {list_str_values}")
    qty_str_values = len(list_str_values)
    #print(f"qty_str_values : {qty_str_values}")

    #print(f"rows_MYSQL : {rows_MYSQL}")

    for row_MYSQL in rows_MYSQL:
        id_row=row_MYSQL['id_row']
        date_update=row_MYSQL['date_update']
        # We need to see if there is a row more recent in our SQLITE db.db ============
        SQLITE_updated=sqlite_cursor.execute(f"SELECT {column_names_sqlite} FROM {p_table} WHERE id=?  \
        AND date(date_update)>?",(id_row,date_update)).fetchone()
        #print(f"SQLITE_updated N°{id_row} for mysql date_update {date_update} : {SQLITE_updated}")
        if SQLITE_updated:
            logger.info(f"Let's UPDATE the row N° {id_row} - client :{p_user_id}")
            # We need now to prepare the tuple of arguments values for the final Mysql UPDATE
            args_mysql=()
            for i in range(0,qty_str_values):
                #print(f"SQLITE_updated[{i}] : {SQLITE_updated[i]}")
                args_mysql+=(SQLITE_updated[i],)

            # Then we add the values for the WHERE id_client AND id_row
            args_mysql+=(p_user_id,id_row)
            #print(f"Qty of arguments for SQL update : {len(args_mysql)}")
            #print(f"args_mysql : {args_mysql}")
            sql_update_mysql_contact=f"UPDATE W551je5v_phonebot_{p_table} set  \
                {str_values} WHERE id_client=%s AND id_row=%s"
            #  UPDATE
            mysql_cursor.execute(sql_update_mysql_contact,args_mysql)
            mysql_connection.commit()

        bar.next()

    bar.finish()
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

def IsAffiliate(p_email,p_license_key_config):
    """
    This function will check if user is affiliate or not and return the campaign id
    If it is not an affiliate, it will return "None" and this result will be tested in the file PhoneBot.py

    """

    # The first thing is to check if user type 'affiliate' as license key
    if str(p_license_key_config).lower() != "affiliate":
        return None
    else:
        # Databases
        mysql_connection, mysql_cursor = get_mysql_connection()
        sqlite_connection = sqlite3.connect(LoadFile('db.db'))
        sqlite_cursor = sqlite_connection.cursor()

        sql_get_affiliate_details = f"SELECT license_id, enable,tracking_code_affiliate,   \
            coupon_affiliate, url_affiliate FROM W551je5v_pb_affiliates WHERE email ='{p_email}'"
        mysql_cursor.execute(sql_get_affiliate_details)
        affiliate_details = mysql_cursor.fetchone()
        if not affiliate_details:
            logger.info(f"It is not affiliate because sql query return {affiliate_details}")
            return None
        else:
            # Ok we found an affiliate with the email but is he/she enable by user?
            if affiliate_details['enable'] == 0:

                # Affiliate is not enable
                return None
            else:
                # Affiliate is enable, so we can get the campaign id
                license_id = affiliate_details['license_id']
                #master_user_id is our client who has an affiliate network
                sql_get_master_user_id=f"SELECT user_id FROM W551je5v_lmfwc_licenses WHERE id={license_id}"
                mysql_cursor.execute(sql_get_master_user_id)
                master_user_id_tuple = mysql_cursor.fetchone()
                print(f"master_user_id : {master_user_id_tuple}")

                sql_get_campaign_id = f"SELECT id FROM W551je5v_pb_campaigns WHERE id_user={master_user_id_tuple['user_id']} AND affiliates=1"
                mysql_cursor.execute(sql_get_campaign_id)
                campaign_id_tuple = mysql_cursor.fetchone()
                if not campaign_id_tuple:
                    logger.error(f"PhoneBot couldn't find any campaign for affiliates for user id {master_user_id_tuple['user_id']}")
                else:

                    # Then we save the parameters of affilaite in SALITE table 'settings'
                    sqlite_cursor.execute("UPDATE settings set tracking_code_affiliate=?,   \
                    coupon_affiliate=?, url_affiliate=?  WHERE id=?",(affiliate_details['tracking_code_affiliate'], affiliate_details['coupon_affiliate'],affiliate_details['url_affiliate'],1))
                    sqlite_connection.commit()
                    logger.info(f"campaign_id_tuple : {campaign_id_tuple}")
                    return campaign_id_tuple['id']


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


def GetIDTask(p_taskuser_id):
    print (f"======================== GetIDTask {p_taskuser_id} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection ()
        SQL_GET_ID_TASK = f"SELECT id_task FROM W551je5v_pb_tasks_users WHERE id={p_taskuser_id}"
        mysql_cursor.execute (SQL_GET_ID_TASK)
        id_task_dic = mysql_cursor.fetchone ()
        id_task = int (id_task_dic['id_task'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return id_task
    except Exception as ex:
        logger.error (f"ERROR GetIDTask : {ex}")

def GetIDTaskUser(p_campaign_id,p_task_id):
    print (f"======================== GetIDTaskUser {p_campaign_id} {p_task_id} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection ()
        SQL_GET_ID_TASKUSER = f"SELECT id FROM W551je5v_pb_tasks_users WHERE id_task={p_task_id} and id_campaign={p_campaign_id}"
        mysql_cursor.execute (SQL_GET_ID_TASKUSER)
        id_taskuser_dic = mysql_cursor.fetchone ()
        id_taskuser = int (id_taskuser_dic['id'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return id_taskuser
    except Exception as ex:
        logger.error (f"ERROR GetIDTask : {ex}")


def GetDetailsTask(p_id_task_user):
    print (f"======================== GetDetailsTask from TaskUser_id {p_id_task_user} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection ()
        SQL_GET_DETAILS_TASK = f"SELECT W551je5v_pb_tasks.name,W551je5v_pb_tasks_users.daily_limit,W551je5v_pb_tasks.hourly_limit,W551je5v_pb_tasks.id_type_task,W551je5v_pb_tasks.id_platform FROM W551je5v_pb_tasks INNER JOIN W551je5v_pb_tasks_users ON W551je5v_pb_tasks.id=W551je5v_pb_tasks_users.id_task WHERE W551je5v_pb_tasks_users.id={p_id_task_user}"
        print(f"SQL_GET_DETAILS_TASK : {SQL_GET_DETAILS_TASK}")
        mysql_cursor.execute (SQL_GET_DETAILS_TASK)
        dico = mysql_cursor.fetchone()
        print(f"dico : {dico}")

        # Sometimes, the limits vlaues are empty and it bugs
        if not dico['hourly_limit']:
            dico['hourly_limit']=10
        else:
            hourly_limit = int (dico['hourly_limit'])

        if not dico['daily_limit']:
            dico['daily_limit']=10
        else:
                daily_limit = int (dico['daily_limit'])

        id_type_task = int (dico['id_type_task'])
        id_platform = int (dico['id_platform'])
        name_task = str (dico['name'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")

        return name_task, daily_limit, hourly_limit, id_type_task, id_platform

    except Exception as ex:
        logger.error (f"ERROR GetDetailsTask : {ex}")


def GetDetailsTypeTask(p_id_type_task):
    """
    This function return the name of the social platform by id_taskuser
    :param p_id_type_task:
    :return:
    """
    print (f"======================== GetDetailsTypeTask {p_id_type_task} ===========================")
    try:
        mysql_connection, mysql_cursor = get_mysql_connection ()

        SQL_GET_TYPE_TASK = f"SELECT name FROM W551je5v_pb_type_tasks WHERE id={p_id_type_task}"
        mysql_cursor.execute (SQL_GET_TYPE_TASK)
        name_type_task_dic = mysql_cursor.fetchone ()
        name_type_task = str (name_type_task_dic['name'])
        try:
            mysql_cursor.close()
            mysql_connection.close()
        except Exception as ex:
            logger.error(f"Error closing mysql : {ex}")
        return name_type_task
    except Exception as ex:
        logger.error (f"ERROR GetDetailsTypeTask : {ex}")


def GetPlatformName(p_id_platform):
    """
    This function return the name of the social platform by id_taskuser
    :param p_id_platform:
    :return:
    """
    print (f"======================== GetPlatformName {p_id_platform} ===========================")

    mysql_connection, mysql_cursor = get_mysql_connection ()
    # Get the name of platform
    SQL_GET_PLATFORM_NAME = f"SELECT name FROM W551je5v_pb_platforms WHERE id={p_id_platform}"
    mysql_cursor.execute (SQL_GET_PLATFORM_NAME)
    platform_name_dic = mysql_cursor.fetchone ()
    platform_name = str (platform_name_dic['name'])
    try:
        mysql_cursor.close()
        mysql_connection.close()
    except Exception as ex:
        logger.error(f"Error closing mysql : {ex}")
    return platform_name


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
    logger.info (
        f"# ======== GetQuantityActions ========= GET THE LIMITS {p_taskuser_id} - {p_username} ==========================")
    # ===================== DATABASES ===========================
    sqlite_connection = sqlite3.connect (LoadFile ('db.db'))
    sqlite_cursor = sqlite_connection.cursor ()
    mysql_connection, mysql_cursor = get_mysql_connection ()

    # ==================== GET id_task ==========================
    id_task = GetIDTask (p_taskuser_id)
    # Get details of task
    name_task, daily_limit, hourly_limit, id_type_task, id_platform = GetDetailsTask (p_taskuser_id)
    # Get the name of platform
    platform_name_tmp = GetPlatformName (id_platform)
    platform_name = str (platform_name_tmp).lower ()
    print (f"""
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
    # behavior for id_type_task 13 wasn't defined - Please verify the value of string_to_search in this case
    elif id_type_task == 13:
        string_to_search = "comment"

    # ====================== CALCULATE ACTIONS DONE ALREADY ==========================
    now = datetime.now ()
    yesterday = now - timedelta (days=1)
    one_hour_ago = now - timedelta (hours=1)
    print (f"""
    now = {now}
    yesterday = {yesterday}
    one_hour_ago = {one_hour_ago}
    """)

    actions_done_last_1H_tuple = sqlite_cursor.execute ("SELECT COUNT(*) FROM actions WHERE platform LIKE ? AND  \
        id_social_account LIKE ? AND type_action LIKE ? AND date_created >?", \
                                                       (
                                                       f"%{platform_name}%", f"%{p_username}%", f"%{string_to_search}%",
                                                       one_hour_ago)).fetchall ()
    actions_done_last_24H_tuple = sqlite_cursor.execute ("SELECT COUNT(*) FROM actions WHERE platform LIKE ? AND  \
        id_social_account LIKE ? AND type_action LIKE ? AND date_created >?", \
                                                        (f"%{platform_name}%", f"%{p_username}%",
                                                         f"%{string_to_search}%", yesterday)).fetchall ()
    actions_done_last_1H = actions_done_last_1H_tuple[0][0]
    actions_done_last_24H = actions_done_last_24H_tuple[0][0]
    print (f"""
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
            logger.info (f"User {p_username} can make {quantity_actions_possible_this_hour} actions now")
            if quantity_actions_possible_this_hour > 10:
                quantity_actions_possible_this_hour = 10

            try:
                mysql_cursor.close()
                mysql_connection.close()
            except Exception as ex:
                logger.error(f"Error closing mysql : {ex}")

            return quantity_actions_possible_this_hour / 2
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




# ========================================================================================


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
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'misc/credentials_Google_Sheet_API_Account.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = p_sheet_id
    # https://developers.google.com/sheets/api/quickstart/python
    service = build('sheets', 'v4', credentials=creds,cache_discovery=False)
    # Call the Sheets API
    sheet = service.spreadsheets()
    try:
        """
        https://stackoverflow.com/a/51852293/10551444
        This sample retrieves the sheet name, the number of last row and last column of data range using sheet index. When 0 is used for the sheet index, it means the first sheet.
        """
        res = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
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
        if str(ex).find("HttpError 403")!=-1:
            PopupMessage("Error Google Sheet!",f"Please share for everyone the Google sheet : {ex}",f"https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}")
            return None


def GoogleSheetAddValues(p_sheet_id,p_list_values):
    """
    This function go to Google sheet and Add t a row of values.
    :param p_sheet_id:
    :return:
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = '../credentials_Google_Sheet_API_Account.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = p_sheet_id
    # https://developers.google.com/sheets/api/quickstart/python
    service = build('sheets', 'v4', credentials=creds,cache_discovery=False)
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
        request = service.spreadsheets().values().append(spreadsheetId=p_sheet_id, range=range_, valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body=value_range_body)
        response = request.execute()
        # TODO: Change code below to process the `response` dict:
        print(response)
        return True
    except Exception as ex:
        print(f"ERROR : {ex}")
        if str(ex).find("HttpError 403")!=-1:
            PopupMessage("Error Google Sheet!",f"Please share for everyone the Google sheet : {ex}",f"https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}")
            return False




def GoogleSheetClearValues(p_sheet_id):
    """
    This function go to Google sheet and clear all the values.
    :param p_sheet_id:
    :return:
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'misc/credentials_Google_Sheet_API_Account.json'
    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = p_sheet_id
    # https://developers.google.com/sheets/api/quickstart/python
    service = build('sheets', 'v4', credentials=creds,cache_discovery=False)
    # Call the Sheets API
    sheet = service.spreadsheets()
    try:
        """
        https://stackoverflow.com/a/51852293/10551444
        This sample retrieves the sheet name, the number of last row and last column of data range using sheet index. When 0 is used for the sheet index, it means the first sheet.
        """
        res = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
        sheetIndex = 0
        sheetName = res['sheets'][sheetIndex]['properties']['title']
        lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
        lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])
        # ==================================================
    except Exception as ex:
        logger.error(f"ERROR with  GoogleSheetClearValues calculationg lastcolumn and lastrow: {ex}")
    try:
        # The A1 notation of the values to clear.
        range_ = f"{sheetName}!a1:{lastColumn}{lastRow}"  # TODO: Update placeholder value.

    except Exception as ex:
        logger.error(f"ERROR with  GoogleSheetClearValues creating the range: {ex}")
    try:
        request = service.spreadsheets().values().clear(spreadsheetId=p_sheet_id, range=range_)
        response = request.execute()
        return True

    except Exception as ex:
        logger.error(f"ERROR with  GoogleSheetClearValues executing the request: {ex}")
        if str(ex).find("HttpError 403")!=-1:
            PopupMessage("Error Google Sheet!",f"Please share for everyone the Google sheet with 'Edit' access in order to clear the values : {ex}",f"https://docs.google.com/spreadsheets/d/{SAMPLE_SPREADSHEET_ID}")
            return False


# ===================================================================
#import CookiesBrowserCredentials
def GetListUsernamePassword(p_browser,p_platform):
    """
    This function will get all the rows from social_accounts table where status =1
    and p_browser and p_platform
    :param p_browser:
    :param p_platform:
    :return:
    """
    logger.info("# ================== ADD NEW ROWS IN TABLE 'contacts' =================")
    # ======================================================================================
    # =============================== DATABASES ==========================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()

    usernames_passwords_crypted_tuple=sqlite_cursor.execute("SELECT username,password FROM social_accounts WHERE browser=? AND platform=?",(p_browser,p_platform)).fetchall()
    list_username_password=[]
    for username_password_crypted_tuple in usernames_passwords_crypted_tuple:
        username=username_password_crypted_tuple[0]
        password = CookiesBrowserCredentials.UncryptPassword(username_password_crypted_tuple[1])
        list_username_password.append((username,str(password.decode('utf-8'))))

    return list_username_password


def CleanTable_social_accounts():
    """
    This function will remove duplicate and clean google.com platform column in social_accounts table
    :return:
    """
    print("# ================== ADD NEW ROWS IN TABLE 'contacts' =================")
    # ======================================================================================
    # =============================== DATABASES ==========================================
    sqlite_connection = sqlite3.connect(LoadFile('db.db'))
    sqlite_cursor = sqlite_connection.cursor()
    # FIrst we clean the google accounts:
    # accounts.google.com and myaccount.google.com
    sqlite_cursor.execute("UPDATE social_accounts SET platform=? WHERE platform LIKE ? ",('google.com',f'%google%'))
    sqlite_connection.commit()
    sqlite_cursor.execute("DELETE FROM social_accounts WHERE id NOT IN (SELECT min(id) FROM social_accounts GROUP BY username,platform);")
    sqlite_connection.commit()



# =====================================================================================================
#                                     UI LOG MESSAGE ERRORS
# ====================================================================================================

def DisplayMessageLogUI(p_label_log,p_text,p_color="Black",p_tab="run"):
    """
    This function will append a message line in the label_log
    THis is very useful for users
    :param p_label_log:
    :param p_text:
    :return:
    """
    print("================================= DisplayMessageLogUI ===========================================")
    if p_tab=="run_one_task":
        max_lines = 24
    elif p_tab=="run":
        max_lines = 8

    try:
        tmp=p_label_log.text()
        # === WE NEED TO COUNT THE LINES
        counter_lines_1 = tmp.count('<br>')
        counter_lines_2 = tmp.count('<br/>')
        #print(f"tmp : {tmp} - {type(tmp)}")
        #print(f"counter_lines_2 : {counter_lines_2}")
        #print(f"counter_lines_1 : {counter_lines_1}")
        #print("-------------------------------------------------------------")
        if counter_lines_1 + counter_lines_2>max_lines:
            #print(f"counter_lines_1 + counter_lines_2 : {counter_lines_1 + counter_lines_2}")
            pos_end_first_line_1=tmp.find('<br>')
            pos_end_first_line_2 = tmp.find('<br/>')
            #print(f"pos_end_first_line_1 = {pos_end_first_line_1} - {type(pos_end_first_line_1)}")
            #print(f"pos_end_first_line_2 = {pos_end_first_line_2} - {type(pos_end_first_line_2)}")
            # We have only 1 <br>
            if pos_end_first_line_1!=-1 and pos_end_first_line_2==-1:
                new_pos = pos_end_first_line_1 + 4
                #print(f"new_pos : {new_pos}")
                tmp2 = tmp[new_pos:]
                tmp = tmp2
                #print(f"We have only 1 <br> : {tmp}")

            # We have only 2 <br/>
            elif pos_end_first_line_1 == -1 and pos_end_first_line_2 != -1:
                new_pos = pos_end_first_line_2 + 5
                #print(f"new_pos : {new_pos}")
                tmp2 = tmp[new_pos:]
                tmp = tmp2
                #print(f"We have only 2 <br/> : {tmp}")

            # We have both 1 & 2 <br><br/>
            elif pos_end_first_line_1 != -1 and pos_end_first_line_2 != -1:
                if pos_end_first_line_1<pos_end_first_line_2:
                    new_pos = pos_end_first_line_1 + 4
                    #print(f"new_pos : {new_pos}")
                    tmp2 = tmp[new_pos:]
                    tmp = tmp2
                    #print(f" We have both 1 & 2 <br><br/>: {tmp}")
                else:
                    new_pos = pos_end_first_line_2 + 5
                    #print(f"new_pos : {new_pos}")
                    tmp2 = tmp[new_pos:]
                    tmp = tmp2
                    #print(f" We have both 1 & 2 <br><br/>: {tmp}")


            # We have none 1 & 2 <br><br/>
            elif pos_end_first_line_1 == -1 and pos_end_first_line_2 == -1:
                #print("There is no lines. We need to remove all if there is a lot of text.")
                if len(tmp) > 250:
                    tmp2 = ""
                    tmp = tmp2
                    #print(f"We have none 1 & 2 <br><br/> and >150: {tmp}")


        #print("------------------- MAKE CONCATENATION -----------------------")
        tmp+=f'<br><span style="color:{p_color}">' + p_text + '</span>'
        #print(f"Result : {tmp}")

        p_label_log.setText(tmp)
    except Exception as ex:
        logger.error(f"Error DisplayMessageLogUI : {ex}")


# ==========================================================
# FUNCTION TO ETRACT NUMBERS FROM STRING
def extract_numbers_from_string(string):
    number = ''
    for i in string:
        if i.isnumeric():
            number += str(int(i))
    return number




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
            PopupMessage("Error Database!",f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

            logger.info(
                f"Problem with Mysql Database!\n{ex}\nIt is certainly a problem of Internet connexion. PhoneBot will retry to run in 15 seconds.")

    return  mysql_connection, mysql_cursor


#=============================================================================================================
