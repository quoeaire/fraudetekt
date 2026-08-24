CREATE TABLE IF NOT EXISTS transactions (
    transaction_id       TEXT PRIMARY KEY,
    ts                   TIMESTAMP NOT NULL,
    account_id           TEXT NOT NULL,          -- cardholder/account identifier
    amount                REAL NOT NULL,
    merchant_category      TEXT,
    merchant_country         TEXT,
    card_type                 TEXT,               -- credit/debit, if available
    device_id                  TEXT,               -- IEEE-CIS only
    is_fraud                     BOOLEAN,            -- ground truth label, historical only
    ingested_at                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_txn_account_ts ON transactions(account_id, ts);
CREATE INDEX IF NOT EXISTS idx_txn_ts ON transactions(ts);

CREATE TABLE IF NOT EXISTS account_profiles (
    account_id             TEXT PRIMARY KEY,
    avg_txn_amount_30d      REAL,
    txn_count_30d             INTEGER,
    distinct_merchants_30d      INTEGER,
    distinct_countries_30d        INTEGER,
    last_txn_ts                    TIMESTAMP,
    home_country                     TEXT,
    updated_at                        TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaction_features (
    transaction_id          TEXT PRIMARY KEY REFERENCES transactions(transaction_id),
    amount_zscore            REAL,     -- vs account's historical avg
    time_since_last_txn_sec    REAL,
    is_new_merchant             BOOLEAN,
    is_new_country                BOOLEAN,
    txn_velocity_1h                 INTEGER,  -- # txns in past hour, same account
    txn_velocity_24h                  INTEGER,
    amount_pct_of_30d_avg               REAL,
    hour_of_day                           INTEGER,
    is_weekend                              BOOLEAN,
    is_fraud                                 BOOLEAN   -- carried through for training/eval
);

-- Model scoring output
CREATE TABLE IF NOT EXISTS fraud_scores (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id         TEXT REFERENCES transactions(transaction_id),
    fraud_probability        REAL NOT NULL,
    model_version              TEXT,
    scored_at                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alert queue — this is the decision layer output
CREATE TABLE IF NOT EXISTS alerts (
    alert_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id            TEXT REFERENCES transactions(transaction_id),
    fraud_probability           REAL,
    expected_loss                 REAL,     -- fraud_probability * amount, drives triage priority
    priority_rank                    INTEGER,  -- computed by decision layer given analyst capacity
    status                             TEXT DEFAULT 'open',  -- open/investigating/confirmed_fraud/false_positive/dismissed
    assigned_analyst                     TEXT,
    created_at                             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at                              TIMESTAMP
);

-- Analyst capacity constraint — feeds the triage optimization
CREATE TABLE IF NOT EXISTS analyst_capacity (
    date                DATE,
    analyst_id            TEXT,
    available_hours         REAL,
    avg_minutes_per_alert     REAL DEFAULT 15
);

-- Outcome tracking — closes the loop, lets you measure the system's actual value
CREATE TABLE IF NOT EXISTS alert_outcomes (
    alert_id             INTEGER REFERENCES alerts(alert_id),
    outcome                TEXT,        -- confirmed_fraud / false_positive
    loss_prevented            REAL,        -- if confirmed_fraud, amount stopped
    analyst_time_spent_min      REAL,
    recorded_at                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);