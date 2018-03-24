# app/api/resources/business.py
"""Contains business logic"""

from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from

from .auth import token_required, string_empty

from app.db import db
from app.models.category import Category
from app.models.location import Location
from app.models.business import Business
from app.models.review import Review


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


# for search by name q
q_request_parser = RequestParser(bundle_errors=True)
q_request_parser.add_argument(
    "q", type=str, required=False, help="Search business by name")
q_request_parser.add_argument(
    "limit", type=int, required=False, help="Businesses results limit")


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class BusinessCollection(Resource):
    """Operate on a list of Businesses, to view and add them"""

    @token_required
    @swag_from('docs/get_businesses.yml')
    def get(self, limit=None):
        """Retrieves all businesses"""

        args = q_request_parser.parse_args()
        q = args["q"]
        limit = args["limit"]
        if q:
            q = q.lower()
            if limit:
                businesses_query = Business.query.filter(Business.name.like(
                    '%' + q + '%')).limit(limit).paginate(page=1, per_page=10, error_out=False, max_per_page=10)
            else:
                businesses_query = Business.query.filter(Business.name.like(
                    '%' + q + '%')).paginate(page=1, per_page=10, error_out=False, max_per_page=10)
        else:
            if limit:
                businesses_query = Business.query.order_by(Business.name).limit(
                    limit).paginate(page=1, per_page=10, error_out=False, max_per_page=10)
            else:
                businesses_query = Business.query.order_by(Business.name).paginate(
                    page=1, per_page=10, error_out=False, max_per_page=10)

        businesses = businesses_query.items
        if not businesses:
            return make_response(jsonify({"message": "No business found"}), 200)

        businesses_list = [business.business_as_dict()
                           for business in businesses]

        next_page = businesses_query.next_num if businesses_query.has_next else None
        prev_page = businesses_query.prev_num if businesses_query.has_prev else None

        businesses_result = {"businesses": businesses_list,
                             "next_page": next_page, "prev_page": prev_page}

        return make_response(jsonify(businesses_result), 200)

    @token_required
    @swag_from('docs/post_business.yml')
    def post(self):
        """Register a business"""

        args = business_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key + " must be a string"}), 400)

        business = Business.query.filter_by(name=args["name"]).first()
        if not business:
            category = Category.query.filter_by(name=args["category"]).first()
            if not category:
                category_object = Category(
                    args["category"], args["category"] + ' description')
                db.session.add(category_object)
                db.session.commit()
                category = Category.query.filter_by(
                    name=args["category"]).first()

            location = Location.query.filter_by(name=args["location"]).first()
            if not location:
                location_object = Location(
                    args["location"], args["location"] + ' description')
                db.session.add(location_object)
                db.session.commit()
                location = Location.query.filter_by(
                    name=args["location"]).first()

            business_object = Business(args["name"], args["description"],
                                       category.id, location.id, args["photo"])

            db.session.add(location_object)
            db.session.add(business_object)
            db.session.commit()

            return make_response(
                jsonify({"message": "Business added"}), 201)

        return make_response(jsonify({"message": "Business already exists"}), 409)


class BusinessResource(Resource):
    """Operate on a single Business, to view, update and delete it"""

    @token_required
    @swag_from('docs/get_business.yml')
    def get(self, business_id):
        """Get a business"""

        business = Business.query.get(business_id)
        if business:
            return make_response(jsonify(business.business_as_dict()), 200)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/put_business.yml')
    def put(self, business_id):
        """Updates a business profile"""

        args = business_request_parser.parse_args()
        for key, value in args.items():
            if string_empty(value):
                return make_response(jsonify({"message": key + " must be a string"}), 400)

        user_data = request.data["user"]

        business = Business.query.get(business_id)

        if business:
            if user_data.id != business.created_by:
                return make_response(jsonify({"message": "Only the Business owner can update"}), 409)

            # to avoid duplicating a business name
            business_by_name = Business.query.filter_by(name=args.name).first()
            if not business_by_name or (business_by_name and (business_by_name.id == business_id)):
                category = Category.query.filter_by(
                    name=args["category"]).first()
                if not category:
                    category_object = Category(
                        args["category"], args["category"] + ' description')
                    db.session.add(category_object)
                    db.session.commit()
                    category = Category.query.filter_by(
                        name=args["category"]).first()

                location = Location.query.filter_by(
                    name=args["location"]).first()
                if not location:
                    location_object = Location(
                        args["location"], args["location"] + ' description')
                    db.session.add(location_object)
                    db.session.commit()
                    location = Location.query.filter_by(
                        name=args["location"]).first()

                business.name = args.name
                business.description = args.description
                business.category = category.id
                business.location = location.id
                business.photo = args.photo

                db.session.commit()

                return make_response(jsonify({"message": "Business updated"}), 200)

            return make_response(jsonify({"message": "Business by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/delete_business.yml')
    def delete(self, business_id):
        """Delete a business"""

        user_data = request.data["user"]

        business = Business.query.get(business_id)
        if business:
            if user_data.id != business.created_by:
                return make_response(jsonify({"message": "Only the Business owner can delete"}), 409)

            db.session.delete(business)
            db.session.commit()

            return make_response(jsonify({"message": "Business deleted"}), 200)

        return make_response(jsonify({"message": "Business not found"}), 404)


class BusinessReviews(Resource):
    """Business Reviews"""

    @token_required
    @swag_from('docs/get_reviews.yml')
    def get(self, business_id):
        """Get all reviews for a business"""

        business = Business.query.get(business_id)

        if business:
            reviews = Review.query.filter_by(
                business=business_id).order_by(Review.name).all()

            if reviews:
                reviews_list = [review.review_as_dict() for review in reviews]

                return make_response(jsonify(reviews_list), 200)

            return make_response(jsonify({"message": "Business reviews not found"}), 200)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/post_review.yml')
    def post(self, business_id):
        """Add a review for a business"""

        business = Business.query.get(business_id)
        args = review_request_parser.parse_args()

        if business:
            for key, value in args.items():
                if string_empty(value):
                    return make_response(jsonify({"message": key + " must be a string"}), 400)

            # check if review already exists
            review_by_name = Review.query.filter_by(name=args.name).first()
            if not review_by_name:
                review_object = Review(
                    args.name, args.description, business_id)

                db.session.add(review_object)
                db.session.commit()

                # Post create success
                return make_response(
                    jsonify({"message": "Business review added"}), 201)

            return make_response(
                jsonify({"message": "Business review by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)
