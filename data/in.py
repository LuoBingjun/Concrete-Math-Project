import csv

file0 = open("used_movies.csv", "r")
data0 = list(csv.reader(file0))
file1 = open("average.csv", "r")
data1 = list(csv.reader(file1))

for i in data1:
	k = 0
	for j in data0:
		if i[0] == j[1]:
			k = 1
			break
	if k == 0:
		data1.remove(i)
		
file3 = open("usedaverage.csv", "w")
writer = csv.writer(file3)
writer.writerows(data1)