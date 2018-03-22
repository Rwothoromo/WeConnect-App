import unittest

from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

from app.models.blacklist import Blacklist
from app.models.category import Category
from app.models.location import Location
from app.models.business import Business
from app.models.review import Review
from app.models.user import User


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    # if result.wasSuccessful() return 0 else 1
    # return the opposite boolean
    return not result.wasSuccessful()

@app.route('/')
def main():
    """Redirect to api endpoints"""

    return redirect('/api/v2/')

if __name__ == '__main__':
    manager.run()
