import PySimpleGUI as pyGUI
from ctypes import windll
from math import floor
from connection import connectToDatabase
from SQL import userVerify
from hashlib import md5
from vunerability import *
import re as regex

def getCenterScreen():
    user32 = windll.user32
    screensize = floor(user32.GetSystemMetrics(0) / 2) * 2, floor(user32.GetSystemMetrics(1) / 2) * 2
    return screensize

def createWindow(layout):
    global windowSize

    windowSize = getCenterScreen()
    window = pyGUI.Window("Scottish Glen Database Portal", layout, size = windowSize, background_color="grey80", element_justification='c')
    return window

def reloadFrame(window, layout):

    window.close()
    window = createWindow(layout)
    return window

def individualVunSearch(val, window):
    data = []

    rowCount, desc, rating = format(vunerabilitySearch(val.replace(" ", "+")))
    row = []
    ratingValue = []
        
    if rowCount > 0:
        row.append(val + ' ' + 'has ' + str(rowCount) + ' vunerabilities')
            
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

    layout = [
        [pyGUI.Button('Create the Asset')],
        [pyGUI.Button('Discard the Asset')],
    ]

    for c in range(len(data)):
        layout.append([pyGUI.Listbox(values=(data[c]), size=(100,10), horizontal_scroll=True)])
   
    return layout
    
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
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display'), pyGUI.Button('Create')],
            [pyGUI.Button('Update'), pyGUI.Button('Delete')],
            [pyGUI.Button('Backup')],
        ]
        window = reloadFrame(window, layout)
        return window


    
def verifyLogin(window, username, password):


    if (userVerify(username, md5(password.encode()).hexdigest())):
        window = crudControls(window)
    else:
        window.Element('-INCORRECT_LOGIN-').Update(visible=True)
        
    return window
    
def createItem(window):
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Creation', key='-CREATION-')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_NAME-')],
            [pyGUI.Text('Device Type', size = (15, 1)), pyGUI.Combo(values=['Network', 'Physical'], size=(43, 1), readonly=True, key='-C_TYPE-', enable_events=True)],
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
            [pyGUI.Text('NIST Keywords', size =(15, 1)), pyGUI.InputText(enable_events=True, key='-C_KEYWORDS-')],
            [pyGUI.Button('Create Asset', bind_return_key = True)],
        ]
    
    window = reloadFrame(window, layout)
    return window

def deleteItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Delete')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Button('Delete Asset', bind_return_key = True)],
        ]
    window = reloadFrame(window, layout)
    return window


def updateItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Update')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Device Type', size =(15, 1)), pyGUI.InputText('Insert Asset ID',disabled=True)],
            [pyGUI.Text('Description', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Purchase Date', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Warranty Information', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Text('Notes', size =(15, 1)), pyGUI.InputText('Insert Asset ID', disabled=True)],
            [pyGUI.Button('Find Asset')],
        ]
    window = reloadFrame(window, layout)
    return window
    
def updateItemShowData(window, vals):
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Update')],
            [pyGUI.Text('Asset ID', size =(15, 1)), pyGUI.InputText(vals[0][0], disabled=True)],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText(vals[0][1])],
            [pyGUI.Text('Device Type', size =(15, 1)), pyGUI.InputText(vals[0][2])],
            [pyGUI.Text('Description', size =(15, 1)), pyGUI.InputText(vals[0][3])],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText(vals[0][4])],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText(vals[0][5])],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText(vals[0][6])],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText(vals[0][7])],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText(vals[0][8])],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText(vals[0][9])],
            [pyGUI.Text('Purchase Date', size =(15, 1)), pyGUI.InputText(vals[0][10])],
            [pyGUI.Text('Warranty Information', size =(15, 1)), pyGUI.InputText(vals[0][11])],
            [pyGUI.Text('Notes', size =(15, 1)), pyGUI.InputText(vals[0][12])],
            [pyGUI.Button('Update Asset')],
        ]
    window = reloadFrame(window, layout)
    return window

def displayItems(window, get):

    global toSearch
    
    data = []

    toSearch = []

    for i in range(0, len(get)):
        row = []
        for j in range(len(get[i])):
            
            if (j==3):
               toSearch.append(get[i][j])
               
            row.append(get[i][j])
        data.append(row)

    layout = [
        [pyGUI.Button('Return to Operations')],
        [pyGUI.Table(data, headings=['Asset ID', 'Name', 'Device Type', 'Description', 'Model', 'Manufacturer', 'Internal ID', 'MAC Address', 'IP Address', 'Physical Location', 'Purchase Date', 'Warranty Info', 'Notes'])],
        [pyGUI.Button('Check entire table for vunerabilities')],
    ]

    window = reloadFrame(window, layout)
    return window



def checkVun(window):
    global toSearch
    data = []

    for i in range(0, len(toSearch)):
        rowCount, desc, rating = format(vunerabilitySearch(toSearch[i].replace(" ", "+")))
        row = []
        ratingValue = []
        
        if rowCount > 0:
            row.append(toSearch[i] + ' ' + 'has ' + str(rowCount) + ' vunerabilities')
            
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


    

        

    layout = [
        [pyGUI.Button('Return to display')],
    ]

    for c in range(len(data)):
        layout.append([pyGUI.Listbox(values=(data[c]), size=(50,10), horizontal_scroll=True)])

    
    
    return layout



