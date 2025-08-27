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

def sel_cutom_data(filter: str = "",area: str = "path", type: int = 0, data = []  ):

    filtered = []
    if type == 0:
        
        for release in data:
            if filter in release[area]:
                filtered.append(release)

    elif type == 1:
        
        for release in data:
            if release[area].startswith(filter):
                filtered.append(release)

    elif type == 2:
        
        for release in data:
            if release[area].endswith(filter):
                filtered.append(release)

    return filtered

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

def printDefinition(data):
    for release in data:
        print(f"ID: {release['id']}\t-  Path: {release['path']} \\ {release['name']} ")


def printReleases(data):
    for release in data:
        print(f"ID: {release['id']}\t-Name: {release['releaseDefinition']['name']} \\ {release['name']} ")
    
def printData(data):

    for release in data:
        artifacts = getArtifacts(release["id"])
        print(f"ID: {release['id']}\t-  Path: {release['path']} \\ {release['name']} --NumArtif = {len(artifacts)}")
        for i in artifacts:
            print( '-'*10, f"\n-Alias: {i["alias"]}\n-Type: {i["type"]}\nSource: {i["source"]}")
        print('-'*10)

if __name__ == "__main__":

    data = get_allDefinitions()
    newData = sel_cutom_data("Team 29","path",0,data)
    newData2 = sel_cutom_data("NPV\\GCP\\PARTICULARES","path",0,newData)
    newData3 = sel_cutom_data("api-tienda-cajas","name",0,newData2)

    printDefinition(newData3)

    releases = get_allReleaseswDef( newData3[0]["id"] )

    #printReleases(releases)

    printData(newData3)



    