# DB Creation
CREATE DATABASE `wave-rider`;

# User Creation
CREATE USER 'rider'@'%' IDENTIFIED BY '[YOUR_PASSWORD]';
GRANT ALL PRIVILEGES ON `wave-rider`.* TO 'rider'@'%';
FLUSH PRIVILEGES;

# Tables Creation
CREATE TABLE `tickers` (
    `symbol` VARCHAR(20) PRIMARY KEY,  -- Stock Symbol，Primary Key
    `name` VARCHAR(255) NOT NULL,      -- Stock Name
    `region` VARCHAR(50),              -- Country/Region (US, HK, CN etc.)
    `exchange` VARCHAR(50),            -- Market (NASDAQ, NYSE etc.）
    `ipo_date` DATE,                   -- IPO Date
    `status` VARCHAR(255),             -- Status (active, inactive, delisted, invalid, excluded etc.)
    `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE INDEX idx_status ON tickers (status);

