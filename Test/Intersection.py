import os
import csv

def main():
    path = "D:NetKit-SRL/testing/movie-two pairs"
    os.chdir(path)
    GetIntersection('MvGrph3Th-user-ocean_kwai.csv', 'MvGrph3Th-user-new4new4.csv')
    #未修改完，修改完再运行
def GetIntersection(file1,file2):
    file1set = set()
    file2set = set()
    with open(file1, encoding='utf-8') as f1:
        f1_csv = csv.reader(f1)
        headers = next(f1_csv)
        for row in f1_csv:
            #print(row[0])
            file1set.add(row[0])
            file1set.add(row[1])

    with open(file2, encoding='utf-8') as f2:
        f2_csv = csv.reader(f2)
        headers = next(f2_csv)
        for row in f2_csv:
            #print(row[0])
            file2set.add(row[0])
            file2set.add(row[1])

    ITS = file1set.intersection(file2set)
    print(str(len(ITS)))
    for imd in ITS:
        print(imd)

main()