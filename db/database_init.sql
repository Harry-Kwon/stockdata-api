CREATE TABLE IF NOT EXISTS meta_data (
  ticker VARCHAR(20) PRIMARY KEY,
  company_name VARCHAR(255),
  data_start_date DATE,
);

CREATE TABLE IF NOT EXISTS latest_price (
  ticker VARCHAR(20) PRIMARY KEY,
  open_price FLOAT,
  high_price FLOAT,
  low_price FLOAT,
  close_price FLOAT,
  volume INTEGER,
  updated_date DATE,
);