import json
import peticiones as pet
import get_releases as releases

import requests
from requests.auth import HTTPBasicAuth
from decouple import config

ORGANIZATION = config('ORGANIZATION')
PROJECTS = [p.strip() for p in config('PROJECTS').split(',')]
PAT = config('PERSONAL_TOKEN')
API_VERSION = '7.1'


auth = HTTPBasicAuth("",PAT)

def getListIndex(env: list, name: str )-> int:
    
    for inx,i, in enumerate(env):
        if name.lower() in i["name"].lower():
            return int(inx)
        
    return int(-1)

def recorrerDefinition(original: dict, path: list, value: str):
    definition = original
    returnal = definition
    for j,i in enumerate(path):
        
        if(type(definition) == list):
            i = int(i)
        
        if j+1 == len(path):
            definition[i] = value
        else:

            definition = definition[i]
        
    
    definition = value
    return returnal 


def modificarRelease(id,payload):

    
    url_def = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/definitions/{id}?api-version={API_VERSION}"
    header = {"Content-Type": "application/json"}

    response = requests.put(
        url_def,
        headers=header,
        auth=auth,
        json=payload,)

    if response.status_code == 200:
        return True
    else:
        print("⛔ Algo fallo en la ejecucion")
        print(response.status_code )
        return False



if __name__ == "__main__":

    #path = "\\XObsoletos\\Coordinacion1\\Equipo 11"
    path = "\\NPV\\GCP\\PROD\\C1"

    definitions = releases.get_allDefinitions()
    
    definitions = pet.sel_custom_data(path,"path",0,definitions)
    #definitions = pet.sel_custom_data("api-bodeguita-jersey-cd-gke-c1","name",0,definitions)

    f = open("new.config")
    config = json.load(f)

    for j in definitions:

        definition = releases.get_Definition(j["id"])
        pet.makefile([definition],"./try/"+j["name"]+".json")

        for i in config:
            lista = i["path"].split(sep="/")
            if "environments" in lista:
                index = lista.index("environments")
                lista[index + 1] = int( 
                    getListIndex(definition["environments"],lista[index + 1])
                    )
                
            if i["op"] == "replace":
                valor = definition["path"].replace(path,i["value"])
            else:
                valor = i["value"]

            recorrerDefinition(definition,lista,valor)
        
        pet.makefile([definition],"./try/"+j["name"]+"_NEW.json")
        good = False
        
        good = modificarRelease(j["id"],definition)

        if good:
            print(f"✅ Release {j["name"]} modificado con exito")


        
