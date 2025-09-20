from modulos import get_pipelines as pipelines
from modulos import peticiones as pet


def getPipeFromVersion(Path: str):
    version = ""
    name = ""
    with open("pipelines.list","r") as file:
        for line in file:
            name,version = line.split("\t")
            name = name.replace(":","").strip()
            version = version.strip()
            val_pipes = []
            
            definitions = pipelines.get_allDefinitions()
            definitions = pet.sel_custom_data(name,"name",0,definitions)
            definitions = pet.sel_custom_data(Path,"path",3,definitions)
            
            pipes = []
            for v in definitions :
                pipes += pipelines.get_allPipeswDef(v["id"]) 

            pet.makefile(pipes,"./pipe_def/" + name + ".json")            
            pipes = pet.sel_custom_data("succeeded","result",0,pipes)

            for pipe in pipes:
                runs = pipelines.get_Log(pipe["id"],20).decode("utf-8")
                if version in runs:
                    val_pipes.append(pipe["buildNumber"])
                pet.makefile(val_pipes,"./list_pipes/" + name +"-"+ version + ".txt")

if __name__ == "__main__":
    
    getPipeFromVersion("\\yml version gcp")