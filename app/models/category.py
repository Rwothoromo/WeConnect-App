# app/models/category.py
"""Code for creating Category class objects"""

class Category:
    """Class to create a Category class object"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
