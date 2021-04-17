import smtplib
import requests
from email.message import EmailMessage
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://keerthi:kk3600@cluster0.jd3jb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DatabaseName = client.assesment3
CollectionName = DatabaseName.AssessmentCollection


def send_email_message(message_to_send, sender_email):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("kkvasan3600@gmail.com", "keerthi@2000")
        email = EmailMessage()
        email['From'] = 'kkvasan3600@gmail.com'
        email['To'] = sender_email
        email['Subject'] = 'Change in MongoDB collection'
        email.set_content(message_to_send)
        server.send_message(email)
        print("email sent")

    except Exception as e:
        print(e)


def send_slack_message(message_to_send, user_name):
    try:
        mes = f'{user_name} -> {message_to_send}'
        messages = '{ "text":"%s" }' % mes
        response = requests.post("https://hooks.slack.com/services/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",
                                 data=messages)
        print(response.text)

    except Exception as e:
        print(e)


send_to_list = CollectionName.find({"sent": "false"})
for send_to in send_to_list:
    userEmail = send_to['email']
    userName = send_to['name']
    message = send_to['message']
    send_slack_message(message, userName)
    send_email_message(message, userEmail)
    CollectionName.update_one({"name": userName}, {"$set": {"sent": "true"}})
