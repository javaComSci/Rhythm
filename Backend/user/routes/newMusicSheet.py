from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # When a composition is made this will init all the data of that new composition
 ##

def newCompo():
    content = request.json
    print("newSheetMusic Call")
    col = ["composition_id", file, "sheet_id"];
    values = ["'{}', '{}', '{}'".format(content['id'], content['description'], content['name'])];
    MySQLConnect.insert("composition", ",".join(col), ",".join(values));
    return 'newCompoAdded'
