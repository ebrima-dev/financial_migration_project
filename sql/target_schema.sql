\connect postgres;

-- Terminate all other connections first
DO $$
BEGIN
   PERFORM pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE datname = 'modern_financials'
     AND pid <> pg_backend_pid();
END;
$$;


-- Drop the database if it exists
DROP DATABASE IF EXISTS modern_financials;

-- Create the new database
CREATE DATABASE modern_financials;

-- Connect to the new database
\c modern_financials;

-- Chart of Accounts
CREATE TABLE chart_of_accounts (
    account_id SERIAL PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(50) CHECK (account_type IN ('ASSET','LIABILITY','EQUITY','REVENUE','EXPENSE')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Parties (Merged Customers/Vendors)
CREATE TABLE parties (
    party_id SERIAL PRIMARY KEY,
    party_type VARCHAR(20) CHECK (party_type IN ('CUSTOMER','VENDOR')),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(50)
);

-- Transactions Header
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    description TEXT,
    source_system VARCHAR(50)
);

-- Journal Entries (Double-Entry)
CREATE TABLE journal_entries (
    journal_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(transaction_id),
    account_id INT REFERENCES chart_of_accounts(account_id),
    debit_amount DECIMAL(12,2) CHECK (debit_amount >= 0),
    credit_amount DECIMAL(12,2) CHECK (credit_amount >= 0),
    currency CHAR(3)
);

-- Audit Log
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50),
    details TEXT
);

-- Example Trigger: Log every journal entry insert
CREATE OR REPLACE FUNCTION log_journal_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (event_type, details)
    VALUES ('JOURNAL_INSERT', 'Journal entry ' || NEW.journal_id || ' added.');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_journal_insert
AFTER INSERT ON journal_entries
FOR EACH ROW
EXECUTE FUNCTION log_journal_insert();

-- Example Stored Procedure: Validate Transaction Balances
CREATE OR REPLACE FUNCTION validate_balances()
RETURNS TABLE(transaction_id INT, is_balanced BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT t.transaction_id,
           SUM(j.debit_amount) = SUM(j.credit_amount) AS is_balanced
    FROM transactions t
    JOIN journal_entries j ON t.transaction_id = j.transaction_id
    GROUP BY t.transaction_id;
END;
$$ LANGUAGE plpgsql;
