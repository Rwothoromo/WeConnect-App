# app/api/resources/business.py
"""Contains business logic"""

from flask import jsonify
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser

from app.models import business

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
business_request_parser.add_argument("description", type=str, required=True, help="Description must be a valid string")
business_request_parser.add_argument("category", type=str, required=True, help="Category must be a valid string")
business_request_parser.add_argument("location", type=str, required=True, help="Location must be a valid string")
business_request_parser.add_argument("photo", type=str, required=True, help="Photo must be a valid string")

business_fields = {
    'name': fields.String,
    'description': fields.String,
    'category': fields.String,
    'location': fields.String,
    'photo': fields.String
}


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

    @marshal_with(business_fields)
    def get(self):
        """Retrieves all businesses"""

        return jsonify(businesses)

    @marshal_with(business_fields)
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

    @marshal_with(business_fields)
    def get(self, name):
        """Get a business"""

        business = get_business(name)
        if not business:
            return jsonify({"error": "Business not found"})

        return jsonify(business)

    @marshal_with(business_fields)
    def put(self, name):
        """Updates a business profile"""

        args = business_request_parser.parse_args()
        business = get_business(name)
        if business:
            businesses.remove(business)
            businesses.append(args)

        return jsonify(args), 201  # Update success

    @marshal_with(business_fields)
    def delete(self, name):
        """Remove a business"""

        business = get_business(name)
        if business:
            businesses.remove(business)

        return jsonify({"message": "Deleted"}), 204  # Delete success


class BusinessReviews(Resource):
    """Business Reviews"""

    @marshal_with(business_fields)
    def get(self, name):
        """Get all reviews for a business"""

        return jsonify(businesses)

    @marshal_with(business_fields)
    def post(self, name):
        """Add a review for a business"""

        return jsonify(businesses), 201
