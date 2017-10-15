
from bs4 import BeautifulSoup
from bs4 import element
import os
import csv
import re
import sqlite3
import win32crypt
import requests
import random
import time

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

stNum = 0
items = {}

path = "D:Documents/IS Project/Data"
os.chdir(path)

with open("Bks-user-1320642.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["bId", "rating", "comment"])

Numlmt = 303
Numlmt =Numlmt - Numlmt%15 + 1
while stNum < Numlmt :
    get_url = 'https://book.douban.com/people/1320642/collect?start=' + str(
        stNum) + '&sort=time&rating=all&filter=all&mode=grid'
    rd1 = random.randint(3, 11)
    time.sleep(rd1)

    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    with requests.Session() as response:
        response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find("ul", class_="interest-list").find_all("li", class_="subject-item")
    lobbying = {}

    for item in items:
        lobbying[item] = {}

    for item in items:
        link = item.find("div", class_="pic").a["href"]
        lobbying[item]["mId"] = link.replace("https://book.douban.com/subject/", "").replace("/", "")
        print(lobbying[item]["mId"])

        regex = re.compile('rating.*')
        rating = item.find("div", class_="short-note").find("span", {"class": regex})
        if isinstance(rating, element.Tag):
            lobbying[item]["rating"] = str(rating.attrs['class']).replace("['rating", "").replace("-t']", "")
        else:
            lobbying[item]["rating"] = ''
        #print(lobbying[item]["rating"])

        comment = item.find("p", class_="comment")
        if isinstance(comment, element.Tag):
            lobbying[item]["comment"] = comment.get_text(strip=True)
        else:
            lobbying[item]["comment"] = ''
        print(lobbying[item]["comment"])

    for row in lobbying.keys():
        with open("Bks-user-1320642.csv", "a", encoding='gb18030') as toWrite:
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
            writer.writerow([lobbying[row]["mId"], lobbying[row]["rating"],
                             lobbying[row]["comment"]])

    print(stNum)
    stNum = stNum + 15

