# app/models/review.py
"""Script for creating Review class objects"""

class Review(object):
    """Review class"""

    def __init__(self, name, description, business):
        self.name = name
        self.description = description
        self.business = business
