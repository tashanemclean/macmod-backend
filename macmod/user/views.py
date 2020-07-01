import os
import json
from datetime import datetime, timedelta

from flask import Blueprint, request, redirect, json, jsonify
from werkzeug import exceptions
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token

from macmod import db
from .models import User, Persona

user = Blueprint("user", __name__, url_prefix='/user')

@user.route("/signup/", methods=['GET', 'POST'])
def signup_user():

    user_info = request.get_json()

    if user_info is not None:

        user = User()
        persona = Persona()

        try:
            user.username = user_info['username']
            user.password = user_info['password']
            user.hash_password()
            user.save()

            persona._id = user.id
            persona.firstname = user_info['firstname']
            persona.lastname = user_info['lastname']
            persona.email = user_info['email']
            persona.address = user_info['address']
            persona.save()
        except Exception as e:
            return {"code": e.code, "message": e.args}, 500

        return {'id': str(persona._id)}, 200

    return {"code": 900, "message": "No information"}, 500

@user.route("/login/", methods=['GET', 'POST'])
def login_user():

    login_info = request.get_json()

    user = User.objects.get(username=login_info['username'])
    authorized = user.check_password(login_info['password'])

    if not authorized:
        return {'code': 999, "message": "username or password is incorrect."}, 403

    persona = Persona.objects.get(_id=user.id)

    auth_info = {
        'username': user.username,
        'firstname': persona.firstname,
        'lastname': persona.lastname,
        'email': persona.email
    }

    expires = timedelta(minutes=30) # Just 30 minutes
    access_token = create_access_token(identity=auth_info, expires_delta=expires)

    return {"token": access_token}, 200

######################
##   Error methods  ##
######################

@user.errorhandler(exceptions.HTTPException) # menu error handler
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })

    response.content_type = "application/json"

    print(response.data)

    return response