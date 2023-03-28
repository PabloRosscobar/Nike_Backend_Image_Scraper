from curses import keyname
from fileinput import close
import requests
import json
import platform
import sys
import random
import time
import random
import os
from datetime import datetime
import time
from threading import Lock
from colorama import Fore, init
import sys
import ssl
import urllib3
import PySimpleGUI as sg


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
end='\n'
init(autoreset=True)
machineOS = platform.system()
lock = Lock()
machineOS = platform.system()

now = str(datetime.now())[:-3]
requests.packages.urllib3.disable_warnings()


class Scraper():

    def __init__(self, chosenSKU, window):
        
        self.session = requests.Session()

        self.chosenSKU= chosenSKU
       
        self.getImage()


    def getImage(self):

        headers = {
            'authority': 'api.nike.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }


        s = self.session.get(
            f"https://api.nike.com/product_feed/threads/v2?filter=exclusiveAccess(true,false)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=marketplace(GB)&filter=language(en-GB)&filter=productInfo.merchProduct.styleColor({self.chosenSKU})", 
            headers=headers
        )

        raw = s.text.replace('\"', '"')

        data = json.loads(raw)

        try:
            for product in data["objects"]:
                if self.chosenSKU in product["productInfo"][0]["merchProduct"]["styleColor"]:
                    imageEnd = product["publishedContent"]["nodes"][0]["nodes"][0]["properties"]["squarishURL"].split("https://static.nike.com/a/images/t_default/")[1]
        except:
            sg.popup("ERROR - PARSING NIKE DATA")
      
        try:
            self.productImage = f"https://static.nike.com/a/images/t_PDP_864_v1/f_auto,b_rgb:f5f5f5/{imageEnd}"
            self.saveImage()
        except:
            sg.popup("ERROR - SKU NOT FOUND")
   
        
    def saveImage(self):

        try:
            if machineOS == "Darwin":
                x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES/")
            elif machineOS == "Windows":
                x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES\\")

            img_data = self.session.get(self.productImage).content
            with open(f"{x}{self.chosenSKU}.png", 'wb') as handler:
                handler.write(img_data)
        
            sg.popup(F"{self.chosenSKU} IMAGE HAS BEEN SAVED SUCCESSFULLY")
        except Exception as e:
            print(e)
    

    def info(self,s, end='\n'):
        now = str(datetime.now())[:-3]
        string = f'[{now}] {Fore.GREEN}{s}{end}'
        with lock:
            sys.stdout.write(string)
            sys.stdout.flush()

    def warning(self,s, end='\n'):
        now = str(datetime.now())[:-3]
        string = f'[{now}] {Fore.YELLOW}{s}{end}'
        with lock:
            sys.stdout.write(string)
            sys.stdout.flush()

    def error(self,s, end='\n'):
        now = str(datetime.now())[:-3]
        string = f'[{now}] {Fore.RED}{s}{end}'
        with lock:
            sys.stdout.write(string)
            sys.stdout.flush()

    def now_milliseconds(self):
        return int(time.time() * 1000)

    def date_time_milliseconds(self,date_time_obj):
        return int(time.mktime(date_time_obj.timetuple()) * 1000)


