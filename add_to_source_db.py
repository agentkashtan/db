import psycopg2
from psycopg2 import Error


def add_to_db(first_name, last_name, phone, image):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="source")

        cursor = connection.cursor()
        query = str(
                """INSERT INTO persons (first_name, last_name, phone, image) VALUES ('{0}', '{1}', '{2}', '{3}');""").format(first_name,
                                                                                                                             last_name,
                                                                                                                             phone,
                                                                                                                             image)

        cursor.execute(query)
        connection.commit()
    except (Exception, Error) as error:
        print(error)


if __name__ == '__main__':
    print('Enter your name:')
    name = input()
    print('Enter your last name:')
    last_name = input()
    print('Enter your phone:')
    phone = input()
    print('Enter image path:')
    image = input()
    add_to_db(name, last_name, phone, image)
    print('added to db')