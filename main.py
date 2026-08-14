import sqlite3 as db
import numpy as np
import pandas as pd
import matplotlib as mpl

print("Hello, FraudTech")

DB_LOCATION     = 'db/financial.db'
SCHEMA_LOCATION = 'db/schema.sql'

# open database, create cursor
db_connection = db.connect(DB_LOCATION)
c = db_connection.cursor()
print("database connection created...\ndatabase cursor created...")

# create tables in database
with open(SCHEMA_LOCATION) as f:
    db_connection.executescript(f.read())
print("schema executed on database (if needed)...")

# clean-up
c.close()
db_connection.close()
print("database connection closed... goodbye!")