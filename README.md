# Mailing_manager

## Description
In order to retain current customers, they often use "warm-up" mailings to inform and attract customers. This project organizes and systematizes the creation and management of your newsletters.


## Requirements
- `Django`
- `psycopg2`
- `pillow`
- `django-background-tasks`

## Set Up your personal settings
Create a `conf.py` configuration file with your personal settings in the root of the project.

File content example:
```ini
# Email connection
HOST = 'smtp.mail.ru'
PORT = 465
EMAIL = 'example@mail.ru'
EMAIL_PASSWORD = '12345678'

# DataBase connection
DB_NAME = 'mailing_manager'
DB_USER = 'postgres'
DB_PASSWORD = '12345'
```
Fill out the file according to your personal data. Create a database in postgresql. The name of the database must match the name specified in the file.
## Backgrond Tasks connection
After the django-background-tasks installation (`pip install django-background-tasks`), some adjustments may need to be made (this arose due to the difference in django versions):
<br>Migrate your database: `python manage.py migrate`.
## Running
To run the project, enter the `python manage.py runserver` command in the terminal. Open a second terminal window and enter `python manage.py process_tasks` (it is necessary to monitor and execute background tasks). 
<br>Follow the link - the project is ready to use!
