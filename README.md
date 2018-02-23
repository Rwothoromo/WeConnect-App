[![Build Status](https://travis-ci.org/Rwothoromo/WeConnect-App.svg?branch=master)](https://travis-ci.org/Rwothoromo/WeConnect-App)
[![Coverage Status](https://coveralls.io/repos/github/Rwothoromo/WeConnect-App/badge.svg?branch=master)](https://coveralls.io/github/Rwothoromo/WeConnect-App?branch=master)
<a href="https://codeclimate.com/github/codeclimate/codeclimate/maintainability"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability" /></a>
<a href="https://codeclimate.com/github/codeclimate/codeclimate/test_coverage"><img src="https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage" /></a>


# WeConnect-App
WeConnect brings businesses and users together, and allows users to review businesses.

## Features
1. Users can create an account and log in
2. Authenticated Users can register a business.
3. Only the user that creates the business can update and delete a business
4. Users can view businesses.
5. Users can give reviews about a business.
6. Users can search for businesses based on business location or business category.

| EndPoint                                             | Functionality                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| [POST   /api/v1/auth/register](#)                    | Creates a user account                           |
| [POST   /api/v1/auth/login](#)                       | Logs in a user                                   |
| [POST   /api/v1/auth/logout](#)                      | Logs out a user                                  |
| [POST   /api/v1/auth/reset-password](#)              | Password reset                                   |
| [POST   /api/v1/businesses](#)                       | Register a business                              |
| [PUT    /api/v1/businesses/\<string:name>](#)        | Updates a business profile                       |
| [DELETE /api/v1/businesses/\<string:name>](#)        | Remove a business                                |
| [GET    /api/v1/businesses](#)                       | Retrieves all businesses                         |
| [GET    /api/v1/businesses/\<string:name>](#)        | Get a business                                   |
| [POST   /api/v1/businesses/\<string:name>/reviews](#)| Add a review for a business by the logged in user|
| [GET    /api/v1/businesses/\<businessId>/reviews](#) | Get all reviews for a business                   |

**Technologies**
* Python 3.6 or 2.7

**Requirements**
* Install [Python](https://www.python.org/downloads/)
* Run `pip install virtualenv` on command prompt
* Run `pip install virtualenvwrapper-win` on command prompt
* Run `set WORKON_HOME=%USERPROFILES%\Envs` on command prompt

**Setup**
* Run `git clone` this repository and `cd` into the project root.
* Run `mkvirtualenv venv` on command prompt
* Run `workon venv` on command prompt
* Run `pip install -r requirements.txt` on command prompt
* Run `set FLASK_CONFIG=development` on command prompt
* Run `set FLASK_APP=run.py` on command prompt
* Run `flask run` on command prompt
* View the app on `http://127.0.0.1:5000/`

**Use endpoints**
* Run `python app/api/app.py` on command prompt
* View the api on `http://127.0.0.1:5000/api/v1/`

**Unittests**
* Run `pytest` on command prompt


## GitHub pages
Go to [WeConnect](https://rwothoromo.github.io/WeConnect-App/)
