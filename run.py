from flask import redirect
from api.v1 import app

@app.route('/')
def main():  # pragma: no cover
    """Redirect to api endpoints"""

    # return redirect('/api/v1/')
    return redirect('/apidocs')

if __name__ == '__main__':
    app.run()
