# app/models/location.py
"""Script for creating Location class objects"""

class Location(object):
    """Location class"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
