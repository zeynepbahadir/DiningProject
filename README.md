# DiningProject with Flask RestApi

This project is a RestApi example with Flask Framework.

Project includes recipes, ingredients and users as models that have each many-to-many relationships on database. 

Recipes can have various ingredients, an ingredient can be included in various recipes.

Recipes, ingredients and users can be added, deleted and updated.

When a user is logged in, he can add himself ingredients, search recipes which includes that ingredient, get all missing ingredients on that recipe which he matched with his own ingredient.


Main libraries used:

- Flask-Smorest - Marshmallow based database-agnostic framework library 
- Flask-SQLAlchemy - adds support for SQLAlchemy ORM.
- Flask-Migrate - for handling all database migrations.
- Flask-Jwt-Extended - to create web tokens for login logout register and some special operations


Project structure:
```bash
├── README.md
├── migrations
│   ├──versions
│   │   ├── 32b45a87796e_.py
│   │   └── a1c5af0c16c5.py
│   ├── alembic.ini
│   ├── env.py
│   └── resource.py
├── models
│   ├── __init__.py
│   ├── ingredient.py
│   ├── recipe_ingredients.py
│   ├── recipe.py
│   ├── user_ingredients.py
│   ├── user_recipes.py
│   └── user.py
├── resources
│   ├── ingredient.py
│   ├── recipe.py
│   ├── user_extensive.py
│   └── user.py
├── testing
│   ├── test_ingredient.py
│   ├── test_recipe.py
│   ├── test_user_extensive.py
│   └── test_user.py
├── app.py
├── blocklist.py
├── db.py
├── docker-compose.yml
├── Dockerfile
├── Insomnia_2024-07-04.json
├── requirements.txt
└── schemas.py


```
- migrations - holds database migrations according to structural changes in database
- models - database models created according to Sqlalchemy
- resources - endpoints created with Blueprint
- testing - unit tests
- app.py - flask application initialization.
- blocklist.py - adding acces tokens to a blocklist when logout
- docker-compose.yml - create services
- Dockerfile - to build project on docker and run
- Insomnia_2024-07-04.json - insomnia project for all endpoints and usage of project
- requirements.txt - listed all requirements to run project also on docker
- schemas.py - Marshmallow schemas for all database tables (also for secondary tables)

Running
- Clone repository.
```bash
pip install requirements.txt
```
- Run following commands:
```bash
flask db init
flask db migrate
flask db upgrade
```
- Start server by running `flask run`

Usage

- on 	[localhost/swagger-ui](/swagger-ui) there are all endpoints with usages and with possible parameters and response templates with all schemas
- with Insomnia_2024-07-04.json Insomnia collections all endpoints are ready to use
- in the help of Dockerfile it is ready to run and use the project on docker
