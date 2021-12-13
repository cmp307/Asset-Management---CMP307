#----------------------------------------------------------
import PySimpleGUI as pyGUI  #GUI handling
import re as regex           #Input Validation
import subprocess
import os

from ctypes import windll    #Screen size
from SQL import *
from vunerability import *   #Vulnerability check

from user import *
#----------------------------------------------------------
access = False
account = User()
#----------------------------------------------------------

def dump(txt):
    if type(txt) == list:
        with open("../nist/NIST dump.txt", 'a', newline="") as text_file:
            for a in txt:
                text_file.write(a)
            text_file.write("\n\n")


def getCenterScreen():  #get screen size
    user32 = windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize

def createWindow(layout):   #create window screen, used whenever a new frame is loaded
    global windowSize

    windowSize = getCenterScreen()
    window = pyGUI.Window("Scottish Glen Database Portal", layout, size = windowSize, background_color="grey80", element_justification='c')
    return window

def reloadFrame(window, layout):

    window.close()
    window = createWindow(layout)
    return window


def createLinks(window):
    layout = [
        [pyGUI.Button('Return to Operations')],
        [pyGUI.Text('Please enter the asset IDs of the assets you would like to link', font = 'ANY 12')],
        [pyGUI.Text('Hardware Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-L_HARDWARE-'), pyGUI.Text('Invalid Hardware ID', size =(15, 1), enable_events=True, key='-INCORRECT_HARDWARE-', visible = False)],
        [pyGUI.Text('Software Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-L_SOFTWARE-'), pyGUI.Text('Invalid Software ID', size =(15, 1), enable_events=True, key='-INCORRECT_SOFTWARE-', visible = False)],
        [pyGUI.Text('Link already exists', size =(15, 1), enable_events=True, key='-INVALID-', visible = False)],
        [pyGUI.Button('Submit', key='-L_SUBMIT-', bind_return_key = True)]
    ]
        
    window = reloadFrame(window, layout) 
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

def controlPanel(window):
    global account
    
    if account.accessLevel:
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display', size=(10,1)), pyGUI.Button('Create', size=(10,1))],
            [pyGUI.Button('Update',size=(10,1)), pyGUI.Button('Delete', size=(10,1))],
            [pyGUI.Button('Backup'), pyGUI.Button('Create Asset Links')],
            [pyGUI.Button('Log Out', size=(10,1))],

        ]
        
    else:
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display', size=(10,1)), pyGUI.Button('Log Out',  size=(10,1))],
        ]
            
    window = reloadFrame(window, layout)
    return window

def vulnerabilitySearch(window, hardware, software):
        global toSearch
        
        toSearch = []

        #scan through data for vulnerability keywords
        
        for i in range(0, len(hardware)):
            for j in range(len(hardware[i])):     
                if (j==13):
                    if (hardware[i][j] != ""):
                       toSearch.append(hardware[i][j])
                       
        for i in range(0, len(software)):
            for j in range(len(software[i])):     
                if (j==10):
                    if (software[i][j] != ""):
                       toSearch.append(software[i][j])
                   
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Button('Search entire table for vulnerabilities')],
            [pyGUI.Button('Submit', key='-S_ASSET_ID_SUBMIT-', visible=False)],
        ]
        
        window = reloadFrame(window, layout)
        return window
    
def verifyLogin(window, username, password):

    global account

    account.verify(username, password)
    

    if (account.accessLevel !=""):           #if access exists
        window = controlPanel(window)   #show control panel
    else:
        window.Element('-INCORRECT_LOGIN-').Update(visible=True)

    return account, window


    
def createItem(window):

    assetType = [
            [pyGUI.Text('Select an Asset Type', font = 'ANY 12')],
            [pyGUI.Text('Asset Type', size = (15, 1)), pyGUI.Combo(values=['Hardware', 'Software'], size=(43, 1), readonly=True, key='-C_CHOICE-', enable_events=True)],
            [pyGUI.Button('Return to Operations')],
    ]
    
    hardware = [
            [pyGUI.Text('Hardware Creation', font = 'ANY 14', key='-CREATE_HARDWARE-')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_NAME-',  disabled=True)],
            [pyGUI.Text('Device Type', size = (15, 1)), pyGUI.Combo(values=['Portable', 'Mobile', 'Network', 'Non-Computing', 'IOT', 'Other'], size=(43, 1), readonly=True, key='-C_TYPE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_DESCRIPTION-', enable_events=True, disabled=True)],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MODEL-', disabled=True)],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MANU-', disabled=True)],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_INTERNAL_ID-', disabled=True)],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_MAC-', disabled=True), pyGUI.Text('Invalid MAC', text_color='red', key='-C_INVALID_MAC-', visible= False, enable_events=True)],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_IP-', disabled=True), pyGUI.Text('Invalid IP', text_color='red', key='-C_INVALID_IP-', visible= False, enable_events=True)],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_LOC-', disabled=True)],
            [pyGUI.Text('Buy Date', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_DATE-', disabled=True)],
            [pyGUI.CalendarButton('Calendar', key='-CAL_BUTTON-', target='-CAL-', pad=None, button_color=('black'), format=('%d-%m-%y'), disabled=True)],
            [pyGUI.Text('Warranty Information', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_WARRANTY-', enable_events=True, disabled=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_NOTES-', enable_events=True, disabled=True)],
            [pyGUI.Text('NIST Keywords ', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), key='-C_KEYWORDS-', enable_events=True, disabled=True)],
            [pyGUI.Button('Create Hardware', bind_return_key = True, disabled=True)],
            [pyGUI.In(key='-CAL-', enable_events=True, visible=False, disabled=True)],
    ]

    software = [
            [pyGUI.Text('Software Creation', font = 'ANY 14', key='-CREATE_SOFTWARE-')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_NAME_SOFTWARE-', disabled=True)],
            [pyGUI.Text('Type', size = (15, 1)), pyGUI.Combo(values=['Application', 'System', 'Firmware', 'Programming', 'Driver', 'Other'], size=(43, 1), readonly=True, key='-C_TYPE_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_DESCRIPTION_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Version', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_VERSION-', disabled=True)],
            [pyGUI.Text('Developer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_DEVELOPER-', disabled=True)],
            [pyGUI.Text('License', size = (15, 1)), pyGUI.Combo(values=['Public domain', 'Permissive', 'Copyleft', 'Non-commercial', 'Proprietary', 'Other'], size=(43, 1), readonly=True, key='-C_LICENSE-', enable_events=True, disabled=True)],
            [pyGUI.Text('License Key ', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_LICENSE_KEY-', disabled=True)],
            [pyGUI.Text('Buy Date', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_DATE_SOFTWARE-', disabled=True)],
            [pyGUI.CalendarButton('Calendar', key='-CAL_BUTTON_SOFTWARE-', target='-CAL_SOFTWARE-', pad=None, button_color=('black'), format=('%d-%m-%y'), disabled=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-C_NOTES_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Text('NIST Keywords ', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), key='-C_KEYWORDS_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Button('Create Software', bind_return_key = True, disabled=True)],
            [pyGUI.In(key='-CAL_SOFTWARE-', enable_events=True, visible=False, disabled=True)],
    ]

    x, y = getCenterScreen()
    
    col1 = x/5
    col2 = x/3 + 50
    
    layout = [
        [
            pyGUI.Column(assetType, scrollable=True,  size=(col1,y-200), vertical_scroll_only=False),
            pyGUI.Column(hardware, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
            pyGUI.Column(software, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
        ]
    ]
        

    
    window = reloadFrame(window, layout)
    return window

def deleteItem(window):
        
    assetType = [
            [pyGUI.Text('Select an Asset Type', font = 'ANY 12')],
            [pyGUI.Text('Asset Type', size = (15, 1)), pyGUI.Combo(values=['Hardware', 'Software'], size=(43, 1), readonly=True, key='-D_CHOICE-', enable_events=True)],
            [pyGUI.Button('Return to Operations')],
    ]
    
    hardware = [
            [pyGUI.Text('Hardware Delete', font = 'ANY 14', key='-DELETE_HARDWARE-')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-D_ID-',  disabled=True)],
            [pyGUI.Text('Invalid Asset ID', size =(15, 1), text_color='red', key='-D_INVALID-', enable_events=True, visible = False)],
            [pyGUI.Button('Delete Hardware', disabled=True)],
    ]

    software = [
            [pyGUI.Text('Software Delete', font = 'ANY 14', key='-DELETE_SOFTWARE-')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-D_ID_SOFTWARE-',  disabled=True)],
            [pyGUI.Text('Invalid Asset ID', size =(15, 1),text_color='red', key='-D_INVALID_SOFTWARE-', enable_events=True, visible = False)],
            [pyGUI.Button('Delete Software', disabled=True)],
    ]

    x, y = getCenterScreen()
    col1 = x/5
    col2 = x/3 + 50
    
    layout = [
        [
            pyGUI.Column(assetType, scrollable=True,  size=(col1,y-200), vertical_scroll_only=False),
            pyGUI.Column(hardware, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
            pyGUI.Column(software, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
        ]
    ]
        

    
    window = reloadFrame(window, layout)
    return window


def updateItem(window):
    
    
    assetType = [
            [pyGUI.Text('Select an Asset Type', font = 'ANY 12')],
            [pyGUI.Text('Asset Type', size = (15, 1)), pyGUI.Combo(values=['Hardware', 'Software'], size=(43, 1), readonly=True, key='-U_CHOICE-', enable_events=True)],
            [pyGUI.Button('Return to Operations')],
    ]
    
    hardware = [
            [pyGUI.Text('Hardware Creation', font = 'ANY 14', key='-UPDATE_HARDWARE-')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_ID-', disabled=True), pyGUI.Button('Find Asset', key='-U_FIND-', disabled= True, visible = True)],
            [pyGUI.Text('Invalid ID', font = 'ANY 14', key='-U_INVALID-', visible= False, enable_events=True, text_color = 'red')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_NAME-',disabled=True)],
            [pyGUI.Text('Device Type', size = (15, 1)), pyGUI.Combo(values=['Portable', 'Mobile', 'Network', 'Non-Computing', 'IOT', 'Other'], size=(43, 1), readonly=True, key='-U_TYPE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_DESC-', disabled=True, enable_events=True)],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MODEL-', disabled=True)],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MANU-', disabled=True)],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_INTERNAL_ID-', disabled=True)],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_MAC-', disabled=True), pyGUI.Text('Invalid MAC', text_color='red', key='-U_INVALID_MAC-', visible= False, enable_events=True)],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_IP-', disabled=True), pyGUI.Text('Invalid IP', text_color='red', key='-U_INVALID_IP-', visible= False, enable_events=True)],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_LOC-', disabled=True)],
            [pyGUI.Text('Buy Date', size =(15, 1)), pyGUI.InputText(enable_events=True, disabled=True, key='-U_DATE-')],
            [pyGUI.CalendarButton('Calendar', target='-U_CAL-', key='-CAL_BUTTON-', pad=None, disabled=True, button_color=('black'), format=('%d-%m-%y'))],
            [pyGUI.Text('Warranty Information', size = (15, 1)), pyGUI.Multiline(size=(43, 5), disabled=True, key='-U_WARRANTY-', enable_events=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_NOTES-', disabled=True, enable_events=True)],
            [pyGUI.Text('NIST Keywords ', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), disabled=True,key='-U_KEYWORDS-', enable_events=True)],
            [pyGUI.Button('Update Asset', key='-U_UPDATE-', visible = False)],
            [pyGUI.In(key='-U_CAL-', enable_events=True, visible=False)], 
    ]

    software = [
            [pyGUI.Text('Software Creation', font = 'ANY 14', key='-SOFTWARE_HARDWARE-')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_ID_SOFTWARE-', disabled=True), pyGUI.Button('Find Asset', key='-U_FIND_SOFTWARE-', disabled= True,visible = True)],
            [pyGUI.Text('Invalid ID', text_color = 'red', font = 'ANY 14', key='-U_INVALID_SOFTWARE-', visible= False, enable_events=True)],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_NAME_SOFTWARE-',disabled=True)],
            [pyGUI.Text('Type', size = (15, 1)), pyGUI.Combo(values=['Application', 'System', 'Firmware', 'Programming', 'Driver', 'Other'], size=(43, 1), readonly=True, key='-U_TYPE_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Text('Description', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_DESCRIPTION_SOFTWARE-', disabled=True, enable_events=True)],
            [pyGUI.Text('Version', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_VERSION-', disabled=True)],
            [pyGUI.Text('Developer', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_DEVELOPER-', disabled=True)],
            [pyGUI.Text('License', size = (15, 1)), pyGUI.Combo(values=['Public domain', 'Permissive', 'Copyleft', 'Non-commercial', 'Proprietary', 'Other'], size=(43, 1), readonly=True, key='-U_LICENSE-', enable_events=True, disabled=True)],
            [pyGUI.Text('License Key ', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_LICENSE_KEY-', disabled=True)],
            [pyGUI.Text('Buy Date', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-U_DATE_SOFTWARE-', disabled=True)],
            [pyGUI.CalendarButton('Calendar', key='-CAL_BUTTON_SOFTWARE-', target='-U_CAL_SOFTWARE-', pad=None, button_color=('black'), format=('%d-%m-%y'), disabled=True)],
            [pyGUI.Text('Notes', size = (15, 1)), pyGUI.Multiline(size=(43, 5), key='-U_NOTES_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.Text('NIST Keywords ', font = 'ANY 8', size = (20, 1)), pyGUI.Multiline(size=(43, 5), key='-U_KEYWORDS_SOFTWARE-', enable_events=True, disabled=True)],
            [pyGUI.In(key='-CAL_SOFTWARE-', enable_events=True, visible=False, disabled=True)],
            [pyGUI.Button('Update Asset', key='-U_UPDATE_SOFTWARE-', visible = False)],
            [pyGUI.In(key='-U_CAL_SOFTWARE-', enable_events=True, visible=False)], 
    ]

    x, y = getCenterScreen()

    col1 = x/5
    col2 = x/3 + 50
    
    layout = [
        [
            pyGUI.Column(assetType, scrollable=True,  size=(col1,y-200), vertical_scroll_only=False),
            pyGUI.Column(hardware, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
            pyGUI.Column(software, scrollable=True,  size=(col2,y-200), vertical_scroll_only=False),
        ]
    ]
        

    
    window = reloadFrame(window, layout)
    return window
    

def displayItems(window, assets):

    global toSearch
    
    toSearch = []

    hardwareAsset = []
    softwareAsset = []
    row = []
    
    for i in range(0, len(assets)):
        assets[i].getLinks()
        if assets[i].keyword != "":
            toSearch.append(assets[i].keyword)
        
        if assets[i].assetType == 'hardware':
            row = []
            for j in range(len(assets[i].assetData)):
                row.append(assets[i].assetData[j])
            hardwareAsset.append(row)
            
        if assets[i].assetType == 'software':
            row = []
            for j in range(len(assets[i].assetData)):
                row.append(assets[i].assetData[j])
            softwareAsset.append(row)            

            
    if not softwareAsset:
        layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Hardware Assets', font = 'ANY 14')],
            [pyGUI.Table(hardwareAsset, vertical_scroll_only = False, headings=['Asset ID', 'Name', 'Device Type', 'Description', 'Model', 'Manufacturer', 'Internal ID', 'MAC Address', 'IP Address', 'Physical Location', 'Purchase Date', 'Warranty Info', 'Notes', 'NIST Keywords', 'Links (Software ID)'])],
            [pyGUI.Button('Search entire table for vunerabilities')],
        ]
        
    if not hardwareAsset:
        layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Software Assets', font = 'ANY 14')],
            [pyGUI.Table(softwareAsset, vertical_scroll_only = False, headings=['Software ID', 'Name', 'Type', 'Description', 'Version', 'Developer', 'License', 'Key', 'Date Purchased', 'Notes', 'NIST Keywords'])],
            [pyGUI.Button('Search entire table for vunerabilities')],
        ]

    if not hardwareAsset and not softwareAsset:
        layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('No data', font = 'ANY 14')],
        ]

    if hardwareAsset and softwareAsset:
        layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Hardware Assets', font = 'ANY 14')],
            [pyGUI.Table(hardwareAsset, vertical_scroll_only = False, headings=['Asset ID', 'Name', 'Device Type', 'Description', 'Model', 'Manufacturer', 'Internal ID', 'MAC Address', 'IP Address', 'Physical Location', 'Purchase Date', 'Warranty Info', 'Notes', 'NIST Keywords', 'Links (Software ID)'])],
            [pyGUI.Text('Software Assets', font = 'ANY 14')],
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

    

    

    if os.path.exists("../nist/NIST dump.txt"):
      os.remove("../nist/NIST dump.txt")
 

    a = [
        [pyGUI.Button('Return to display')],
        [pyGUI.Text('NIST Vulnerabilities', font = 'ANY 14')],
        [pyGUI.Text('TXT dump in ../nist/NIST dump.txt', text_color="red", font = 'ANY 12')]
    ]

    for c in range(len(data)):
        a.append([pyGUI.Listbox(values=(data[c]), size=(100,10), key=dump(data[c]), horizontal_scroll=True)])

    x,y = getCenterScreen()
    
    layout = [
        [
            pyGUI.Column(a, scrollable=True,  size=(x,y-200), vertical_scroll_only=False),
        ]
    ]


            
    return layout



