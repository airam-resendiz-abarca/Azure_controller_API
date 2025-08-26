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

def getData(path,vsrm:bool = False):

    url = url_base + path if vsrm else url_base2 + path

    response = requests.get(url,auth=auth)

    if response.status_code == 200:
        data = response.json()
        if "value" in data:
            data = data["value"]
        return data
    else:
        print("Error" , response.status_code, response.text)
        return None