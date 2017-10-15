import os
import csv

path = "D:Documents/IS Project/Data"
os.chdir(path)
with open('Movies-user-loca.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    OptMvs = set()
    for row in f_csv:
        OptMvs.add(str(row[0]))

with open('MTags-user-loca.csv', encoding='utf-8') as inp, open('-user-loca.csv', "a", encoding='utf-8-sig') as oup :
    r_csv = csv.reader(inp)
    w_csv = csv.writer(oup, delimiter=",")

    for row in r_csv:
        if OptMvs.__contains__(row[0]):
            w_csv.writerow(row)
            print(str(row[0]))