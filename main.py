import os
import time
import json
import collections


class Analysor:
    result = collections.defaultdict(int)
    errors = 0

    def parse(self, filename):
        with open(filename) as data_file:
            try:
                data = json.load(data_file)
            except ValueError as e:
                self.errors = self.errors + 1
            else:
                # pprint(data)
                for member in data["members"]:
                    playerClass = member["playerClass"]
                    self.result[playerClass] += 1

    def printstats(self):
        for key, val in self.result.items():
            print("{}: {}".format(key, val))

    def __init__(self):
        for boss in os.listdir('/media/sf_Stats/processing/'):
            # print(boss)
            for fight in os.listdir('/media/sf_Stats/processing/' + boss):
                self.parse('/media/sf_Stats/processing/' + boss + '/' + fight)
        self.printstats()


start_time = time.time()
analysor = Analysor()
print("--- %s seconds ---" % (time.time() - start_time))
