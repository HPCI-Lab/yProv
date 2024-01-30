from flask import request, jsonify
import jwt
import os
from functools import wraps
from .user_handling import check_user_presence, is_blacklisted, add_to_blacklist


def auth_required(f):
    @wraps(f)  # /api/v0/route?token=secret_token
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            header_data = jwt.get_unverified_header(token)
            data = jwt.decode(token, os.getenv('SECRET_KEY', "secret_key"), algorithms=[header_data['alg'],])
            user = data["user"]
            if not check_user_presence(user):
                return jsonify({'message': 'User not valid. Please register!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token. Please log in again!'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated
