1. install postgresql:
    sudo apt update
    sudo apt install postgresql postgresql-contrib

2. create test databases:
    python3 create_source_db.py
    python3 create_db_to_read.py

3. start server:
    activate virtual env: source venv/bin/activate
    install required libs: pip install -r requirements.txt
    cd project
    python3 manage.py migrate
    python3 manage.py createsuperuser (and fill fields you will be asked to)
    python3 manage.py runserver
    if everything went well, then you will be able to log into admin panel at http://127.0.0.1:8000/admin using credentials from previous step

cd ..

4. add person to source db:
    python add_to_source_db.py

5. send data to main db:
    python push_updates.py
    person must appear in the admin panel(Person)
    also you can add/delete person directly to main db from admin panel

6. send data to read_db:
    python pull_updates.py
    to check data in read_db: pull_from_read_db.py

Also, if in source db person's info is updated, then it will be updated in main and "read" dbs


