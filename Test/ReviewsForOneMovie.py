from bs4 import BeautifulSoup
from bs4 import element
import os
import csv
import re
from requests.exceptions import RequestException
import sqlite3
import win32crypt
import requests
import time
import random

path = "D:Documents/IS Project/Data"
os.chdir(path)

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


def RwsForOneMv(mId, stN):
    DOMAIN_NAME = '.douban.com'
    stNum = stN
    items = {}
    headers = {
        'User-Agent': 'User-Agent:User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Connection': 'close'}
    get_numlmt = 'https://movie.douban.com/subject/'+mId
    #with requests.Session() as response:
      #response = requests.get(get_numlmt, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
    #soup = BeautifulSoup(response.text, "html.parser")
    #Numlmt = soup.find("div", class_="mod-hd").find("span", class_="pl").find('a').get_text().replace("全部 ","").replace(" 条","")
    Numlmt =40141  #int(Numlmt)
    Numlmt =Numlmt - Numlmt%20 + 1
    #print(str(Numlmt))
    while stNum < Numlmt:
        rd =random.random()
        slp =rd *2 + 4
        time.sleep(slp)
        #print(mId)

        get_url = 'https://movie.douban.com/subject/1484091/comments?start='+str(stNum)+'+%20%27&limit=20&sort=new_score&status=P'
        print("begin to send request")
        with requests.Session() as response:
            response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)

        soup = BeautifulSoup(response.text, "html.parser")
        #print(response.text)
        #print(soup)

        items = soup.find_all("div", class_="comment-item")
        if (len(items) < 2):
            break

        lobbying = {}
        for item in items:
            lobbying[item] = {}

        for item in items:

            link = item.find("div", class_="avatar").a["href"]
            lobbying[item]["uId"] = link.replace("https://www.douban.com/people/", "").replace("/", "")

            regex = re.compile('allstar.*')
            rating = item.find("span", {"class": regex})
            if isinstance(rating, element.Tag):
                lobbying[item]["rating"] = str(rating.attrs['class']).replace("['allstar", "").replace("0', 'rating']",
                                                                                                       "")
            else:
                lobbying[item]["rating"] = ''

            comment = item.find("p")
            if isinstance(comment, element.Tag):
                lobbying[item]["comment"] = comment.text
            else:
                lobbying[item]["comment"] = ''
                # print(rating.attrs['class'])

        for row in lobbying.keys():
            with open(mId + "-raw.csv", "a", encoding='gb18030') as toWrite:
                writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
                writer.writerow([mId, lobbying[row]["uId"], lobbying[row]["rating"],
                                 lobbying[row]["comment"]])
                # print(lobbying[row]["comment"])

        print(stNum)
        stNum = stNum + 20
        #print("has add on "+str(stNum))



def main():
    print('爬虫启动中')
    RwsForOneMv('1484091', 39900)



main()

'''

        with open(mId+"-raw.csv", "w") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["uId", "rating", "comment"])



    with open('mIds-ocean_kwai.csv', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            mId =str(row[0])
            print("Now is movie-"+mId)
            #Numlmt =int(row[1])
            RwsForOneMv(mId)


            try:
            with requests.Session() as response:
                response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=5)
        except RequestException:
            print("Restart crawler after short sleep !")
            time.sleep(rd*3)
            RwsForOneMv('1484091', stNum)

        'https://movie.douban.com/subject/'+mId+'/comments?start=' + str(
            stNum) + '&limit=20&sort=new_score&status=P'

'''