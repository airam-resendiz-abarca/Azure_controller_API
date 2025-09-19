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


def getPipeFromVersion(Path: str):
    version = ""
    name = ""
    with open("pipelines.list","r") as file:
        for line in file:
            name,version = line.split("\t")
            name = name.replace(":","").strip()
            version = version.strip()
            val_pipes = []
            
            definitions = get_allDefinitions()
            definitions = pet.sel_custom_data(name,"name",0,definitions)
            definitions = pet.sel_custom_data(Path,"path",3,definitions)
            
            pipes = []
            for v in definitions :
                pipes += get_allPipeswDef(v["id"]) 

            pet.makefile(pipes,"./pipe_def/" + name + ".json")            
            pipes = pet.sel_custom_data("succeeded","result",0,pipes)

            for pipe in pipes:
                runs = get_Log(pipe["id"],20).decode("utf-8")
                if version in runs:
                    val_pipes.append(pipe["buildNumber"])
                pet.makefile(val_pipes,"./list_pipes/" + name +"-"+ version + ".txt")
            
    
if __name__ == "__main__":
    
    getPipeFromVersion("\\yml version gcp")
    #data = pet.sel_custom_data()
    #pipes = get_allPipeswDef()
    #newData = pet.sel_custom_data("api-credito-springboot-npv-qa-gcp-ci","definition/name",0,pipes)


    
    


    