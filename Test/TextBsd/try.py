import sklearn
import os
import csv
import numpy

path = "D:Documents/IS Project/text-expmt"
os.chdir(path)
dataset = numpy.loadtxt('Rvws-movie-3882715 .csv', delimiter=",")
X = dataset[:, 6]
y = dataset[:, 4]
