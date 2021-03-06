from flask import Flask, render_template, json, url_for, request, jsonify
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
    check = MySQLConnect.findUser('user', content['email']);

    if len(check) == 0:
        MySQLConnect.insert("user", ",".join(col), ",".join(values));
    else:
        result = {
            "ok": "false",
            "id": -1
        }
        return jsonify(result);
    em = MySQLConnect.findByEmail('user', content['email']);
    result = {
        "ok": "true",
        "id": em[0][0]
    }
    return jsonify(result);
