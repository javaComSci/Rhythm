
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

v = []
v.append({
      "note": 0,
      "length": 0,
      "pitch": 1
});
v.append({
      "note": 3,
      "length": 2,
      "pitch": 8
});
v.append({
      "note": 3,
      "length": 2,
      "pitch": 8
});

exmapledata = {
    "clef": 1,
    "notes": v,
}
exmapledata2 = {
    "clef": 1,
    "notes": 2,
}

print(exmapledata2);

# def JsonToCloud():
print("GOT CALLED\n JSON SENDING")
# print(data); UPDATE mytable SET jcol = '{"a": 10, "b": 25}')
# sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
# sql = "UPDATE sheet_music SET fileJSON = {} WHERE sheet_id=216;".format(exmapledata);
# UPDATE players SET player_and_games = JSON_SET(player_and_games, '$.games_played.Battlefield', 'no', '$.games_played.Puzzler', JSON_OBJECT('time', 15)) WHERE id = 3;
# UPDATE players SET player_and_games = JSON_INSERT(player_and_games, '$.games_played.Puzzler', JSON_OBJECT('time', 20)) WHERE player_and_games->'$.name' = 'Henry';
sql = "UPDATE sheet_music SET fileJSON = JSON_INSERT(fileJSON, '$.filey', {}) WHERE sheet_id = 216;".format(exmapledata2);
#FilePath -> C:/foldername/filename.bin
# sql = "INSERT INTO {}({}) VALUES ({});".format(table,query,value);
print("\n\n\n\nMYSQL COMMAND: {}".format(sql));
cursor.execute(sql)
db.commit()
cursor.close()
db.close()
# return;
