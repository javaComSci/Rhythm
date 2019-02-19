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

def update(table, id, query, value):
    print("MYSQL COMMAND: {}".format(sql));
    print('update');

##
 # This will find everything in a specific table and matching the id with the user_id
 #
 ##
def find(table, id):
    sql = "SELECT * FROM {} WHERE user_id = '{}'".format(table, id);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    print(result)
    return result;

##
 # This will find everything in a specific table and matching the id with the user_id
 #
 ##
def findUser(table, value):
    sql = "SELECT * FROM {} WHERE email = '{}'".format(table, value);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    print(result)
    return result;

##
 # This will delete everything in the specific table matching the id to user_id AND
 # value[0] to value[1]
 #
 # @table what table you are looking at
 # @id the ID of the person
 # @value an array of the condition you want met
 # @return void
 ##
def delete(table, id, value):
    sql = "DELETE FROM {} WHERE {} = '{}' AND user_id = '{}';".format(table, value[0], value[1], id);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    return;

##
 # This will insert new information into the specific table
 #
 # @table what table you are looking at
 # @query the varible names you are inserting with
 # @value the values of the varibles you are inserting
 # @return void
 ##
def insert(table, query, value):
    sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
    print("MYSQL COMMAND: {}".format(sql));
    cursor.execute(sql)
    db.commit()
    return;
