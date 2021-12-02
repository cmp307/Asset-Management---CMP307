from connection import connectToDatabase

def userVerify(p1, p2):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT accessAll FROM cmp307logins WHERE username = %s AND password = %s"
    conn.execute(sqlString, (p1,p2))
    return conn.fetchall()


def create_asset(formData):
    conn, mydb = connectToDatabase()
    sqlString = "INSERT INTO cmp307data (assetName, deviceType, description, model, manufacturer, internalID, macAddress, ipAddress, physicalLocation, purchaseDate, warrantyInfo, notes, NISTKeywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn.execute(sqlString, (formData['-C_NAME-'], formData['-C_TYPE-'], formData['-C_DESCRIPTION-'], formData['-C_MODEL-'], formData['-C_MANU-'], formData['-C_INTERNAL_ID-'], formData['-C_MAC-'], formData['-C_IP-'], formData['-C_LOC-'], formData['-C_DATE-'], formData['-C_WARRANTY-'], formData['-C_NOTES-'], formData['-C_KEYWORDS-']))
    mydb.commit()

def get():
    conn, mydb = connectToDatabase()
    sqlString = "SELECT * FROM cmp307data"
    conn.execute(sqlString)
    records = conn.fetchall()
    row = []
    data = []

    try:
        for i in range(len(records)):
            row = []
            for j in range(len(records[i])):
                if not (type(records[i][j]) == int):
                    row.append(records[i][j].decode())
                else:
                    row.append(records[i][j])
            data.append(row)
        return data
    except:
        return records
        
    
def getWhere(id):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT * FROM cmp307data WHERE assetID = %s"
    conn.execute(sqlString, (id,))
    return conn.fetchall()

def update(formData):
    conn, mydb = connectToDatabase()
    sqlString = "update cmp307data SET assetName = %s, deviceType = %s, description = %s, model = %s, manufacturer = %s, internalID = %s, macAddress = %s, ipAddress = %s, physicalLocation = %s, purchaseDate = %s, warrantyInfo = %s, notes = %s , NISTKeywords = %s WHERE assetID = %s"
    conn.execute(sqlString, (formData['-U_NAME-'], formData['-U_TYPE-'], formData['-U_DESC-'], formData['-U_MODEL-'], formData['-U_MANU-'], formData['-U_INTERNAL_ID-'], formData['-U_MAC-'], formData['-U_IP-'], formData['-U_LOC-'], formData['-U_DATE-'], formData['-U_WARRANTY-'], formData['-U_NOTES-'], formData['-U_KEYWORDS-'], formData['-U_ID-']))
    mydb.commit()

def delete(formData):
    conn, mydb = connectToDatabase()
    sqlString = "delete from cmp307data WHERE assetID = %s"
    conn.execute(sqlString, (formData['-D_ID-'],))
    mydb.commit()
    return conn.rowcount

def backup():
    conn, mydb = connectToDatabase()

