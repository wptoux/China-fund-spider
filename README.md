# China-fund-spider
A spider for access to China's open-end fund data

## Usage 
Type the following code in the console to download or update data.  
```
python spider.py
```
The first run takes a long time, then the update will be much faster. After the operation, you can get the fund data from ./data/fund-data.db, 
which is a sqlite file. The following code describes the database table design.

```
CREATE TABLE fundValue (
    code int NOT NULL, 
    name varchar(50) NOT NULL, 
    trade_date date NOT NULL, 
    net_val decimal, 
    acc_net decimal, 
    day_growth_percent decimal
);

CREATE INDEX idx_fund ON fundValue (code, trade_date);
```
