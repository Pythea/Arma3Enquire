from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import requests
import modXML

def getInfoFromCollection():
    # Downloads mod names and workshop ids from collection
    COLLECTION_ID = modXML.getCollectionID()
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={COLLECTION_ID}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    items = soup.find_all("div", {"class":"collectionItemDetails"})
    modNames = soup.find_all("div", {"class":"workshopItemTitle"})
    modNames.pop(0) # first element is title of collection, not needed here
    modIds = []

    for item in items:
        modIds.append(item.find('a')['href'].split("?id=")[1])

    modInfo = zip(modNames, modIds)
    return modInfo

def writeModsToTree(modInfo, overwrite=False):
    if overwrite:
        #removes all previous mod information in data.xml, while keeping everything after presets
        with open("data.xml", 'r+') as file:
            data = file.read()
            presets = data.split("<presets>")[1]
            file.seek(0)
            file.write(f"<root><mods></mods><presets>{presets}")
            file.truncate()
    
    # Write mods names and ids to xml file
    tree = ET.parse('data.xml')
    root = tree.getroot()
    mods = ElementTree.Element("mods")
    mods.clear()

    for name, id in modInfo:
        mod = ElementTree.Element("mod")
        mod.set("name", name.text)
        modId = ElementTree.Element("id")
        modId.set('id', id)
        mod.append(modId)
        root[0].append(mod)

    tree.write("data.xml")

def getModInfo():
    # Gets mod names and ids from xml file
    names = []
    ids = []
    root = ET.parse('data.xml').getroot()
    for mod in root.find('mods'):
        names.append(mod.attrib['name'])
        ids.append(mod[0].attrib['id'])
    modInfo = [names, ids]
    return modInfo

def createPreset(selection):
    # creates a new modlist preset based on selection
    presetName = input("Enter name of preset: ")
    tree = ET.parse("data.xml")
    root = tree.getroot()
    preset = ElementTree.Element("preset")
    preset.set("name", presetName)
    presets = root.find('presets')
    presets.append(preset)

    for i in range(len(selection[0])):
        mod = ElementTree.Element("mod")
        mod.set("name", selection[0][i])
        modId = ElementTree.Element("id")
        modId.set('id', selection[1][i])
        mod.append(modId)
        preset.append(mod)

    tree.write("data.xml")
    pass

def viewPreset(preset):
    root = ET.parse("data.xml").getroot()
    search = root.find(f"./presets/*[@name='{preset}']")
    mods = []
    for mod in search:
        mods.append(mod.attrib['name'])
    return mods

def getPresetIds(preset):
    root = ET.parse("data.xml").getroot()
    search = root.find(f"./presets/*[@name='{preset}']")
    ids = []
    for mod in search:
        ids.append(mod[0].attrib['id'])
    return ids

def getPresets():
    root = ET.parse("data.xml").getroot()
    presets = root.find('presets')
    names = []
    for preset in presets:
        names.append(preset.attrib['name'])
    return names

def deletePreset(preset):
    tree = ET.parse("data.xml")
    root = tree.getroot()
    search = root.find(f"./presets/*[@name='{preset}']")
    presets = root.find("presets")
    presets.remove(search)
    tree.write("data.xml")


def setSteamAccount(newAccount):
    tree = ET.parse("data.xml")
    root = tree.getroot()
    account = root.find('options/account')
    account.text = newAccount
    tree.write('data.xml')

def getSteamAccount():
    root = ET.parse("data.xml").getroot()
    account = root.find('options/account')
    return account.text

def getInstallDir():
    root = ET.parse("data.xml").getroot()
    gameFiles = root.find('options/gameFiles')
    return gameFiles.text

def getCollectionID():
    root = ET.parse("data.xml").getroot()
    collectionID = root.find('options/collectionID')
    return collectionID.text

def setColletionID(newID):
    tree = ET.parse("data.xml")
    root = tree.getroot()
    collectionID = root.find('options/collectionID')
    collectionID.text = newID
    tree.write('data.xml')

def getScriptLocation():
    root = ET.parse("data.xml").getroot()
    scriptLocation = root.find('options/scriptLocation')
    return scriptLocation.text

def setScriptLocation(newLocation):
    tree = ET.parse("data.xml")
    root = tree.getroot()
    scriptLocation = root.find('options/ScriptLocation')
    scriptLocation.text = newLocation
    tree.write('data.xml')