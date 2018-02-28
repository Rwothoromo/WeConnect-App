# run.py
"""Weconnect entry point"""

from app.api.api_run import app

if __name__ == '__main__':
    app.run(debug=True)
