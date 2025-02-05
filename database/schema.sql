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
    list_status ENUM('L', 'D', 'P') NOT NULL,
    list_date DATE NOT NULL,
    delist_date DATE,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ts_code),
    INDEX idx_symbol (symbol),
    INDEX idx_list_status (list_status)
);


