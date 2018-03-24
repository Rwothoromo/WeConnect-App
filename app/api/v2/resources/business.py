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
    def get(self, q=None, limit=None):
        """Retrieves all businesses"""

        args = q_request_parser.parse_args()
        q = args.get('q', None)
        limit = args.get('limit', None)
        # q = 'oNd'
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
            return make_response(jsonify({"message": "No business found"}), 404)

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
                return make_response(jsonify({"message": "{} must be a string".format(key)}), 400)

        business_name = args.get("name", None)
        category_name = args.get("category", None)
        location_name = args.get("location", None)
        description = args.get("description", None)
        photo = args.get("photo", None)

        business = Business.query.filter_by(name=business_name).first()
        if not business:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category_object = Category(
                    category_name, '{} description'.format(category_name))
                db.session.add(category_object)
                db.session.commit()
                category = Category.query.filter_by(name=category_name).first()

            location = Location.query.filter_by(name=location_name).first()
            if not location:
                location_object = Location(
                    location_name, '{} description'.format(location_name))
                db.session.add(location_object)
                db.session.commit()
                location = Location.query.filter_by(name=location_name).first()

            business_object = Business(
                business_name, description, category.id, location.id, photo)

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

        business = Business.query.get(business_id)
        if business:
            user_data = request.data.get("user", None)
            if not user_data or (user_data and (user_data.id != business.created_by)):
                return make_response(jsonify({"message": "Only the Business owner can update"}), 409)

            args = business_request_parser.parse_args()
            for key, value in args.items():
                if string_empty(value):
                    return make_response(jsonify({"message": "{} must be a string".format(key)}), 400)

            business_name = args.get("name", None)
            category_name = args.get("category", None)
            location_name = args.get("location", None)
            description = args.get("description", None)
            photo = args.get("photo", None)

            # to avoid duplicating a business name
            business_by_name = Business.query.filter_by(
                name=business_name).first()
            if not business_by_name or (business_by_name and (business_by_name.id == business_id)):
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category_object = Category(
                        category_name, '{} description'.format(category_name))
                    db.session.add(category_object)
                    db.session.commit()
                    category = Category.query.filter_by(
                        name=category_name).first()

                location = Location.query.filter_by(location_name).first()
                if not location:
                    location_object = Location(
                        location_name, '{} description'.format(location_name))
                    db.session.add(location_object)
                    db.session.commit()
                    location = Location.query.filter_by(
                        name=location_name).first()

                business.name = business_name
                business.description = description
                business.category = category.id
                business.location = location.id
                business.photo = photo

                db.session.commit()

                return make_response(jsonify({"message": "Business updated"}), 200)

            return make_response(jsonify({"message": "Business by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/delete_business.yml')
    def delete(self, business_id):
        """Delete a business"""

        business = Business.query.get(business_id)
        if business:
            user_data = request.data.get("user", None)
            if not user_data or (user_data and (user_data.id != business.created_by)):
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
        if business:
            args = review_request_parser.parse_args()
            for key, value in args.items():
                if string_empty(value):
                    return make_response(jsonify({"message": "{} must be a string".format(key)}), 400)

            review_name = args.get("name", None)
            description = args.get("description", None)

            # check if review already exists
            review_by_name = Review.query.filter_by(name=review_name).first()
            if not review_by_name:
                review_object = Review(review_name, description, business_id)

                db.session.add(review_object)
                db.session.commit()

                # Post create success
                return make_response(jsonify({"message": "Business review added"}), 201)

            return make_response(jsonify({"message": "Business review by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)
