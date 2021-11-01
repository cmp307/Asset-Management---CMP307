import PySimpleGUI as pyGUI
from ctypes import windll
from math import floor
from connection import connectToDatabase
from SQL import userVerify
from hashlib import md5
import re as regex

def getCenterScreen():
    user32 = windll.user32
    screensize = floor(user32.GetSystemMetrics(0) / 2), floor(user32.GetSystemMetrics(1) / 2)
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
            [pyGUI.Button('Backup'), pyGUI.Button('Submit')],
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

def displayItems(window):
    
    layout = [
            [pyGUI.Text('Asset Display')],
        ]
    window = reloadFrame(window, layout)
    return window

def badCreateItem(window):
    
    layout = [
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

