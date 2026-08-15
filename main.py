import sqlite3 as db
import numpy as np
import pandas as pd
import matplotlib as mpl

print("Hello, fraudetekt")

DB_LOCATION         = 'db/chase.db'
SCHEMA_LOCATION     = 'db/ledger.sql'
DATASET_LOCATION    = 'datasets/chase_y24-25.csv'

# open database, create cursor
db_connection = db.connect(DB_LOCATION)
c = db_connection.cursor()
print("database connection created...\ndatabase cursor created...")

# create tables in database
with open(SCHEMA_LOCATION) as f:
    db_connection.executescript(f.read())
print("schema executed on database (if needed)...")

# read in csv
with open(DATASET_LOCATION, 'r') as f:
    # line = np.array(f.readline().rstrip(',').split(','))
    # table = np.genfromtxt(f, delimiter=',')
    table = np.genfromtxt(f, delimiter=',', filling_values='NaN', dtype=str)
    print(table)

# clean-up
c.close()
db_connection.close()
print("database connection closed... goodbye!")