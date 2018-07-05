import csv

file0 = open("movies.csv", "r")
data0 = list(csv.reader(file0))
file1 = open("average.csv", "r")
data1 = list(csv.reader(file1))

# 生成节点csv
filepoint = open("point.csv", "w", newline='')
point = []
for i in data0:
    point.append([i[1]])
writer = csv.writer(filepoint)
writer.writerows(point)

for i in data1:
    i[2] = float(i[2])

a = [0]
b = []
c = []

for i in data0:
    i[2] = i[2].split(";")
    i[3] = i[3].split(";")
    i[4] = i[4].split(";")
    i[5] = i[5].split(";")
    i[6] = i[6].split(" / ")
    i[7] = i[7].split(" / ")

m = -1
for i in data0:
    for j in data0:
        if i == j:
            continue
        if [v for v in i[5] if v in j[5]] == []:
            continue
        if abs(data1[data0.index(i)][2] - data1[data0.index(j)][2]) >= 2:
            continue
        m += 1
        b.append(data0.index(j))
        if i[5] == j[5]:
            c.append(0.75)
        else:
            c.append(0.5)
        for k in range(2, 5):
            if [v for v in i[k] if v in j[k]] == []:
                continue
            else:
                if i[k] != j[k]:
                    c[m] += 0.02
                else:
                    c[m] += 0.05
        for k in range(6, 8):
            if [v for v in i[k] if v in j[k]] == []:
                continue
            else:
                if i[k] != j[k]:
                    c[m] += 0.02
                else:
                    c[m] += 0.05
    a.append(m + 1)

print(len(a))
print(len(b))

# 生成正向表csv
filemap = open("map.csv", "w", newline='')
writer = csv.writer(filemap)
writer.writerow(a)
writer.writerow(b)
writer.writerow(c)

        
