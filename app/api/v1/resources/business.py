# app/api/resources/business.py
"""Contains business logic"""

from flask import jsonify
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser

from ....models.weconnect import WeConnect
from ....models.business import Business
from ....models.review import Review


weconnect = WeConnect()

all_reviews = []

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
    "username", type=str, required=True, help="Username must be a valid string")
business_request_parser.add_argument(
    "name", type=str, required=True, help="Business name must be a valid string")
business_request_parser.add_argument(
    "description", type=str, required=True, help="Description must be a valid string")
business_request_parser.add_argument(
    "category", type=str, required=True, help="Category must be a valid string")
business_request_parser.add_argument(
    "location", type=str, required=True, help="Location must be a valid string")
business_request_parser.add_argument(
    "photo", type=str, required=True, help="Photo must be a valid string")

business_fields = {
    'username': fields.String,
    'name': fields.String,
    'description': fields.String,
    'category': fields.String,
    'location': fields.String,
    'photo': fields.String
}


# for reviews
review_request_parser = RequestParser(bundle_errors=True)
review_request_parser.add_argument(
    "username", type=str, required=True, help="Username must be a valid string")
review_request_parser.add_argument(
    "name", type=str, required=True, help="Review name must be a valid string")
review_request_parser.add_argument(
    "description", type=str, required=True, help="Description must be a valid string")
review_request_parser.add_argument(
    "business", type=str, required=True, help="Business name must be a valid string")

review_fields = {
    'name': fields.String,
    'description': fields.String,
    'business': fields.String
}


def get_business(name):
    """Return business if name matches"""

    for business in businesses:
        if business.get("name") == name:
            return business
    return None

def get_review(name):
    """Return review if name matches"""

    for review in all_reviews:
        if review.get("name") == name:
            return review
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

        business = get_business(args.name)
        if not business:
            reg_business = weconnect.create_business(
                args.username, args.name, args.description, args.category, args.location, args.photo)

            if isinstance(reg_business, Business):
                businesses.append(args)
                # Post success
                return jsonify({"message": "Business added", "business_data": args}), 201
            else:
                # Unprocessable entity
                return jsonify({"message": reg_business, "business_data": args}), 422

        return jsonify({"error": "Business already exists"})


class BusinessResource(Resource):
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
            updated_business = weconnect.edit_business(
                args.username, args.name, args.description, args.category, args.location, args.photo)

            if isinstance(updated_business, Business):
                businesses.remove(business)
                businesses.append(args)
                # Post success
                return jsonify({"message": "Business updated", "business_data": args}), 201
            else:
                # Unprocessable entity
                return jsonify({"message": updated_business, "business_data": args}), 422

        return jsonify({"error": "Business not found"})

    @marshal_with(business_fields)
    def delete(self, name):
        """Remove a business"""

        args = business_request_parser.parse_args()
        business = get_business(name)
        if business:
            businesses_list = weconnect.delete_business(
                args.username, args.name)

            if name not in businesses_list.keys():
                businesses.remove(business)
                # Delete success
                return jsonify({"message": "Business deleted", "businesses": businesses}), 204
            else:
                # Unprocessable entity
                return jsonify({"message": businesses_list, "business_data": args}), 422

        return jsonify({"error": "Business not found"})


class BusinessReviews(Resource):
    """Business Reviews"""

    @marshal_with(business_fields)
    def get(self, name):
        """Get all reviews for a business"""

        business = get_business(name)
        if business:
            business_object = weconnect.businesses[name]
            business_reviews = business_object.reviews # a dictionary of reviews

            reviews = []
            for review in business_reviews:
                args = {"name": review.name, "description": review.description, "business": review.business}
                reviews.append(args)

                # update all reviews list
                if not get_review(review.name):
                    all_reviews.append(args)
                    
            return jsonify(reviews)

        return jsonify({"error": "Business not found"})

    @marshal_with(business_fields)
    def post(self, name):
        """Add a review for a business"""

        business = get_business(name)
        if business:
            business_object = weconnect.businesses[name]
            business_reviews = business_object.reviews # a dictionary of reviews

            args = review_request_parser.parse_args()

            # check if review already exists
            if not get_review(args.name):
                reg_review = weconnect.create_review(args.username, args.name, args.description, args.business)

                reviews = []
                for review in business_reviews:
                    if isinstance(reg_review, Review):
                        args = {"name": review.name, "description": review.description, "business": review.business}
                        reviews.append(args)
                        all_reviews.append(args)

                # Post success
                return jsonify({"message": "Business review added", "review_data": reviews}), 201

            return jsonify({"error": "Business already exists"})

        return jsonify({"error": "Business not found"})
