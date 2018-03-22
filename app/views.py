# # app/views.py
# """Routes to view pages"""

# from flask import render_template

# from app import app

# @app.route('/')
# def index():
#     """Route to home page"""

#     return render_template("home/index.html")
#     # return 'Hello WeConnect!'

# # users
# @app.route('/user/register')
# def register():
#     """Route to user registration page"""

#     return render_template("user/register.html")

# @app.route('/user/login')
# def login():
#     """Route to user login page"""

#     return render_template("user/login.html")

# @app.route('/user/update')
# def update_user():
#     """Route to user update page"""

#     return render_template("user/update.html")


# # businesses
# @app.route('/business')
# def businesses():
#     """Route to businesses list page"""

#     return render_template("business/index.html")

# @app.route('/business/register')
# def register_business():
#     """Route to business registration page"""

#     return render_template("business/register.html")

# @app.route('/business/show')
# def show_business():
#     """Route to show a business page"""

#     return render_template("business/show.html")

# @app.route('/business/update')
# def update_business():
#     """Route to update a business page"""

#     return render_template("business/update.html")


# # categories
# @app.route('/category')
# def categories():
#     """Route to categories list page"""

#     return render_template("category/index.html")

# @app.route('/category/register')
# def register_category():
#     """Route to category registration page"""

#     return render_template("category/register.html")

# @app.route('/category/update')
# def update_category():
#     """Route to update a category page"""

#     return render_template("category/update.html")


# # locations
# @app.route('/location')
# def locations():
#     """Route to locations list page"""

#     return render_template("location/index.html")

# @app.route('/location/register')
# def register_location():
#     """Route to location registration page"""

#     return render_template("location/register.html")

# @app.route('/location/update')
# def update_location():
#     """Route to update a location page"""

#     return render_template("location/update.html")
