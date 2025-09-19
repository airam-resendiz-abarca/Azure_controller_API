import requests
from requests.auth import HTTPBasicAuth
from decouple import config

import peticiones as pet

ORGANIZATION = config('ORGANIZATION')
PROJECTS = [p.strip() for p in config('PROJECTS').split(',')]
PAT = config('PERSONAL_TOKEN')




url_base = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/"
url_base2 = f"https://dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/"
auth = HTTPBasicAuth("",PAT)

def getData(path: str,vsrm:bool = False):

    url = url_base + path if vsrm else url_base2 + path

    response = requests.get(url,auth=auth)
    if response.status_code == 200:
        
        if "json" in response.headers["Content-Type"]:
            data = response.json()
        else:
            return response.content
        
        if "value" in data:
            data = data["value"]
        return data
    else:
        print("Error" , response.status_code, response.text)
        return None
    
def makefile(data,document = "example.json"):
    
    with open(document,"w",errors="replace") as file:
        for i in data:
            text = str(i).replace("'",'"') + "\n\n" 
            
            file.write(text )

def sel_custom_data(filter: str = "",area: str = "path", type: int = 0, data = []  ):

    filtered = []
    deep = area.split("/")

    for release in data:
        value = ""
        holder = release.copy()
        for i in deep:
            holder = holder[i]

        value:str = holder.lower()
        filter = filter.lower()

        if type == 0:

            if filter in value:
                filtered.append(release)

        elif type == 1:
        
            if value.startswith(filter):
                filtered.append(release)

        elif type == 2:
        
            if value.endswith(filter):
                filtered.append(release)

        elif type == 3:
        
            if value == filter:
                filtered.append(release)

    return filtered