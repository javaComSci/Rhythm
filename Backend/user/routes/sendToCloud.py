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

json_data = {"server": "ec2-18-237-79-152.us-west-2.compute.amazonaws.com","username": "server-api","password": "Pigsdontlikeeagles1"}

def cloud(sheetFile, sheetID):
	db = pymysql.connect(json_data['server'], json_data['username'], json_data['password'], "Rhythm")
	cursor = db.cursor()
	cursor.execute("UPDATE sheet_music SET file=%s WHERE sheet_id=%s", (sheetFile, sheetID))
	db.commit()
	lastrowid = cursor.lastrowid
	cursor.close()
	db.close()
	return lastrowid
