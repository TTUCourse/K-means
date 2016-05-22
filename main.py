import csv
import datetime
import random
import sys
from math import sqrt


def distance(node_a, node_b):
    total = 0
    for x, y in zip(node_a, node_b):
        total += abs(x ** 2 - y ** 2)
    return sqrt(total)


class KMeans(object):
    """docstring for KMeans"""

    def __init__(self, input_file):
        super(KMeans, self).__init__()
        """generate initial center of cluster"""
        self.input_file = input_file
        self.data_type = input_file.split('/')[-1].split('_')[0].lower()
        self.data = []
        self.center = 0
        self.centers = []
        self.cluster = []
        self.label = []
        random.seed()

        if self.data_type == 'game':
            self.center = 2
        elif self.data_type == 'gif':
            self.center = 2

        # Random center & generate cluster
        # type decide the amount of center
        #
        # GIF   ==> 2
        # Game  ==> 2 (actually 3)
        for center in range(self.center):
            init_center = []
            for j in range(0, 8):
                init_center.append(random.randrange(2 ** 32))
            self.centers.append(init_center)
            self.cluster.append([])

        self.get_data(self.input_file)

    def calssify(self):
        index = 0
        for datum in self.data:
            # calculate distance to centers
            # minimum = index, dist
            minimum = 0, -1
            for idx, center in enumerate(self.centers):
                dist = distance(datum, center)
                if minimum[1] < 0 or dist < minimum[1]:
                    minimum = idx, dist

            self.cluster[minimum[0]].append(index)
            index += 1

    def cal_center(self, clus):
        new_center = []
        for x in range(0, 8):
            temp = 0
            for index in clus:
                temp += self.data[index][x]
            if len(clus) != 0:
                temp /= len(clus)
            else:
                temp = 0
            new_center.append(temp)

        return new_center

    def get_data(self, file):  # Mod complete yet
        # t = file.split('/')[-1].split('_')[0].lower()
        with open(file, newline='\n') as csvfile:
            read = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in read:
                if row[1] == '0' and row[12] != '2':
                    self.data.append([int(value) for value in row[2:10]])
                    self.label.append(int(row[12]))

            # need complete the handle GIF later

    def update_center(self):
        # clean up cluster
        for index in range(len(self.cluster)):
            self.cluster[index] = []

        self.calssify()
        for index in range(0, len(self.centers)):
            self.centers[index] = self.cal_center(self.cluster[index])

    def verify(self):
        # idle = 2
        # left = 1
        # right = 0

        # show center
        for index in range(self.center):
            print("Center " + str(index) + " " + str([int(x) for x in self.centers[index]]))

        # cal label for clusters
        for index, subcluster in enumerate(self.cluster):
            count = [0] * self.center
            for clus in subcluster:
                count[self.label[clus]] += 1

            # show accuracy
            # major = index, count
            major = 0, -1
            for idx in range(len(count)):
                if count[idx] > major[1]:
                    major = idx, count[idx]
            if len(subcluster) != 0:
                acc = major[1] / len(subcluster)
            else:
                acc = 0
            print(count)
            print("Cluster " + str(index) + " is Label " + str(major[0]) + " Accuracy: " + str(acc))
            index += 1


# input file name in argv
inputs = sys.argv[1]
cluster = KMeans(inputs)

update = int(input('Update times(0 to end)\n'))
while update != 0:
    start_time = datetime.datetime.now()
    for i in range(update):
        cluster.update_center()
    duration_time = datetime.datetime.now() - start_time
    print('Calculate time for ' + str(update) + ' update_center(datetime ver.): ' + str(duration_time))
    cluster.verify()
    update = int(input('Update times(0 to end)\n'))
