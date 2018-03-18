# WeConnect-App

[![Build Status](https://travis-ci.org/Rwothoromo/WeConnect-App.svg?branch=master)](https://travis-ci.org/Rwothoromo/WeConnect-App)
[![CircleCI](https://circleci.com/gh/Rwothoromo/WeConnect-App/tree/master.svg?style=svg)](https://circleci.com/gh/Rwothoromo/WeConnect-App/tree/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77986672d52f482abca70e59e314beba)](https://www.codacy.com/app/Rwothoromo/WeConnect-App?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Rwothoromo/WeConnect-App&amp;utm_campaign=Badge_Grade)
<a href='https://coveralls.io/github/Rwothoromo/WeConnect-App?branch=master'><img src='https://coveralls.io/repos/github/Rwothoromo/WeConnect-App/badge.svg?branch=master' alt='Coverage Status' /></a>
[![Maintainability](https://api.codeclimate.com/v1/badges/a5415dbb6881457126bd/maintainability)](https://codeclimate.com/github/Rwothoromo/WeConnect-App/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a5415dbb6881457126bd/test_coverage)](https://codeclimate.com/github/Rwothoromo/WeConnect-App/test_coverage)

WeConnect brings businesses and users together, and allows users to review businesses

## Features

1. Users can create an account and log in
2. Authenticated Users can register a business.
3. Only the user that creates the business can update and delete a business
4. Users can view businesses.
5. Users can give reviews about a business.
6. Users can search for businesses based on business location or business category.

[View on Heroku](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/)

| EndPoint                                             | Functionality                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| [POST   /api/v1/auth/register](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v1_auth_register)                    | Creates a user account                           |
| [POST   /api/v1/auth/login](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v1_auth_login)                       | Logs in a user                                   |
| [POST   /api/v1/auth/logout](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v1_auth_logout)                      | Logs out a user                                  |
| [POST   /api/v1/auth/reset-password](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v1_auth_reset_password)              | Password reset                                   |
| [POST   /api/v1/businesses](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/post_api_v1_businesses)                       | Register a business                              |
| [PUT    /api/v1/businesses/\<businessId>](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/put_api_v1_businesses_business_id)         | Updates a business profile                       |
| [DELETE /api/v1/businesses/\<businessId>](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/delete_api_v1_businesses_business_id)         | Remove a business                                |
| [GET    /api/v1/businesses](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v1_businesses)                       | Retrieves all businesses                         |
| [GET    /api/v1/businesses/\<businessId>](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v1_businesses_business_id)         | Get a business                                   |
| [POST   /api/v1/businesses/\<businessId>/reviews](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/post_api_v1_businesses_business_id_reviews) | Add a review for a business by the logged in user|
| [GET    /api/v1/businesses/\<businessId>/reviews](https://weconnect-app-rwothoromo.herokuapp.com/apidocs/#!/Business/get_api_v1_businesses_business_id_reviews) | Get all reviews for a business                   |

## Technologies

* Python 3.6 or 2.7

## Requirements

* Install [Python](https://www.python.org/downloads/)
* Run `pip install virtualenv` on command prompt
* Run `pip install virtualenvwrapper-win` on command prompt
* Run `set WORKON_HOME=%USERPROFILES%\Envs` on command prompt

## Setup

* Run `git clone` this repository and `cd` into the project root.
* Run `mkvirtualenv venv` on command prompt
* Run `workon venv` on command prompt
* Run `pip install -r requirements.txt` on command prompt
* Run `set FLASK_CONFIG=production` on command prompt
* Run `set FLASK_APP=run.py` on command prompt
* Run `flask run` on command prompt
* View the app on `http://127.0.0.1:5000/`

## Use endpoints

* You can proceed with the above url or run `python app/api/api_run.py` on command prompt
* View the api on `http://127.0.0.1:5000/api/v1/`
* Test it's usage with postman

## Unittests

* Run `pytest` on command prompt

## GitHub pages

Go to [WeConnect](https://rwothoromo.github.io/WeConnect-App/)
