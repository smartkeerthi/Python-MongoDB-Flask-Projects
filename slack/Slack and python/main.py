import smtplib
import requests
from email.message import EmailMessage
from pymongo import MongoClient

client = MongoClient(
    "<Mongo Db cluster Url>")
DatabaseName = client.assesment3
CollectionName = DatabaseName.AssessmentCollection


def send_email_message(message_to_send, sender_email):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("<email-id>", "<email-password>")
        email = EmailMessage()
        email['From'] = '<email-id>'
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
        response = requests.post("<slack webhook url >",
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
