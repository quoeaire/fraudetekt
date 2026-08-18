import os
import sys

def clean_workspace(location='datasets/in-use.csv'):
    if os.path.isfile(location):
        os.remove(location)
        print("cleaned workspace...")

def clean_csv(source, destination):
    
    # ensure file exists
    if not os.path.isfile(source): 
        print("source file does not exist...")
        sys.exit()

    # clean
    isClean, workingList, i = True, [], 1
    with open(source,'r') as s: 
        for line in s:
            workingLine = line.strip().rstrip(',').split(',')
            if len(workingLine) != 6:
                isClean = False
                print(f"line {i} has {len(workingLine)} columns, expected 6:\n{workingLine}")
            if len(workingLine) == 5 and workingLine[4] == 'ACCT_XFER':
                workingLine.append('0.0')
            workingList.append(workingLine)
            i += 1

    if isClean is False:
        print("source file is not clean, check output above...")
        sys.exit()
    else:
        print("source file is clean, writing to destination...")
        with open(destination, 'wb') as f:
            for line in workingList:
                f.write(','.join(line).encode() + b'\n')

    print("cleaning complete...")