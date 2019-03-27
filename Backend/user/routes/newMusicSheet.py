from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # When a composition is made this will init all the data of that new composition
 ##

def newMusicSheets():
    content = request.json
    print("newSheetMusic Call")
    col = ["composition_id", "name"];
    values = ["'{}', '{}'".format(content['comp_id'], content['name'])];
    MySQLConnect.insert("sheet_music", ",".join(col), ",".join(values));
    return 'newMusicSheets'

def addSheetFile():
    sheetFile = request.files['file']
    sheetID = request.form['sheet_id']
    query = "UPDATE sheet_music SET file=%s WHERE sheet_id=%s", (sheetFile.read(), sheetID)
    MySQLConnect.runQuery(query)
    query = "SELECT file FROM sheet_music WHERE sheet_id=%s", (15)
    MySQLConnect.runQuery(query)
    return 'addFile'

def duplicateSheet():
    content = request.json
    query = "INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where sheet_id=%s", (content['comp_id'], content['sheet_id'])
    MySQLConnect.runQuery(query)
    return 'duplicateSheet'
