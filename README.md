# Display Board API

This project provides API interface to schedule activities.

## Prerequisites
Before setting up the project, you have the following installed:
1. Install Docker Desktop [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install Pgadmin 4  [Download Pgadmin 4](https://www.pgadmin.org/download/)

# Setup

clone the application using git clone https://github.com/athul-narayanan/displayboardapi.git

cd displayboardapi

# Install and prepare dependencies

1) Install and prepare dependencies using ```pip install -r requirements.txt```

2) Pull the docker image for postgres using ``` docker pull postgres```
3) Run the docker container using ```docker run --name asepostgres -e POSTGRES_PASSWORD=Algoma@2024 -p 5433:5432 -d postgres```
4) Create database in the container ```docker exec -it asepostgres psql -U postgres -c "CREATE DATABASE displayboarddatabase"```
5) Prepare database migrations for all tables using ```python manage.py makemigrations user```
6) Apply Migrations to the database using ```python manage.py migrate```
7) Add Entry for user roles by running below SQL commands
   ```sql
    INSERT INTO public.userrole (id, role_name)
    VALUES (1, 'USER');

    INSERT INTO public.userrole (id, role_name)
    VALUES (2, 'ADMIN');

    INSERT INTO public.userrole (id, role_name)
    VALUES (3, 'MASTER');
8) Run the application using ```python manage.py runserver```
   
   The above command runs the application on port 8000. Make sure that you have installed required dependencies and started postgres sql in docker.
  
10) Once the application is started cron jobs can be started using ```python manage.py runapscheduler```
11) shut down the application manually using ```Ctrl-C```

