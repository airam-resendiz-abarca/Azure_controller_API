import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import sys
import argparse

import re

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

isbuild = lambda v: re.fullmatch(r"\d+(\.\d+)*",v)
iscommit = lambda v: re.fullmatch(r"[0-9a-f]{5,40}",v,re.I)

new_Artifact = lambda artif,source: {
            "alias": str( artif['alias'] ),
            "InstanceReference": source
        }

new_Definition = lambda def_id,art_list: {
        "definitionId": int(def_id),
        "description": f"release creado con python",
        "artifacts": art_list

    }

def getPipeline(i: dict, buildNumber: list) -> list:
    
    pipeline = []
    for j in buildNumber:
        pipeline = pipes.getPipeline(i["source"],j)
        if pipeline:
            break
    if not pipeline:
            pipeline = pipes.getPipeline(i["source"])

    return [ b for b in pipeline if b["result"] == "succeeded"]

def getCommit(i: dict,commitsid: list):
    commit = []
    for j in commitsid:
        commit = commits.getCommit(i["source"],"master",j)
        if commit:
            break
    if not commit:
            commit = commits.getCommit(i["source"],"master")
    return commit

def makePayload(def_id,lista):

    def_art = releases.getArtifacts(def_id)
    artifacts = []
    buildnums = [p for p in lista if isbuild(p)]
    commitsid = [p for p in lista if iscommit(p)]

    for i in def_art:

        source = {}
        
        if i['type'].lower() == "build":
            
            pipeline = getPipeline(i,buildnums)
            if pipeline:
                source['id'] = pipeline[0]['id']
                source["name"] = i['source']

        elif i['type'].lower() == "git":

            commit = getCommit(i,commitsid)
            if commit:
                source['id'] = commit[0]['commitId']
                source["name"] = "master"

        artifacts.append(new_Artifact(i,source))
    return new_Definition(def_id,artifacts)


def createRelease(payload):
    pet.makefile([payload])
    response = requests.post(url_rel,json=payload,auth=auth)

    if response.status_code == 200:
        release = response.json()
        print("Release creado con exito")
    else:
        print(f"Algo fallo en la ejecucion url: {url_rel} - {response.status_code}")

if __name__ == "__main__":

    with open("releases.list","r") as file:
        for line in file:
            if line in [" ","\n",""] :
                continue
            params = line.split("|")
            params = [p.strip() for p in params]
            artifacts = [p for p in params[2:] if p]
            
            definitions = releases.get_allDefinitions()
            definitions = pet.sel_custom_data(params[0],"name",0,definitions)
            definitions = pet.sel_custom_data(params[1],"path",0,definitions)

            if not definitions:
                print(f"Error creando release para {params[1]}\\{params[0]}: definition no encontrado")
                continue
            
            payload = makePayload(definitions[0]['id'],artifacts)
            print(f"creando release de: {params[1]}\\{params[0]} status: ",end=" ")
            #createRelease(payload)

            