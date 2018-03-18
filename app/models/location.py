# app/models/location.py


class Location:
    """Class to create a Location class object"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
