# EMG PROJECT

Courses web-site built on Python Django framework.
Refer to the official documentation for more info: https://docs.djangoproject.com/en/3.1/contents/

## Setup

1. Install Python 3.8+.

2. Navigate to the project directory.

3. Create a Python virtual environment:
```bash
python -m venv env
```

4. Activate it 
```bash
source env/bin/activate
```

5. Install the dependencies
```bash
pip install -r requirements.txt
```

6. Make Migrations
```bash
python manage.py makemigrations users
```
```bash
python manage.py makemigrations
```

7. Prepare the DB
```bash
python manage.py migrate
```

## Running locally

1. Activate Python virtual environment 
```bash
source env/bin/activate
```

2. Start the website
```bash
python manage.py runserver
```

3. Navigate to http://127.0.0.1:8000/ or http://127.0.0.1:8000/admin

## SuperUser

1. Create SuperUser 
```bash
python manage.py createsuperuser
```

