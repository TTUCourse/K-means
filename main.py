import csv

## init
centerA = [0, 0, 0, 0, 0, 0, 0, 0]
centerB = [50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000]
clusterA = []
clusterB = []

countA = 0
countB = 0


def distance(nodeA, nodeB):
	total = 0
	for x, y in zip(nodeA, nodeB):
		total+= abs(x**2 - y**2)
	return total

def updateCenter(data):
	temp = []
	for x in range(0,8):
		temp.append(0)
		for node in data:
			temp[x]+=node[x]
		temp[x]/=len(data)
	return	temp

with open('left.csv', newline='') as csvfile:
     read = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in read:
         if row[1] is "0":
         	#print(row)
         	node = []
         	for x in row[2:10]:
         		node.append(int(x))

         	if distance(node, centerA) < distance(node, centerB):
         		countA+=1
         		clusterA.append(node)
         	else:
         		countB+=1
         		clusterB.append(node)
	 ## first cluster         		
     print("%d %d" % (countA, countB))

centerA = updateCenter(clusterA)
centerB = updateCenter(clusterB)
print(centerA)
print(centerB)
		
	



