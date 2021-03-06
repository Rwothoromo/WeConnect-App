# app/api/resources/business.py

from flask import jsonify, make_response, request, session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flasgger import swag_from

from api.db import db
from api.v2.models.category import Category
from api.v2.models.location import Location
from api.v2.models.business import Business
from api.v2.models.review import Review
from api.v2.models.log import Log

from .auth import token_required, validate_inputs


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
q_request_parser.add_argument(
    "page", type=int, required=False, help="Businesses results page to view")
q_request_parser.add_argument(
    "location", type=str, required=False, help="Business location filter")
q_request_parser.add_argument(
    "category", type=str, required=False, help="Business category filter")


# When we write our Resources, Flask-RESTful generates the routes
# and the view handlers necessary to represent the resource over RESTful HTTP


class BusinessCollection(Resource):
    """Operate on a list of Businesses, to view and add them"""

    @token_required
    @swag_from('docs/get_businesses.yml')
    def get(self):
        """Retrieves all businesses"""

        args = q_request_parser.parse_args()
        q = args.get('q', None)
        limit = args.get('limit', None)
        page = args.get('page', 1)
        location_name = args.get('location', None)
        category_name = args.get('category', None)

        if q:
            q = q.lower()
            businesses_query = Business.query.order_by(
                Business.name).filter(Business.name.ilike('%' + q + '%'))
        else:
            businesses_query = Business.query.order_by(Business.name)

        if location_name:
            locations = Location.query.filter(
                Location.name.ilike('%' + location_name + '%'))
            if locations:
                location_ids = [location.id for location in locations]
                businesses_query = businesses_query.filter(
                    Business.location.in_(location_ids))

        if category_name:
            categories = Category.query.filter(
                Category.name.ilike('%' + category_name + '%'))
            if categories:
                category_ids = [category.id for category in categories]
                businesses_query = businesses_query.filter(
                    Business.category.in_(category_ids))

        businesses_query = businesses_query.paginate(
            page=page, per_page=limit, error_out=False)

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

        user_data = request.data["user"]
        session["user_id"] = user_data.id
        args = business_request_parser.parse_args()

        invalid_input = validate_inputs(args)
        if invalid_input:
            return make_response(jsonify(
                {"message": "{} must be a string of maximum {} characters".format(
                    invalid_input[2], invalid_input[1])}), 400)

        business_name = args.get("name", None)
        category_name = args.get("category", None)
        location_name = args.get("location", None)
        description = args.get("description", None)
        photo = args.get("photo", None)

        business = Business.query.filter_by(name=business_name).first()
        if not business:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(
                    category_name, '{} description'.format(category_name))
                db.session.add(category)
                db.session.commit()
                category = Category.query.filter_by(name=category_name).first()

                log1 = Log(
                    "Insert", "Added category: {}".format(category_name),
                    "categories", user_data.id)
                db.session.add(log1)
                db.session.commit()

            location = Location.query.filter_by(name=location_name).first()
            if not location:
                location = Location(
                    location_name, '{} description'.format(location_name))
                db.session.add(location)
                db.session.commit()
                location = Location.query.filter_by(name=location_name).first()

                log2 = Log(
                    "Insert", "Added location: {}".format(location_name), "locations", user_data.id)
                db.session.add(log2)
                db.session.commit()

            business = Business(
                business_name, description, category.id, location.id, photo)
            db.session.add(business)
            db.session.commit()

            log3 = Log(
                "Insert", "Added business: {}".format(business_name), "businesses", user_data.id)
            db.session.add(log3)
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
                return make_response(jsonify(
                    {"message": "Only the Business owner can update"}), 409)

            args = business_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify(
                    {"message": "{} must be a string of maximum {} characters".format(
                        invalid_input[2], invalid_input[1])}), 400)

            session["user_id"] = user_data.id
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
                    category = Category(
                        category_name, '{} description'.format(category_name))
                    db.session.add(category)
                    db.session.commit()
                    category = Category.query.filter_by(
                        name=category_name).first()

                    log1 = Log(
                        "Insert", "Added category: {}".format(category_name),
                        "categories", user_data.id)
                    db.session.add(log1)
                    db.session.commit()

                location = Location.query.filter_by(name=location_name).first()
                if not location:
                    location = Location(
                        location_name, '{} description'.format(location_name))
                    db.session.add(location)
                    db.session.commit()
                    location = Location.query.filter_by(
                        name=location_name).first()

                    log2 = Log(
                        "Insert", "Added location: {}".format(location_name),
                        "locations", user_data.id)
                    db.session.add(log2)
                    db.session.commit()

                business.name = business_name
                business.description = description
                business.category = category.id
                business.location = location.id
                business.photo = photo

                db.session.commit()

                log3 = Log(
                    "Update", "Updated business: {}".format(business_name),
                    "businesses", user_data.id)
                db.session.add(log3)
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
            business_name = business.name
            user_data = request.data.get("user", None)
            if not user_data or (user_data and (user_data.id != business.created_by)):
                return make_response(jsonify(
                    {"message": "Only the Business owner can delete"}), 409)

            db.session.delete(business)
            db.session.commit()

            session["user_id"] = user_data.id
            log = Log(
                "Delete", "Deleted business: {}".format(business_name), "businesses", user_data.id)
            db.session.add(log)
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

            return make_response(jsonify({"message": "Business reviews not found"}), 404)

        return make_response(jsonify({"message": "Business not found"}), 404)

    @token_required
    @swag_from('docs/post_review.yml')
    def post(self, business_id):
        """Add a review for a business"""

        user_data = request.data["user"]
        session["user_id"] = user_data.id
        business = Business.query.get(business_id)
        if business:
            args = review_request_parser.parse_args()

            invalid_input = validate_inputs(args)
            if invalid_input:
                return make_response(jsonify(
                    {"message": "{} must be a string of maximum {} characters".format(
                        invalid_input[2], invalid_input[1])}), 400)

            review_name = args.get("name", None)
            description = args.get("description", None)

            # check if review already exists
            review_by_name = Review.query.filter_by(name=review_name).first()
            if not review_by_name:
                review = Review(review_name, description, business_id)
                db.session.add(review)
                db.session.commit()

                log = Log(
                    "Insert", "Added review: {}".format(review_name), "reviews", user_data.id)
                db.session.add(log)
                db.session.commit()

                return make_response(jsonify({"message": "Business review added"}), 201)

            return make_response(jsonify(
                {"message": "Business review by that name already exists"}), 409)

        return make_response(jsonify({"message": "Business not found"}), 404)
