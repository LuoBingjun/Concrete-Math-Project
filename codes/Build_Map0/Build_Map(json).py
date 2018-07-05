import csv
import json

file0 = open("movies.csv", "r")
data0 = list(csv.reader(file0))
file1 = open("average.csv", "r")
data1 = list(csv.reader(file1))

for i in data1:
    i[0] = int(i[0])
    i[2] = float(i[2])

# 生成Nodes
nodes = []
for i in data0:
    nodes.append({"ID": i[0], "影片": i[1], "导演": i[2], "编剧": i[3], "主演": i[4], "类型": i[5], "国家/地区": i[6], "语言": i[7], "上映日期": i[8]})

for i in data0:
    i[0] = int(i[0])
    i[2] = i[2].split(";")
    i[3] = i[3].split(";")
    i[4] = i[4].split(";")
    i[5] = i[5].split(";")
    i[6] = i[6].split(" / ")
    i[7] = i[7].split(" / ")

links = []
for i in range(len(data0)):
    for j in range(i + 1, len(data1)):
        if [v for v in data0[i][5] if v in data0[j][5]] == []:
            continue
        if abs(data1[i][2] - data1[j][2]) >= 2:
            continue
        value = 0
        if data0[i][5] == data0[j][5]:
            value += 0.75
        else:
            value += 0.5
        for k in range(2, 5):
            if [v for v in data0[i][k] if v in data0[j][k]] == []:
                continue
            else:
                if data0[i][k] != data0[j][k]:
                    value += 0.02
                else:
                    value += 0.05
        for k in range(6, 8):
            if [v for v in data0[i][k] if v in data0[j][k]] == []:
                continue
            else:
                if data0[i][k] != data0[j][k]:
                    value += 0.02
                else:
                    value += 0.05
        links.append({"ID": len(links), "source": i, "target": j, "value": value})

Map = {"nodes": nodes, "links": links}

json = json.dumps(Map)
filejson = open("map.json", "w", encoding='gbk')
filejson.write(json)
