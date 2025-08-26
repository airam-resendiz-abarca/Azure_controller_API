from time import sleep
import sys 
import peticiones as pet

API_VERSION = '7.0'

def get_allDefinitions():

    rel_path = f"build/definitions?api-version={API_VERSION}"
    return pet.getData(rel_path)

def get_allPipes():
    rel_path = f"build/builds?api-version={API_VERSION}"
    return pet.getData(rel_path)

def get_allPipeswDef(id):
    rel_path = f"build/builds?definitions={id}&api-version={API_VERSION}"
    return pet.getData(rel_path)
    
def sel_cutom_data(filter: str = "",area: str = "path", type: int = 0, data = []  ):

    filtered = []
    deep = area.split("/")
    if type == 0:
        
        for release in data:
            
            value = ""
            holder = release.copy()
            for i in deep:
                holder = holder[i]

            value = holder
            if filter in value:
                filtered.append(release)

    elif type == 1:
        
        for release in data:
            value = ""
            holder = release.copy()
            for i in deep:
                holder = holder[i]

            value = holder
            if value.startswith(filter):
                filtered.append(release)

    elif type == 2:
        
        for release in data:
            value = ""
            holder = release.copy()
            for i in deep:
                holder = holder[i]

            value = holder
            if value.endswith(filter):
                filtered.append(release)

    return filtered
    
def printPath(data):

    for release in data:
        print(f"ID: {release['id']}\t-  Path: {release['path']} \\ {release['name']} ")

def printPipes(data):

    for release in data:
        print(f"ID: {release['id']}\t- -Name: {release['buildNumber']}\t\t-Source: {release["definition"]["name"]} ")

if __name__ == "__main__":

    data = get_allDefinitions()
    pipes = get_allPipes()
    newData = sel_cutom_data("api-credito-springboot-npv-qa-gcp-ci","definition/name",0,pipes)

    
    
    printPipes(pipes)


    