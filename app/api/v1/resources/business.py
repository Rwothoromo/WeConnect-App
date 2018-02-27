# app/api/resources/business.py
"""Contains business logic"""

import jwt

from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.models.weconnect import WeConnect
from app.models.business import Business
from app.models.review import Review
from app.models.user import User
from .auth import token_required


weconnect = WeConnect()

all_reviews = []

# businesses list of business dictionary objects
businesses = [
    {"username": "johndoe", "name": "Buyondo Hardware", "description": "One stop center for building materials...",
     "category": "Construction", "location": "Kabale", "photo": "photo"}
]

# create initial user
init_user = User("john", "doe", "johndoe", "password_hash")
weconnect.register(init_user)

# create initial category
weconnect.create_category("johndoe", "Construction", "General hardware")

# create initial location
weconnect.create_location("johndoe", "Kabale", "Opposite Topper's")

# create initial business
weconnect.create_business("johndoe", "Buyondo Hardware", "One stop center for building materials...", 
"Construction", "Kabale", "photo")


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

    @token_required
    def get(self):
        """Retrieves all businesses"""

        
        print(businesses)


        return jsonify(businesses)

    @token_required
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
                return jsonify({"message": "Business added", "business_data": args})
            else:
                # Unprocessable entity
                return jsonify({"message": reg_business, "business_data": args})

        return jsonify({"error": "Business already exists"})


class BusinessResource(Resource):
    """Operate on a single Business, to view, update and delete it"""

    @token_required
    def get(self, name):
        """Get a business"""

        business = get_business(name)
        if not business:
            return jsonify({"error": "Business not found"})

        return jsonify(business)

    @token_required
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
                return jsonify({"message": "Business updated", "business_data": args})
            else:
                # Unprocessable entity
                return jsonify({"message": updated_business, "business_data": args})

        return jsonify({"error": "Business not found"})

    @token_required
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
                return jsonify({"message": "Business deleted", "businesses": businesses})
            else:
                # Unprocessable entity
                return jsonify({"message": businesses_list, "business_data": args})

        return jsonify({"error": "Business not found"})


class BusinessReviews(Resource):
    """Business Reviews"""

    @token_required
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

    @token_required
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
                return jsonify({"message": "Business review added", "review_data": reviews})

            return jsonify({"error": "Business already exists"})

        return jsonify({"error": "Business not found"})
