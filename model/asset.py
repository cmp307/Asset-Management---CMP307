from connection import connectToDatabase
import numpy as np


class Asset:
    
    assetData = []
    links = ""
    
    def setData(self, assetType, assetData):
        self.assetType = assetType
        self.assetData = np.asarray(assetData)
        
        if self.assetType == 'hardware':
            self.id = self.assetData[0]
            self.name = self.assetData[1]
            self.deviceType = self.assetData[2]
            self.description = self.assetData[3]
            self.model = self.assetData[4]
            self.manufacturer = self.assetData[5]           
            self.internalID = self.assetData[6]
            self.MAC = self.assetData[7]           
            self.IP = self.assetData[8]
            self.physicalLocation = self.assetData[9]
            self.date = self.assetData[10]
            self.warranty = self.assetData[11]
            self.notes = self.assetData[12]
            self.keyword = self.assetData[13]
        else:
            self.id = self.assetData[0]
            self.name = self.assetData[1]
            self.type = self.assetData[2]
            self.description = self.assetData[3]
            self.version = self.assetData[4]
            self.developer = self.assetData[5]
            self.license = self.assetData[6]
            self.key = self.assetData[7]
            self.date = self.assetData[8]
            self.notes = self.assetData[9]
            self.keyword = self.assetData[10]

        

        
    def deleteAsset(self):
        conn, mydb = connectToDatabase()
        
        if self.assetType == 'hardware':
            sqlString = "delete from cmp307hardware WHERE assetID = %s"
        elif self.assetType == 'software':
            sqlString = "delete from cmp307software WHERE assetID = %s"
            
        conn.execute(sqlString, (self.id, ))
        mydb.commit()

    def updateAsset(self):
        conn, mydb = connectToDatabase()
        
        if self.assetType == 'hardware':
            sqlString = "update cmp307hardware SET assetName = %s, deviceType = %s, description = %s, model = %s, manufacturer = %s, internalID = %s, macAddress = %s, ipAddress = %s, physicalLocation = %s, purchaseDate = %s, warrantyInfo = %s, notes = %s , NISTKeywords = %s WHERE assetID = %s"
            conn.execute(sqlString, (self.name, self.deviceType, self.description, self.model, self.manufacturer, self.internalID, self.MAC, self.IP, self.physicalLocation, self.date, self.warranty, self.notes, self.keyword, self.id))          
        if self.assetType == 'software':
            sqlString = "update cmp307software SET assetName = %s, type = %s, description = %s, version = %s, developer = %s, license = %s, licenseKey = %s, date = %s, notes = %s, NISTKeywords = %s WHERE assetID = %s"
            conn.execute(sqlString, (self.name, self.type, self.description, self.version, self.developer, self.license, self.key, self.date, self.notes, self.keyword, self.id))

        mydb.commit()
    
    def linkAsset(self, softwareID, hardwareID):
        conn, mydb = connectToDatabase()
        sqlString = "INSERT INTO cmp307links (assetID, softwareID) VALUES (%s, %s)"
        conn.execute(sqlString, (hardwareID, softwareID))
        mydb.commit()

    def getLinks(self):
        conn, mydb = connectToDatabase()
        sqlString = "SELECT softwareID FROM cmp307links WHERE assetID = %s"
        conn.execute(sqlString, (self.id, ))
        data = conn.fetchall()
        for a in data:
            if self.links != "":
                self.links += " " + str(a[0])
            else:
                self.links += str(a[0])
        self.assetData = np.append(self.assetData, self.links)
        
    def getID(self):
        return self.id
      
    def getKeyword(self):
        return self.keyword

