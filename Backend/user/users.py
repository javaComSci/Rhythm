from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

##
 # RegisterRoute first checks to make sure the email registering with is unique,
 # and then calls the insert in MySQLConnect.py
 ##
def registerRoute():
    content = request.json
    print("RegisterRoute Call")
    col = ["email"];
    values= ["'{}'".format(content['email'])];
    #content['username'];
    MySQLConnect.insert("user", ",".join(col), ",".join(values));
    # json_data = json.load(request.data)
    # print(json_data['username'])
    return 'Registered'
