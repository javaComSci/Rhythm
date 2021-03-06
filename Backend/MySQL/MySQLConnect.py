##
 # This file is used to soloy connect to MySQL and make changes to the database
 ##
from flask import Flask, render_template, json, url_for, send_file
# Importing a MySQL helper
import pymysql
import subprocess
from user.routes.MIDImaker import MIDImaker
import os
import shlex
import io
c = 0
# Opens mysql.json file to grab mySQL super secret data
with open("config/mysql.json") as json_file:
    json_data = json.load(json_file)

##
 # Connecting to mySQL with username/password (in .config file)
 # Connect using mysql -u root -p (Must have mysql downloaded)
 ##

# takes string and a tuple
def runQuery(query, args):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return lastrowid

def update(table, update, where):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "UPDATE {} SET {}='{}' WHERE {}='{}';".format(table, update[0], update[1], where[0], where[1])
    cursor.execute(sql)
    db.commit()
    cursor.close()
    # print("MYSQL COMMAND: {}".format(sql))
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    db.close()
    return


def updateMulti(table, update, where):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "UPDATE {} SET {}='{}' WHERE {}='{}';".format(table, update[0], update[1], where[0], where[1])
    cursor.execute(sql)
    db.commit()
    sqll = "UPDATE {} SET {}='{}' WHERE {}='{}';".format(table, update[2], update[3], where[0], where[1])
    cursor.execute(sqll)
    db.commit()
    cursor.close()
    print("MYSQL COMMAND: {}".format(sqll))
    db.close()
    return

##
 # This will find everything in a specific table and matching the id with the user_id
 #
 ##
def find(table, id):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE user_id = '{}';".format(table, id)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def findByEmail(table, email):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE email = '{}';".format(table, email)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def findVerf(table, code):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE verf_code = {};".format(table, code)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result

def findSheet(table, email):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE composition_id = '{}';".format(table, email)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def findSheetBySheetID(table, sheet_id):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT song_json FROM {} WHERE sheet_id = '{}';".format(table, sheet_id)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def findSheetBySheetIDD(table, sheet_id):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE sheet_id = '{}';".format(table, sheet_id)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


# when given the sheet id, the instrument is updated for the selection
def updateInstrumentById(table, sheet_id, instrument):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()

    # NEED TO FILL THIS THING!!!!!!
    sql = "update sheet_music set instrument = '{}' where sheet_id={}".format(instrument, sheet_id)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

##
 # This will find everything in a specific table and matching the id with the user_id
 #
 ##
def findUser(table, value):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "SELECT * FROM {} WHERE email = '{}';".format(table, value)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    print(result)
    cursor.close()
    db.close()
    return result

##
 # This will delete everything in the specific table matching the id to user_id AND
 # value[0] to value[1]
 #
 # @table what table you are looking at
 # @id the ID of the person
 # @value an array of the condition you want met
 # @return void
 ##
def delete(table, delete):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "DELETE FROM {} WHERE {} = '{}';".format(table, delete[0], delete[1])
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return

##
 # This will insert new information into the specific table
 #
 # @table what table you are looking at
 # @query the varible names you are inserting with
 # @value the values of the varibles you are inserting
 # @return void
 ##
def insert(table, query, value):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value)
    print("MYSQL COMMAND: {}".format(sql))
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return

def getSong(sheet_id):
    # print os.path.abspath(os.curdir)
    print 'get song route'
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    cursor.execute('SELECT song_json, instrument, tempo FROM sheet_music where sheet_id=%s', (sheet_id,))
    db.commit()
    global c
    song_json = cursor.fetchone()
    print("segrio " , type(song_json))
    if song_json is None:
        print("IN THE JSPN")
        return "False"
    cursor.close()
    db.close()
    # def jsons_to_MIDI(self, json_arr, sheet_id, instruments=["Piano"], start_times=[1]):
    makermidi = MIDImaker()
    #print 'TYPE of THING' + str(type(song_json))
    if song_json[1]:
        inst = song_json[1]
    else:
        inst = 'Piano'
    print 'tempo', song_json[2]
    if song_json[2]:
        tempo = song_json[2]
    else:
        tempo = 80
    sheetIdRet = makermidi.jsons_to_MIDI([song_json[0]], sheet_id, [inst], [1], tempos=[tempo])
    print 'tempo: ', song_json[2]
    subprocess.call(shlex.split('/home/Rhythm/Backend/MidiConversion/ConvertToMP3.sh '+sheet_id+'.mid'))
    flPath = '/home/Rhythm/Backend/'+sheet_id+'.mp3'
    c += 1
    newPath = '/home/Rhythm/Backend/'+sheet_id+str(c)+'.mp3'
    print 'testies'
    print flPath
    print newPath
    os.rename(flPath, newPath)
    print 'FLPATH: ' + flPath
    attFname = sheet_id+str(c)+'.mp3'
    print 'attfname', attFname
    return send_file(newPath, cache_timeout=-1,as_attachment=True,attachment_filename=sheet_id+str(c)+".mp3",mimetype="audio/mpeg")

def getCompSong(comp_id):
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    cursor.execute('SELECT song_json, instrument, tempo FROM sheet_music where composition_id=%s', (comp_id,))
    db.commit()
    song_json = cursor.fetchall()
    '''
        song_json = tuple ( tuple (song_json, instrument, tempo) )
        song_json[0] = (song_json, instrument, tempo)
        song_json[0][0] = song_json
    '''
    print 'SONG JSON: '
    print song_json
    songsToUse = []
    instrumentsToUse = []
    tempo = [80]
    global c
    for i in song_json:
        if (i[0]):
            songsToUse.append(i[0])
            if (i[1]):
                instrumentsToUse.append(i[1])
            else:
                instrumentsToUse.append("Piano")
            tempo[0] = i[2]
    print songsToUse
    print instrumentsToUse
    cursor.close()
    db.close()
    #def jsons_to_MIDI(self, songsToUse, comp_id, instruments=instrumentsToUse, start_times=[1], tempo=tempo):
    makermidi = MIDImaker()
    #print 'TYPE of THING' + str(type(song_json))
    makermidi.jsons_to_MIDI(songsToUse, comp_id, instrumentsToUse, start_times=[1], tempos=tempo)

    subprocess.call(shlex.split('/home/Rhythm/Backend/MidiConversion/ConvertToMP3.sh '+comp_id+'.mid'))
    flPath = '/home/Rhythm/Backend/'+comp_id+'.mp3'
    c+=1
    newPath = '/home/Rhythm/Backend/'+comp_id+str(c)+'.mp3'
    os.rename(flPath, newPath)
    attFname = comp_id+str(c)+'.mp3'
    # print 'FLPATH: ' + flPath
    return send_file(newPath,cache_timeout=-1,as_attachment=True,attachment_filename=attFname,mimetype="audio/mpeg")

def jsonToCloud(data):
	print("DATA", data)
