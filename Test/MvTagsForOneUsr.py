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

DOMAIN_NAME = '.douban.com'
path = "D:Documents/IS Project/Data"
#ocean_kwai's
with open('continue1.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print("rrrrrrrrrrrrrow seperater")
        id= str(row[0])
        print(id)
        rd1 = random.randint(2, 11)
        time.sleep(rd1)
        cnt_url = 'https://movie.douban.com/subject/' + id
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Connection': 'close'}

        with requests.Session() as response:
            response = requests.get(cnt_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
        soup = BeautifulSoup(response.text, "html.parser")

        Tags=set()
        Utbody =soup.find("div", class_="tags-body")
        if isinstance(Utbody, element.Tag):
            Utgs = Utbody.find_all('a')
            for tg in Utgs:
                Tg = tg.get_text()
                # print(Tg)
                Tags.add(Tg)

#paste here !

        TagsStr =""
        for tag in Tags:
            TagsStr =TagsStr + tag + " "

        print(TagsStr)
        with open("MTags(pure).csv", "a", encoding='utf-8-sig') as toWrite:
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
            writer.writerow([id, TagsStr])

'''

        sjclf =soup.find("div", class_="subject clearfix")
        if isinstance(sjclf,element.Tag):
            Ftgs=sjclf.find("div",id="info")
        else:
            continue
        Attrs = Ftgs.find_all("span", class_="attrs")
        # print("Heads: ")
        for attr in Attrs:
            Names = attr.find_all('a')
            for name in Names:
                DOrW = name.get_text()
                Tags.add(DOrW)
                # print(DOrW)

        #print("Actors: ")
        scope=Ftgs.find("span",class_="actor")
        if(isinstance(scope,element.Tag)):
            actors=scope.find_all('a')
            for actor in actors:
                Actr=actor.get_text()
                #print(Actr)
                Tags.add(Actr)

        #print("Genres: ")
        genres=Ftgs.find_all("span", property="v:genre")
        for genre in genres:
            Gnr=genre.get_text()
            #print(Gnr)
            Tags.add(Gnr)


'''
