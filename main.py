import os.path
import time
import json
import collections
import statistics

directory = "/media/sf_Stats/processing"
errors = 0

def parse(filename):
    with open(filename) as data_file:
        try:
            data = json.load(data_file)
            return data
        except ValueError as e :
          errors += 1

        return None

def parseall(datadir):
    for root, dirs, files in os.walk(datadir):
        boss = os.path.basename(root)
        
        for fight in files:
            data = parse(os.path.join(root, fight))
            data["boss"] = boss
            yield data

if __name__ == "__main__":
    start_time = time.time()

    analyzer = statistics.Analyzer()

    for encounter in parseall(directory):
        analyzer.consume(encounter)

    analyzer.results()

    print ("Errors:", errors)
    print("--- %s seconds ---" % (time.time() - start_time))


