# WeConnect-App
WeConnect brings businesses and users together, and allows users to review businesses.

## Features
1. Users can create an account and log in
2. Authenticated Users can register a business.
3. Only the user that creates the business can update and delete a business
4. Users can view businesses.
5. Users can give reviews about a business.
6. Users can search for businesses based on business location or business category.

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
* Run `set FLASK_APP=run.py` on command prompt
* Run `flask run` on command prompt
* View the app on `http://127.0.0.1:5000/`

**Unittests**
* Run `pytest` on command prompt


## GitHub pages
Go to [WeConnect](https://rwothoromo.github.io/WeConnect-App/)
Then navigate `app/designs/UI`
Then `user`/(`login.html`)(`register.html`)(`update.html`)
Or business/(`index.html`)(`register.html`)(`show.html`)