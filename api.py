from collections import namedtuple
from flask import Flask, json, request, jsonify, make_response
from flask_restful import Api
from documents import db, User, Profile # This is for the DataModule
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
# setting up the API and the app
app = Flask(__name__)
api = Api(app)

# configuring the database connection
DB_URI = 'mongodb+srv://Mulder:123@cluster0.woeko.mongodb.net/Customers?retryWrites=true&w=majority'
app.config['MONGODB_HOST'] = DB_URI

# JWT Setup
app.config['JWT_SECRET_KEY'] = 'codeasecretnooneguesstheywillnot'
jwt = JWTManager(app)

# Joining the database object to the app
db.init_app(app)

# Add a new user to the database. The client will do this with the help of a json body
@app.route('/register', methods=['POST'])
def add_User():
    try:
        content = request.json
       
        email = content['email']
        password = content['password']
        created = content['created']
        updated = content['updated']

        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password',400

        tempUser = User(
            email=email,
            password=password,
            created=created,
            updated=updated
        )

        tempUser.save()

        access_token = create_access_token(identity={"email":email})
        
        return {"access_token": access_token}, 200

    except AttributeError:
        return 'Please add user email and password as a JSON body request', 400

# The client requestes a user access with a login route
@app.route('/login', methods=["GET"])
def login():
    try:
        content = request.json
        email = content['email']
        password = content['password']

        if not email:
            return 'Please provide an email address', 400

        if not password:
            return 'Please provide a password', 400

        users = User.objects(email__exact=email)

        if not users:
            return 'No such a user found', 400

        for user in users:
            if password == user.password:
                access_token = create_access_token(identity={'email':email})
                return {'access_token': access_token}, 200
            else:
                return 'Login Failed', 400

    except AttributeError:
        return 'Please add user email and password as a JSON body request',400        

@app.route('/profile',methods=['GET'])
@jwt_required
def profile():
    user = get_jwt_identity()
    print(user['email'])
    content = request.json
    id_user = content['id_user']
    
    profiles = Profile.objects(id_user__exact=id_user)

    if profiles:
        return make_response(jsonify(profiles.to_json),200)

@app.route('/list_profiles', methods=['GET'])
def register():
    profiles = []
    for p in Profile.objects:
        profiles.append(p)
    return make_response(jsonify(profiles),200)

if __name__ == "__main__":
    app.run(debug=True)