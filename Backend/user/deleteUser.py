from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

##
 # This will delete a user. We will not delete their information just incase they want
 # to account recovery ever, but we will put their account into "ghost" mode.
 ##

def deleteUsers():
    MySQLConnect.find(1,2,3);
    print ("Pizza")
    return 'deleteUser';
