from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import requests

client = MongoClient(
    "<mongo db cluster url>")
DatabaseName = client.assesment3
CollectionName = DatabaseName.AssessmentCollection

app = Flask(__name__)


def get_all_names():
    namelist = []
    names = CollectionName.find({}, {"name": 1, "_id": 0})
    for name in names:
        namelist.append(name["name"])
    return namelist


@app.route('/', methods=['POST', 'GET'])
def root():
    get_all_names()
    if request.method == "POST":
        return redirect(request.form["Name"])
    return render_template('index.html', listofname=get_all_names())


@app.route('/<user_name>/')
def send_slack_message(user_name):
    try:
        names = CollectionName.find({"name": user_name})
        for name in names:
            user_message = name['message']
            mes = f'{user_name} -> {user_message}'
            messages = '{ "text":"%s" }' % mes
            response = requests.post("<slack webhook url >",
                                     data=messages)
            print(response.text)

    except Exception as e:
        print(e)

    return f'Message sent to {user_name}'


if __name__ == '__main__':
    app.run(debug=False)
