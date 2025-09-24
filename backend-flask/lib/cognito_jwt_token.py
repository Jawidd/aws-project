import jwt
import requests
import json
from functools import wraps
from flask import request, jsonify, current_app
import os

class CognitoJwtToken:
    def __init__(self, user_pool_id=None, user_pool_client_id=None, region=None):
        self.region = region or os.getenv('REACT_APP_AWS_REGION')
        self.user_pool_id = user_pool_id or os.getenv('REACT_APP_USER_POOL_ID')
        self.user_pool_client_id = user_pool_client_id or os.getenv('REACT_APP_USER_POOL_CLIENT_ID')
        self.claims = None
        
    def verify(self, token):
        try:
            # Decode token without verification
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            headers = jwt.get_unverified_header(token)
            kid = headers['kid']
            
            # Fetch public keys from Cognito
            url = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
            response = requests.get(url)
            keys = response.json()['keys']
            
            # Find correct key
            key = next((jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(k)) for k in keys if k['kid'] == kid), None)
            if not key:
                current_app.logger.error("Key not found for JWT verification")
                return False
            
            # Verify token
            token_use = unverified_payload.get('token_use')
            if token_use == 'access':
                self.claims = jwt.decode(
                    token,
                    key,
                    algorithms=['RS256'],
                    issuer=f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}',
                    options={"verify_aud": False}
                )
            else:
                self.claims = jwt.decode(
                    token,
                    key,
                    algorithms=['RS256'],
                    audience=self.user_pool_client_id,
                    issuer=f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}'
                )
            return True
        except Exception as e:
            current_app.logger.error(f"JWT verification error: {e}")
            return False


def require_jwt(optional=False):
    """
    Decorator for Flask routes.
    optional=True allows routes to work without JWT.
    Injects claims into route function as first argument.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                if optional:
                    return f(None, *args, **kwargs)
                return jsonify({"error": "Please sign in to access this"}), 401
            
            token = auth_header.split(' ')[1]
            jwt_instance = CognitoJwtToken()
            if not jwt_instance.verify(token):
                return jsonify({"error": "Invalid token, please sign in"}), 401
            
            return f(jwt_instance.claims, *args, **kwargs)
        return wrapper
    return decorator
