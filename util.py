import os
import sys
import json

# read and load config
def load_config(location='config.json'):
    if not os.path.isfile(location):
        print(f"(util) config file is not valid: {location}")
        sys.exit();

    with open(location) as f:
        return json.load(f)    

# check if a set of file locations exist
def check_workspace(*args):
    if len(args) < 1:
        print("(util) no locations provided to check...")
        return
    
    non_existing = []
    for location in args:
        if not os.path.exists(location):
            non_existing.append(location)

    if len(non_existing) > 0:
        print("(util) certain locations do not exist")

    return non_existing

# clean workspace by replacing previously created files with empty ones
def clean_workspace(*args):
    for location in args:
        if os.path.exists(location):
            os.remove(location)
        with open(location, "w"):
            pass

# CSV cleaning function, checks for correct number of columns and adds missing column if needed
# TAILORED FOR A CERTAIN DATASET
def clean_csv(source, destination):
    
    # ensure source and destination files exists
    if not os.path.isfile(source): 
        print("(util) source file does not exist...")
        sys.exit()

    # if not os.path.isfile(destination):
    #     print("(util) destination file does not exist...")
    #     print(f"\t(util) creating file at {destination}...")

    # build and clean csv dictionary
    # NOTE: this is specifically tailored to a certain dataset
    workingList, erroneousLines, i = [], {}, 1
    with open(source,'r') as s: 
        for line in s:
            workingLine = line.strip().rstrip(',').split(',')

            # adjust header
            if i == 1: # header = 7
                workingList.append(workingLine[:5])
                i += 1
                continue

            # if length isnt appropriate add to erroneous lines
            if len(workingLine) != 6:
                erroneousLines[i] = workingLine

            # if conditions are right, correct line
            if len(workingLine) == 5 and workingLine[4] == 'ACCT_XFER':
                workingLine.append('0.0')

            # add to workingList
            workingList.append(workingLine)
            i += 1

    # if there are errors return them, else write to destination
    if len(erroneousLines.items()) > 0:
        print("(util) source file is not clean")
        return erroneousLines
    else:
        with open(destination, 'wb') as f:
            for line in workingList:
                f.write(','.join(line).encode() + b'\n')