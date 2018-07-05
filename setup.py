import csv
import copy
import eel
import os
import random
import json

eel.init('web')                     # Give folder containing web files


class point:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.path = []


@eel.expose
# 最短路径算法
def shortest_path(n, m, filename):
    file = open(filename, 'r')
    reader = csv.reader(file)
    data = list(reader)
    p = [int(i) for i in data[0]]
    q = [int(i) for i in data[1]]
    r = [float(i) for i in data[2]]

    pt = []

    for i in range(len(data[0])-1):
        pt.append(point(i, 0))
    pt[n].value = 1

    def BFS(stack):
        maxpath = []
        maxvalue = 0
        find = False
        while len(stack):
            for p0 in stack:
                for j in range(p[p0.id], p[p0.id+1]):
                    if pt[q[j]].value == 0:
                        pt[q[j]].value = p0.value*r[j]
                        pt[q[j]].path = copy.copy(p0.path)
                        pt[q[j]].path.append(j)
                        stack.append(pt[q[j]])
                    if q[j] == m:
                        find = True
                        if pt[q[j]].value > maxvalue:
                            maxpath = pt[q[j]].path
                            maxvalue = pt[q[j]].value
                if find and len(stack[0].path) < len(stack[1].path):
                    return maxpath
                stack.pop(0)
        return maxpath

    stack = [pt[n]]
    maxpath = BFS(stack)

    result = str(pt[m].value)+' '
    for i in maxpath:
        result += (str(i)+" ")
    return result

# 推荐算法


def recommand(ID, type, num):
    filename = ''
    if type == 0:
        filename = 'map0_forward_table.csv'
    else:
        filename = 'map1_forward_table.csv'
    file = open(filename, "r")
    data = list(csv.reader(file))

    p = [int(i) for i in data[0]]
    q = [int(i) for i in data[1]]
    r = [float(i) for i in data[2]]

    pt = []

    for i in range(len(data[0])-1):
        pt.append(point(i, 0))
    pt[ID].value = 1
    pt[ID].path.append(pt[ID])

    def BFS(stack):
        points = []
        while len(stack):
            for p0 in stack:
                for j in range(p[p0.id], p[p0.id+1]):
                    if pt[q[j]].value == 0:
                        pt[q[j]].value = p0.value*r[j]
                        pt[q[j]].path = copy.copy(p0.path)
                        pt[q[j]].path.append(j)
                        stack.append(pt[q[j]])
                        points.append(pt[q[j]])
                if len(points) >= num and len(stack[0].path) < len(stack[1].path):
                    return points
                stack.pop(0)
        return points

    stack = [pt[ID]]
    points = BFS(stack)
    points.sort(key=lambda point: point.value, reverse=True)
    result = ''
    for i in range(num):
        result += (str(points[i].id)+' ')
    return result

recommand(312, 0, 10)


web_app_options={
    'mode': "chrome",
    'port': 80,
    'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
}

eel.start('index.html', options=web_app_options)    # Start
