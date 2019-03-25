from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

##
 # When a composition is made this will init all the data of that new composition
 ##

def newCompo():
    content = request.json
    print("NewCompo Call")
    col = ["user_id", "description", "name"];
    values = ["'{}', '{}', '{}'".format(content['id'], content['description'], content['name'])];
    MySQLConnect.insert("composition", ",".join(col), ",".join(values));
    return 'newCompoAdded'

def duplicateComposition():
    content = request.json
    if(content['comp_id'] < 0):
        return "false"
    if(content['user_id'] < 0):
        return "false"
    if(content['comp_id'] > 1000):
        return "false"
    if(content['user_id'] > 1000):
        return "false"
    if(content['title'] == "NotARealCompo"):
        return "false"
    #MySQLConnect.cursor.execute("INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where sheet_id=%s", (content['comp_id'], content['sheet_id']))
    MySQLConnect.cursor.execute("INSERT INTO composition(name,description,user_id) SELECT %s, description, %s from `composition` where composition_id=%s", (content['title'], content['user_id'], content['comp_id']))
    oldCompID = content['comp_id']
    newCompID = MySQLConnect.cursor.lastrowid
    MySQLConnect.cursor.execute("INSERT INTO sheet_music(file,composition_id,name) SELECT file, %s, name from `sheet_music` where composition_id=%s", (newCompID, oldCompID))
    MySQLConnect.db.commit()
    return 'duplicatedComposition'
