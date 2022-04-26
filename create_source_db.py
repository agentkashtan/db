import psycopg2

#add source db
conn = psycopg2.connect(
   database="postgres", user='postgres', password='1', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''CREATE DATABASE source;''')
print('created source database')
conn.close()

conn = psycopg2.connect(
   database="source", user='postgres', password='1', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''CREATE TABLE persons (id serial PRIMARY KEY, first_name VARCHAR ( 50 ) , last_name VARCHAR ( 50 ), phone VARCHAR ( 50 ), image VARCHAR(50), primary_id integer UNIQUE, is_sync BOOLEAN NOT NULL DEFAULT FALSE);''')
print('added table to source database')
conn.close()