import csv
import random
import sys
from math import sqrt

dimension = 8
# input file name in argv
inputs = sys.argv[1]
output_file = ''
# output_file = 'range_jason.csv'


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
        self.cal_label = []
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
        # clean up cluster
        self.cluster = []
        for index in range(self.center):
            self.cluster.append([])

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

    # cal the range of each cluster
    def cal_range(self):
        _range = []
        for index, _cluster in enumerate(self.cluster):
            _cluster = list(filter(lambda x: self.cal_label[index] == self.label[x], _cluster))
            temp_range = []
            for _i in range(dimension):
                _r = []
                values = list(map(lambda clus: self.data[clus][_i], _cluster))
                _r.append(min(values))
                _r.append(max(values))
                temp_range.append(_r)
            _range.append(temp_range)

        return _range

    def get_data(self, file):
        self.data = []
        self.label = []
        with open(file, newline='\n') as csvfile:
            read = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in read:
                if row[1] == '0' and row[12] != '2':
                    self.data.append([int(value) for value in row[2:10]])
                    self.label.append(int(row[12]))

            # need complete the handle GIF later

    def update_center(self):
        self.calssify()
        for index in range(0, len(self.centers)):
            self.centers[index] = self.cal_center(self.cluster[index])

    def verify(self):
        # idle = 2
        # left = 1
        # right = 0

        # Emtpy self.cal_label
        self.cal_label = []

        # show center
        for index in range(self.center):
            print("Center " + str(index) + " " + str([int(x) for x in self.centers[index]]))

        # cal label for clusters
        for index, each_cluster in enumerate(self.cluster):
            count = [0] * self.center
            for clus in each_cluster:
                count[self.label[clus]] += 1

            # Cal greatest label in each cluster
            # show accuracy
            # major = index, count
            major = 0, -1
            for idx in range(len(count)):
                if count[idx] > major[1]:
                    major = idx, count[idx]
            if len(each_cluster) != 0:
                acc = major[1] / len(each_cluster)
            else:
                acc = 0

            self.cal_label.append(major[0])
            print("Cluster " + str(index) + " is Label " + str(major[0]) + " Accuracy: " + str(acc))
            index += 1


cluster = KMeans(inputs)

update = int(input('Update times(0 to end)\n'))
while update != 0:
    for i in range(update):
        cluster.update_center()
    cluster.verify()
    ranges = cluster.cal_range()
    print('Range of clusters 0' + str(ranges[0]))
    print('Range of clusters 1' + str(ranges[1]))
    update = int(input('Update times(0 to end)\n'))

ranges = cluster.cal_range()
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if cluster.cal_label[0] == 0:
        centers = cluster.centers
        ranges = cluster.cal_range()
    else:
        centers = cluster.centers[::-1]
        ranges = cluster.cal_range()[::-1]

    for c in centers:
        writer.writerow(c)
    for c in ranges:
        r = list(map(lambda x: str(x[0]) + ':' + str(x[1]), c))
        writer.writerow(r)
