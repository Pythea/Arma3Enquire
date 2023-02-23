import os
import enquiries as enq
import modXML
import steamEnq

FileXT = '"-servermod=steamapps/workshop/content/107410/2162811561;"'

class Settings:
    def __init__(self):
        self.INSTALL_DIR = modXML.getInstallDir()
        self.STEAM_ACCOUNT = modXML.getSteamAccount()
        self.COLLECTION_ID = modXML.getCollectionID()
        self.SCRIPT_LOCATION = modXML.getScriptLocation()

def start():

    mainOptions = ['Download Mods',"Preset Management", 'Misc Options', 'Enquire Options', 'Debug', 'Exit']
    response = enq.choose("What would you like to do?", mainOptions)

    if response == 'Exit':
        exit(0)
    elif response == 'Download Mods': 
        downloadOptions() # After downloading, it will auto-set everything to lowercase, then copy keys
    elif response == "Preset Management":
        presetOptions()
    elif response == 'Misc Options':
        miscOptions()
    elif response == 'Enquire Options':
        enquireOptions()
    elif response == 'Debug':
        debugOptions()

def downloadOptions():
    options = ["Redownload All Mods", "Back"]
    downloadResponse = enq.choose("Download Options: ", options)
    if downloadResponse == "Redownload All Mods":
        if enq.confirm("Are You Sure You Want To Redownload All Mods?"):
            modIds = modXML.getModInfo()[1]
            print("Downloading all mods. This is going to take a while.\n")
            steamEnq.downloadMods(modIds)
            allFilesToLower()
            copyKeys()
            text = enq.freetext("All mods have been successfully redownloaded!")
            print(text)
            downloadOptions()
        else:
            downloadOptions()
    elif downloadResponse == "Back":
        start()


def presetOptions():
    options = ['Create Preset', 'Load Preset', 'View Preset', "Delete Preset", 'Back']
    presetResponse = enq.choose("Preset Management: ", options)
    
    if presetResponse == "Create Preset":
        modInfo = modXML.getModInfo()
        modInfo[0].append("Cancel")
        response = enq.choose("Select mods to create a new preset: ", modInfo[0], multi=True)
        if "Cancel" in response:
            presetOptions()
        selection = []
        for mod in response:
            selection.append(modInfo[1][modInfo[0].index(mod)])
        modXML.createPreset([response, selection])
        text = enq.freetext("A new preset has been created!")
        print(text)

        presetOptions() # Create a new preset from mod selection
    
    if presetResponse == "Load Preset":
        # load mods to the server from a preset in the xml file
        names = modXML.getPresets()
        names.append("Cancel")
        response = enq.choose("Select a Preset to Load: ", names)
        if response == "Cancel":
            presetOptions()
        
        ids = modXML.getPresetIds(response)
        writeToStartupScript(True, ids)        
        text = enq.freetext(f"The mods from {response} has been applied to the arma startup script!")
        print(text)
        presetOptions()
    
    elif presetResponse == "View Preset":
        # Prints a list of mod names in selected preset
        names = modXML.getPresets()
        names.append("Cancel")
        response = enq.choose("Select a preset to view: ", names)
        if response == "Cancel":
            presetOptions()

        mods = modXML.viewPreset(response)
        view = f"List of mods in {response}:\n"
        for i in mods:
            view += i + "\n"
        print(view)
        presetOptions() # Print out mods from a selected preset
    
    elif presetResponse == "Delete Preset":
        names = modXML.getPresets()
        names.append("Cancel")
        response = enq.choose("Select a preset to delete: ", names)
        if response == "Cancel":
            presetOptions()
        modXML.deletePreset(response)
        text = enq.freetext(f"The preset {response} has been deleted!")
        print(text)
        presetOptions() # Choose which preset to delete, confirmation please
    
    elif presetResponse == "Back":
        start()

def miscOptions():
    if modXML.getFileXT():
        fileXT = "Disable File XT"
    else:
        fileXT = "Enable File XT"

    options = ['Update Mod XML', fileXT, 'Set Server to 32 Bit', 'Set Server to 64 Bit', 'Back']
    miscResponse = enq.choose("Misc Options: ", options)

    if miscResponse == "Update Mod XML":
        modInfo = modXML.getInfoFromCollection()
        modXML.writeModsToTree(modInfo, True)
        text = enq.freetext("XML Data Updated From Collection!")
        print(text)
        miscOptions()

    elif miscResponse == "Disable File XT":
        modXML.setFileXT("False")
        writeToStartupScript(modChanges = False)
        print("File XT has been disabled!")
        miscOptions()
    elif miscResponse == "Enable File XT":
        modXML.setFileXT("True")
        writeToStartupScript(modChanges = False)
        print("File XT has been enabled!")
        miscOptions()
    
    elif miscResponse == 'Set Server to 32 Bit':
        modXML.setBit("32")
        writeToStartupScript(modChanges = False)
        print("Server Has Been Set to 32 Bit!")
        miscOptions()
    elif miscResponse == 'Set Server to 64 Bit':
        modXML.setBit("64")
        writeToStartupScript(modChanges = False)
        print("Server Has Been Set to 64 Bit!")
        miscOptions()

    elif miscResponse == "Back":
        start()

def enquireOptions():
    options = ['Set Steam Account', 'Set Start Script Location', 'Set Install Directory', 'Set Collection ID', 'Back']
    enquireResponse = enq.choose("Enquire Options: ", options)
    
    if enquireResponse == "Set Steam Account":
        newAccount = input("What would you like to set your account to? ")
        modXML.setSteamAccount(newAccount)
        print("Account info has been set")
        miscOptions()

    elif enquireResponse == "Set Start Script Location":
        newLocation = input("Where would you like to select ")
        modXML.setScriptLocation(newLocation)
        miscOptions()
    
    elif enquireResponse == "Set Install Directory":
        newInstall = input("Select the location for game files: ")

    elif enquireResponse == "Set Collection ID":
        newID = input("Please enter the steam workshop collection ID: ")
        modXML.setColletionID(newID)
        miscOptions()

    elif enquireResponse == "Back":
        start()

def debugOptions():
    options = ["Get Steam Account", "Get Game Files Base Dir", "Back"]
    debugResponse = enq.choose("Debug Options: ", options)
    if debugResponse == "Get Steam Account":
        print(modXML.getSteamAccount())
        debugOptions()
    if debugResponse == "Get Game Files Base Dir":
        print()
        debugOptions()
    elif debugResponse == "Back":
        start()

def copyKeys():
    #Copies the .bikeys from the mod directories to the arma base directory
    basedir = f"{settings.INSTALL_DIR}/steamapps/workshop/content/107410/"

    mods = os.listdir(basedir)
    keys = []
    fullPath = []

    for i in mods:
        try:
            keys.append(os.listdir(basedir+f'{i}/keys')[0])
            fullPath.append(basedir+f'{i}/keys/{keys[-1]}')
        except FileNotFoundError:
            print(f"Keys directory not found for mod id {i}, skipping")


    for i in range(len(keys)):
        cmd = f"cp {fullPath[i]} {settings.INSTALL_DIR}/keys/{keys[i]}"
        os.system(cmd)
        print(f"Copied {keys[i]}...")


def allFilesToLower():
    # Runs a shell script which sets all filenames in the mod directory to lowercase
    print("\nSetting all files to lowercase, this is going to take a while")
    baseCMD = f"find {settings.INSTALL_DIR}"
    cmd = baseCMD + "/steamapps/workshop/content/107410/ -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;"
    os.system(cmd)


def writeToStartupScript(modChanges=False, mods=[]):
    #Gets sent a list of mods, and applies them to the startup script based on settings
    FileXT = ' "-servermod=steamapps/workshop/content/107410/2162811561;" '
    modBase = "steamapps/workshop/content/107410/"

    if not modXML.getFileXT():
                FileXT = " "
    Bit = modXML.getAndProcBit()
    
    if not modChanges:
        #Reads the start script first before opening as write
        with open(f"{settings.SCRIPT_LOCATION}/arma3.sh", 'r') as file:
            fileSplit = file.readlines()
        mods = fileSplit[2].split('"-mod=')[1]


    with open(f"{settings.SCRIPT_LOCATION}/arma3.sh",'w') as file:
        #Opens the start script as write and truncats the file before applying updates
        file.write("#!/bin/bash\n")
        file.write(f"cd {settings.INSTALL_DIR}\n")

        lastWrite = f'screen -A -m -d -S arma3 ./arma3server{Bit} -profiles={settings.INSTALL_DIR}/profiles -config=server.cfg -name=custom{FileXT}"-mod=' 
        
        if modChanges:
            for mod in mods:
                lastWrite +=  modBase + mod + ";" 
        else:
           lastWrite += mods
        lastWrite += '"'

        file.write(lastWrite)


if __name__ == "__main__":
    settings = Settings()
    
    print(""" _____                  _          
|  ___|                (_)         
| |__ _ __   __ _ _   _ _ _ __ ___ 
|  __| '_ \ / _` | | | | | '__/ _ \\
| |__| | | | (_| | |_| | | | |  __/
\____/_| |_|\__, |\__,_|_|_|  \___|
               | |                 
               |_|                 """)
    start()