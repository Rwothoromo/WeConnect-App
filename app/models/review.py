# app/models/review.py
"""Code for creating Review class objects"""

class Review:
    """Class to create a Review class object"""

    def __init__(self, name, description, business):
        self.name = name
        self.description = description
        self.business = business
