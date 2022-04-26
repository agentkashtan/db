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

6. send data to main db:
    python push_updates.py
    person must appear in the admin panel(Person)
    also you can add/delete person directly to main db from admin panel

6. send data from main to local read_db:
    python pull_updates.py
    to check data in read_db: pull_from_read_db.py

Also, if in source db person's info is updated, then it will be updated in main and "read" dbs
To add another source db to system you have to trigger push-function periodically.
To update data in read_db you have to trigger pull-function periodically passing "key" as a parameter. Key - db identifier, which must be added to the main db via admin panel.