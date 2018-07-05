import csv

file = open("movie_data.csv", "r")
reader=csv.reader(file)
data=list(reader)

name=[]
num=[]
for i in data:
    if(name.count(i[1])):
        num[name.index(i[1])]+=1
    else:
        name.append(i[1])
        num.append(1)

username=[]

for i in name:
    if num[name.index(i)]>80:
        username.append(i)

print(len(username))

file1 = open("80.csv", "w")
writer = csv.writer(file1)
writer.writerow(username)