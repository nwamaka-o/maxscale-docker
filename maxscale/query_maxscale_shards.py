"""
Name: Nwamaka Okalla
Email: nuokalla@student.rtc.edu
Date: 15 June 2025
Class: CNE370

What the code does:
This script connects to a MariaDB MaxScale instance and performs the following queries:
1. Finds the largest zipcode in the 'zipcodes_one' table.
2. Retrieves all zipcodes where the state is Kentucky (KY).
3. Retrieves all zipcodes between 40000 and 41000.
4. Retrieves the TotalWages column where the state is Pennsylvania (PA).
"""

import mysql.connector

# Connection configuration
config = {
    'host': '127.0.0.1',
    'port': 4006,  # MaxScale read-write listener port
    'user': 'maxuser',
    'password': 'maxpwd',
    'database': 'zipcodes_one'
}

def query_and_print(cursor, description, sql):
    print(f"\n--- {description} ---")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)

def main():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # 1. Largest zipcode in zipcodes_one
        query_and_print(cursor, "Largest zipcode in zipcodes_one",
                        "SELECT MAX(zipcode) FROM zipcodes_one")

        # 2. All zipcodes where state = KY
        query_and_print(cursor, "All zipcodes where state = 'KY'",
                        "SELECT * FROM zipcodes_one WHERE state = 'KY'")

        # 3. All zipcodes between 40000 and 41000
        query_and_print(cursor, "Zipcodes between 40000 and 41000",
                        "SELECT * FROM zipcodes_one WHERE zipcode BETWEEN 40000 AND 41000")

        # 4. TotalWages where state = PA
        query_and_print(cursor, "TotalWages where state = 'PA'",
                        "SELECT TotalWages FROM zipcodes_one WHERE state = 'PA'")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
