from connection import connectToDatabase

def userVerify(p1, p2):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT username FROM cmp307logins WHERE username = %s AND password = %s"
    conn.execute(sqlString, (p1,p2))
    return conn.fetchall()


def create(formData):
    conn, mydb = connectToDatabase()
    sqlString = "INSERT INTO cmp307data (assetName, deviceType, description, model, manufacturer, internalID, macAddress, ipAddress, physicalLocation, purchaseDate, warrantyInfo, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn.execute(sqlString, (formData[0], formData[1], formData[2], formData[3], formData[4], formData[5], formData[6], formData[7], formData[8], formData[9], formData[10], formData[11]))
    mydb.commit()

def get():
    conn, mydb = connectToDatabase()
    sqlString = "SELECT * FROM cmp307data"
    conn.execute(sqlString)
    return conn.fetchall()

def update(formData):
    conn, mydb = connectToDatabase()
    sqlString = "update cmp307data SET assetName = %s, deviceType = %s, description = %s, model = %s, manufacturer = %s, internalID = %s, macAddress = %s, ipAddress = %s, physicalLocation = %s, purchaseDate = %s, warrantyInfo = %s, notes = %s WHERE assetID = %s"
    conn.execute(sqlString, (formData[1], formData[2], formData[3], formData[4], formData[5], formData[6], formData[7], formData[8], formData[9], formData[10], formData[11], formData[12], formData[0]))
    mydb.commit()

def delete(formData):
    conn, mydb = connectToDatabase()
    sqlString = "delete from cmp307data WHERE assetID = %s"
    conn.execute(sqlString, (formData[0],))
    mydb.commit()

def backup():
    conn, mydb = connectToDatabase()
    sqlString = "BACKUP DATABASE cmp307data"
    TO DISK = 'D:\backups\testDB.bak'; 
