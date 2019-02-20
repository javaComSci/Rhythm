from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect
from flask_mail import Mail, Message
import random


# https://pythonhosted.org/Flask-Mail/
def AccountRecovery(mail):
    content = request.json
    msg = Message('Account Recovery', sender = content['email'], recipients = [content['email']])
    x = "".join([str(random.randint(1,9)) for i in range(11)])
    print(x);
    msg.body = "Your code is {}".format(x)
    mail.send(msg)
    value = ["email", content['email']]
    MySQLConnect.update("user", "verf_code", x, value)
    return 'sent'

def checkKey():
    content = request.json
    check = MySQLConnect.findVerf("user", content['code'])
    if len(check) == 0:
        result = {
            "ok": "false",
            "id": -1
        }
    else:
        result = {
            "ok": "true",
            "id": check[0][0]
        }
        value = ["user_id", check[0][0]]
        MySQLConnect.update("user", "verf_code", 'NULL', value)
    return jsonify(result);
    return "true"
