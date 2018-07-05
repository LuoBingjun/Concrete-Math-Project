import json
import csv
file0=open("map.json","r")
file1=open("tree.csv","r")

load=json.load(file0)
links=load["links"]
tree=list(csv.reader(file1))

for i in range(len(tree)):
    for j in range(len(tree)):
        if tree[i][j]=='1':
            n=0
            for k in links:
                if n==2:
                    break
                if (k["source"]==i and k["target"]==j) or (k["source"]==j and k["target"]==i):
                    k["flags"]=1
                    n+=1

file2=open("map1.json","w")
json.dump(load,file2)