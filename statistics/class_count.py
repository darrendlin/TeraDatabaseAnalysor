from statistics import statistic
import datetime
import os.path
from collections import defaultdict

class Class:
    def __init__(self):
        self.data = defaultdict(int)

    def consume(self, cls):
        self.data[cls] += 1

    def export(self, filename):
        f = open(filename, 'w')
        for key in self.data:
            f.write("{}:{}\n".format(key, self.data[key]))
        f.close()

@statistic
class ClassCount:
    def __init__(self):
        self.data_global = Class()
        self.data_region = defaultdict(Class)
        self.data_region_date = defaultdict(Class)

    def consume(self, encounter, basedir, filename):
        region = basedir.split(".")[0]
        timestamp = encounter["timestamp"]
        date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m')
        for member in encounter["members"]:
            self.data_global.consume(member["playerClass"])
            self.data_region[region].consume(member["playerClass"])
            self.data_region_date[(region, date)].consume(member["playerClass"])

    def results(self):

        for dirname in ["data/class/EU", "data/class/NA", "data/class/RU", "data/class/JP", "data/class/KR", "data/class/TW"]:
            if os.path.isdir(dirname): continue

            # should probably delete it here, cause if it's a file it will fail, but meh
            os.makedirs(dirname)

        self.data_global.export('data/class/global.txt')

        for region, data in self.data_region.items():
            data.export("data/class/"+region+".txt")

        for (region, date),  data in self.data_region_date.items():
            data.export("data/class/"+region+"/"+date+".txt")