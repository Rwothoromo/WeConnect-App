# manage.py

import unittest

from flask import redirect
from flask_script import Manager

from api.v1 import app


manager = Manager(app)


@manager.command
def test():
    """Run tests"""

    tests = unittest.TestLoader().discover('api/v1/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    return not result.wasSuccessful()


@app.route('/')
def main():  # pragma: no cover
    """Redirect to api endpoints"""

    # return redirect('/api/v1/')
    return redirect('/apidocs')


if __name__ == '__main__':
    manager.run()
