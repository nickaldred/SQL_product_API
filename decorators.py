from functools import wraps
from flask import Flask, jsonify, request, make_response
import jwt
import os


def token_required(f):
    """
    Implements a decorator so the function it covers can only be 
    accessed with a correct token.
    
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            #Decodes the inputted token.
            data = jwt.decode(token, os.environ.get("SECRET_KEY"), 
            algorithms=['HS256'])

        except:
            return jsonify({'message' : 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated


