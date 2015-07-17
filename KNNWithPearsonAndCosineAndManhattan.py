"""
K Nearest Neighbors with Pearson, Cosine and Manhattan distance.
"""

#!/usr/bin/python
from math import sqrt
from math import cos
import os
import math
import collections
import codecs 

os.chdir("F:\\college\\Sem7\\CF\\ml-100k\\ml-100k");

def computeNearestNeighbor(users, username):
  """creates a sorted list of users based on their distance to username"""
  distances = []
  for user in users:
    if user != username:
      # distance = cosine(users[username],users[user])
      # distance = manhattan(users[username],users[user])
      distance = pearson(users[username],users[user])
      
      distances.append((user, distance))
  # sort based on distance -- closest first
  distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
  return distances

def pearson(rating1, rating2):
  sumXY = 0
  sumX = 0
  sumY = 0
  sumXSquare = 0
  sumYSquare = 0
  n = 0
  for key in rating1:
    if key in rating2:
      n += 1
      x = rating1[key]
      y = rating2[key]
      sumXY += x * y
      sumX += x
      sumY += y
      sumXSquare += pow(x, 2)
      sumYSquare += pow(y, 2)
  if n == 0:
    return 0
  # now compute denominator
  denominator = (sqrt(sumXSquare - pow(sumX, 2) / n) * sqrt(sumYSquare - pow(sumY, 2) / n))
  if denominator == 0:
    return 0
  else:
    return (sumXY - (sumX * sumY) / n) / denominator

def manhattan(rating1, rating2):
  """Computes the Manhattan distance. Both rating1 and rating2 are dictionaries 
  of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
  
  distance = 0.0
  total = 0.0
  for key in rating1:
    if key in rating2:
      distance += abs(rating1[key] - rating2[key])
      total += 1
  if total > 0 and distance!=0:
    return 1/distance
  else:
    return -1 #Indicates no ratings in common

def cosine(rating1, rating2):
  sumXY = 0
  sumXSquare = 0
  sumYSquare = 0
  n = 0
  for key in rating1:
    if key in rating2:
      n += 1
      x = rating1[key]
      y = rating2[key]
      sumXY =sumXY + x*y
      sumXSquare += pow(x, 2)
      sumYSquare += pow(y, 2)
      if n == 0:
        return 0
      denominator = sqrt(sumXSquare)*sqrt(sumYSquare)
      numerator = sumXY
      val = numerator / float(denominator)
      if denominator == 0:
        return 0
      else:
        return cos(val)

f = open('u1.test','r');
listTest = []
for line in f:
  temp = line.split()
  listTest.append([temp[0], temp[1], int(temp[2])])

f = open('u1.base','r');
users = defaultdict(lambda: defaultdict(int))
for line in f:
    temp = line.split()
    users[temp[0]][temp[1]] = int(temp[2])

error = 0.0
count = 0
for l in listTest:
  neighborsOrdered = computeNearestNeighbor(users, l[0])
  for k in range(5):
    for neighbor in range(k):
      error = 0.0
      count = 0
      toConsider[neighbor] = neighbprsOrdered[neighbor][0]
      
    listRatingsDistance = []
    for neighbor in range(k):
      if l[1] in users[toConsider[neighbor]]:
        r1 = users[toConsider[neighbor]][l[1]]
        d1 = neighborsOrdered[neighbor][1]
        listRatingsDistance.append([r1,d1])
    
    denom = 0
    myRating = 0
    for tup in list:
      denom+=tup[1]
    for tup in list:
      myRating += tup[0]*tup[1]/denom
    error+= abs(myRating - l[2])
    count+=1
    print 'For k = ', k
    print error/count
