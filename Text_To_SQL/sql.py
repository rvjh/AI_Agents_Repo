import sqlite3

try:
    # Connect to the SQLite database (creates the DB if it doesn't exist)
    connection = sqlite3.connect('student.db')
    cursor = connection.cursor()

    # Create the STUDENT table if it doesn't already exist
    table_info = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME TEXT, 
        CLASS TEXT, 
        SECTION TEXT
    );
    """
    cursor.execute(table_info)

    # Try inserting sample data
    try:
        cursor.execute('''INSERT INTO STUDENT VALUES ('Krish', 'Data Science', 'A')''') 
        cursor.execute('''INSERT INTO STUDENT VALUES ('Darius', 'Data Science', 'B')''') 
        cursor.execute('''INSERT INTO STUDENT VALUES ('Sudhanshu', 'Devops', 'C')''') 
        cursor.execute('''INSERT INTO STUDENT VALUES ('Vikash', 'Data Science', 'C')''') 
    except sqlite3.IntegrityError as e:
        print(f"Data insertion skipped due to: {e}")
    except Exception as e:
        print(f"Unexpected error during data insertion: {e}")

    # Show all records in the table
    print("Current records in STUDENT table:")
    cursor.execute("SELECT * FROM STUDENT")
    for row in cursor.fetchall():
        print(row)

    # Commit the changes
    connection.commit()

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if connection:
        connection.close()
