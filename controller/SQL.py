from connection import connectToDatabase

def assetLink(formData):
    conn, mydb = connectToDatabase()
    sqlString = "INSERT INTO cmp307links (assetID, softwareID) VALUES (%s, %s)"
    conn.execute(sqlString, (formData['-L_HARDWARE-'], formData['-L_SOFTWARE-']))
    mydb.commit()

def assetSelectWhere(formData):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT * FROM cmp307links WHERE assetID = %s and softwareID = %s"
    conn.execute(sqlString, (formData['-L_HARDWARE-'], formData['-L_SOFTWARE-']))
    return conn.fetchall()

def assetLinkRetrieve(id):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT softwareID FROM cmp307links WHERE assetID = %s"
    conn.execute(sqlString, (id, ))
    return conn.fetchall()
    

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

    
    
def getAssetWhere(request, id):
    conn, mydb = connectToDatabase()
    
    if request == 'hardware':
        sqlString = "SELECT * FROM cmp307hardware WHERE assetID = %s"
    elif request == 'software':
        sqlString = "SELECT * FROM cmp307software WHERE assetID = %s"
        
    conn.execute(sqlString, (id,))
    return conn.fetchall()

def updateAsset(request,formData):
    conn, mydb = connectToDatabase()
    if request == 'hardware':
        sqlString = "update cmp307hardware SET assetName = %s, deviceType = %s, description = %s, model = %s, manufacturer = %s, internalID = %s, macAddress = %s, ipAddress = %s, physicalLocation = %s, purchaseDate = %s, warrantyInfo = %s, notes = %s , NISTKeywords = %s WHERE assetID = %s"
        conn.execute(sqlString, (formData['-U_NAME-'], formData['-U_TYPE-'], formData['-U_DESC-'], formData['-U_MODEL-'], formData['-U_MANU-'], formData['-U_INTERNAL_ID-'], formData['-U_MAC-'], formData['-U_IP-'], formData['-U_LOC-'], formData['-U_DATE-'], formData['-U_WARRANTY-'], formData['-U_NOTES-'], formData['-U_KEYWORDS-'], formData['-U_ID-']))
        mydb.commit()
    if request == 'software':
        sqlString = "update cmp307software SET assetName = %s, type = %s, description = %s, version = %s, developer = %s, license = %s, licenseKey = %s, date = %s, notes = %s, NISTKeywords = %s WHERE assetID = %s"
        conn.execute(sqlString, (formData['-U_NAME_SOFTWARE-'], formData['-U_TYPE_SOFTWARE-'], formData['-U_DESCRIPTION_SOFTWARE-'], formData['-U_VERSION-'], formData['-U_DEVELOPER-'], formData['-U_LICENSE-'], formData['-U_LICENSE_KEY-'], formData['-U_DATE_SOFTWARE-'], formData['-U_NOTES_SOFTWARE-'], formData['-U_KEYWORDS_SOFTWARE-'], formData['-U_ID_SOFTWARE-']))
        mydb.commit()

def deleteAsset(request, formData):
    conn, mydb = connectToDatabase()
    
    if request == 'hardware':
        sqlString = "delete from cmp307hardware WHERE assetID = %s"
        conn.execute(sqlString, (formData['-D_ID-'],))
        mydb.commit()
    elif request == 'software':
        sqlString = "delete from cmp307software WHERE assetID = %s"
        conn.execute(sqlString, (formData['-D_ID_SOFTWARE-'],))
        mydb.commit()

    return conn.rowcount



