import csv


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

	def append(self, node):
		self.data.append(node)

	def calssify(self):
		self.clusterA = []
		self.clusterB = []
		index = 0
		for x in self.data:
			if distance(x, self.centerA) < distance(x, self.centerB):
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
				temp[x]+=self.data[index][x]
			temp[x]/=len(cluster)
		return	temp

	def display(self):
		#print("centerA     centerB")
		#for x, y in zip(self.centerA, self.centerB):
		#	print("%09.2f    %09.2f" % (x, y))

		print(self.centerB[0], self.centerB[1], self.centerB[2], self.centerB[3], self.centerB[4], self.centerB[5], self.centerB[6], self.centerB[7])
		#print(self.centerB)

def traversal(cluster1, cluster2):
	for x in cluster1:
		pass

cluster = KMeans()
with open('left.csv', newline='') as csvfile:
     read = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in read:
         if row[1] is "0":
            #print(row)
         	node = []
         	for x in row[2:10]:
         		node.append(int(x))
			cluster.append(node)

for x in range(1,100):
	cluster.updateCenter()
	cluster.display()
	
#Traversal	



