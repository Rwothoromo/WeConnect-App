# app/models/review.py
"""Script for creating Review class objects"""

class Review:
    """Review class"""

    def __init__(self, name, description, business):
        self.name = name
        self.description = description
        self.business = business
