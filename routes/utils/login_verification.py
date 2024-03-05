from flask import request, jsonify
import jwt
import os
from functools import wraps
from .user_handling import check_user_presence


def auth_required(f):
    @wraps(f)  # /api/v0/route
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            header_data = jwt.get_unverified_header(token)
            data = jwt.decode(token, os.getenv('SECRET_KEY', "secret_key"), algorithms=[header_data['alg'],])
            user = data["user"]
            if not check_user_presence(user):
                return jsonify({'error': 'User not valid. Please register!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Signature expired. Please log in again!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token. Please log in again!'}), 401
        except:
            return jsonify({'error': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
