# app/models/category.py
"""Script for creating Category class objects"""

class Category(object):
    """Category class"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}