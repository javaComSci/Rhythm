from flask import Flask, render_template, json, url_for, request
from MySQL import MySQLConnect

##
 # When a composition is made this will init all the data of that new composition
 ##

def newCompo():
    x = 5;
