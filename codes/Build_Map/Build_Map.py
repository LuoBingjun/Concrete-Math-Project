import csv

file0 = open("movies.csv", "r")
data0 = list(csv.reader(file0))
file1 = open("average.csv", "r")
data1 = list(csv.reader(file1))

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
            c.append(0.9)
        else:
            c.append(0.7)
        for k in range(2, 5):
            if [v for v in i[k] if v in j[k]] == []:
                continue
            else:
                if i[k] != j[k]:
                    c[m] += 0.05
                else:
                    c[m] += 0.1
        for k in range(6, 8):
            if [v for v in i[k] if v in j[k]] == []:
                continue
            else:
                if i[k] != j[k]:
                    c[m] += 0.05
                else:
                    c[m] += 0.1
    a.append(m + 1)

file3 = open("map.csv", "w")
writer = csv.writer(file3)
writer.writerow(a)
writer.writerow(b)
writer.writerow(c)

        
