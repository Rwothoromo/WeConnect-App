# views.py

from flask import render_template

from app import app

@app.route('/')
def index():
    # return render_template("index.html")
    return 'Hello WeConnect!'

@app.route('/user/register')
def register():
    """Route to user registration page"""

    return render_template("user/register.html")

@app.route('/user/login')
def login():
    """Route to user login page"""

    return render_template("user/login.html")

@app.route('/user/update')
def update_user():
    """Route to user update page"""

    return render_template("user/update.html")

@app.route('/business')
def businesses():
    """Route to businesses list page"""

    return render_template("business/index.html")

@app.route('/business/register')
def register_business():
    """Route to businesses list page"""

    return render_template("business/register.html")

@app.route('/business/show')
def show_business():
    """Route to businesses list page"""

    return render_template("business/show.html")

@app.route('/category')
def categories():
    """Route to categories list page"""

    return render_template("category/index.html")

@app.route('/location')
def locations():
    """Route to locations list page"""

    return render_template("location/index.html")
