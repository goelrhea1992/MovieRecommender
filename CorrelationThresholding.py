#!/usr/bin/python
from math import sqrt
from math import cos
import os
import math
import collections
import codecs 
feom collections import defaultdict

os.chdir("F:\\college\\Sem7\\CF\\ml-100k\\ml-100k");
vmin = 1000.0
vmax = 0.0
movieVariances = defaultdict()
movieRatings = defaultdict(list)

def avg(ratings):
  s = 0.0
  for i in ratings:
    s = s + i
    return (s * 1.0)/len(ratings)

def variance(ratings):
  s = 0.0
  a = avg(ratings)
  for i in ratings:
    s = s + ((a-i)**2)
    return (s * 1.0)/len(ratings)

def computeNearestNeighbor(users, username):
  """creates a sorted list of users based on their distance to username"""
  distances = []
  for user in users:
    if user != username:
      distance = pearson(users[username],users[user])
      distances.append((user, distance))
      # sort based on distance -- closest first
      distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
      return distances

def pearson(rating1, rating2):
  x = 0.0
  y = 0.0
  sumX = 0.0
  sumY = 0.0
  sumXSquare = 0.0
  sumYSquare = 0.0
  n = 0.0
  sumVar = 0.0
  newSum = 0.0
  xList = []
  for key in rating1.keys():
    xList.append(int(rating1[key]))
    xAvg = avg(xList)
    yList = []
  
  for key in rating2.keys():
    yList.append(int(rating2[key]))
    yAvg = avg(yList)
  
  for key in rating1.keys():
    if key in rating2.keys():
      n += 1.0
      x = float(rating1[key])
      y = float(rating2[key])
      thisVar = (movieVariances[int(key)] - vmin)/vmax
      newSum += thisVar * (x - xAvg) * (y - yAvg)
      sumVar += thisVar
      sumX += x
      sumY += y
      sumXSquare += pow(x, 2)
      sumYSquare += pow(y, 2)
  
  if n == 0.0:
    return 0.0
  
  # now compute denominator
  denominator = (sqrt(sumXSquare - pow(sumX, 2) / n) * sqrt(sumYSquare - pow(sumY, 2) / n))
  if denominator == 0.0:
    return 0.0
  else:
    coeff = ((newSum)/ denominator)/sumVar
    # print "Pearson: ", coeff
    return coeff

f = open('u.data','r')
for line in f:
  temp = line.split()
  movieid = int(temp[1].strip())
  rating = int(temp[2])
	movieRatings[movieid].append(rating)

count = 0
for movieid in movieRatings.keys():
  count += 1
  v = variance(movieRatings[movieid])
  movieVariances[movieid]=v
  if v < vmin:
    vmin = v
  if v > vmax:
    vmax = v

f = open('u1.test','r');
listTest = []
for line in f:
  temp = line.split()
  t = [temp[0], temp[1], int(temp[2])]
  listTest.append(t)

f = open('u1.base','r');
users = defaultdict(lambda: defaultdict(int))
for line in f:
  temp = line.split()
  users[temp[0]][temp[1]] = int(temp[2])

threshold = 0.5
# print "Threshold: ", threshold
count = 0
error = 0.0

for l in listTest:
  neighborsOrdered = computeNearestNeighbor(users, l[0])
  count1 = 0
  topK = []
  for i in range(0,942):
    if neighborsOrdered[i][1] > threshold:
      topK.append((neighborsOrdered[i][0], i))
  
  numUsers = 0
  for pairs in topK:
    numUsers += 1
  # print "Number of users chosen for this threshold: ", numUsers
  
  listRatingsDistance = []
  for thisK in topK:
    if l[1] in users[thisK[0]]:
      r1 = users[thisK[0]][l[1]]
      d1 = neighborsOrdered[thisK[1]][1]
      count1 += 1
      # print "Pearson coeff for user: ", d1
      listRatingsDistance.append([r1,d1])
  
  if count1>0:
    # print count, " users have rated this movie"
    myRating = 0.0
    denom = 0.0
    for tup in listRatingsDistance:
      denom += tup[1]
    for tup in listRatingsDistance:
      myRating += (float(tup[0]) * float(tup[1])) / denom
    # print "My rating for movie ", l[1], " is: ", myRating
    # print "but his rating was ", l[2], "So error is: ", abs(myRating - l[2])
    # print
    error += abs(myRating - l[2])
    count += 1
print "MAE k = 5: ",(error/count)                     
