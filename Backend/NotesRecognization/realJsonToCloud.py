
# from MySQL import MySQLConnect
# import MySQLConnect as f

# def jsonToCloud(data):
print("data")
# print(data)
# MySQLConnect.jsonToCloud();
from flask import json
import pymysql

# Opens mysql.json file to grab mySQL super secret data
with open("config/mysql.json") as json_file:
    json_data = json.load(json_file)


db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
cursor = db.cursor()

def JsonToCloud(data):
    print("GOT CALLED\n JSON SENDING")
    print(data);
    # sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
    sql = "UPDATE 'sheet_music' SET 'file'={} WHERE 'sheet_id'=216".format(data);
    #FilePath -> C:/foldername/filename.bin
    # sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
    print("\n\n\n\nMYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    return;
