
mysql -u root -pa12345

find . -name '00*.py'
find . -name '00*.py' -delete
find . -name '*.pyc' -delete
python  manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell

