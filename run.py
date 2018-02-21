# run.py
"""Weconnect entry point"""

from flask import Flask

app = Flask(__name__)               # Create Flask WSGI appliction

if __name__ == '__main__':
    app.run(debug=True)
