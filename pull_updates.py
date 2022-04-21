import requests
import psycopg2
from psycopg2 import Error
import json

LOCAL_PERSON_MODEL_FIELDS = ('first_name', 'last_name', 'phone', 'image', 'primary_id')


def pull(db_key):
    payload = {'key': db_key}
    response = requests.get("http://127.0.0.1:8000/api/data/pull", params=payload)

    if response.status_code == 200:
        added_ids = list()
        for item in json.loads(response.text):
            try:
                try:
                    connection = psycopg2.connect(user="postgres",
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="pull")

                    cursor = connection.cursor()
                    cursor.execute(str("""SELECT id FROM persons WHERE primary_id='{0}';""").format(item['id']))
                except (Exception, Error) as error:
                    print(error)
                    continue

                if cursor.fetchall():
                    query = str("""UPDATE persons 
                                    SET first_name = '{0}',
                                    last_name = '{1}',
                                    phone = '{2}',
                                    image = '{3}'
                                    WHERE primary_id = '{4}';""").format(item['first_name'], item['last_name'],
                                                                         item['phone'], item['image'], item['id'])
                else:
                    query = str(
                        """INSERT INTO persons (first_name, last_name, phone, image, primary_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');""").format(
                        item['first_name'], item['last_name'],
                        item['phone'], item['image'], item['id'])
                try:
                    connection = psycopg2.connect(user="postgres",
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="pull")

                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                    added_ids.append(item['id'])
                except (Exception, Error) as error:
                    print(error)
                    continue
            except KeyError:
                pass
        header = {'content-type': 'application/json'}
        requests.post("http://127.0.0.1:8000/api/data/confirm-pull/", data=json.dumps({"data": added_ids,
                                                                                       "key": db_key}),
                      headers=header)
        cursor.close()


if __name__ == '__main__':
    pull('123')
