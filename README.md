# Display Board API

This project provides API interface to schedule activities.

# Setup
git clone https://github.com/athul-narayanan/displayboardapi.git

cd displayboardapi

# Install and prepare dependencies

pip install -r requirements.txt

docker pull postgres

docker run --name asepostgres -e POSTGRES_PASSWORD={Password} -p 5433:5432 -d postgres

docker exec -it asepostgres psql -U postgres -c "CREATE DATABASE displayboarddatabase";

python manage.py makemigrations user - make database migrations

python manage.py migrate - apply migrations to actual database

python manage.py runserver 

The above command runs the application on port 8000. Make sure that you have installed required dependencies and started postgres sql in docker.

shut it down manually with Ctrl-C.

