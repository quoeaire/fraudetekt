import util
import sys
import sqlite3 as db
import numpy as np
import pandas as pd
import matplotlib as mpl

print("Hello, TO {SOMETHING}")

# can add a different location if need be
# default: ./config.js
print("configuring structure...")
config = util.load_config()
DB_LOCATION             = config["keyLocation"]["database"].rstrip('/') + '/' + config["dataFilename"]["database"]
SCHEMA_LOCATION         = config["keyLocation"]["schemas"].rstrip('/') + '/' + config["dataFilename"]["schema"]
DATASET_RAW_LOCATION    = config["keyLocation"]["datasets"].rstrip('/') + '/' + config["dataFilename"]["csvUnprocessed"]
DATASET_CLEAN_LOCATION  = config["keyLocation"]["datasets"].rstrip('/') + '/' + config["dataFilename"]["csvProcessed"]

#### WORKSPACE AND CONFIG CHECKS ####
print ("checking that config locations and files exist...")

# check that locations and files exist
missing_locations = util.check_workspace(SCHEMA_LOCATION, DATASET_RAW_LOCATION)
if len(missing_locations) > 0:
    for location in missing_locations:
        print(f"\tmissing location/file: {location}")
    sys.exit() # TODO: implement some sort of logging function

#### PROCESSING ####
print(f"cleaning workspace and provided csv: {DATASET_RAW_LOCATION}")

# clean workspace
util.clean_workspace(DATASET_CLEAN_LOCATION)

# clean csv
erroneous_lines = util.clean_csv(DATASET_RAW_LOCATION, DATASET_CLEAN_LOCATION)
if erroneous_lines is not None:
    for key, value in erroneous_lines.items():
        print(f"\tline {key}: {value}")
    sys.exit()

#### DATABASE ####
# open database, create cursor
db_connection = db.connect(DB_LOCATION)
c = db_connection.cursor()
print("database connection created...\ndatabase cursor created...")

# create tables in database
with open(SCHEMA_LOCATION) as f:
    db_connection.executescript(f.read())
print("schema executed on database (if needed)...")

# read in csv
print("loading clean csv to databse...")
with open(DATASET_CLEAN_LOCATION, 'r') as f:
    for line in f:
        print(line)
        print(np.array(line.rstrip('\n').split(',')))
        # table = np.genfromtxt(f, delimiter=',', skip_header=1, dtype=str)

#### CLOSING ####
c.close()
db_connection.close()
print("database connection closed.")

# be nice
print("...goodbye!")