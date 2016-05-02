import csv
import random


def distance(nodeA, nodeB):
	total = 0
	for x, y in zip(nodeA, nodeB):
		total+= abs(x**2 - y**2)
	return total

class KMeans(object):
	"""docstring for KMeans"""
	def __init__(self):
		super(KMeans, self).__init__()
		"""generate initial center of cluster"""
		self.centerA = [0, 0, 0, 0, 0, 0, 0, 0]
		self.centerB = [50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000]
		self.data = []
		self.clusterA = []
		self.clusterB = []
		random.seed()

		""" Random center"""
		for x in range(0, 8):
			self.centerA[x] = random.randrange(200000)
			self.centerB[x] = random.randrange(200000)

	def append(self, node):
		self.data.append(node)

	def calssify(self):
		self.clusterA = []
		self.clusterB = []
		index = 0
		for x in self.data:
			if distance(x[:-1], self.centerA) < distance(x[:-1], self.centerB):
				self.clusterA.append(index)
			else:
				self.clusterB.append(index)
			index+=1

	def updateCenter(self):
		self.calssify()
		self.centerA = self.calCenter(self.clusterA)
		self.centerB = self.calCenter(self.clusterB)

	def calCenter(self, cluster):
		temp = []
		for x in range(0,8):
			temp.append(0)
			for index in cluster:
				temp[x] += self.data[index][x]
			if len(cluster) is not 0:
				temp[x] /= len(cluster)
			else:
				temp[x] = 0
		return	temp

	def display(self):
		#print("centerA     centerB")
		#for x, y in zip(self.centerA, self.centerB):
		#	print("%09.2f    %09.2f" % (x, y))

		print(self.centerB[0], self.centerB[1], self.centerB[2], self.centerB[3], self.centerB[4], self.centerB[5], self.centerB[6], self.centerB[7])
		#print(self.centerB)

	def verify(self):
		LEFT = 1
		RIGHT = 0
		countA = 0
		countB = 0

		for a in self.clusterA:
			#print (self.data[a][-1])
			if self.data[a][-1] is LEFT:
				countA += 1
		for b in self.clusterB:
			#print (self.data[a])
			if self.data[b][-1] is RIGHT:
				countB += 1
		#####
		correct = LEFT if countA > len(self.clusterA) - countA else RIGHT
		acc = (countA if countA > len(self.clusterA) - countA else (len(self.clusterA) - countA)) / len(self.clusterA)
		if correct == LEFT:
			print("Cluster A is {}, accuracy: {} ---- {}/{}".format("LEFT", acc, countA, len(self.clusterA)))
		else:
			print("Cluster A is {}, accuracy: {} ---- {}/{}".format("RIGHT", acc, len(self.clusterA) -countA, len(self.clusterA)))

		correct = RIGHT if countB > len(self.clusterB) - countB else LEFT
		acc = (countB if countB > len(self.clusterB) - countB else (len(self.clusterB) - countB)) / len(self.clusterB)
		if correct == RIGHT:
			print("Cluster B is {}, accuracy: {} ---- {}/{}".format("RIGHT", acc, countB, len(self.clusterB)))
		else:
			print("Cluster B is {}, accuracy: {} ---- {}/{}".format("LEFT", acc, len(self.clusterB) -countB, len(self.clusterB)))

		countA = 0
		countB = 0
		for x in self.data:
			if x[-1] is RIGHT:
				countA += 1
			else:
				countB += 1
		print("RIGHT is {}".format(countA))
		print("LEFT is {}".format(countB))
		print("ClusterA " + str(len(self.clusterA)))
		print("ClusterB " + str(len(self.clusterB)))


cluster = KMeans()
with open('./../Testing.csv', newline='') as csvfile:
	read = csv.reader(csvfile, delimiter=',', quotechar='"')
	i = 1
	for row in read:
		if i is 1:
			pass
		elif row[1] is "0" and i > 1 and i < 5:
			#print(row)
			node = []
			index = 0
			for x in row[2:-1]:
				if index != 8 and index != 9:
					node.append(int(x))
				index += 1
			cluster.append(node)
		if i == 5:
			i = 0
		i += 1
		
OcA = cluster.centerA
OcB = cluster.centerB
for x in range(1,100):
	cluster.updateCenter()
	#cluster.display()
	
cluster.verify()
print("Origin Center A")
print(str(OcA))
print("Origin Center B")
print(str(OcB))
print("New Center A")
print(str(cluster.centerA))
print("New Center B")
print(str(cluster.centerB))


