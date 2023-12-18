import json, random

def set_startpoint():
    with open("dataset.json") as datafile:
        json_data = json.load(datafile)
        
        endpoint = round(len(json_data)/10)
        startpoint = str(random.randint(1, endpoint))

        print("Setting STARTPOINT as {}".format(startpoint))

        with open(".env", "w") as f:
            f.write("STARTPOINT={}".format(startpoint))

if __name__ == '__main__':
    set_startpoint()