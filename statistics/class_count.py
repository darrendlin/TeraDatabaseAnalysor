from statistics import statistic
import datetime
import collections

@statistic
class ClassCount:
    def __init__(self):
        self.data_global = {}
        self.data_region = {}
        self.data_region_date = {}

    def consume(self, encounter, basedir, filename):
        region = basedir.split(".")[0]
        timestamp = encounter["timestamp"]
        date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m')
        for member in encounter["members"]:

            if self.data_global.get(member["playerClass"]) is None:
                self.data_global[member["playerClass"]] = 0
            if self.data_region.get(region) is None:
                self.data_region_date[region] = {}
                self.data_region[region] = {}
            if self.data_region[region].get(member["playerClass"]) is None:
                self.data_region[region][member["playerClass"]] = 0
            if self.data_region_date[region].get(date) is None:
                self.data_region_date[region][date] = {}
            if self.data_region_date[region][date].get(member["playerClass"]) is None:
                self.data_region_date[region][date][member["playerClass"]] = 0

            self.data_global[member["playerClass"]] += 1
            self.data_region[region][member["playerClass"]] += 1
            self.data_region_date[region][date][member["playerClass"]] += 1

    def results(self):
        f = open('class.txt', 'w')
        for cls, count in self.data_global.items():
            f.write("{}:{}\n".format(cls, count))
        f.close()

        for region, data in self.data_region.items():
            f = open("class_"+region+".txt", 'w')
            for cls, count in data.items():
                f.write("{}:{}\n".format(cls, count))
            f.close()

        for region, data in self.data_region_date.items():
            for date, data in data.items():
                f = open("class_" + region+"_"+date+".txt", 'w')
                for cls, count in data.items():
                    f.write("{}:{}\n".format(cls, count))
                f.close()
