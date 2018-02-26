# app/models/location.py
"""Code for creating Location class objects"""

class Location:
    """Class to create a Location class object"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
