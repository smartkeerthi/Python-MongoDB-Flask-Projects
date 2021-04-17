from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient(
    "<mongo db cluter url>")
NameListDatabase = client.NameListDatabase
CollectionList = NameListDatabase.CollectionList

app = Flask(__name__)


def getallnames():
    namelist = []
    names = CollectionList.find({}, {"Name": 1, "_id": 0})
    for name in names:
        namelist.append(name["Name"])
    return namelist


@app.route('/', methods=['POST', 'GET'])
def root():
    getallnames()
    if request.method == "POST":
        return redirect(request.form["Name"])
    return render_template('index.html', listofname=getallnames())


@app.route('/<name>/')
def fetchJson(name):
    names = list(CollectionList.find({"Name": name}, {"_id": 0}))
    nameListInStr = str(names)
    if len(names) == 0:
        return redirect(url_for("root"))

    return nameListInStr


if __name__ == '__main__':
    app.run(debug=True)
