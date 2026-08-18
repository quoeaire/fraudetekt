import sqlite3 as db
import numpy as np
import pandas as pd
import matplotlib as mpl
import util

print("Hello, fraudetekt")

DB_LOCATION             = 'db/chase.db'
SCHEMA_LOCATION         = 'db/ledger.sql'
DATASET_RAW_LOCATION    = 'datasets/chase_y24-25.csv'
DATASET_CLEAN_LOCATION  = 'datasets/in-use.csv'

# clean workspace
util.clean_workspace(DATASET_CLEAN_LOCATION)

# open database, create cursor
db_connection = db.connect(DB_LOCATION)
c = db_connection.cursor()
print("database connection created...\ndatabase cursor created...")

# create tables in database
with open(SCHEMA_LOCATION) as f:
    db_connection.executescript(f.read())
print("schema executed on database (if needed)...")

# clean csv
util.clean_csv(DATASET_RAW_LOCATION, DATASET_CLEAN_LOCATION)

# read in csv
print("reading in csv...")
with open(DATASET_CLEAN_LOCATION, 'r') as f:
    for line in f:
        print(np.array(line.rstrip('\n').split(',')))
        print(line)
    # table = np.genfromtxt(f, delimiter=',', skip_header=1, dtype=str)

# clean-up
c.close()
db_connection.close()
print("database connection closed... goodbye!")