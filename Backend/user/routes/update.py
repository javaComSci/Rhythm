from flask import Flask, render_template, json, url_for, request, jsonify
from MySQL import MySQLConnect

##
 # update calls MySQLConnect.py update function to update a specific value
 ##

#  {
# 	"table": "composition",
# 	"update": ["name", "Chucken"],
# 	"where": ["composition_id", 2]
# }
def update():
    content = request.json
    print("update Route Call")
    results = MySQLConnect.update(content['table'], content['update'], content['where']);
    return 'updated'
