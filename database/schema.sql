# DB Creation
CREATE DATABASE `wave-rider`;

# User Creation
CREATE USER 'rider'@'%' IDENTIFIED BY 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON `wave-rider`.* TO 'rider'@'%';
FLUSH PRIVILEGES;

# Tables Creation
CREATE TABLE tickers_cn (
    ts_code VARCHAR(20) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    area VARCHAR(100),
    industry VARCHAR(100),
    market VARCHAR(50),
    exchange VARCHAR(50),
    list_status CHAR(1) NOT NULL,
    list_date DATE NOT NULL,
    delist_date DATE,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ts_code),
    INDEX idx_symbol (symbol),
    INDEX idx_list_status (list_status)
);

CREATE TABLE tickers_us (
    ts_code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NULL,
    enname VARCHAR(100) NOT NULL,
    classify VARCHAR(100) NOT NULL,
    list_date DATE NOT NULL,
    delist_date DATE NULL,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    list_status CHAR(1) DEFAULT 'L' NOT NULL,
    INDEX idx_list_status (list_status)
);

CREATE TABLE tickers_hk (
    ts_code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL COMMENT 'Stock Abbreviation',
    fullname VARCHAR(255) NOT NULL COMMENT 'Full Company Name',
    enname VARCHAR(100) NOT NULL COMMENT 'English Name',
    cn_spell VARCHAR(100) NOT NULL COMMENT 'Pinyin',
    market VARCHAR(50) NOT NULL COMMENT 'Market Category',
    list_status VARCHAR(20) NOT NULL COMMENT 'Listing Status',
    list_date DATE NOT NULL COMMENT 'Listing Date',
    delist_date DATE NULL COMMENT 'Delisting Date',
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update Time',
    PRIMARY KEY (ts_code),  -- ts_code as primary key
    INDEX idx_list_status (list_status)
);

CREATE TABLE tickers_hk (
    ts_code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL COMMENT 'Stock Abbreviation',
    fullname VARCHAR(255) NOT NULL COMMENT 'Full Company Name',
    enname VARCHAR(100) NOT NULL COMMENT 'English Name',
    cn_spell VARCHAR(100) NOT NULL COMMENT 'Pinyin',
    market VARCHAR(50) NOT NULL COMMENT 'Market Category',
    list_status VARCHAR(20) NOT NULL COMMENT 'Listing Status',
    list_date DATE NOT NULL COMMENT 'Listing Date',
    delist_date DATE COMMENT 'Delisting Date',
    trade_unit FLOAT NULL COMMENT 'Trade Unit',
    isin VARCHAR(12) NULL COMMENT 'ISIN Code',
    curr_type VARCHAR(10) NULL COMMENT 'Currency Code',
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update Time',
    PRIMARY KEY (ts_code),  -- ts_code as primary key
    INDEX idx_list_status (list_status)
);

CREATE TABLE daily_prices_realtime_cn (
    code VARCHAR(20) NOT NULL COMMENT 'Stock Code',
    trade_date DATE NOT NULL COMMENT 'Trade Date',
    open FLOAT NOT NULL COMMENT 'Opening Price',
    high FLOAT NOT NULL COMMENT 'Highest Price',
    low FLOAT NOT NULL COMMENT 'Lowest Price',
    close FLOAT NOT NULL COMMENT 'Closing Price',
    pre_close FLOAT NOT NULL COMMENT 'Previous Closing Price (Adjusted)',
    chg FLOAT NOT NULL COMMENT 'Price Change',
    pct_chg FLOAT NOT NULL COMMENT 'Percentage Change (Adjusted)',
    volume FLOAT NOT NULL COMMENT 'Trading Volume (in lots)',
    amount FLOAT NOT NULL COMMENT 'Trading Amount (in thousand yuan)',
    PRIMARY KEY (code, trade_date)  -- Composite primary key
);


