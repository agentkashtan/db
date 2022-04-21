import requests
import psycopg2
from psycopg2 import Error
import json
PRIMARY_PERSON_MODEL_FIELDS = ('local_id', 'first_name', 'last_name', 'phone', 'image', 'primary_id',)


def push():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="test")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM persons WHERE is_sync is FALSE ;")
    except (Exception, Error) as error:
        print(error)
        return error
    data = list()
    for record in cursor.fetchall():
        person_data = dict()
        for idx, val in enumerate(PRIMARY_PERSON_MODEL_FIELDS):
            if record[idx] is not None:
                person_data[val] = record[idx]
        data.append(person_data)
    header = {'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/api/data/push/", data=json.dumps({"data": data}), headers=header)
    if response.status_code == 200:
        for item in json.loads(response.text):
            try:
                query = str("""UPDATE persons SET primary_id = '{0}', is_sync = TRUE WHERE id = '{1}';""").format(item['id'], item['local_id'])
                cursor.execute(query)
                connection.commit()
            except KeyError:
                pass
            except Exception as error:
                print(error)
                connection = psycopg2.connect(user="postgres",
                                              password="123",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="test")

                cursor = connection.cursor()


if __name__ == '__main__':
    push()