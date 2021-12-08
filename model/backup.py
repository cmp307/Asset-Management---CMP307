import csv
import datetime
import PySimpleGUI as pyGUI  #GUI handling

class Backup:
    
    header = []
    path = []
    hardwareAsset = []
    softwareAsset = []
    
    header.append(['assetID', 'assetName', 'deviceType', 'description', 'model', 'manufacturer', 'internalID', 'macAddress', 'ipAddress', 'physicalLocation', 'purchaseDate', 'warrantyInfo', 'notes', 'NISTKeywords'])
    header.append(['assetID', 'assetName', 'type', 'description', 'version', 'developer', 'license', 'licenseKey', 'date', 'notes', 'NISTKeywords'])

    def __init__(self, softwareAsset, hardwareAsset):
        time = str(datetime.datetime.now())
        head, sep, tail = time.partition('.')   #discard seconds
        head = head.replace(':', '-')           #replace colon with hyphen as filename doesn't permit

        self.path.append('../backups/backup-hardware-'+head+'.csv')  
        self.path.append('../backups/backup-software-'+head+'.csv')

        self.hardwareAsset = softwareAsset
        self.softwareAsset = hardwareAsset


    def writeAsset(self, path, header, data):
        try:
            with open(path, 'w', newline='') as f:  #create new file with hardware path
                writer = csv.writer(f)
                writer.writerow(header)
                        
                for i in range(0, len(data)):
                    row = []
                    for j in range(len(data[i])):            
                        row.append(data[i][j])
                    writer.writerow(row)

                f.close()
            return 1
        except:
            return 0

    def writeToCSV(self):
        status = 0
        
        status = self.writeAsset(self.path[0], self.header[0], self.hardwareAsset)
        status += self.writeAsset(self.path[1], self.header[1], self.softwareAsset)

        if status < 2:
            layout = [  [pyGUI.Text('Error in creating backups', font='ANY 10')],
                        [pyGUI.Button('Close')],
            ]
            
        else:
            layout = [  [pyGUI.Text('Asset and Software placed in /backups', font='ANY 10')],
                        [pyGUI.Button('Close')],
            ]
            
        return pyGUI.Window("Backup", layout, size = (400,100), background_color="grey80", element_justification='c') 

            






