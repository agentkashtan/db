import psycopg2
from psycopg2 import Error


try:
    connection = psycopg2.connect(user="postgres",
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="db_to_read")

    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM persons;""")
    for item in cursor.fetchall():
        print(item)
    cursor.close()

except (Exception, Error) as error:
    print(error)

