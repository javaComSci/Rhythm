from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect
import StringIO

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
    sheetFile = request.form['file']
    sheetID = request.form['sheet_id']
    MySQLConnect.cursor.execute("UPDATE sheet_music SET song_json=%s WHERE sheet_id=%s", (sheetFile, sheetID))
    MySQLConnect.db.commit()
    MySQLConnect.cursor.execute("SELECT file FROM sheet_music WHERE sheet_id=%s", (15))
    record = MySQLConnect.cursor.fetchall()
    return 'addFile'

def duplicateSheet():
    content = request.json
    MySQLConnect.cursor.execute("INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where sheet_id=%s", (content['comp_id'], content['sheet_id']))
    MySQLConnect.db.commit()
    return 'duplicateSheet'
