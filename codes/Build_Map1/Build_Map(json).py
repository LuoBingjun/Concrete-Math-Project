import csv
import json

file0 = open("movie_data.csv", "r")
data0 = list(csv.reader(file0))

name = []
num = []
for i in data0:
    if(name.count(i[2])):
        num[name.index(i[2])] += 1
    else:
        name.append(i[2])
        num.append(1)

users = []
nodes = []

# 初始化Nodes(用户)
for i in range(len(name)):
    if num[i] >= 60 or (num[i] >= 10 and num[i] <= 20):
        nodes.append(
            {"userID": len(nodes), "username": name[i], "movie name": [], "comment": []})
        users.append(name[i])

# 生成Nodes(用户)
for i in data0:
    if users.count(i[2]):
        nodes[users.index(i[2])]["movie name"].append(i[1])
        nodes[users.index(i[2])]["comment"].append(int(i[3]))

links = []
for i in nodes:
    degree = 0
    for j in nodes:
        if i == j:
            continue
        movies = [v for v in i["movie name"] if v in j["movie name"]]
        if movies == []:
            continue
        value = 0
        for n in movies:
            if abs(i["comment"][i["movie name"].index(n)]-j["comment"][j["movie name"].index(n)]) <= 1:
                value += 0.05
            else:
                value -= 0.05
        if value <= 0.3:
            continue
        else:
            if value >= 1:
                value = 1
        links.append({"ID": len(links), "source": i["userID"],
                      "target": i["userID"], "value": value})
        degree += 1
    i["degree"] = degree


Map = {"nodes": nodes}

json = json.dumps(Map)
filejson = open("map1.json", "w", encoding='gbk')
filejson.write(json)
