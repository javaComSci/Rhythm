from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

##
 # deleteRoute calls MySQLConnect.py delete function to delete a user
 # IMPORTANT: THIS SHOULD NOT BE CALLED WHEN TRYING TO DELETE A USER
 ##
def deleteRoute():
    content = request.json
    print("delete Route Call")
    print(content)
    MySQLConnect.delete("user", content['_id'], content['delete']);
    return 'Deleted'
