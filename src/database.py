import mysql.connector


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Imakash@12",
    "database": "customer_churn_db"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


if __name__ == "__main__":

    try:
        connection = get_connection()

        print("===================================")
        print("CUSTOMER CHURN DATABASE")
        print("===================================")
        print("MySQL connected successfully!")
        print("Database: customer_churn_db")

        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")

        print("\nTables:")

        for table in cursor.fetchall():
            print("-", table[0])

        cursor.close()
        connection.close()

        print("\nConnection closed successfully!")

    except mysql.connector.Error as error:

        print("===================================")
        print("MYSQL CONNECTION ERROR")
        print("===================================")
        print(error)