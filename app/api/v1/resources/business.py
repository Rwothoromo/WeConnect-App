# app/api/resources/business.py
"""Contains business logic"""

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser



# businesses list of business dictionary objects
businesses = [
    {"name": "Buyondo Hardware", "description": "One stop center for building materials...",
     "category": "Construction", "location": "Kabale", "photo": "photo"},
    {"name": "Bondo furniture", "description": "Quality imported furniture for all your needs",
     "category": "Furniture", "location": "Kampala", "photo": "photo"}
]


# RequestParser and added arguments will know which fields to accept and how to validate those
business_request_parser = RequestParser(bundle_errors=True)
business_request_parser.add_argument(
    "name", type=str, required=True, help="Business name must be a valid string")
business_request_parser.add_argument("description", required=True)
business_request_parser.add_argument("category", required=True)
business_request_parser.add_argument("location", required=True)
business_request_parser.add_argument("photo", required=True)


def get_business(name):
    """Return business if name matches"""

    for business in businesses:
        if business.get("name") == name:
            return business
    return None


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class BusinessCollection(Resource):
    """Operate on a list of Businesses, to view and add them"""

    def get(self):
        """Retrieves all businesses"""

        return jsonify(businesses)

    def post(self):
        """Register a business"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        args = business_request_parser.parse_args()
        businesses.append(args)

        # Post success
        return jsonify({"msg": "Business added", "business_data": args}), 201


class Business(Resource):
    """Operate on a single Business, to view, update and delete it"""

    def get(self, name):
        """Get a business"""

        business = get_business(name)
        if not business:
            return jsonify({"error": "Business not found"})

        return jsonify(business)

    def put(self, name):
        """Updates a business profile"""

        args = business_request_parser.parse_args()
        business = get_business(name)
        if business:
            businesses.remove(business)
            businesses.append(args)

        return jsonify(args), 201  # Update success

    def delete(self, name):
        """Remove a business"""

        business = get_business(name)
        if business:
            businesses.remove(business)

        return jsonify({"message": "Deleted"}), 204  # Delete success


class BusinessReviews(Resource):
    """Business Reviews"""

    def get(self, name):
        """Get all reviews for a business"""

        return jsonify(businesses)

    def post(self, name):
        """Add a review for a business"""

        return jsonify(businesses), 201
