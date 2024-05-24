import pymysql


def create_database_and_table():
    # Connect to the MySQL server
    connection = pymysql.connect(
        host="localhost",
        user="your_username",
        password="your_password"
    )

    try:
        with connection.cursor() as cursor:
            # Create the database
            cursor.execute("CREATE DATABASE IF NOT EXISTS todo_db")

            # Use the database
            cursor.execute("USE todo_db")

            # Create the table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255) NOT NULL, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")

        print("Database and table created/exists successfully!")
    except pymysql.Error as error:
        print(f"Error: {error}")
    finally:
        # Close the connection
        connection.close()


if __name__ == "__main__":
    create_database_and_table()
