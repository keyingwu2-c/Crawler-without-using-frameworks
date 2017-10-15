import os
import csv

path = "D:NetKit-SRL/testing/movie-two pairs"
os.chdir(path)
with open('Rvws-movie-4888853-FM.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    Opts = set()
    for row in f_csv:
        Opts.add(str(row[0]))

with open('RvwrNet-movie-4888853-FM(old).csv', encoding='utf-8') as inp, open('RvwrNet-movie-4888853-FM.csv', "a", encoding='utf-8') as oup :
    r_csv = csv.reader(inp)
    w_csv = csv.writer(oup, delimiter=",", lineterminator='\n')

    for row in r_csv:
        if Opts.__contains__(row[0]) & Opts.__contains__(row[1]):
            w_csv.writerow(row)
            #print(str(row[0]))