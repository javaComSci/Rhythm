from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # When a composition is made this will init all the data of that new composition
 ##

def newMusicSheets():
    content = request.json
    print("newSheetMusic Call")
    col = ["composition_id", "name", "author", "tempo"];
    values = ["'{}', '{}', '{}', '{}'".format(content['comp_id'], content['name'], content['author'], content['tempo'])];
    MySQLConnect.insert("sheet_music", ",".join(col), ",".join(values));
    return 'newMusicSheets'

def addSheetFile():
    sheetFile = request.files['file']
    sheetID = request.form['sheet_id']
    MySQLConnect.runQuery("UPDATE sheet_music SET file=%s WHERE sheet_id=%s", (sheetFile.read(), sheetID))
    MySQLConnect.runQuery("SELECT file FROM sheet_music WHERE sheet_id=%s", (15))
    return 'addFile'

def duplicateSheet():
    content = request.json
    MySQLConnect.runQuery("INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where sheet_id=%s", (content['comp_id'], content['sheet_id']))
    return 'duplicateSheet'

def updateAuthor():
    content = request.json
    MySQLConnect.runQuery("UPDATE sheet_music SET author=%s WHERE sheet_id=%s", (content['author'], content['sheet_id']))
    return 'updateAuthor'

def updateTempo():
    content = request.json
    MySQLConnect.runQuery("UPDATE sheet_music SET tempo=%s WHERE sheet_id=%s", (content['tempo'], content['sheet_id']))
    return 'updateTempo'
