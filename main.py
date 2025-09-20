import sys
import os

for p in sys.path:
    print("-\t",p)

print("_"*100)
print(os.listdir(os.path.dirname(__file__)),end="\n\n")

print(os.listdir(os.path.dirname(__file__)),end="\n\n")

print(os.listdir(os.path.join(os.path.dirname(__file__),"modulos")),end="\n\n")