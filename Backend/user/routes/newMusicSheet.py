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

def duplicateSheet():
    # print("WTF");
    content = request.json
    # print(content['comp_id'])
    if(content['comp_id'] < 0):
        # print("GOT HERE");
        return "false"
    if(content['sheet_id'] < 0):
        return "false"
    if(content['comp_id'] > 1000):
        # print("GOT HERE");
        return "false"
    if(content['sheet_id'] > 1000):
        # print("GOT HERE");
        return "false"

    MySQLConnect.cursor.execute("INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where sheet_id=%s", (content['comp_id'], content['sheet_id']))
    MySQLConnect.db.commit()
    return 'duplicateSheet'
