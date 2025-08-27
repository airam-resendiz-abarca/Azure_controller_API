from time import sleep
import sys 
import peticiones as pet

API_VERSION = '7.0'

def get_allRepositories():

    rel_path = f"git/repositories?api-version={API_VERSION}"
    return pet.getData(rel_path)

def get_allBranches(repo_id):
    rel_path = f"git/repositories/{repo_id}/refs?filter=heads/&api-version={API_VERSION}"
    return pet.getData(rel_path)

def get_allCommits(repo_id,branch:str):
    branch = branch.replace("refs/heads/","")
    rel_path = f"git/repositories/{repo_id}/commits?searchCriteria.itemVersion.version={branch}&api-version={API_VERSION}"
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
    
def getCommit(api:str,branch:str):
    repos = get_allRepositories()

    repos = sel_cutom_data(api,"name",0,repos)

    branches = get_allBranches(repos[0]["id"])

    branches = sel_cutom_data(branch,"name",0,branches)

    commits = get_allCommits(repos[0]["id"],branches[0]["name"])

    makefile(commits)

def makefile(data):
    
    with open("example.json","w",errors="replace") as file:
        for i in data:
            text = str(i).replace("'",'"') + "\n\n" 
            
            file.write(text )

if __name__ == "__main__":

    getCommit("api-articulo","master")

    