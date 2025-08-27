from time import sleep
import sys 

import peticiones as pet

API_VERSION = '7.0'

def get_allDefinitions():

    rel_path = f"release/definitions?api-version={API_VERSION}"
    return pet.getData(rel_path,True)
def get_allReleases():

    rel_path = f"release/releases?api-version={API_VERSION}"
    return pet.getData(rel_path,True)

def get_allReleaseswDef(def_id):

    rel_path = f"release/releases?definitionId={def_id}&api-version={API_VERSION}"
    return pet.getData(rel_path,True)

def get_Definition(def_id):
    url_art = f"release/definitions/{def_id}?api-version={API_VERSION}"
    return pet.getData(url_art,True)

def getArtifacts(art_id):
    definition = get_Definition(art_id)
    artifacts = []

    if definition:
        for artifact in definition["artifacts"]:
            with open("example.json","a") as file:
                file.write(str( artifact) + "\n" )
            alias = artifact.get("alias")
            art_type = artifact.get("type")
            ref = artifact.get("definitionReference",{})
            sourceName = ref.get("definition",{}).get("name")
            pipe_def = ref.get("definition",{}).get("id")

            artifacts.append({
                "alias": alias,
                "type": art_type,
                "source": sourceName,
                "def_id": pipe_def
            })
    else:
        print("fallo obtener artifacts")

    return artifacts

def getReleases(api:str,path:str,release: str = ""):
    data = get_allDefinitions()
    data = pet.sel_custom_data(api,"name",0,data)
    data = pet.sel_custom_data(path,"path",0,data)

    releases = get_allReleaseswDef(data[0]["id"])

    if release != "":
        releases = pet.sel_custom_data(release,"name",3,releases)
    
    pet.makefile(releases)



if __name__ == "__main__":

    #getReleases("api-cancelaciones","NPV\\GCP\\PARTICULARES\\Team 18","Release-1")
    data = get_allDefinitions()
    data = pet.sel_custom_data("api-cancelaciones","name",0,data)
    data = pet.sel_custom_data("GCP\\PARTICULARES\\Team 18","path",0,data)

    definition = get_Definition(data[0]["id"])
    pet.makefile([definition])




    