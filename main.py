import os.path
import time
import json
import collections
import statistics
import threading

directory = "G:\TeraStats\processing"
#directory = "../tera_data_full"
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


def parse(filename):
    global errors
    with open(filename) as data_file:
        try:
            data = json.load(data_file)
            return data
        except:
          errors += 1

        return None

def parsedirectory(files, root):
    for fight in files:
        basedir = os.path.basename(os.path.normpath(root))
        data = parse(os.path.join(root, fight))
        if (data == None):
            continue
        translate_moonrune_classes(data)
        yield [data, basedir, fight]

def parseall(datadir):
    for root, dirs, files in os.walk(datadir):
        thread = threading.Thread(target=parsedirectory,args=(files, root),)
        thread.start()


def thread_function(files, root, analyzer):
    global loaded
    for encounter in parsedirectory(files, root):
        if loaded % 4200 == 0:
            print("\rParsing {:.4%}".format(loaded / total), end="")

        analyzer.consume(encounter[0], encounter[1], encounter[2])
        loaded += 1

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
        thread_function(files, root, analyzer)
        #thread = threading.Thread(target=thread_function, args=(files, root, analyzer), )
        #threads.append(thread)
        #thread.start()

    #for x in threads:
    #    x.join()


    print ("\rParsing {:.4%}".format(loaded / total))
    print ()

    print ("Collecting results... ")
    analyzer.results()


    print("{:-^40}".format(" {:.2f} seconds ".format(time.time() - start_time)))
    print ("Errors:", errors)


