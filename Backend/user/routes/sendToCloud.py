import pymysql

'''
    db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    lastrowid = cursor.lastrowid
    cursor.close()
    db.close()
    return lastrowid
'''

json_data = {"server": "localhost","username": "root","password": "Pigsdontlikeeagles1"}

def cloud(sheetFile, sheetID):
	db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
	print 'made it HERE'
        print 'sheet id' + sheetID
        print 'jsoon:'+sheetFile
        cursor = db.cursor()
	cursor.execute("UPDATE sheet_music SET song_json=%s WHERE sheet_id=%s", (sheetFile, sheetID))
	db.commit()
	lastrowid = cursor.lastrowid
	cursor.close()
	db.close()
	return lastrowid
