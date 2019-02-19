from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # getInfo will call the find function int MySQLConnect.py and return a json array
 # of the results
 ##
def getInfo():
    content = request.json
    print("getInfo Route Call")
    results = MySQLConnect.find(content['table'], content['id']);
    return jsonify(results)
