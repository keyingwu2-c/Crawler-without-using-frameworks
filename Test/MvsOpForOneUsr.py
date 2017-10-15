
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

stNum = 0
items = {}

path = "D:Documents/IS Project/Data"
os.chdir(path)

with open("movies-user.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["mId", "rating", "comment"])

Numlmt = 71
Numlmt =Numlmt - Numlmt%15
while stNum < Numlmt :
    get_url = 'https://movie.douban.com/people/flowermumu/collect?start=' + str(
        stNum) + '&sort=time&rating=all&filter=all&mode=grid'
    rd1 = random.randint(3, 10)
    time.sleep(rd1)

    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    with requests.Session() as response:
        response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(response.text)

    items = soup.find_all("div", class_="item")
    lobbying = {}
    for item in items:
        lobbying[item] = {}

    for item in items:
        link = item.find("div", class_="pic").a["href"]
        lobbying[item]["mId"] = link.replace("https://movie.douban.com/subject/", "").replace("/", "")
        print(lobbying[item]["mId"])

        regex = re.compile('rating.*')
        rating = item.find("div",class_="info").find("span", {"class": regex})
        if isinstance(rating, element.Tag):
            lobbying[item]["rating"] = str(rating.attrs['class']).replace("['rating", "").replace("-t']", "")
            #print(lobbying[item]["rating"])
        else:
            lobbying[item]["rating"] = ''
        #print(lobbying[item]["rating"])

        comment = item.find("span", class_="comment")
        if isinstance(comment, element.Tag):
            lobbying[item]["comment"] = comment.text
        else:
            lobbying[item]["comment"] = ''


    for row in lobbying.keys():
        with open("movies-user.csv", "a", encoding='utf-8') as toWrite:
            writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
            writer.writerow([lobbying[row]["mId"], lobbying[row]["rating"],
                             lobbying[row]["comment"]])
        #print(lobbying[row]["comment"])

    print(stNum)
    stNum = stNum + 15




#print(soup.prettify()[17000:19700])



#lobbying = {}

#print(letters[0].a.get_text()+"\n\t"+"link: ")
#print(letters[0].a["href"])




    #writer.writerow(["name", "link", "date"])



'''
'https://book.douban.com/people/1320642/collect?start=' + str(
        stNum) + '&sort=time&rating=all&filter=all&mode=grid'

for item in letters:
    print(item.a.get_text()+"\n\t"+"link: "+item.a["href"] + "\n\t")

for element in letters:
    lobbying[element.a.get_text()]["link"] = element.a["href"]

for item in lobbying.keys():
    print(item + ": " + "\n\t" + "link: " + lobbying[item]["link"])


from bs4 import BeautifulSoup
import urllib
import pip._vendor
url = "http://blog.gting.me"  # 目标URL

from urllib import request
#resp = request.urlopen('https://movie.douban.com/nowplaying/hangzhou/')
#html_data = resp.read().decode('utf-8')

from bs4 import BeautifulSoup as bs
#soup = bs(html_data, 'html.parser')


#request= pip._vendor.requests.models.Request(url)
#response= pip._vendor.requests.models.urlopen(request)
#response = pip._vendor.requests.packages.urllib3.request.urlopen(request)  # 获取目标网页
#response = pip._vendor.requests.packages.urllib3.request.urlopen(url)

#page = BeautifulSoup(response, "html.parser")  # 解析目标网页，建立HTML对象
'''