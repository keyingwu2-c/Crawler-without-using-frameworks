import os
import csv

path = "D:Documents/IS Project/Data"
os.chdir(path)
with open('movies-user-new4new4.csv', encoding='utf-8') as inp, open('-user-new4new4.csv', "a", encoding='utf-8-sig') as oup :
    r_csv = csv.reader(inp)
    w_csv = csv.writer(oup, delimiter=",")
    headers = next(r_csv)
    emptyOis = set()
    w_csv.writerow(["mId","rating","comment"])
    for row in r_csv:
        if row[1]==""and row[2]=="":
            continue
        w_csv.writerow(row)
        print(str(row[1]))
            #emptyOis.add(str(row[1]))