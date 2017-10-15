import urllib
import http.cookiejar
import re
from bs4 import BeautifulSoup
import sqlite3
import os
import win32crypt
import requests
from requests.exceptions import RequestException

'''
filename = 'cookie'
cookie = http.cookiejar.LWPCookieJar(filename)
try:
    cookie.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载')

'''

#SOUR_COOKIE_FILENAME = 'C:\用户\\user\AppData\Local\Google\Chrome\\User Data\Default\Cookies'
#DIST_COOKIE_FILENAME = 'D:\python-chrome-cookies'


def get_chrome_cookies(url):
    #subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    #os.system('copy "C:\用户\\user\AppData\Local\Google\Chrome\\User Data\Default\Cookies" D:\\python-chrome-cookies')

    conn = sqlite3.connect("d:\\chrome-cookies-dongmian")
    ret_dict = {}
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        #print(row[0])
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    #subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_dict

#DOMAIN_NAME = '.douban.com'
DOMAIN_NAME = 'douban.com'
get_url = 'https://www.douban.com/people/3573533/'
cookies=get_chrome_cookies(DOMAIN_NAME)
for key, value in cookies.items():
    print(key + "=" + value)

try:
    response = requests.get(get_url, cookies=cookies, timeout=10)
    print(response.status_code)
except RequestException:
    #response = requests.get('https://www.douban.com/people/3573533/', cookies=get_chrome_cookies(DOMAIN_NAME),timeout=1)
    print("Enter the error dealing code !")

response.close()
#soup = BeautifulSoup(response.text, "html.parser")
#Utbody =soup.find("div", id="content")
#print(str(Utbody))



