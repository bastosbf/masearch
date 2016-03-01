cd ../..

del db.sqlite3
python manage.py migrate auth
python manage.py migrate
python manage.py syncdb
pause