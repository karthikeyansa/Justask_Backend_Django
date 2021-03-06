web: pip3 install -r "requirements.txt"
release: python3 manage.py makemigrations
release: python3 manage.py migrate
release: python3 manage.py crontab remove
release: python3 manage.py crontab add .
release: python3 manage.py crontab show
release: python3 manage.py collectstatic
web: gunicorn mysite.wsgi
