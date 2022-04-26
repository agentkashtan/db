import psycopg2

#add db to read
conn = psycopg2.connect(
   database="postgres", user='postgres', password='1', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()


cursor.execute('''CREATE DATABASE db_to_read;''')
print('created db to get data')
conn.close()

conn = psycopg2.connect(
   database="db_to_read", user='postgres', password='1', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''CREATE TABLE persons (id serial PRIMARY KEY, first_name VARCHAR ( 50 ) , last_name VARCHAR ( 50 ), phone VARCHAR ( 50 ), image VARCHAR(50), primary_id integer UNIQUE);''')
print('added table to the database')
cursor = conn.cursor()