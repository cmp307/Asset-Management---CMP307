from connection import connectToDatabase

def assetSelectWhere(formData):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT * FROM cmp307links WHERE assetID = %s and softwareID = %s"
    conn.execute(sqlString, (formData['-L_HARDWARE-'], formData['-L_SOFTWARE-']))
    return conn.fetchall()

def getAssetWhere(request, id):
    conn, mydb = connectToDatabase()
    
    if request == 'hardware':
        sqlString = "SELECT * FROM cmp307hardware WHERE assetID = %s"
    elif request == 'software':
        sqlString = "SELECT * FROM cmp307software WHERE assetID = %s"
        
    conn.execute(sqlString, (id,))
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

    
def createAsset(request, formData):
    conn, mydb = connectToDatabase()
    if request == 'hardware':
        sqlString = "INSERT INTO cmp307hardware (assetName, deviceType, description, model, manufacturer, internalID, macAddress, ipAddress, physicalLocation, purchaseDate, warrantyInfo, notes, NISTKeywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        conn.execute(sqlString, (formData['-C_NAME-'], formData['-C_TYPE-'], formData['-C_DESCRIPTION-'], formData['-C_MODEL-'], formData['-C_MANU-'], formData['-C_INTERNAL_ID-'], formData['-C_MAC-'], formData['-C_IP-'], formData['-C_LOC-'], formData['-C_DATE-'], formData['-C_WARRANTY-'], formData['-C_NOTES-'], formData['-C_KEYWORDS-']))
        mydb.commit()
    if request == 'software':
        sqlString = "INSERT INTO cmp307software (assetName, type, description, version, developer, license, licenseKey, date, notes, NISTKeywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        conn.execute(sqlString, (formData['-C_NAME_SOFTWARE-'], formData['-C_TYPE_SOFTWARE-'], formData['-C_DESCRIPTION_SOFTWARE-'], formData['-C_VERSION-'], formData['-C_DEVELOPER-'], formData['-C_LICENSE-'], formData['-C_LICENSE_KEY-'], formData['-C_DATE_SOFTWARE-'], formData['-C_NOTES_SOFTWARE-'], formData['-C_KEYWORDS_SOFTWARE-']))
        mydb.commit()
        
def getAsset(request):
    conn, mydb = connectToDatabase()
    if request == 'hardware':
        sqlString = "SELECT * FROM cmp307hardware"
    elif request == 'software':
        sqlString = "SELECT * FROM cmp307software"

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
