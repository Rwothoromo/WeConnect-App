# manage.py

import unittest

from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app, db


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    tests = unittest.TestLoader().discover('api/v2/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return not result.wasSuccessful()


@app.route('/')
def main():  # pragma: no cover
    """Redirect to api endpoints"""

    # return redirect('/api/v2/')
    return redirect('/apidocs')


if __name__ == '__main__':
    manager.run()
