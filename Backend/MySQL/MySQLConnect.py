##
 # This file is used to soloy connect to MySQL and make changes to the database
 ##
from flask import Flask, render_template, json, url_for
# Importing a MySQL helper
import pymysql

# Opens mysql.json file to grab mySQL super secret data
with open("config/mysql.json") as json_file:
    json_data = json.load(json_file)

##
 # Connecting to mySQL with username/password (in .config file)
 # Connect using mysql -u root -p (Must have mysql downloaded)
 ##
db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
cursor = db.cursor()

def update(table, query, value):
    print('update');

def find(table, query, value):
    print('insert');

def delete(table, query, value):
    sql = "DELETE FROM {} WHERE {} = '{}';".format(table,query,value);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    return;
    #DELETE FROM user WHERE email = 'Test';

def insert(table, query, value):
    sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    return;
