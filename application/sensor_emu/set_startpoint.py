import json, random

def set_startpoint():
    """
    Sets a STARTPOINT value based on the dataset's size and writes it to an .env file.
    """
    with open("dataset.json") as datafile:
        json_data = json.load(datafile) # Load the dataset from a JSON file
        
        endpoint = round(len(json_data)/10) # Determine the upper limit for the STARTPOINT range
        startpoint = str(random.randint(1, endpoint))

        print("Setting STARTPOINT as {}".format(startpoint))

        with open(".env", "w") as f:
            f.write("STARTPOINT={}".format(startpoint)) # Write the STARTPOINT to the .env file

if __name__ == '__main__':
    set_startpoint()