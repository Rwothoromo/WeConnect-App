from flask import redirect
from api.v2 import app

@app.route('/')
def main():  # pragma: no cover
    """Redirect to api endpoints"""

    # return redirect('/api/v2/')
    return redirect('/apidocs')

if __name__ == '__main__':
    app.run()
