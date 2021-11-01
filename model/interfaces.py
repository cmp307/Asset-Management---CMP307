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
        [pyGUI.Button('Submit', bind_return_key = True)]
    ]

    window = createWindow(layout)
    
    return window
  
    
def verifyLogin(window, username, password):


    if (userVerify(username, md5(password.encode()).hexdigest())):
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Button('Display'), pyGUI.Button('Create')],
            [pyGUI.Button('Update'), pyGUI.Button('Delete')],
            [pyGUI.Button('Backup'), pyGUI.Button('Submit')],
        ]
        window = reloadFrame(window, layout)
    else:
        layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Text('Please enter your login')],
            [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*')],
            [pyGUI.Text('Incorrect Login. Please try again!')],
            [pyGUI.Button('Submit', bind_return_key = True)],
        ]
        window = reloadFrame(window, layout)
    return window

def badLogin(window):
    layout = [
            [pyGUI.Image('scottishGlenLogo.png', background_color="grey80")],
            [pyGUI.Text('Please enter your login')],
            [pyGUI.Text('Username', size =(15, 1)), pyGUI.InputText()],
            [pyGUI.Text('Password', size =(15, 1)), pyGUI.InputText('', password_char='*')],
            [pyGUI.Text('Illegal Characters!')],
            [pyGUI.Button('Submit', bind_return_key = True)],
        ]
    window = reloadFrame(window, layout)
    return window

def inputCheck(val):
    
    if (regex.sub('[^A-Za-z0-9]+', '', val)):
        return True
    else:
        return False
