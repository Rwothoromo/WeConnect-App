# app/api/resources/business.py
"""Contains business logic"""

from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from

from .auth import token_required, string_empty


# businesses list of business dictionary objects
businesses = []

# all reviews list of review dictionary objects
all_reviews = []


# RequestParser and added arguments will know which fields to accept and how to validate those
business_request_parser = RequestParser(bundle_errors=True)
business_request_parser.add_argument(
    "name", type=str, required=True,
    help="Business name must be a valid string")
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


def get_business_by_id(business_id):
    """Return business if business id matches"""

    for business in businesses:
        if business.get("business_id") == business_id:
            return business
    return False


def get_business_by_name(name):
    """Return business if name matches"""

    for business in businesses:
        business_data = business.get("business_data")
        if business_data["name"] == name:
            return business
    return False


def get_review_by_id(review_id):
    """Return review if review id matches"""

    for review in all_reviews:
        if review.get("review_id") == review_id:
            return review
    return False


def get_review_by_name(name):
    """Return review if name matches"""

    for review in all_reviews:
        review_data = review.get("review_data")
        if review_data["name"] == name:
            return review
    return False


def get_review(name):
    """Return review if name matches"""

    for review in all_reviews:
        if review.get("name") == name:
            return review
    return False

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

        args = business_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key + " must be a string"}), 400)

        user = request.data["user"]

        business = get_business_by_name(args["name"])
        if not business:
            business_id = len(businesses) + 1
            business_id = business_id if not get_business_by_id(
                business_id) else business_id + 1
            business = {"user_id": user.get("user_id"),
                        "business_id": business_id, "business_data": args}
            businesses.append(business)
            return make_response(
                jsonify({"message": "Business added"}), 201)

        return make_response(jsonify({"message": "Business already exists"}), 409)


class BusinessResource(Resource):
    """Operate on a single Business, to view, update and delete it"""

    @token_required
    @swag_from('docs/get_business.yml')
    def get(self, business_id):
        """Get a business"""

        business = get_business_by_id(business_id)
        if not business:
            return make_response(jsonify({"message": "Business not found"}), 404)

        return make_response(jsonify(business), 200)

    @token_required
    @swag_from('docs/put_business.yml')
    def put(self, business_id):
        """Updates a business profile"""

        args = business_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key + " must be a string"}), 400)

        user = request.data["user"]

        business = get_business_by_id(business_id)

        if business:
            # to avoid duplicating a business name
            business_by_name = get_business_by_name(args.name)
            if business_by_name['business_id'] == business_id:
                businesses.remove(business)
                business = {"user_id": user.get("user_id"),
                            "business_id": business_id, "business_data": args}
                businesses.append(business)
                return make_response(jsonify({"message": "Business updated"}), 200)

            return make_response(jsonify({"message": "Business by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/delete_business.yml')
    def delete(self, business_id):
        """Delete a business"""

        business = get_business_by_id(business_id)
        if not business:
            return make_response(jsonify({"message": "Business not found"}), 404)

        businesses.remove(business)
        return make_response(jsonify({"message": "Business deleted"}), 200)


class BusinessReviews(Resource):
    """Business Reviews"""

    @token_required
    @swag_from('docs/get_reviews.yml')
    def get(self, business_id):
        """Get all reviews for a business"""

        business = get_business_by_id(business_id)

        if business:
            reviews = [
                review for review in all_reviews if business_id == review.get("business_id")]

            if reviews:
                return make_response(jsonify(reviews), 200)
            return make_response(jsonify({"message": "Business reviews not found"}), 200)

        return make_response(jsonify({"message": "Business not found"}), 400)

    @token_required
    @swag_from('docs/post_review.yml')
    def post(self, business_id):
        """Add a review for a business"""

        user = request.data["user"]

        business = get_business_by_id(business_id)

        if business:
            args = review_request_parser.parse_args()
            for key, value in args.items():
                if string_empty(value):
                    return make_response(jsonify({"message": key + " must be a string"}), 400)

            # check if review already exists
            if not get_review_by_name(args.name):
                review_id = len(all_reviews) + 1
                review_id = review_id if not get_review_by_id(
                    review_id) else review_id + 1

                review = {
                    "user_id": user.get("user_id"),
                    "business_id": business_id,
                    "review_id": review_id,
                    "review_data": args
                }
                all_reviews.append(review)

                # Post create success
                return make_response(
                    jsonify({"message": "Business review added"}), 201)

            return make_response(
                jsonify({"message": "Business review by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 400)
