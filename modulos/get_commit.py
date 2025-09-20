from time import sleep
import sys 
from . import peticiones as pet

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
    

    
def getCommit(repo:str,branch:str = "master", commit: str = ""):
    repos = get_allRepositories()

    repos = pet.sel_custom_data(repo,"name",0,repos)

    branches = get_allBranches(repos[0]["id"])

    branches = pet.sel_custom_data(branch,"name",0,branches)

    commits = get_allCommits(repos[0]["id"],branches[0]["name"])

    if commit != "":

        commits = pet.sel_custom_data(commit,"commitId",1,commits)

    pet.makefile(commits)

    return commits



if __name__ == "__main__":

    getCommit("api-articulo","master","74aa44")

    