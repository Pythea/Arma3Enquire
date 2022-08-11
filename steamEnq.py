import requests
from bs4 import BeautifulSoup
import os
import modXML

def getWorkshopIdsFromCollection(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    items = soup.find_all("div", {"class":"collectionItemDetails"})
    temp = []

    for item in items:
        temp.append(item.find('a')['href'].split("?id=")[1])
    return temp

def downloadMods(workshopIds):
    STEAM_ACCOUNT = modXML.getSteamAccount()
    INSTALL_DIR = modXML.getInstallDir()
    cmd = f"steamcmd +force_install_dir {INSTALL_DIR} +login {STEAM_ACCOUNT}"
    for i in workshopIds:
        cmd += f" +workshop_download_item 107410 {i}"
    cmd += " +quit"
    os.system(cmd)