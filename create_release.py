import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import sys
import argparse

import get_pipelines as pipes
import get_releases as releases
import get_commit as commits
import peticiones as pet

ORGANIZATION = config('ORGANIZATION')
PROJECTS = [p.strip() for p in config('PROJECTS').split(',')]
PAT = config('PERSONAL_TOKEN')
API_VERSION = '7.0'

url_def = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/definitions?api-version={API_VERSION}"
url_rel = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/releases?api-version={API_VERSION}"
auth = HTTPBasicAuth("",PAT)




def makePayload(def_id,lista):

    def_art = releases.getArtifacts(def_id)
    artifacts = []
    for i in range(len(def_art)):

        source = {}
        
        if def_art[i]['type'].lower() == "build":
            
            pipeline = pipes.getPipeline(def_art[i]["source"],lista[i])
            
            if pipeline:
                source['id'] = pipeline[0]['id']
                source["name"] = def_art[i]['source']

        elif def_art[i]['type'].lower() == "git":

            commit = commits.getCommit(def_art[i]["source"],"master",lista[i])
            
            if commit:
                source['id'] = commit[0]['commitId']
                source["name"] = "master"


        artifact = {
            "alias": str( def_art[i]['alias'] ),
            "InstanceReference": source
        }

        artifacts.append(artifact)
    

    return {
        "definitionId": int(def_id),
        "description": f"release creado con python",
        "artifacts": artifacts

    }


def createRelease(payload):
    
    response = requests.post(url_rel,json=payload,auth=auth)

    if response.status_code == 200:
        release = response.json()
        print("Release creado con exito")
    else:
        print("Algo fallo en la ejecucion")

if __name__ == "__main__":

    with open("releases.list","r") as file:
        for line in file:
            params = line.split("|")
            artifacts = params[2:]

            definitions = releases.get_allDefinitions()
            definitions = pet.sel_custom_data(params[0],"name",0,definitions)
            definitions = pet.sel_custom_data(params[1],"path",0,definitions)
            
            payload = makePayload(definitions[0]['id'],artifacts)

            pet.makefile([payload])