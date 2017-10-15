from bs4 import BeautifulSoup
from bs4 import element
import os
import csv
import sqlite3
import win32crypt
import requests
import random
import time


path = "D:Documents/IS Project/Data"
os.chdir(path)
with open('Rvws-movie-25662327.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    rvwrs = set()
    for row in f_csv:
        rvwrs.add(str(row[1]))

print("Are there any elements in rvwrs ? " + str(len(rvwrs)))


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
#os.chdir(path)
with open('Rvws-movie-25662327(cont).csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print("Now get the connections in reviewers of user-"+str(row[0]))
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Connection': 'close'}

        cnt_url = 'https://www.douban.com/people/' + str(row[0]) + '/contacts'
        rcnt_url = 'https://www.douban.com/people/' + str(row[0]) + '/rev_contacts'
        rd1 = random.randint(2, 7)
        time.sleep(rd1)
        with requests.Session() as response:
            req = requests.get(cnt_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
        rd2 = random.randint(3, 8)
        time.sleep(rd2)
        with requests.Session() as response:
            rreq = requests.get(rcnt_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)

        soup = BeautifulSoup(req.text, "html.parser")
        rsoup = BeautifulSoup(rreq.text, "html.parser")
        flwees = soup.find_all("dl", class_="obu")
        flwers = rsoup.find_all("dl", class_="obu")
        flweeids = set()
        flwerids = set()
        for flwee in flwees:
            eelink = flwee.find("dd").a["href"]
            # print(flwlink)
            flweeid = eelink.replace("https://www.douban.com/people/", "").replace("/", "")
            # print(flwid)
            flweeids.add(flweeid)
        for flwer in flwers:
            erlink = flwer.find("dd").a["href"]
            # print(flwlink)
            flwerid = erlink.replace("https://www.douban.com/people/", "").replace("/", "")
            # print(flwid)
            flwerids.add(flwerid)
        fds = flweeids.intersection(flwerids)
        FdInRws = fds.intersection(rvwrs)
        print("Are there any elements in flwees ? " + str(len(flweeids)))
        print("Are there any elements in flwers ? " + str(len(flwerids)))
        print("Are there any elements in fds ? " + str(len(fds)))
        print("Are there any elements in FdInRws ? " + str(len(FdInRws)))
        for rfd in FdInRws:
            #print(rfd)
            with open("RvwrNet.csv", "a", encoding='utf-8') as toWrite:
                writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
                writer.writerow([row[0], rfd])



