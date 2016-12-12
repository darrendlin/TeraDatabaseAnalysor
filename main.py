import os.path
import time
import json
import collections
import statistics
import threading
import traceback

directory = "E:/Tera/teraNewStats/"
errors = 0

#thanks to Loriri for these
moonrunes = {
    "인술사": "Ninja", 
    "비검사": "Reaper", 
    "정령사": "Mystic", 
    "궁수": "Archer", 
    "사제": "Priest", 
    "광전사": "Berserker", 
    "창기사": "Lancer", 
    "권술사": "Brawler", 
    "무사": "Slayer", 
    "검투사": "Warrior", 
    "마공사": "Gunner", 
    "마법사": "Sorcerer", 
}

def translate_moonrune_classes(encounter):
    for member in encounter["members"]:
        if member["playerClass"] in moonrunes:
            member["playerClass"] = moonrunes[member["playerClass"]]

def normalize(filename):
    json = ""
    with open(filename) as data_file:
        for line in data_file:
            if not (len(line) > 80 and len(line) < 200):
                json = json + line
    return json


def parse(filename):
    global errors
    try:
        data = json.loads(normalize(filename))
        return data
    except:
      errors += 1
      print(traceback.format_exc())

    return None

def thread_function(files, analyzer):
    i = 1
    for file in files:
        print("Parsing "+file+" : "+str(i)+"/"+str(len(files)))
        i += 1
        all_data = parse(os.path.join(directory, file))
        if (all_data == None):
            continue
        for data in all_data:
            translate_moonrune_classes(data["content"])
            analyzer.consume(data["content"], data["directory"])

def count_files(datadir):
    res = 0

    for root, dirs, files in os.walk(datadir):
        res += len(files)

    return res


if __name__ == "__main__":
    start_time = time.time()

    print("Counting encounters...")
    total = count_files(directory)

    print(total, "encounters")
    print("Loading statistic colectors...")

    analyzer = statistics.Analyzer()

    print("Loaded", *[type(obj).__name__ for obj in analyzer.stats])

    loaded = 0
    threads = []
    for root, dirs, files in os.walk(directory):
        thread_function(files, analyzer)

    print ("Collecting results... ")
    analyzer.results()


    print("{:-^40}".format(" {:.2f} seconds ".format(time.time() - start_time)))
    print ("Errors:", errors)


