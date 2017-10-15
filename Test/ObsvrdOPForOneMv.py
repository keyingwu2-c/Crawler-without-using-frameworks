from bs4 import BeautifulSoup
from bs4 import element
import urllib.request
import os
import csv
import re

stNum = 0
items = {}

path = "D:Documents/IS Project/Data"
os.chdir(path)

with open("lobbying.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["uLink", "rating", "comment"])

while stNum < 181:
    r = urllib.request.urlopen('https://movie.douban.com/subject/3882715/collections?start=' + str(
        stNum)).read()
    soup = BeautifulSoup(r, "html.parser")

    items = soup.find("div", class_="sub_ins").find_all("table")
    lobbying = {}
    for item in items:
        lobbying[item] = {}


    for item in items:

        link = item.find("div", class_="pl2").a["href"]
        lobbying[item]["link"] = link
        #print(type(link))

        regex = re.compile('allstar.*')
        rating = item.find("span", {"class": regex})
        if isinstance(rating, element.Tag):
            lobbying[item]["rating"] = rating.attrs['class']
        else:
            lobbying[item]["rating"] = ''
        #print(lobbying[item]["rating"])

        comment = item.find("p", class_="")
        if isinstance(comment, element.Tag):
            lobbying[item]["comment"] = comment.text
        else:
            lobbying[item]["comment"] = ''
        #print(lobbying[item]["comment"])

    for row in lobbying.keys():
        with open("lobbying.csv", "a", encoding='utf-8') as toWrite:
            writer = csv.writer(toWrite, delimiter=",")
            writer.writerow([lobbying[row]["link"], lobbying[row]["rating"],
                             lobbying[row]["comment"]])
            #print(lobbying[row]["comment"])

    print(stNum)
    stNum = stNum + 20