# run.py
"""Weconnect entry point"""

from app.api.api_run import app
from flasgger import Swagger

swagger = Swagger(app)

if __name__ == '__main__':
    app.run()
