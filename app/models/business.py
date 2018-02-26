# app/models/business.py
"""Script for creating Business class objects"""

class Business:
    """Business class"""

    def __init__(self, name, description, category, location, photo):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.photo = photo
        self.reviews = {}
