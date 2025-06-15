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
It repeats the same queries for the 'zipcodes_two' table if available.
"""

import mysql.connector

# Connection configuration for MaxScale
config = {
    'host': '127.0.0.1',
    'port': 4006,
    'user': 'maxuser',
    'password': 'maxpwd'
}

def query_and_print(cursor, db, description, sql):
    print(f"\n--- {description} ({db}) ---")
    cursor.execute(f"USE {db}")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)

def main():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        for db in ['zipcodes_one', 'zipcodes_two']:
            # 1. Largest zipcode
            query_and_print(cursor, db, "Largest zipcode",
                            f"SELECT MAX(Zipcode) FROM {db}")

            # 2. All zipcodes where state = KY
            query_and_print(cursor, db, "All zipcodes where state = 'KY'",
                            f"SELECT * FROM {db} WHERE State = 'KY'")

            # 3. All zipcodes between 40000 and 41000
            query_and_print(cursor, db, "Zipcodes between 40000 and 41000",
                            f"SELECT * FROM {db} WHERE Zipcode BETWEEN 40000 AND 41000")

            # 4. TotalWages where state = PA
            query_and_print(cursor, db, "TotalWages where state = 'PA'",
                            f"SELECT TotalWages FROM {db} WHERE State = 'PA'")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
