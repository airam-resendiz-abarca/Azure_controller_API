from time import sleep
import requests
from requests.auth import HTTPBasicAuth
from decouple import config

import sys 

ORGANIZATION = config('ORGANIZATION')
PROJECTS = [p.strip() for p in config('PROJECTS').split(',')]
PAT = config('PERSONAL_TOKEN')
API_VERSION = '7.0'


url = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/definitions?api-version={API_VERSION}"
auth = HTTPBasicAuth("",PAT)

def get_allReleases():

    response = requests.get(url,auth=auth)

    if response.status_code == 200:
        data = response.json()["value"]
        return data
    else:
        print("Error" , response.status_code, response.text)
        return None
    
def sel_cutom_data(filter: str = "", type: int = 0, data = []  ):

    filtered = []
    if type == 0:
        
        for release in data:
            if filter in release["path"]:
                filtered.append(release)

    elif type == 1:
        
        for release in data:
            if release["path"].startswith(filter):
                filtered.append(release)

    return filtered

def printData(data):

    for release in data:
            print(f"ID: {release['id']}\t-  Path: {release['path']} \\ {release['name']}")

if __name__ == "__main__":

    data = get_allReleases()
    newData = sel_cutom_data("Team 29",0,data)
    newData2 = sel_cutom_data("NPV\\GCP\\PARTICULARES",0,newData)

    printData(newData2)



    