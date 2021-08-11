# WeConnect-App

[![Build Status](https://travis-ci.org/Rwothoromo/WeConnect-App.svg?branch=master)](https://travis-ci.org/Rwothoromo/WeConnect-App)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77986672d52f482abca70e59e314beba)](https://www.codacy.com/app/Rwothoromo/WeConnect-App?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Rwothoromo/WeConnect-App&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/Rwothoromo/WeConnect-App/badge.svg?branch=master)](https://coveralls.io/github/Rwothoromo/WeConnect-App?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/a5415dbb6881457126bd/maintainability)](https://codeclimate.com/github/Rwothoromo/WeConnect-App/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a5415dbb6881457126bd/test_coverage)](https://codeclimate.com/github/Rwothoromo/WeConnect-App/test_coverage)
[![CircleCI](https://circleci.com/gh/Rwothoromo/WeConnect-App/tree/master.svg?style=svg)](https://circleci.com/gh/Rwothoromo/WeConnect-App/tree/master)

WeConnect brings businesses and users together, and allows users to review businesses

## Features

1. Users can create an account and log in
2. Authenticated Users can register a business.
3. Only the user that creates the business can update and delete a business
4. Users can view businesses.
5. Users can give reviews about a business.
6. Users can search for businesses based on business location or business category.

[View on Heroku](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/)

| EndPoint                                             | Functionality                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| [POST   /api/v2/auth/register](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v2_auth_register)                    | Creates a user account                           |
| [POST   /api/v2/auth/login](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v2_auth_login)                       | Logs in a user                                   |
| [POST   /api/v2/auth/logout](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v2_auth_logout)                      | Logs out a user                                  |
| [POST   /api/v2/auth/reset-password](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v2_auth_reset_password)              | Password reset                                   |
| [POST   /api/v2/businesses](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/post_api_v2_businesses)                       | Register a business                              |
| [PUT    /api/v2/businesses/\<businessId>](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/put_api_v2_businesses_business_id)         | Updates a business profile                       |
| [DELETE /api/v2/businesses/\<businessId>](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/delete_api_v2_businesses_business_id)         | Remove a business                                |
| [GET    /api/v2/businesses](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v2_businesses)                       | Retrieves all businesses                         |
| [GET    /api/v2/businesses/\<businessId>](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v2_businesses_business_id)         | Get a business                                   |
| [POST   /api/v2/businesses/\<businessId>/reviews](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/post_api_v2_businesses_business_id_reviews) | Add a review for a business by the logged in user|
| [GET    /api/v2/businesses/\<businessId>/reviews](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v2_businesses_business_id_reviews) | Get all reviews for a business                   |

## Tested with

* [Python 3.8](https://www.python.org/downloads)
* [PostgreSQL 11](https://www.postgresql.org/download/)

## Requirements

* Install [Python](https://www.python.org/downloads/).
* Install [PostgreSQL](https://www.postgresql.org/download/).
* Run `pip install virtualenv` on command prompt.
* Run `pip install virtualenvwrapper-win` for Windows.
* Run `set WORKON_HOME=%USERPROFILES%\Envs` for Windows.

## Setup

* Run `git clone` this repository and `cd` into the project root.
* Run `createdb <weconnect_dev>` and `createdb <weconnect_test>` on the psql bash terminal.

### Docker

* Run `docker-compose down -v` to remove the volumes along with the containers.
* Run `docker compose build` to set up.
* Run `docker compose up` to start and run the entire app.
* Run `docker compose exec web python manage.py db init` in a separate terminal.

### Regular

* Run `mkvirtualenv venv` or `virtualenv venv` for Windows. `python3 -m venv ../wc-venv` for Unix/Mac.
* Run `workon venv` or `venv\Scripts\activate` for Windows. `source ../wc-venv/bin/activate` for Unix/Mac.
* Run `pip install -r requirements.txt`.
* Run `touch .env.dev` to create a file for storing environment variables. Add the following lines (use `set` for Windows instead of `export`, used here for Unix/Mac) to it:

```env
DATABASE_URL=postgresql://postgres@localhost/weconnect_dev
SECRET_KEY=some_secret_value
FLASK_CONFIG=development
FLASK_ENV=development
```

* Run `source .env.dev` to activate the environment variables on Unix/Mac.
* Run `env` to verify the above.
* Run the migrations:
  * `python manage.py db init` to create a migration repository.
  * `python manage.py db migrate` to update the migration script.
  * `python manage.py db upgrade` to apply the migration to the database.
* Run `python manage.py runserver` or `python3 run.py` to run on the default ip and port.
* View the app on `http://127.0.0.1:5000/`.

## Use endpoints

* View the api on `http://127.0.0.1:5000/api/v2/`
* Test it's usage with postman

## Use api documentation

* View the api on [Heroku](https://weconnect-api-v2-rwothoromo.herokuapp.com/apidocs/)
* View the api on `http://127.0.0.1:5000/apidocs`

## Unittests

* Set the `.env.test` file to:

```env
DATABASE_URL=postgresql://postgres@localhost/weconnect_test
SECRET_KEY=some_secret_value
FLASK_CONFIG=testing
FLASK_ENV=testing
```

### Docker Test

* Coming soon

### Regular Test

* Run `source .env`.
* Run the migrations like before.
* Run `python manage.py test` or `pytest`.

## GitHub pages

Go to [WeConnect](https://rwothoromo.github.io/WeConnect-App/)

## Notes

For detailed instructions on heroku deployments, go [here](https://medium.com/@johnkagga/deploying-a-python-flask-app-to-heroku-41250bda27d0) or [here](https://devcenter.heroku.com/articles/heroku-cli)

## Extra

* Run `find . | grep -E "(\__pycache__|\migrations|\.pytest_cache)" | xargs rm -rf` to remove unnecessary files.
