import os
import csv

''' Helpers '''

def getCategoryNames():
    categories = []
    with open('./lists/list_ids.csv', mode='r') as file:
        csvList = list(csv.reader(file,delimiter=','))[1:]
        categories = [x for [x,_] in csvList]
    return categories
