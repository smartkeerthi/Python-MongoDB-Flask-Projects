# totalValues = []
#
# with open('Academics.csv', 'r') as file:
#     lines = file.readlines()
#     TotalLines = len(lines)
#     fields = lines[0].split(',')
#     for x in range(1, TotalLines):
#         totalValues.append(lines[x])
#
#
# print(totalValues)
# print(fields)
#
# # def upload(field, value):

from pymongo import MongoClient

client = MongoClient("<mongo db cluster url>")
Db = client.test
CsvCollection = Db.csvFile

with open('Academics.csv', 'r') as file:
    myList = []
    for lines in file:
        # print(lines)
        rows = lines.split(',')
        # print(rows)
        myList.append(rows)

    print(myList)
    CompleteList = []
    for i in range(1, len(myList)):
        ToDict = {}
        for j in range(len(myList[0])):
            ToDict[myList[0][j]] = myList[i][j]

        CompleteList.append(ToDict)

    print(CompleteList)

CsvCollection.insert_many(CompleteList)


