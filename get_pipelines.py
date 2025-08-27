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

    pet.makefile(pipes)

    return pipes
    
    
if __name__ == "__main__":

    getPipeline("api-tienda-cajas-npv-dev-gcp-ci")
    #data = pet.sel_custom_data()
    #pipes = get_allPipeswDef()
    #newData = pet.sel_custom_data("api-credito-springboot-npv-qa-gcp-ci","definition/name",0,pipes)


    
    


    