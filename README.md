# django-project

## About this project:
This is a *Tourist arrangements* web application.  
Users who are not logged in can see all available arrangements hosted on this app, but are not able to reserve any.  
In case a user would like to create a profile on this app, he should specify whether he would like to reserve arrangements (**TOURIST** user type) or to create arrangements as an agency (**AGENCY** user type).  
Users with user type AGENCY have more privileges over the TOURIST users. They can create, update, delete arrangements.  
All users on this app can update their profiles.  


## Setting up this project:
### Create a virtual environment in the django-assignement folder
How to create a virtual environment can be found here: https://docs.python.org/3/library/venv.html    

After creating the environment, run:
 ``` 
 source virtual_env_folder/bin/activate
 ```
Then, install the needed dependencies with:
```
pip3 -r install requirements3.txt
```

Now we need to setup the database for this project - PostgreSQL.

Tutorials on how to set it up and download needed packages can be found here:
* https://www.postgresql.org/download
* https://www.youtube.com/watch?v=KqcS3P32s6Y
* https://www.youtube.com/watch?v=d--mEqEUybA
* https://www.pgadmin.org/download/pgadmin-4-apt/

After we have completed this step, we need to create a database in which all the application data will be stored.  

Below are the steps on how to do it from the terminal:
```
sudo -u postgres psql
```
```
CREATE DATABASE test;
CREATE USER <username> WITH PASSWORD '<password>';
ALTER ROLE <username> SET client_encoding TO 'utf-8';
ALTER ROLE <username> SET timezone TO 'UTC';
ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE test TO username;
/q
```

After you create the database, make sure to change the db fields in the **DATABASES** section of the file **agency/agency_inner/settings.py** with the appropriate ones.
  
Then,  cd into the **django_project/agency** and run the following commands:
  ```
python manage.py makemigrations
python manage.py migrate
 ```
That should create tables and relations in the database.
  
To start the project, run:
```
python manage.py runserver 
```
and visit http://127.0.0.1:8000/ to start using the project.
  
 
  
  
## Technologies
Project is created using:
* Python V3.8.10
* Django V4.1


  
  
