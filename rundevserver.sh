pip3 install django==3.2.6
pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
