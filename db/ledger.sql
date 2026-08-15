CREATE TABLE IF NOT EXISTS transactions (
    posted_date                  TIMESTAMP NOT NULL,
    transaction_type            TEXT,
    transaction_amount                 REAL NOT NULL,
    transaction_description            TEXT,
    transaction_method        TEXT
)