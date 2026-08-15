import os
import sys

def clean(source, destination):
    i = 1
    if os.path.isfile(source):
        with open(source,'r') as s:
            with open(destination, 'wb') as f:
                for line in s:
                    yee = line.strip().rstrip(',').split(',')
                    if len(yee) != 6:
                        print(f"line {i} has {len(yee)} columns, expected 6")
                        print(yee)
                    i += 1
    else: 
        print("source or destination file does not exist")
        sys.exit(1)

clean('datasets/chase_y24-25.csv', 'datasets/test.csv')