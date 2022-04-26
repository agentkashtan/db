import psycopg2

#add main db
conn = psycopg2.connect(
   database="postgres", user='postgres', password='1', host='127.0.0.1', port='5432')
conn.autocommit = True
cursor = conn.cursor()

cursor.execute('''CREATE DATABASE main;''')
print('created main database')
conn.close()
