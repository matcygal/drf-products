python3 manage.py makemigrations products

python3 manage.py migrate --database=storage

python3 manage.py runserver 0.0.0.0:8000 --noreload