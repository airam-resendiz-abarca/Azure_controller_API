import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import sys
import argparse

import get_pipelines as pipes
import get_releases as releases
import get_commit as commits

ORGANIZATION = config('ORGANIZATION')
PROJECTS = [p.strip() for p in config('PROJECTS').split(',')]
PAT = config('PERSONAL_TOKEN')
API_VERSION = '7.0'

url_def = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/definitions?api-version={API_VERSION}"
url_rel = f"https://vsrm.dev.azure.com/{ORGANIZATION}/{PROJECTS[0]}/_apis/release/releases?api-version={API_VERSION}"
auth = HTTPBasicAuth("",PAT)




def makePayload(def_id):

    def_artifacts = releases.getArtifacts(def_id)
    artifacts = []

    for i in def_artifacts:

        source = {}

        if i['type'].lower() == "build":
            pipelines = pipes.get_allPipeswDef(i["def_id"])
            buildNum = input("Ingrese el buildNumber: ")
            pipeline = pipes.sel_cutom_data(str(buildNum),"buildNumber",0,pipelines)

            if pipeline:
                source['id'] = pipeline[0]['id']
                source["name"] = i['source']

        elif i['type'].lower() == "git":

            repos = commits.get_allRepositories()
            repos = commits.sel_cutom_data("api-tienda-cajas","name",0,repos)
            branches = commits.get_allBranches(repos[0]["id"])
            branches = commits.sel_cutom_data("master","name",0,branches)
            commit = commits.get_allCommits(repos[0]["id"],branches[0]["name"])

            if commit:
                source['id'] = commit[0]['commitId']
                source["name"] = branches[0]["name"]


        artifact = {
            "alias": str( i['alias'] ),
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

    name = "api-tienda-cajas-springboot-cd-gke-team29"

    definitions = releases.get_allDefinitions()
    definitions = releases.sel_cutom_data(name,"name",0,definitions)
    
    createRelease( makePayload(definitions[0]['id']) ) 