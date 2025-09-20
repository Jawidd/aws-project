import jwt
import requests
import json
from functools import wraps
from flask import request, jsonify, current_app
import os

class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region):
        self.region = region
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        
    def verify(self, token):
        try:
            
            # Decode token without verification to see payload
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
         
            # Get JWT header to find key ID
            headers = jwt.get_unverified_header(token)
            kid = headers['kid']
            
            # Get public keys from Cognito
            url = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
            response = requests.get(url)
            keys = response.json()['keys']
            
            # Find the correct key
            key = None
            for k in keys:
                if k['kid'] == kid:
                    key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(k))
                    break
            
            if not key:
                current_app.logger.error("Key not found!")
                return False
                
            # Verify token - skip audience verification for access tokens
            token_use = unverified_payload.get('token_use')
    
            if token_use == 'access':
                # For access tokens, don't verify audience
                self.claims = jwt.decode(
                    token,
                    key,
                    algorithms=['RS256'],
                    issuer=f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}',
                    options={"verify_aud": False}
                )
            else:
                # For ID tokens, verify audience
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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            token = auth_header.split(' ')[1]  # Remove 'Bearer '
            
        if not token:
            current_app.logger.warning("Token is missing")
            return jsonify({'message': 'Token is missing'}), 401
            
        cognito_jwt_token = CognitoJwtToken(
            user_pool_id=os.getenv('REACT_APP_USER_POOL_ID'),
            user_pool_client_id=os.getenv('REACT_APP_USER_POOL_CLIENT_ID'),
            region=os.getenv('REACT_APP_AWS_REGION')
        )
        
        if not cognito_jwt_token.verify(token):
            current_app.logger.warning("Token is invalid")
            return jsonify({'message': 'Token is invalid'}), 401
            
        current_app.logger.info("Token verification successful")
        return f(cognito_jwt_token.claims, *args, **kwargs)
    return decorated



