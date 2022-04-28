import requests
import psycopg2
from psycopg2 import Error
import json
import base64
import os
script_dir = os.path.dirname(__file__)

PRIMARY_PERSON_MODEL_FIELDS = ('local_id', 'first_name', 'last_name', 'phone', 'primary_id', )
#url = 'http://ec2-18-117-231-98.us-east-2.compute.amazonaws.com:8000'
url = 'http://127.0.0.1:8000'


def push():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="1",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="source")

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

        with open(os.path.join(script_dir, record[6]), "rb") as f:
            im_bytes = f.read()
        person_data['image'] = base64.b64encode(im_bytes).decode("utf8")
        data.append(person_data)
    header = {'content-type': 'application/json'}
    response = requests.post(f"{url}/api/data/push/", data=json.dumps({"data": data}), headers=header)

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
                                              password="1",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="source")

                cursor = connection.cursor()


if __name__ == '__main__':
    push()