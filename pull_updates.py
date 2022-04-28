import requests
import psycopg2
from psycopg2 import Error
import json
import base64
from PIL import Image
import io
from io import BytesIO
from django.core.files import File


LOCAL_PERSON_MODEL_FIELDS = ('first_name', 'last_name', 'phone', 'image', 'primary_id')
#url = 'http://ec2-18-117-231-98.us-east-2.compute.amazonaws.com:8000'
url = 'http://127.0.0.1:8000'


def pull(db_key):
    payload = {'key': db_key}
    response = requests.get(f"{url}/api/data/pull", params=payload)

    if response.status_code == 200:
        added_ids = list()

        for item in json.loads(response.text)['add']:
            if item['image_file'] is not None:
                image = Image.open(io.BytesIO(base64.b64decode(item['image_file'].encode('utf-8'))))
                image_name = f"final_images/{item['first_name']}_{item['last_name']}.{image.format.lower()}"
                image.save(image_name)
                item['image'] = image_name
            else:
                item['image'] = None
            try:
                try:
                    connection = psycopg2.connect(user="postgres",
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="db_to_read")

                    cursor = connection.cursor()
                    cursor.execute(str("""SELECT id FROM persons WHERE primary_id='{0}';""").format(item['id']))

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

                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                    added_ids.append(item['id'])
                except (Exception, Error) as error:
                    print(error)
                    continue
            except KeyError:
                pass

        deleted_ids = list()

        for item in json.loads(response.text)['delete']:
            try:
                try:
                    connection = psycopg2.connect(user="postgres",
                                                  password="123",
                                                  host="127.0.0.1",
                                                  port="5432",
                                                  database="db_to_read")

                    cursor = connection.cursor()
                    cursor.execute(str("""DELETE FROM persons WHERE primary_id='{0}';""").format(item['primary_id']))
                    connection.commit()

                    deleted_ids.append(item['primary_id'])
                except (Exception, Error) as error:
                    print(error)
                    continue
            except KeyError:
                pass

        header = {'content-type': 'application/json'}
        requests.post(f"{url}/api/data/confirm-pull/", data=json.dumps({"data_added": added_ids,
                                                                                       "data_deleted": deleted_ids,
                                                                                       "key": db_key}),
                      headers=header)


if __name__ == '__main__':
    pull('228')
