from flask import request, jsonify
import jwt
import os
from functools import wraps
from .user_handling import check_user_presence
import base64
import hashlib
import requests
import json

# Configuration

INTROSPECTION_ENDPOINT = os.environ['INTROSPECTION_ENDPOINT']

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# List of required entitlements (access granted if ANY match)
REQUIRED_ENTITLEMENTS = eval(os.environ['REQUIRED_ENTITLEMENTS'])

# HTTP Basic Auth header
auth_string = CLIENT_ID+":"+CLIENT_SECRET
auth_header = "Basic " + base64.b64encode(auth_string.encode()).decode()


def introspect_token(token):
    headers = {
        "Authorization": auth_header,
        "User-Agent": "curl/8.7.1",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"token": token}

    try:
        response = requests.post(INTROSPECTION_ENDPOINT, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        #print(f"Introspection failed: {e}")
        return None


def auth_required(f):
    @wraps(f)  # /api/v0/route
    def decorated(*args, **kwargs):

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            introspection_response = introspect_token(token)

            if not introspection_response:
                return jsonify({'error': 'Token is invalid!'}), 401

            active = introspection_response.get("active", False)
            
            # Check if entitlements claim is present
            entitlements = introspection_response.get("entitlements", [])
            entitlements_str = " ".join(entitlements)

            if not active:
                return jsonify({'error': 'Token is invalid!'}), 401

            # Check if ANY of the required entitlements are present
            if not any(entitlement in entitlements for entitlement in REQUIRED_ENTITLEMENTS):
                return jsonify({'error': 'None of the required entitlements found: '+ str(REQUIRED_ENTITLEMENTS)}), 403

            # Success: Return pretty-printed JSON
            #response_body = json.dumps(introspection_response, indent=2).encode()
            user = introspection_response.get("preferred_username",None)
 
            kwargs["user"]=user

            #user = introspection_response.get("preferred_username",None)
            #if not user:
            #    return jsonify({'error': 'Something went wrong with the preferred username'}), 401

        except:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated
