import PySimpleGUI as pyGUI
import sys
import re as regex

sys.path.insert(1, '../model')
sys.path.insert(1, '../controller')

from SQL import create
from interfaces import *

def checkSpecial(val):

    i = 0
    values = []
    
    for c in val:
        values.append(val[c])
        i+=1

    i = 0

    for c in values:
        regexp = regex.compile('[^0-9a-zA-Z]+')
        if regexp.search(values[i]):
            return False
        i+=1
     
    return True
    
def main():
    global window
    window = init()
    window = crudControls(window)
    while True:
        event, values = window.read()
        
        if event == pyGUI.WIN_CLOSED:
            window.close()
            break
        if event == 'Create':
            window = createItem(window)
        if event == 'Display':
            window = displayItems(window)
        if event == 'Create Asset':
            for c in values:
                if values[c] != '':
                   if not (checkSpecial(values)):
                        window = badCreateItem(window)
                        break
                   else:
                        create(values)
                        window = crudControls(window)
                        break
                else:
                    window = badCreateItem(window)
                    break
                    
                    
                
        if event == 'Login':
            if (checkSpecial(values)):
                window = verifyLogin(window, values[1],values[2])
            else:
                window = badLogin(window)
                
main()

