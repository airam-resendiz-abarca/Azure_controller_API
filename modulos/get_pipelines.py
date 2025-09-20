from time import sleep
from modulos import peticiones as pet

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

def getPipeline(name: str,build:str = ""):
    data = get_allDefinitions()
    data = pet.sel_custom_data(name,"name",0,data)
    pipes = get_allPipeswDef(data[0]["id"])
    if build != "":
        pipes = pet.sel_custom_data(build,"buildNumber",0,pipes)

    return pipes

def get_allLogs(pipeid):
    rel_path = f"build/builds/{pipeid}/logs"
    return pet.getData(rel_path) 

def get_Log(pipeid,log):
    rel_path = f"build/builds/{pipeid}/logs/{log}"
    return pet.getData(rel_path)   

def get_allRuns(pipeid,runid):
    rel_path = f"pipelines/{pipeid}/runs/{runid}/logs?api-version={API_VERSION}"
    return pet.getData(rel_path)



            
    
if __name__ == "__main__":
    
    pass