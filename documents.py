from time import sleep
from flask_mongoengine import MongoEngine

db = MongoEngine() 

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    created = db.DateTimeField(required=True)
    updated = db.DateTimeField(required=True)

class Profile(db.Document):
    id_user = db.StringField(required=True)
    name = db.StringField()
    surname = db.StringField()
    phone = db.StringField()
    created = db.DateTimeField(required=True)
    updated = db.DateTimeField(required=True)

    def to_jon(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone,
            'created': self.created,
            'updated': self.update
        }