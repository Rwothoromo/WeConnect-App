# app/models/business.py
"""Code for creating Business class objects"""

class Business:
    """Class to create a Business class object"""

    def __init__(self, name, description, category, location, photo):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.photo = photo
        self.reviews = {}
