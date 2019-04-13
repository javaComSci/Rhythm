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

def getInfoByEmail():
    content = request.json
    print("getInfoByEamil Route Call")
    results = MySQLConnect.findByEmail(content['table'], content['email']);
    return jsonify(results)

def getInfoSheet():
    content = request.json
    # print 'content:', content
    print("getInfoByEamil Route Call")
    results = MySQLConnect.findSheet(content['table'], content['id']);
    return jsonify(results)

def getSong(sheet_id):
    songFile = MySQLConnect.getSong(sheet_id)
    return songFile
