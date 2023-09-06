# Mailing_manager

## Description
In order to retain current customers, they often use "warm-up" mailings to inform and attract customers. This project organizes and systematizes the creation and management of your newsletters.


## Requirements
- `Django`
- `psycopg2`
- `pillow`
- `django-background-tasks`
- `redis`
- `python-dotenv`

## Set Up your personal settings
Create a `conf.py` configuration file with your personal settings in the root of the project, according to the sample? specified in `.env.sample`.

Fill out the file according to your personal data. Create a database in postgresql. The name of the database must match the name specified in the file.
## Backgrond Tasks connection
After the django-background-tasks installation (`pip install django-background-tasks`), some adjustments may need to be made (this arose due to the difference in django versions):
<br>Migrate your database: `python manage.py migrate`.
## Presets
Before starting the project, create a superuser, groups, manager, and content manager by running the following commands in the terminal:
- `python manage.py csu`
- `python manage.py create_groups`
- `python manage.py create_manager`
- `python manage.py create_content_manager`
Fill in the periods of mailings with the command:
- `python manage.py fill_periods`
Also, if you wish, you can fill the blog with a command `python manage.py loaddata blog.json` or create it by yourself!
## Running
To run the project, enter the `python manage.py runserver` command in the terminal. Open a second terminal window and enter `python manage.py process_tasks` (it is necessary to monitor and execute background tasks). 
<br>Follow the link - the project is ready to use!
