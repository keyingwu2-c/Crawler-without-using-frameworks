from bs4 import BeautifulSoup
from bs4 import element
import os
import csv
import sqlite3
import win32crypt
import requests
import time
import random

path = "D:Documents/IS Project/Data"
os.chdir(path)


def get_chrome_cookies(url):

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
    return ret_dict

DOMAIN_NAME = '.douban.com'
path = "D:Documents/IS Project/Data"
#ocean_kwai's
with open('Bks-user-1320642.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print("rrrrrrrrrrrrrow seperater")
        id= str(row[0])
        print(id)
        rd1 = random.randint(2, 11)
        time.sleep(rd1)
        cnt_url = 'https://book.douban.com/subject/' + id
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Connection': 'close'}

        with requests.Session() as response:
            response = requests.get(cnt_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
        soup = BeautifulSoup(response.text, "html.parser")

        Tags=set()
        Utbody =soup.find("div", id="db-tags-section")
        if isinstance(Utbody, element.Tag):
            Utgs = Utbody.find("div", class_="indent").find_all('a')
            for tg in Utgs:
                Tg = tg.get_text()
                #print(Tg)
                Tags.add(Tg)

#paste here !

        TagsStr =""
        for tag in Tags:
            TagsStr =TagsStr + tag + " "

        print(TagsStr)
        with open("BTags(pr)-user-1320642.csv", "a", encoding='utf-8-sig') as toWrite:
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
            writer.writerow([id, TagsStr])