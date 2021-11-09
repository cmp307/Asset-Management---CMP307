import PySimpleGUI as pyGUI
from ctypes import windll
from math import floor
from connection import connectToDatabase
from SQL import userVerify
from hashlib import md5
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



def init():
    
    layout = [
        [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
        [pyGUI.Text('Please enter your login')],
        [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText()],
        [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*')],
        [pyGUI.Button('Login', bind_return_key = True)]
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

def incorrectLogin(window):
    layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Text('Please enter your login')],
            [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*')],
            [pyGUI.Text('Incorrect Login. Please try again!')],
            [pyGUI.Button('Login', bind_return_key = True)],
        ]
    window = reloadFrame(window, layout)
    return window

    
def verifyLogin(window, username, password):


    if (userVerify(username, md5(password.encode()).hexdigest())):
        window = crudControls(window)
    else:
        window = incorrectLogin(window)
    return window
    
def badLogin(window):
    layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Text('Please enter your login')],
            [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*')],
            [pyGUI.Text('Invalid Input')],
            [pyGUI.Button('Login', bind_return_key = True)],
        ]
    window = reloadFrame(window, layout)
    return window

def createItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Creation')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Device Type', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Description', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Purchase Date', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Warranty Information', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Notes', size =(15, 1)), pyGUI.InputText()],
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
    
    data = []

    for i in range(0, len(get)):
        row = []
        for j in range(len(get[i])):
            row.append(get[i][j])
        data.append(row)
    
    layout = [
        [pyGUI.Button('Return to Operations')],
        [pyGUI.Table(data, headings=['Asset ID', 'Name', 'Device Type', 'Description', 'Model', 'Manufacturer', 'Internal ID', 'MAC Address', 'IP Address', 'Physical Location', 'Purchase Date', 'Warranty Info', 'Notes'])],
    ]
   
    window = reloadFrame(window, layout)
    return window

def badCreateItem(window):
    
    layout = [
            [pyGUI.Button('Return to Operations')],
            [pyGUI.Text('Asset Creation')],
            [pyGUI.Text('Asset Name', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Device Type', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Description', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Model', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Manufacturer', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Internal ID', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('MAC Address', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('IP Address', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Physical Location', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Purchase Date', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Warranty Information', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Notes', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Button('Create Asset', bind_return_key = True)],
            [pyGUI.Text('Invalid Input!', size =(15, 1))],
        ]
    window = reloadFrame(window, layout)
    return window

