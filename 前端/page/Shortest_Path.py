import csv
import sys
import copy

class point:
    def __init__(self, id, value):
        self.id=id
        self.value=value
        self.path=[]

filename=sys.argv[1]
n=int(sys.argv[2])
m=int(sys.argv[3])

file=open(filename,'r')
reader=csv.reader(file)
data=list(reader)
p=[int(i) for i in data[0]]
q=[int(i) for i in data[1]]
r=[float(i) for i in data[2]]

pt=[]

for i in range(len(data[0])-1):
    pt.append(point(i,0))
pt[n].value=1
pt[n].path.append(pt[n])

def BFS(stack):
    maxpath=[]
    maxvalue=0
    find=False
    while len(stack):
        for p0 in stack:
            for j in range(p[p0.id],p[p0.id+1]):
                if pt[q[j]].value==0:
                    pt[q[j]].value=p0.value*r[j]
                    pt[q[j]].path=copy.copy(p0.path)
                    pt[q[j]].path.append(pt[q[j]])
                    stack.append(pt[q[j]])
                if q[j]==m:
                    find=True
                    if pt[q[j]].value>maxvalue:
                        maxpath=pt[q[j]].path
                        maxvalue=pt[q[j]].value
            if find and len(stack[0].path)<len(stack[1].path):
                return maxpath
            stack.pop(0)
    return maxpath

stack=[pt[n]]
maxpath=BFS(stack)

print(pt[m].value, ' ', end='')
print(len(maxpath), ' ', end='')
for i in maxpath:
    print(i.id, ' ', end='')

