# app/api/resources/business.py
"""Contains business logic"""

import jwt
import json

from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from

from app.models.weconnect import WeConnect
from app.models.business import Business
from app.models.review import Review
from app.models.user import User
from .auth import token_required, string_empty, users


weconnect = WeConnect()

# businesses list of business dictionary objects
businesses = []

# all reviews list of review dictionary objects
all_reviews = []

# create initial category
weconnect.create_category("johndoe", "Construction", "General hardware")

# create initial location
weconnect.create_location("johndoe", "Kabale", "Opposite Topper's")


# RequestParser and added arguments will know which fields to accept and how to validate those
business_request_parser = RequestParser(bundle_errors=True)
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
    "name", type=str, required=True, help="Review name must be a valid string")
review_request_parser.add_argument(
    "description", type=str, required=True, help="Description must be a valid string")
review_request_parser.add_argument(
    "business", type=str, required=True, help="Business name must be a valid string")


def get_business_by_id(business_id):
    """Return business if business id matches"""

    for business in businesses:
        if business.get("business_id") == business_id:
            return business
    return None


def get_business_by_name(name):
    """Return business if name matches"""

    for business in businesses:
        business_data = business.get("business_data")
        if business_data["name"] == name:
            return business
    return None


def get_review_by_id(review_id):
    """Return review if review id matches"""

    for review in all_reviews:
        if review.get("review_id") == review_id:
            return review
    return None


def get_review_by_name(name):
    """Return review if name matches"""

    for review in all_reviews:
        review_data = review.get("review_data")
        if review_data["name"] == name:
            return review
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
    @swag_from('docs/get_businesses.yml')
    def get(self):
        """Retrieves all businesses"""

        if not businesses:
            return make_response(jsonify({"message": "No business found"}), 200)
        return make_response(jsonify(businesses), 200)        

    @token_required
    @swag_from('docs/post_business.yml')
    def post(self):
        """Register a business"""

        # request parsing code checks if the request is valid,
        # and returns the validated data, and an error otherwise
        # args = business_request_parser.parse_args()
        args = json.loads(request.get_data())
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key+" must be supplied"}), 400)

        user = request.data["user"]

        business = get_business_by_name(args["name"])
        if not business:
            user_data = user.get("user_data")

            # recreate user
            user_object = User(user_data["first_name"], user_data["last_name"], user_data["username"], user_data["password"])
            weconnect.register(user_object)

            reg_business = weconnect.create_business(
                user_data["username"], args["name"], args["description"], args["category"], args["location"], args["photo"])

            if isinstance(reg_business, Business):
                business_id = len(businesses) + 1

                business = {"user_id": user.get("user_id"),
                            "business_id": business_id, "business_data": args}
                businesses.append(business)

                return make_response(jsonify({"message": "Business added", "business_data": args}), 201)

            return make_response(jsonify({"message": reg_business, "business_data": args}), 400)

        return make_response(jsonify({"message": "Business already exists"}), 400)


class BusinessResource(Resource):
    """Operate on a single Business, to view, update and delete it"""

    @token_required
    def get(self, business_id):
        """Get a business"""

        business = get_business_by_id(business_id)
        if not business:
            return make_response(jsonify({"message": "Business not found"}), 404)

        return make_response(jsonify(business), 200)

    @token_required
    def put(self, business_id):
        """Updates a business profile"""

        args = business_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key+" must be supplied"}), 400)

        user = request.data["user"]

        business = get_business_by_id(business_id)

        if business:
            user_data = user.get("user_data")

            updated_business = weconnect.edit_business(
                user_data["username"], args.name, args.description, args.category, args.location, args.photo)

            if isinstance(updated_business, Business):
                businesses.remove(business)

                business = {"user_id": user.get("user_id"),
                            "business_id": business_id, "business_data": args}
                businesses.append(business)

                return make_response(jsonify({"message": "Business updated", "business": business}), 200)

            return make_response(jsonify({"message": updated_business, "business_data": args}), 400)

        return make_response(jsonify({"message": "Business not found"}), 400)

    @token_required
    def delete(self, business_id):
        """Delete a business"""

        business = get_business_by_id(business_id)
        if not business:
            return make_response(jsonify({"message": "Business not found"}), 404)

        return make_response(jsonify(business), 200)

class BusinessReviews(Resource):
    """Business Reviews"""

    @token_required
    def get(self, business_id):
        """Get all reviews for a business"""

        business = get_business_by_id(business_id)

        if business:
            reviews = [
                review for review in all_reviews if business_id == review.get("business_id")]

            return make_response(jsonify(reviews), 200) if reviews else make_response(jsonify({"message": "Business reviews not found"}), 200)

        return make_response(jsonify({"message": "Business not found"}), 400)

    @token_required
    def post(self, business_id):
        """Add a review for a business"""

        user = request.data["user"]

        business = get_business_by_id(business_id)

        if business:
            args = review_request_parser.parse_args()
            for key, value in args.items():
                if string_empty(value):
                    return make_response(jsonify({"message": key+" must be supplied"}), 400)

            # check if review already exists
            if not get_review_by_name(args.name):
                user_data = user.get("user_data")
                reg_review = weconnect.create_review(
                    user_data["username"], args.name, args.description, args.business)

                review = []
                if isinstance(reg_review, Review):
                    args = {
                        "user_id": user.get("user_id"),
                        "business_id": business_id,
                        "review_id": len(all_reviews) + 1,
                        "review_data": args
                    }
                    review.append(args)
                    all_reviews.append(args)

                # Post create success
                return make_response(jsonify({"message": "Business review added", "review": review}), 201)

            return make_response(jsonify({"message": "Business review by that name already exists", "review": args}), 400)

        return make_response(jsonify({"message": "Business not found"}), 400)
