-- MySQL legacy schema + inserts (the messy DB)

-- SOURCE DATABASE (LEGACY)
CREATE DATABASE legacy_financials;
USE legacy_financials;

-- Accounts Table
CREATE TABLE acct_tbl (
    acct_id INT PRIMARY KEY AUTO_INCREMENT,
    acct_code VARCHAR(20),
    acct_name VARCHAR(255),
    acct_type VARCHAR(50),
    is_active CHAR(1)
);

-- Customers Table
CREATE TABLE cust_mstr (
    cust_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_nm VARCHAR(255),
    cust_addr TEXT,
    cust_phone VARCHAR(50)
);

-- Vendors Table
CREATE TABLE vend_mstr (
    vend_id INT PRIMARY KEY AUTO_INCREMENT,
    vend_nm VARCHAR(255),
    vend_addr TEXT,
    vend_phone VARCHAR(50)
);

-- Ledger Entries (Double-Entry)
CREATE TABLE ledger_entries (
    ledg_id INT PRIMARY KEY AUTO_INCREMENT,
    txn_id INT,
    acct_id INT,
    dr_amt DECIMAL(12,2),
    cr_amt DECIMAL(12,2),
    txn_dt DATE,
    currency CHAR(3),
    src_sys VARCHAR(50)
);

-- Invoices
CREATE TABLE inv_hdr (
    inv_id INT PRIMARY KEY AUTO_INCREMENT,
    cust_id INT,
    inv_dt DATE,
    inv_total DECIMAL(12,2),
    currency CHAR(3),
    status VARCHAR(20)
);

-- Payments
CREATE TABLE pay_tbl (
    pay_id INT PRIMARY KEY AUTO_INCREMENT,
    vend_id INT,
    pay_dt DATE,
    pay_amt DECIMAL(12,2),
    currency CHAR(3)
);

-- Insert Sample Data
INSERT INTO acct_tbl (acct_code, acct_name, acct_type, is_active) VALUES
('1000', 'Cash Account', 'ASSET', 'Y'),
('001200', 'Accounts Receivable', 'asset', 'Y'),
('sales-001', 'Sales Revenue', 'REVENUE', 'Y'),
('EXP100', 'Office Supplies', 'Expense', 'Y'),
('L001', 'Accounts Payable', 'LIABILITY', 'Y');

INSERT INTO cust_mstr (cust_nm, cust_addr, cust_phone) VALUES
('Acme Corp', '123 Elm St', '555-1234'),
('   Beta LLC   ', '45 Oak Ave', '555-5678');

INSERT INTO vend_mstr (vend_nm, vend_addr, vend_phone) VALUES
('Supply Co', '78 Maple Rd', '555-2468'),
('   Delta Traders', '99 Pine Blvd', '555-1357');

INSERT INTO ledger_entries (txn_id, acct_id, dr_amt, cr_amt, txn_dt, currency, src_sys) VALUES
(1, 1, 500.00, 0.00, '2023-01-05', 'USD', 'LEGACY_SYS'),
(1, 3, 0.00, 500.00, '2023-01-05', 'USD', 'LEGACY_SYS'),
(2, 2, 1000.00, 0.00, '2023-01-10', 'CAD', 'LEGACY_SYS'),
(2, 5, 0.00, 1000.00, '2023-01-10', 'CAD', 'LEGACY_SYS'),
(3, 4, 250.00, 0.00, '2023-01-15', 'USD', 'LEGACY_SYS'),
(3, 1, 0.00, 250.00, '2023-01-15', 'USD', 'LEGACY_SYS');

INSERT INTO inv_hdr (cust_id, inv_dt, inv_total, currency, status) VALUES
(1, '2023-01-05', 500.00, 'USD', 'PAID'),
(2, '2023-01-10', 1000.00, 'CAD', 'UNPAID');

INSERT INTO pay_tbl (vend_id, pay_dt, pay_amt, currency) VALUES
(1, '2023-01-15', 250.00, 'USD'),
(2, '2023-01-20', 300.00, 'CAD');
