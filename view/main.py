import PySimpleGUI as pyGUI
import sys

sys.path.insert(1, '../model')
sys.path.insert(1, '../controller')

from interfaces import badLogin, inputCheck, reloadFrame, createWindow, verifyLogin, init


def main():
    global window
    window = init()
    
    while True:
        event, values = window.read()
        
        if event == pyGUI.WIN_CLOSED:
            window.close()
            break 
        if event == 'Submit':
            if (inputCheck(values[1])):
                window = verifyLogin(window, values[1],values[2])
            else:
                window = badLogin(window)
                
main()

