import PySimpleGUI as pyGUI
from ctypes import windll
from math import floor
from connection import connectToDatabase
from SQL import userVerify
from hashlib import md5
from vunerability import *
import re as regex
import csv
import datetime

access = False

def getCenterScreen():
    user32 = windll.user32
    screensize = floor(user32.GetSystemMetrics(0) / 2) * 2, floor(user32.GetSystemMetrics(1) / 2) * 2
    return screensize

def backup(assetData):
    
    time = str(datetime.datetime.now())
    head, sep, tail = time.partition('.')
    head = head.replace(':', '-')
    path = '../backups/backup-asset-'+head+'.csv'
    header = ['ID', 'assetName', 'deviceType', 'description', 'model', 'manufacturer', 'internalID', 'macAddress', 'ipAddress', 'physicalLocation', 'purchaseDate', 'warrantyInfo', 'notes', 'NISTKeywords']

    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for i in range(0, len(assetData)):
            row = []
            for j in range(len(assetData[i])):            
                row.append(assetData[i][j])
            writer.writerow(row)

        f.close()


    
    layout = [  [pyGUI.Text('Asset and Software placed in /backups', font='ANY 10')],
                [pyGUI.Button('Close')],
            ]
    
    window = pyGUI.Window("Backup Confirmation", layout, size = (400,100), background_color="grey80", element_justification='c')
 
    while True:
        event, values = window.Read(timeout=25)
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Close':
            window.close()
            break



def createWindow(layout):
    global windowSize

    windowSize = getCenterScreen()
    window = pyGUI.Window("Scottish Glen Database Portal", layout, size = windowSize, background_color="grey80", element_justification='c')
    return window

def reloadFrame(window, layout):

    window.close()
    window = createWindow(layout)
    return window


    
def init():
    
    layout = [
        [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
        [pyGUI.Text('Please enter your login', key="-INIT-")],
        [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-USERNAME-')],
        [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*',enable_events=True, key='-PASSWORD-')],
        [pyGUI.Text('Incorrect Login', size =(15, 1), enable_events=True, key='-INCORRECT_LOGIN-', visible = False)],
        [pyGUI.Button('Login', key='-LOGIN-', bind_return_key = True)]
    ]

    window = createWindow(layout)
    
    return window

def crudControls(window):
    global access
    if access[0][0]:
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display', size=(10,1)), pyGUI.Button('Create', size=(10,1))],
            [pyGUI.Button('Update',size=(10,1)), pyGUI.Button('Delete', size=(10,1))],
            [pyGUI.Button('Backup'), pyGUI.Button('Vulnerability Search')],
            [pyGUI.Button('Log Out', size=(10,1))],

        ]
        
    else:
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display', size=(10,1)), pyGUI.Button('Log Out',  size=(10,1))],
        ]
            
    window = reloadFrame(window, layout)
    return window

def vulsearch(window, get):
        global toSearch
        
        toSearch = []

        for i in range(0, len(get)):
            for j in range(len(get[i])):     
                if (j==13):
                    if (get[i][j] != ""):
                       toSearch.append(get[i][j])
                   
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Button('Search entire table for vunerabilities')],
            [pyGUI.Button('Search for vunerabilities by Asset ID')],
            [pyGUI.InputText(enable_events=True, key='-S_ASSET_ID_INPUT-', visible = False), pyGUI.Text('Enter Asset ID', size =(15, 1), enable_events=True, key='-S_ASSET_ID_TEXT-', visible = False)],
            [pyGUI.Text('No keywords provided in this record', size =(27, 1), enable_events=True, key='-S_ASSET_ID_ERROR-', visible = False)],
            [pyGUI.Button('Submit', key='-S_ASSET_ID_SUBMIT-', visible=False)],
            [pyGUI.Button('Search for vunerabilities by keyword')],
        ]
        
        window = reloadFrame(window, layout)
        return window
    
def verifyLogin(window, username, password):

    global access

    access = userVerify(username, md5(password.encode()).hexdigest())
    if (access):
        window = crudControls(window)
    else:
        window.Element('-INCORRECT_LOGIN-').Update(visible=True)


    return window
    
def createItem(window):
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Creation', key='-CREATION-')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_NAME-')],
            [pyGUI.Text('Device Type', size = (15, 1)), pyGUI.Combo(values=['Portable', 'Mobile', 'Network', 'Non-Computing', 'IOT', 'Other'], size=(43, 1), readonly=True, key='-C_TYPE-', enable_events=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_DESCRIPTION-', enable_events=True)],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MODEL-')],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MANU-')],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_INTERNAL_ID-')],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MAC-')],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_IP-')],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_LOC-')],
            [pyGUI.Text('Buy Date (dd/mm/yyyy)',font='ANY 8', size =(20, 1)), pyGUI.InputText(enable_events=True, key='-C_DATE-')],
            [pyGUI.Text('Warranty Information', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_WARRANTY-', enable_events=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_NOTES-', enable_events=True)],
            [pyGUI.Text('NIST Keywords (CSV)', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), key='-C_KEYWORDS-', enable_events=True)],
            [pyGUI.Button('Create Asset', bind_return_key = True)],
        ]
    
    window = reloadFrame(window, layout)
    return window

def deleteItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Delete')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-D_ID-')],
            [pyGUI.Button('Delete Asset', bind_return_key = True)],
            [pyGUI.Text('Invalid Asset ID', size =(15, 1), key='-D_INVALID-', enable_events=True, visible = False)],
        ]
    window = reloadFrame(window, layout)
    return window


def updateItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Find')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_ID-')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_NAME-', disabled=True)],
            [pyGUI.Text('Device Type', size = (15, 1)), pyGUI.Combo(values=['Portable', 'Mobile', 'Network', 'Non-Computing', 'IOT', 'Other'], size=(43, 1), readonly=True, key='-U_TYPE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_DESC-', disabled=True, enable_events=True)],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MODEL-', disabled=True)],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MANU-', disabled=True)],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_INTERNAL_ID-', disabled=True)],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MAC-', disabled=True)],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_IP-', disabled=True)],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_LOC-', disabled=True)],
            [pyGUI.Text('Purchase Date', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_DATE-', disabled=True)],
            [pyGUI.Text('Warranty Information', size = (15, 1)), pyGUI.Multiline(size=(43, 5), disabled=True, key='-U_WARRANTY-', enable_events=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_NOTES-', disabled=True, enable_events=True)],
            [pyGUI.Text('NIST Keywords (CSV)', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), disabled=True, key='-U_KEYWORDS-', enable_events=True)],
            [pyGUI.Text('Invalid ID', key='-U_INVALID-', enable_events=True, visible=False)],
            [pyGUI.Button('Find Asset', key='-U_FIND-', visible = True)],
            [pyGUI.Button('Update Asset', key='-U_UPDATE-', visible = False)],

        ]
    window = reloadFrame(window, layout)
    return window
    

def displayItems(window, getAsset, getSoftware):

    global toSearch
    
    physicalAsset = []
    softwareAsset = []
    
    toSearch = []

    for i in range(0, len(getAsset)):
        row = []
        for j in range(len(getAsset[i])):
            if (j==13):
                if (getAsset[i][j] != ""):
                   toSearch.append(getAsset[i][j])
               
            row.append(getAsset[i][j])
        physicalAsset.append(row)

    for i in range(0, len(getSoftware)):
        row = []
        for j in range(len(getSoftware[i])):
            if (j==10):
                if (getSoftware[i][j] != ""):
                   toSearch.append(getSoftware[i][j])
               
            row.append(getSoftware[i][j])
        softwareAsset.append(row)

    layout = [
        [pyGUI.Button('Return to Operations')],
        [pyGUI.Table(physicalAsset, vertical_scroll_only = False, headings=['Asset ID', 'Name', 'Device Type', 'Description', 'Model', 'Manufacturer', 'Internal ID', 'MAC Address', 'IP Address', 'Physical Location', 'Purchase Date', 'Warranty Info', 'Notes', 'NIST Keywords'])],
        [pyGUI.Table(softwareAsset, vertical_scroll_only = False, headings=['Software ID', 'Name', 'Type', 'Description', 'Version', 'Developer', 'License', 'Key', 'Date Purchased', 'Notes', 'NIST Keywords'])],
        [pyGUI.Button('Search entire table for vunerabilities')],
    ]

    window = reloadFrame(window, layout)
    return window

def setAPIVals(val):
    global toSearch
    toSearch = []
    toSearch.append(val)

def checkVun(window):
    global toSearch
    data = []

    if len(toSearch) > 0:
        for i in range(0, len(toSearch)):
            rowCount, desc, rating = format(vunerabilitySearch(toSearch[i].replace(" ", "+")))
            row = []
            ratingValue = []
            
            if rowCount > 0:
                row.append(toSearch[i] + ' ' + 'has ' + str(rowCount) + ' vunerability(s)')
                
                for counter in rating:
                    match counter:
                        case "no rating avaliable":
                            ratingValue.append(0)
                        case "LOW":
                            ratingValue.append(1)
                        case "MEDIUM":
                            ratingValue.append(2)
                        case 'HIGH':
                            ratingValue.append(3)
                        case 'CRITICAL':
                            ratingValue.append(4)
                            

                n = len(ratingValue)
                for i in range(n-1):
                    for j in range(0, n-i-1):
                        if ratingValue[j] < ratingValue[j + 1] :
                            ratingValue[j], ratingValue[j + 1] = ratingValue[j + 1], ratingValue[j]
                            rating[j], rating[j + 1] = rating[j + 1], rating[j]
                            desc[j], desc[j + 1] = desc[j + 1], desc[j]

                            
                        
                for j in range(rowCount):            
                    row.append('Severity Level: ' + rating[j] + ' Description:' + desc[j])
                data.append(row)
    else:
        row = []
        row.append('No Keywords Provided')
        data.append(row)

    

    

        

    a = [
        [pyGUI.Button('Return to display')],
    ]

    for c in range(len(data)):
        a.append([pyGUI.Listbox(values=(data[c]), size=(100,10), horizontal_scroll=True)])


    x = floor(windll.user32.GetSystemMetrics(0) / 2) * 2
    y = floor(windll.user32.GetSystemMetrics(0) / 2) 
    
    layout = [
        [
            pyGUI.Column(a, scrollable=True,  size=(x,y), vertical_scroll_only=False),
        ]
    ]


            
    return layout



