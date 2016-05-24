

find . -name '00*.py'
find . -name '00*.py' -delete
find . -name '*.pyc' -delete
rm -f db.sqlite3
python  manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
sudo python manage.py runserver 0.0.0.0:80
