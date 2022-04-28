1. install postgresql(https://phoenixnap.com/kb/how-to-install-postgresql-on-ubuntu):
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql@12-main
    sudo -u postgres psql postgres
    ALTER USER postgres WITH PASSWORD '1';

2. create test databases:
    python3 create_source_db.py
    python3 create_db_to_read.py


3. (optional)start server locally:
    activate virtual env: source venv/bin/activate
    install pip if it isnt
    install required libs: pip install -r requirements.txt (psycopg2 for mac, psycopg2-binary for linux)
    cd project
    python3 create_main_db.py
    python3 manage.py migrate
    python3 manage.py createsuperuser (and fill fields you will be asked)
    python3 manage.py runserver
    if everything went well, then you will be able to log into the admin panel at http://127.0.0.1:8000/admin using credentials from the previous step

4. change url var in push_updates.py and pull_updates.py(for local server http://127.0.0.1:8000)
    admin panel username and password - ad

5. add person to local source db:
    python add_to_source_db.py
    upload image you want to add to the pictures folder
    image path "pictures/{image name}"

6. send data to main db:
    uploads folder stores images from main db
    python push_updates.py
    person must appear in the admin panel(Person)
    also you can add/delete person directly to main db from admin panel

6. send data from main to local read_db:
    final_images folder stores images from "read_db"
    python pull_updates.py
    to check data in read_db: pull_from_read_db.py

Also, if in source db person's info is updated, then it will be updated in main and "read" dbs
To add another source db to system you have to trigger push-function periodically.
To update data in read_db you have to trigger pull-function periodically passing "key" as a parameter. Key - db identifier, which must be added to the main db via admin panel.

How does the push work:
    When you add person to db, the field is_sync by default is set to false. When push function is called, all users whose field is_sync equals to false are sent to the server.
    Server receives data, add users to main db and send back their ids. The "push" program receives ids from main database and adds it to corresponding users as primary id.
    So the source database has users ids from the main database and uses it when user info is updated to update it in the main db not to create new user.


How does the pull work:
    Each "read_db" key is stored on the server and we have a relation between user obj and read_db that is stored in the main db.
    Also we have model for the deleted users, which stores their ids.

    When the "pull" function is triggered, it sends request to the server.
    Server gets db key, checks users who are does not have relation to this db and checks "deleted users" who are not connected to this db.
    All this data is sent as a response and a temp transaction model is created in main db that stores all data sent to read_db.
    When "pull" program receives response, it performs required actions and sends successfull ids back.
    Server receives data, compare it with transaction and adds all confirmed connections.(for example, if user was successfully added server makes connection between this user and db,)
                                                               so the next time pull function is called this user won't be sent)
