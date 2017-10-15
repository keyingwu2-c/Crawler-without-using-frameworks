from bs4 import BeautifulSoup
from bs4 import element
from selenium import webdriver
import re
import os
import csv
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

data = open("reviews-book-7670800.csv").read()
if len(data)>0:
    print("continue to write on the same file")
else:
    with open("reviews-book-7670800.csv", "w") as toWrite:
        writer = csv.writer(toWrite, delimiter=",")
        writer.writerow(["uId", "rating", "comment"])

DOMAIN_NAME = '.goodreads.com'

cnt_url = 'https://www.goodreads.com/book/show/7670800-clementine#other_reviews'

driver = webdriver.PhantomJS(executable_path=r'D:\Python\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
driver.get(cnt_url)
box = driver.find_element_by_id("other_reviews").find_element_by_class_name("bigBoxBody").find_element_by_id("reviews")
print("what the driver get: "+box.find_element_by_class_name('next_page').text)

path = "D:Documents/IS Project/Data/EngData"
os.chdir(path)
count = 1
while count < 11:
    print("Now is page "+ str(count))
    if count > 1:
        driver = webdriver.PhantomJS(executable_path=r'D:\Python\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
        driver.get(cnt_url)
        box = driver.find_element_by_id("other_reviews").find_element_by_class_name("bigBoxBody").find_element_by_id(
            "reviews")
        print(box.find_element_by_class_name('next_page').text)
        box.find_element_by_class_name('next_page').click()
        time.sleep(5)

    test = driver.find_element_by_id("bookReviews").find_elements_by_link_text("...more")
    for tst in test:
        # print(str(len(test)))
        tst.click()
        time.sleep(3)
        seemore = driver.find_element_by_id("bookReviews").find_element_by_class_name("readable")
        cntInIt = seemore.find_elements_by_tag_name("span")
        # print(str(len(cntInIt)))
        # print(cntInIt[0].text)#seemore.get_attribute("id")
        # print()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    BigBox = soup.find("div", id="other_reviews")
    # print(BigBox)
    items = BigBox.find_all("div", class_="review")
    # nextPage= BigBox.find("a", class_="next_page")
    # print(nextPage)

    for it in items:
        print()
        userId = it.find("a", class_="user").attrs['href'].replace("/user/show/", "")
        allstars = it.find("span", class_=" staticStars")
        if isinstance(allstars, element.Tag):
            rating = str(len(allstars.find_all("span", class_="staticStar p10")))

        reg = re.compile('reviewTextContainer.*')
        # driver = webdriver.PhantomJS(executable_path=r'D:\Python\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs')
        # driver.get(cnt_url)
        more = it.find("span", {"id": reg}).find("a")
        # print(type(more))

        regex = re.compile('freeText.*')
        review = it.find("div", class_="reviewText stacked")
        if isinstance(review, element.Tag):
            texts = review.find_all("span", {"id": regex})
            rtext = str(texts[0].text)
            if len(texts) > 1:
                rtext = str(texts[1].text)
        print(userId + " " + rating + " " + str(len(texts)))
        print(rtext)

        try:
            with open("reviews-book-7670800.csv", "a", encoding='gbk') as toWrite:
                writer = csv.writer(toWrite, delimiter=",", lineterminator='\n')
                writer.writerow([userId, rating, rtext])
        except UnicodeEncodeError:
            continue

    count = count + 1




'''
   .find_element_by_id("reviews")
   find_element_by_class_name("uitext")

    headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Connection': 'close'}


    with requests.Session() as response:
    req = requests.get(cnt_url, cookies=get_chrome_cookies(DOMAIN_NAME), headers=headers, timeout=600)

    soup = BeautifulSoup(req.text, "html.parser")
'''