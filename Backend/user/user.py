from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect


def registerRoute():
    print("RegisterRoute Call")
    content = request.json
    print(content['username'])
    MySQLConnect.find();
    # json_data = json.load(request.data)
    # print(json_data['username'])
    return 'Registered'
