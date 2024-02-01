import os

from flask import request, Blueprint, jsonify
import jwt
from .utils.user_handling import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": 'Content-Type not supported!'}), 400

    try:
        # get the request data
        data = request.json
    except:
        return jsonify({"error": "Data not valid"}), 400

    if data and check_account_valid(data):
        token = jwt.encode({'user': data["user"],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                            'iat': datetime.datetime.utcnow()},
                           os.getenv('SECRET_KEY', "secret_key"),
                           algorithm='HS256')

        return jsonify({'result': token}), 200

    return jsonify({'error': "Please register!"}), 401


@auth_bp.route("/register", methods=["POST"])
def register_user():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({"error": 'Content-Type not supported!'}), 400

    try:
        # get the request data
        data = request.json
    except:
        return jsonify({"error": "Data not valid"}), 400

    if data:
        add_user(data)
        return jsonify({"message": 'Registered!'}), 201

    return jsonify({'error': "Registration failed!"}), 401
