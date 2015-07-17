#!/usr/bin/python
import os
from collections import defaultdict

os.chdir("F:\\college\\Sem7\\CF\\ml-100k\\ml-100k");

f = open('u1.test','r');
listTest = []
for line in f:
    temp = line.split()
    listTest.append([temp[0], temp[1], int(temp[2])])

f = open('u1.base','r');
users = defaultdict(list)
items = defaultdict(list)
for line in f:
    temp = line.split()
    users[temp[0]].append((temp[1],int(temp[2])))
    items[temp[1]].append((temp[0],int(temp[2])))


minSumError = 8
lambda1 = 15
lambda2 = 15
while lambda1 > 10:
    itemBias = {}
    while lambda2 < 35:
        userBias = {}
        for item in items:
           sum = 0.0
           for u in items[item]:
               sum = sum + u[1] - 3.52
           itemBias[item] = sum / (lambda1 + len(u))

        for user in users:
           sum = 0.0
           for i in users[user]:
               sum = sum + i[1] - 3.52 - itemBias[i[0]]
           userBias[user] = sum / (lambda2 + len(i))
        sumError = 0.0
        count = 0
        for l in listTest:
           if l[0] in userBias.keys() and l[1] in itemBias.keys():
               sumError += abs(l[2] - userBias[l[0]] - itemBias[l[1]] - 3.52)
               count += 1
           if (sumError/count) < minSumError:
               minSumError = sumError/count
               minLambda1 = lambda1
               minLambda2 = lambda2
               ansU = userBias
               ansI = itemBias
        
        lambda2 += 5
lambda1 -= 1

print "min error: ", minSumError
print "lambda1: ", minLambda1
print "lambda2: ", minLambda2
print "userBias: ", ansU
print "itembias: ", ansI
