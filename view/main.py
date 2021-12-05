#import libraries
#----------------------------------
import PySimpleGUI as pyGUI      #gui 
import sys
import re as regex               #input validation
import concurrent.futures        #multi processing 
import threading                 #threading
#-----------------------------------

#allow access to other directories
#------------------------------------
sys.path.insert(1, '../model')
sys.path.insert(1, '../controller')
sys.path.insert(1, '../backups')
#------------------------------------

#import external functions
#--------------------------------------
from SQL import *
from interfaces import *
#---------------------------------------

#global variables
#---------------------------------------
loaded = False          #handles if vulnerability check finished
#---------------------------------------


def loadingFrame():
    global loaded              #handles when the loading screen is to end
    global layout
    
    #loading animation shape
    loadingGIF = b'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'


    layout = [  [pyGUI.Text('Loading....', font='ANY 15')],
                [pyGUI.Image(data=loadingGIF, key='_IMAGE_')],
            ]
    
    loadWindow = pyGUI.Window('').Layout(layout)


    while True:
        event, values = loadWindow.Read(timeout=25)
        if event in (None, 'Exit', 'Cancel'):
            break
        if (loaded):            #if loading screen over
            loadWindow.Hide()   #hide the screen
            return layout
            break
        if not (loaded):        #if not: continue animation
            loadWindow.Element('_IMAGE_').UpdateAnimation(loadingGIF,  time_between_frames=50)

    



def vunerabilityAPICall():
    global window
    global layout
    global loaded

    with concurrent.futures.ThreadPoolExecutor() as executor:   #allows returning data from multi-processing
        future = executor.submit(checkVun, window)              #run the vulnerability check
        layout = future.result()                                #fetch the window layout from the vulnerability check
        
    loaded = True                                               #end the loading screen

        
def main():
    global window
    global layout
    global loaded

    #keys for input handling
    #---------------------------------------------------------------------------
    updateAssetCapHundred = ['-U_DESC-', '-U_WARRANTY-', '-U_NOTES-']
    updateAssetCapThirty = ['-U_NAME-', '-U_MODEL-', '-U_MANU-', '-U_LOC-']

    updateSoftwareCapHundred = ['-U_DESCRIPTION_SOFTWARE-', '-U_NOTES_SOFTWARE-']
    updateSoftwareCapThirty = ['-U_NAME_SOFTWARE-', '-U_VERSION-', '-U_DEVELOPER-', '-U_LICENSE-', '-U_LICENSE_KEY-']
    
    createHardwareCapHundred = ['-C_DESCRIPTION-', '-C_WARRANTY-', '-C_NOTES-']
    createHardwareCapThirty = ['-C_NAME-', '-C_MODEL-', '-C_MANU-', '-C_LOC-']
    
    createSoftwareCapHundred = ['-C_DESCRIPTION_SOFTWARE-', '-C_NOTES_SOFTWARE-']
    createSoftwareCapThirty = ['-C_NAME_SOFTWARE-', '-C_VERSION-', '-C_DEVELOPER-', '-C_LICENSE-', '-C_LICENSE_KEY-']

    #--------------------------------------------------------------------------------
    
    #keys for value handling: when in create or update only want to access the values of either hardware or software not both
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    createHardwareKeys = ['-C_NAME-', '-C_TYPE-', '-C_DESCRIPTION-', '-C_MODEL-', '-C_MANU-','-C_INTERNAL_ID-', '-C_MAC-','-C_IP-', '-C_LOC-', '-C_DATE-', '-C_WARRANTY-', '-C_NOTES-', '-C_KEYWORDS-', '-CAL-', '-CAL_BUTTON-', 'Create Hardware']
    createSoftwareKeys = ['-C_NAME_SOFTWARE-','-C_TYPE_SOFTWARE-', '-C_DESCRIPTION_SOFTWARE-', '-C_VERSION-', '-C_DEVELOPER-', '-C_LICENSE-', '-C_LICENSE_KEY-', '-C_DATE_SOFTWARE-', '-C_NOTES_SOFTWARE-', '-C_KEYWORDS_SOFTWARE-', '-CAL_SOFTWARE-', '-CAL_BUTTON_SOFTWARE-', 'Create Software']

    updateHardwareKeys = ['-U_ID-', '-U_NAME-', '-U_TYPE-', '-U_DESC-', '-U_MODEL-','-U_MANU-', '-U_INTERNAL_ID-','-U_MAC-', '-U_IP-', '-U_LOC-', '-U_DATE-', '-U_CAL-', '-U_WARRANTY-', '-U_NOTES-', '-U_KEYWORDS-', '-CAL_BUTTON-']
    updateSoftwareKeys = ['-U_ID_SOFTWARE-', '-U_NAME_SOFTWARE-', '-U_TYPE_SOFTWARE-', '-U_DESCRIPTION_SOFTWARE-', '-U_VERSION-', '-U_DEVELOPER-', '-U_LICENSE-', '-U_LICENSE_KEY-', '-U_DATE_SOFTWARE-', '-U_NOTES_SOFTWARE-', '-U_KEYWORDS_SOFTWARE-', '-CAL_SOFTWARE-', '-CAL_BUTTON_SOFTWARE-']
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    window = init() #initialise to the login screen
    
    while True:

        # read event and value data from current window
            
        event, values = window.read()

        # close window, when exit pressed
        
        if event == pyGUI.WIN_CLOSED:
            window.close()
            break

        # operation button events: control panel, display, create, update, delete, vulnerability search , log out
        #-----------------------------------------------------------------------------------------------------------------------------
        if event == 'Return to Operations':     
            window = controlPanel(window)
        if event == 'Display':
            window = displayItems(window, getAsset('hardware'), getAsset('software'))
        if event == 'Create':
            window = createItem(window)
        if event == 'Update':
            window = updateItem(window)
        if event == 'Delete':
            window = deleteItem(window)
        if event == 'Create Asset Links':
            window = createLinks(window)
        if event == 'Log Out':
            window.close
            window = init()
        #-----------------------------------------------------------------------------------------------------------------------------




        # delete frame: input validation and submit button handling
        #----------------------------------------------------------------------------------------------------------------------------------

        #enable/disable either software or hardware depending on user drop down choice
        if event == '-D_CHOICE-':
            if values['-D_CHOICE-'] == 'Hardware':
                window['-D_ID-'].update(disabled=False)
                window['Delete Hardware'].update(disabled=False)
                window['-D_ID_SOFTWARE-'].update(disabled=True)
                window['Delete Software'].update(disabled=True)
            elif values['-D_CHOICE-'] == 'Software':
                window['-D_ID-'].update(disabled=True)
                window['Delete Hardware'].update(disabled=True)
                window['-D_ID_SOFTWARE-'].update(disabled=False)
                window['Delete Software'].update(disabled=False)



        #if asset ID input box detects change: check if last character not an integer input, remove last character accordingly

        if event == '-D_ID-':
            if len(values['-D_ID-']) > 0 and not regex.match('^[0-9]+$', values['-D_ID-'][-1]):
                window['-D_ID-'].update(values['-D_ID-'][:-1])
        if event == '-D_ID_SOFTWARE-':
            if len(values['-D_ID_SOFTWARE-']) > 0 and not regex.match('^[0-9]+$', values['-D_ID_SOFTWARE-'][-1]):
                window['-D_ID_SOFTWARE-'].update(values['-D_ID_SOFTWARE-'][:-1])

                

        #if hardware /software delete button clicked
                
        if event == 'Delete Hardware':
            result = deleteAsset('hardware', values)                                        #send delete request with input ID
            if (result):                                                                    #if successful: go to display
                window = displayItems(window, getAsset('hardware'), getAsset('software'))
            else:                                                                           #show invalid ID on screen
                window['-D_INVALID-'].update(visible=True)

        if event == 'Delete Software':
            result = deleteAsset('software', values)                                                  
            if (result):                                                                    
                window = displayItems(window, getAsset('hardware'), getAsset('software'))
            else:                                                                         
                window['-D_INVALID_SOFTWARE-'].update(visible=True)
        #----------------------------------------------------------------------------------------------------------------------------------        
            

        # update frame: input validation and button handling  
        #----------------------------------------------------------------------------------------------------------------------------------

        #enable/disable either software or hardware depending on user drop down choice
        if event == '-U_CHOICE-':
            if values['-U_CHOICE-'] == 'Hardware':
                    window['-U_ID-'].update(disabled=False)
                    window['-U_ID_SOFTWARE-'].update(disabled=True)
                    window['-U_FIND-'].update(disabled=False)
                    window['-U_FIND_SOFTWARE-'].update(disabled=True)
            elif values['-U_CHOICE-'] == 'Software':
                    window['-U_ID_SOFTWARE-'].update(disabled=False)
                    window['-U_ID-'].update(disabled=True)
                    window['-U_FIND_SOFTWARE-'].update(disabled=False)
                    window['-U_FIND-'].update(disabled=True)


        if '-U_UPDATE-' in window.AllKeysDict:
            try:
                for keys in updateAssetCapHundred:                                                                  #loop for all keys defined as having a max hundred character length
                    if event == keys:                                                                               #if input detected
                        if len(values[keys]) > 0:                                                                   #check if there is data
                            if len(values[keys]) > 100 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):    #check if greater than a hundred and if not a valid character (a-z, A-Z, 0-9, _, -)
                                window[keys].update(values[keys][:-1])                                              #remove last character
                                
                for keys in updateAssetCapThirty:                                                                   #loop for all keys defined as having a max thirty character length
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 30 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):
                                window[keys].update(values[keys][:-1])
                                
                if event == '-U_INTERNAL_ID-':                                                                          #if input id detects input
                    if len(values['-U_INTERNAL_ID-']) > 0:             
                        if len(values['-U_INTERNAL_ID-']) > 10 or not regex.match('^[a-zA-Z0-9-]+$', values['-U_INTERNAL_ID-'][-1]):   #check if greater than 10 and if not a valid character (a-z, A-Z, 0-9, -)
                            window['-U_INTERNAL_ID-'].update(values['-U_INTERNAL_ID-'][:-1])
                            
                if event == '-U_MAC-':                                                                                  #if mac detects input
                    if len(values['-U_MAC-']) > 0:
                        if len(values['-U_MAC-']) > 17 or not regex.match('^[a-zA-Z0-9:]+$', values['-U_MAC-'][-1]):    #check if greater than 17 and if not a valid character (a-z, A-Z, 0-9, -)
                            window['-U_MAC-'].update(values['-U_MAC-'][:-1])
                if event == '-U_IP-':                                                                                   #if IP detects input
                    if len(values['-U_IP-']) > 0:
                        if len(values['-U_IP-']) > 12 or not regex.match('^[0-9.]+$', values['-U_IP-'][-1]):            #check if greater than 12 and if not a valid character (0-9, .)
                            window['-U_IP-'].update(values['-U_IP-'][:-1])
                if event == '-U_CAL-':                                                                                  #update date input box with calendar input 
                    window['-U_DATE-'].update(values['-U_CAL-'])
                if event == '-U_KEYWORDS-':                                                                             #if keywords detects input                                                                    
                    if len(values['-U_KEYWORDS-']) > 0:
                        if not regex.match('^[a-zA-Z0-9]+$', values['-U_KEYWORDS-'][-1]):                              #if not a valid character (a-z, A-Z, 0-9, comma)
                            window['-U_KEYWORDS-'].update(values['-U_KEYWORDS-'][:-1])
            
            except:
                print('hardware validation error')

        if '-U_UPDATE_SOFTWARE-' in window.AllKeysDict:         #same process as hardware using applicable software keys
                for keys in updateSoftwareCapHundred:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 100 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):  
                                window[keys].update(values[keys][:-1])
                for keys in updateSoftwareCapThirty:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 30 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):
                                window[keys].update(values[keys][:-1])
                if event == '-CAL_BUTTON_SOFTWARE-':
                    window['-U_DATE_SOFTWARE-'].update(values['-CAL_BUTTON_SOFTWARE-'])
                if event == '-U_KEYWORDS_SOFTWARE-':
                    if len(values['-U_KEYWORDS_SOFTWARE-']) > 0:
                        if not regex.match('^[a-zA-Z0-9]+$', values['-U_KEYWORDS_SOFTWARE-'][-1]):
                            window['-U_KEYWORDS_SOFTWARE-'].update(values['-U_KEYWORDS_SOFTWARE-'][:-1])
            

        if event == '-U_FIND-':         #same process as hardware using applicable software keys
            if len(values['-U_ID-']) > 0:
                if regex.match('^[0-9]+$', values['-U_ID-'][-1]):
                    data = getAssetWhere('hardware', values['-U_ID-'])                              #get all where SQL search with input ID
                    if data:                                                                        #if record found
                        window['-U_INVALID-'].update(visible=False)                                     #disabled the id field
                        window['-U_ID-'].update(disabled=False)                                     #disabled the id field
                        window['-CAL_BUTTON-'].update(disabled=True)                                #enable calendar
                        window['-CAL_BUTTON_SOFTWARE-'].update(disabled=False)                      
                        
                        i = 0
                        
                        for keys in updateHardwareKeys:                                             #enable all hardware inputs
                                if keys != '-CAL_BUTTON-' and keys !='-U_CAL-':                 
                                    window[keys].update(data[0][i], visible=True, disabled=False)
                                    i+=1
                                else:
                                    window[keys].update(disabled=False)
                                    
                        window['-U_FIND-'].update(visible=False)                                    #disable asset find
                        window['-U_UPDATE-'].update(visible=True)                                   #enable update button
                    else:
                       window['-U_INVALID-'].update(visible = True)
                                    

                   
        if event == '-U_FIND_SOFTWARE-':            #same as hardware with applicabled software fields
            
            if len(values['-U_ID_SOFTWARE-']) > 0:
                if regex.match('^[0-9]+$', values['-U_ID_SOFTWARE-'][-1]):
                    data = getAssetWhere('software', values['-U_ID_SOFTWARE-'])
                    if data:
                        window['-U_INVALID_SOFTWARE-'].update(visible=False)                                     #disabled the id field
                        window['-U_ID_SOFTWARE-'].update(disabled=False)
                        window['-CAL_BUTTON-'].update(disabled=False)
                        window['-CAL_BUTTON_SOFTWARE-'].update(disabled=True)
                        i = 0
                        
                        for keys in updateSoftwareKeys:
                            try:
                                if keys != '-CAL_BUTTON_SOFTWARE-' and keys !='-CAL_SOFTWARE-':
                                    window[keys].update(data[0][i], visible=True, disabled=False)
                                    i+=1
                                else:
                                    window[keys].update(disabled=False)
                            except:
                                print(keys)
                        window['-U_FIND_SOFTWARE-'].update(visible=False)
                        window['-U_UPDATE_SOFTWARE-'].update(visible=True)
                                    

                    else:
                       window['-U_INVALID_SOFTWARE-'].update(visible = True)

        if event == '-U_UPDATE_SOFTWARE-':          #if software update pressed: update the applicable record with new data
            updateAsset('software', values)
            window = displayItems(window, getAsset('hardware'), getAsset('software'))   #return to display
            
                    
        if event == '-U_UPDATE-':                   #if hardware update pressed: update the applicable record with new data
            if regex.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', values['-U_IP-']):   #check valid IP
                window['-U_INVALID_IP-'].update(visible=False)
                if regex.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', values['-U_MAC-']):   #check valid IP
                    updateAsset('hardware',values)
                    window = displayItems(window, getAsset('hardware'), getAsset('software'))
                else:
                    window['-U_INVALID_MAC-'].update(visible=True)
            else:
                window['-U_INVALID_IP-'].update(visible=True)


        if event == '-U_ID-':                       #ID field validation:only allow 0-9
             if len(values['-U_ID-']) > 0:
                if not regex.match('^[0-9]+$', values['-U_ID-'][-1]):
                    window['-U_ID-'].update(values['-U_ID-'][:-1])

        if event == '-U_ID_SOFTWARE-':
             if len(values['-U_ID_SOFTWARE-']) > 0:
                if not regex.match('^[0-9]+$', values['-U_ID_SOFTWARE-'][-1]):
                    window['-U_ID_SOFTWARE-'].update(values['-U_ID_SOFTWARE-'][:-1])
                    
        #------------------------------------------------------------------------------------------


                    
        # create frame: asset type handling, asset input validation
        #------------------------------------------------------------------------------------------

        if event == '-C_CHOICE-':
            if values['-C_CHOICE-'] == 'Hardware':
                for keys in createHardwareKeys:
                    window[keys].update(disabled=False)
                for keys in createSoftwareKeys:
                    window[keys].update(disabled=True)
            elif values['-C_CHOICE-'] == 'Software':
                for keys in createSoftwareKeys:
                    window[keys].update(disabled=False)
                for keys in createHardwareKeys:
                    window[keys].update(disabled=True)

  
            window['-C_DATE-'].update(disabled=True)
            window['-C_DATE_SOFTWARE-'].update(disabled=True)

                
        if event == 'Create Hardware':
            if values['-C_NAME-'] !="":
                if regex.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', values['-C_IP-']):   #check valid IP
                    window['-C_INVALID_IP-'].update(visible=False)
                    if regex.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', values['-C_MAC-']):   #check valid IP
                       createAsset('hardware', values)
                       window = displayItems(window, getAsset('hardware'), getAsset('software'))
                    else:
                       window['-C_INVALID_MAC-'].update(visible=True)
                else:
                       window['-C_INVALID_IP-'].update(visible=True)
                

        if event == 'Create Software':
            if values['-C_NAME_SOFTWARE-'] !="":
               createAsset('software', values)
               window = displayItems(window, getAsset('hardware'), getAsset('software'))
            
        if '-CREATE_HARDWARE-' in window.AllKeysDict:
            try:
                for keys in createHardwareCapHundred:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 100 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):
                                window[keys].update(values[keys][:-1])
                for keys in createHardwareCapThirty:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 30 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):
                                window[keys].update(values[keys][:-1])
                if event == '-C_INTERNAL_ID-':
                    if len(values['-C_INTERNAL_ID-']) > 0:
                        if len(values['-C_INTERNAL_ID-']) > 10 or not regex.match('^[a-zA-Z0-9_-]+$', values['-C_INTERNAL_ID-'][-1]):
                            window['-C_INTERNAL_ID-'].update(values['-C_INTERNAL_ID-'][:-1])
                if event == '-C_MAC-':
                    if len(values['-C_MAC-']) > 0:
                        if len(values['-C_MAC-']) > 17 or not regex.match('^[a-zA-Z0-9:-]+$', values['-C_MAC-'][-1]):
                            window['-C_MAC-'].update(values['-C_MAC-'][:-1])
                if event == '-C_IP-':
                    if len(values['-C_IP-']) > 0:
                        if len(values['-C_IP-']) > 12 or not regex.match('^[0-9.]+$', values['-C_IP-'][-1]):
                            window['-C_IP-'].update(values['-C_IP-'][:-1])
                if event == '-CAL-':
                    window['-C_DATE-'].update(values['-CAL-'])
                if event == '-C_KEYWORDS-':
                    if len(values['-C_KEYWORDS-']) > 0:
                        if not regex.match('^[a-zA-Z0-9]+$', values['-C_KEYWORDS-'][-1]):
                            window['-C_KEYWORDS-'].update(values['-C_KEYWORDS-'][:-1])
            except:
                pass

        if '-CREATE_SOFTWARE-' in window.AllKeysDict:
            
                for keys in createSoftwareCapHundred:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 100 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):  
                                window[keys].update(values[keys][:-1])
                for keys in createSoftwareCapThirty:
                    if event == keys:
                        if len(values[keys]) > 0:
                            if len(values[keys]) > 30 or not regex.match('^[a-zA-Z0-9_-]+$', values[keys][-1]):
                                window[keys].update(values[keys][:-1])
                if event == '-CAL_SOFTWARE-':
                    window['-C_DATE_SOFTWARE-'].update(values['-CAL_SOFTWARE-'])
                if event == '-C_KEYWORDS_SOFTWARE-':
                    if len(values['-C_KEYWORDS_SOFTWARE-']) > 0:
                        if not regex.match('^[a-zA-Z0-9]+$', values['-C_KEYWORDS_SOFTWARE-'][-1]):
                            window['-C_KEYWORDS_SOFTWARE-'].update(values['-C_KEYWORDS_SOFTWARE-'][:-1])
            
                


    #------------------------------------------------------------------------------------------------            
                
        if event == 'Search entire table for vunerabilities':
        
            a = threading.Thread(target=vunerabilityAPICall).start()
            window = reloadFrame(window, loadingFrame())

        if event == 'S_ASSET_ID_INPUT':
             if len(values['-S_ASSET_ID_INPUT-']) > 0:
                if not regex.match('^[0-9]+$', values['-S_ASSET_ID_INPUT-'][-1]):
                    window['-S_ASSET_ID_INPUT-'].update(values['-S_ASSET_ID_INPUT-'][:-1])
            
        
        if event == 'Backup':
            backup(getAsset('hardware'), getAsset('software'))
                   
        if event == 'Return to display':

            loaded = False
            window = displayItems(window, getAsset('hardware'), getAsset('software'))

        initCapTen = ['-USERNAME-', '-PASSWORD-']

        if '-INIT-' in window.AllKeysDict:
            for keys in initCapTen:
                if event == keys:
                    if len(values[keys]) > 0:
                        if len(values[keys]) > 10 or not regex.match('^[a-zA-Z0-9_]+$', values[keys][-1]):
                            window[keys].update(values[keys][:-1])         

        
        if event == '-LOGIN-':                                              #if login button is pressed
            if len(values['-USERNAME-']) and len(values['-PASSWORD-']) > 0:                     #check not empty
                loginResult = verifyLogin(window, values['-USERNAME-'], values['-PASSWORD-'])   #validate login
                if (loginResult != window):                                 #updateAsset window accordingly
                    window = loginResult
                    
    #asset linking: validation and button handling
    #------------------------------------------------------------------------------------------------------------

        if event == '-L_SUBMIT-':
            window['-INVALID-'].update(visible=False)
            
            hardware_id = getAssetWhere('hardware', values['-L_HARDWARE-'])
            software_id = getAssetWhere('software', values['-L_SOFTWARE-'])
            
            if hardware_id:
                window['-INCORRECT_HARDWARE-'].update(visible=False)
            elif not hardware_id:
                window['-INCORRECT_HARDWARE-'].update(visible=True)

            if software_id:
                window['-INCORRECT_SOFTWARE-'].update(visible=False)
            elif not software_id:
                window['-INCORRECT_SOFTWARE-'].update(visible=True)
                
            if hardware_id and software_id:
                if not assetSelectWhere(values):
                    assetLink(values)
                    window = displayItems(window, getAsset('hardware'), getAsset('software'))
                else:
                    window['-INVALID-'].update(visible=True)
                    

        if event == '-L_HARDWARE-':
            if len(values['-L_HARDWARE-']) > 0:
                if not regex.match('^[0-9]+$', values['-L_HARDWARE-'][-1]):
                    window['-L_HARDWARE-'].update(values['-L_HARDWARE-'][:-1])
                    
        if event == '-L_SOFTWARE-':
            if len(values['-L_SOFTWARE-']) > 0:
                if not regex.match('^[0-9]+$', values['-L_SOFTWARE-'][-1]):
                    window['-L_SOFTWARE-'].update(values['-L_SOFTWARE-'][:-1])

            
    #------------------------------------------------------------------------------------------------------------

main()

