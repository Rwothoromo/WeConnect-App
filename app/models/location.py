# app/models/location.py
"""Script for creating Location class objects"""

class Location:
    """Location class"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
