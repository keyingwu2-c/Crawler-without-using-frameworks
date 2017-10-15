import os
import csv

def main():
    path = "D:Documents/IS Project/Data"
    os.chdir(path)
    GraphForOneUser('BTags(pr)-user-1320642.csv')


def GraphForOneUser(filename):
    with open(filename, encoding='utf-8') as f:
        f_csv = csv.reader(f)
        #headers = next(f_csv)
        for row in f_csv:
            Mv1 =str(row[0])
            #print(str(row[0]))
            TgStr1=str(row[1])
            TgSet1 =set(TgStr1.split())
            RelatedMvs=set()
            print("Get the related Bks for bk-"+Mv1)
            with open(filename, encoding='utf-8') as f2:
                f_csv2 = csv.reader(f2)
                #headers = next(f_csv)
                for r in f_csv2:
                    Mv2 = str(r[0])
                    if Mv2 == Mv1:
                        continue
                    TgStr2 = str(r[1])
                    TgSet2 = set(TgStr2.split())
                    Ovrlps = TgSet1.intersection(TgSet2)
                    #print("overlap count : " + str(len(Ovrlps)))
                    if len(Ovrlps)> 4:
                       RelatedMvs.add(Mv2)
                       print(Mv2+"  count: "+str(len(Ovrlps)))

            for rmv in RelatedMvs:
                #print()
                with open("BkGrph4Th(ptgs)-user-1320642.csv", "a", encoding='utf_8') as toWrite:
                    writer = csv.writer(toWrite, delimiter=',', lineterminator='\n')
                    writer.writerow([row[0], rmv])
            print("row seppppppppppppppppppppppppppppppppppppppppppppppppppppp")

main()