# MaxScale Sharding with Python Query Script

## Introduction

This project demonstrates how to set up **MariaDB MaxScale** with a **sharded database architecture** using Docker Compose. It includes:

- **Two master database shards** (`master1` and `master2`)
- **A MaxScale instance** configured with `schemarouter` to distribute queries
- A **Python script** that connects to MaxScale and performs analytical queries on zip code data

The goal is to simulate horizontal sharding and demonstrate how MaxScale can route queries based on schema/database names.


## Running

### 1. Clone the Repository

```bash
git clone https://github.com/nwamaka-o/maxscale-docker.git
cd maxscale
````

### 2. Start the Docker Services

```bash
docker-compose up -d
```

This brings up:

* `master1` (serving the `zipcodes_one` database)
* `master2` (serving the `zipcodes_two` database)
* `maxscale` (routing requests via port `4006`)

### 3. Install Python Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the Python Query Script

```bash
python query_maxscale_shards.py
```

You should see console output like:

```
--- Largest zipcode in zipcodes_one ---
('99999',)

--- All zipcodes where state = 'KY' ---
('40503', 'KY', 'Lexington', 345000)
('40202', 'KY', 'Louisville', 298000)

--- Zipcodes between 40000 and 41000 ---
('40003', 'KY', 'Bagdad', 234000)
('40801', 'KY', 'Harlan', 198000)

--- TotalWages where state = 'PA' ---
(340000,)
(295000,)
```


## Configuration

### Docker Compose (`docker-compose.yml`)

This file defines three services:

* `master1` (MariaDB container with `zipcodes_one` table)
* `master2` (MariaDB container with `zipcodes_two` table)
* `maxscale` (MariaDB MaxScale container with listener on port `4006`)

### MaxScale Configuration (`maxscale.cnf.d/example.cnf`)

This uses `schemarouter` to perform schema-based sharding:

```ini
[shard1]
type=server
address=master1
port=3306
protocol=MariaDBBackend

[shard2]
type=server
address=master2
port=3306
protocol=MariaDBBackend

[Sharded-Service]
type=service
router=schemarouter
servers=shard1,shard2
user=maxuser
password=maxpwd

[Sharded-Listener]
type=listener
service=Sharded-Service
protocol=MySQLClient
port=4006
```


## MaxScale Docker-Compose Setup

### Folder Structure

```
maxscale-docker/
├── LICENSE
├── README.md
└── maxscale/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── docker-entrypoint.sh
    ├── maxscale.cnf
    ├── maxscale.cnf.d/
    │   └── example.cnf
    ├── maxscale.list
    ├── query_maxscale_shards.py
    ├── requirements.txt
    ├── sql/
    │   ├── master1/
    │   │   └── init.sql
    │   └── master2/
    │       └── init.sql
```

### Sample SQL Schema (`init.sql`)

Make sure each `init.sql` defines a table like:

```sql
CREATE TABLE zipcodes_one (
    zipcode VARCHAR(10),
    state CHAR(2),
    city VARCHAR(100),
    TotalWages INT
);

INSERT INTO zipcodes_one (zipcode, state, city, TotalWages) VALUES
('40503', 'KY', 'Lexington', 345000),
('40202', 'KY', 'Louisville', 298000),
('19103', 'PA', 'Philadelphia', 340000);
```

The second shard should use a similar script with the `zipcodes_two` table.


## Python Script Requirements

The Python script requires one dependency, listed in `requirements.txt`:

```txt
mysql-connector-python==8.3.0
```

Install it with:

```bash
pip install -r requirements.txt
```


## References

* [MariaDB MaxScale Docker](https://github.com/mariadb-corporation/maxscale-docker)
* [MaxScale SchemaRouter Documentation](https://mariadb.com/kb/en/mariadb-maxscale-230-schemarouter/)
* [GitHub Markdown Syntax](https://docs.github.com/en/get-started/writing-on-github)
