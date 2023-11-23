import json
import random


with open("dataset.json") as datafile:
    json_data = json.load(datafile)

    print(len(json_data))
    randomizer = random.randint(1, len(json_data))
    print(randomizer)
    print(json_data[str(randomizer)])