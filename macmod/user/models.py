from macmod import db
from datetime import datetime
from flask_mongoengine.wtf import model_form
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Document):
    meta = {'collection': 'Users'} 
    # _id = db.ObjectIdField(default=bson.ObjectId(), primary_key=True)
    username = db.StringField(required=True, max_length=25, unique=True)
    password = db.StringField(required=True, min_length=6, max_length=150)
    active = db.BooleanField(default=True)
    createby = db.StringField(max_length=50)
    createdate = db.DateTimeField(default=datetime.now)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Persona(db.Document):
    meta = {'collection': 'Persona'}
    _id = db.ObjectIdField(primary_key=True)
    firstname = db.StringField(required=True, max_length=30)
    lastname = db.StringField(required=True, max_length=30)
    email = db.StringField(required=True, max_length=100)
    address = db.StringField(required=False, max_lenght=200)
    city_id = db.StringField(required=False, max_lenght=3)
    state_id = db.StringField(required=False, max_lenght=3)
    country_id = db.StringField(required=False, max_lenght=50)
    createdate = db.DateTimeField(default=datetime.now)
