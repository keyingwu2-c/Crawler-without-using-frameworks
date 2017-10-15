#Use this to test out things about "lobbying"

from bs4 import BeautifulSoup
import urllib.request
import re
import os
import subprocess
import win32crypt
import sqlite3
import requests

SOUR_COOKIE_FILENAME = 'C:\用户\\user\AppData\Local\Google\Chrome\\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = 'D:\python-chrome-cookies'

def get_chrome_cookies(url):
    subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    os.system('copy "C:\用户\\user\AppData\Local\Google\Chrome\\User Data\Default\Cookies" D:\\python-chrome-cookies')

    conn = sqlite3.connect("d:\\python-chrome-cookies")
    ret_dict = {}
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        #print(row[0])
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_dict

path = "D:Documents/IS Project/Data"
os.chdir(path)
stNum=840
get_url = r'https://movie.douban.com/subject/26425468/comments?start=' + str(
            stNum) + '&limit=20&sort=new_score&status=P'

DOMAIN_NAME = '.douban.com'
response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME))

soup = BeautifulSoup(response.text, "html.parser")

#print(soup.prettify()[17000:19700])
items = soup.find_all("div", class_="comment-item")
print(str(len(items)))




'''
letters = soup.find_all("div", class_="item")
regex = re.compile('rating.*')
part2 = letters[0].find("span", {"class": regex})
print(part2.attrs['class'])

#print(letters[0].a.get_text()+"\n\t"+"link: ")
#print(letters[0].a["href"])
#print(letters[0].attrs['class'])
'''

'''
regex = re.compile('rating.*')

letters = soup.find_all("span", {"class": regex})

soup.find("", class_="")

for element in letters:
    lobbying[element.a.get_text()] = {}

for element in letters:
    lobbying[element.a.get_text()]["link"] = element.a["href"]

for item in lobbying.keys():
    print(item + ": " + "\n\t" + "link: " + lobbying[item]["link"] + "\n\t")
'''