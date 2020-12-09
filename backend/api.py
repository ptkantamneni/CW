from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager,
                         login_user, logout_user,
                         login_required, UserMixin, current_user)

from sqlalchemy import Integer, String, Date, Boolean, Float, DateTime
from datetime import datetime

app1 = Flask(__name__)

cors = CORS(app1)

#db initialization - don't change the order
app1.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://newuser:12345@localhost:5432/covidwatchers"
db1 = SQLAlchemy()
db1.init_app(app1)
migrate = Migrate(app1, db1)


#login related
app1.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app1)

class User(UserMixin, db1.Model):
    __tablename__ = 'user'
    id = db1.Column(Integer, primary_key=True)
    firstName = db1.Column(String)
    lastName = db1.Column(String)
    email = db1.Column(String)
    password = db1.Column(String)
    address = db1.Column(String)
    age = db1.Column(Integer)
    testResult = db1.Column(Boolean, nullable=True)
    testDate = db1.Column(Date, nullable=True)
    hasSymptoms = db1.Column(Boolean, nullable=True)
    symptomsOnSetDate = db1.Column(Date, nullable=True)
    riskScore = db1.Column(Float, default=0.0)

    def __init__(self, firstName, lastName, email, password, address, age, hasSymptoms):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.address = address
        self.age = age
        self.hasSymptoms = hasSymptoms

    def __repr__(self):
        return f"<User {self.name}>"

    def to_json(self):
        return {"name": self.firstName,
                "email": self.email,
                "riskScore": self.riskScore}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

class Relationship(db1.Model):
    __tablename__ = 'relationship'
    id = db1.Column(Integer, primary_key=True)
    userId = db1.Column(Integer)
    friendId = db1.Column(Integer)
    relationshipType = db1.Column(String, nullable=True)

    def __init__(self, userId, friendId, relationshipType):
        self.userId = userId
        self.friendId = friendId
        self.relationshipType = relationshipType

    def __repr__(self):
        return f"<Relationship {self.userId} {self.friendId} {self.relationshipType}>"

    def to_json(self):
        return {"userId": self.userId,
                "friendId": self.friendId,
                "relationshipType": self.relationshipType}

class Event(db1.Model):
    __tablename__ = 'event'
    id = db1.Column(Integer, primary_key=True)
    placeName = db1.Column(String)
    address = db1.Column(String)
    numPeople = db1.Column(Integer)
    socialDistanceRating = db1.Column(Integer)
    maskComplianceRating = db1.Column(Integer)
    openSpace = db1.Column(Boolean)
    riskScore = db1.Column(Float)
    createdById = db1.Column(Integer)
    checkInDate = db1.Column(DateTime, default=datetime.utcnow)
    checkOutDate = db1.Column(DateTime, default=datetime.utcnow)
    updatedDate = db1.Column(DateTime, default=datetime.utcnow)
    confirmedCases = db1.Column(Integer, default=0)

    def __init__(self, placeName, address, numPeople, socialDistanceRating, maskComplianceRating, openSpace, riskScore, createdById, checkInDate, checkOutDate, updatedDate, confirmedCases):
        self.placeName = placeName
        self.address = address
        self.numPeople = numPeople
        self.socialDistanceRating = socialDistanceRating
        self.maskComplianceRating = maskComplianceRating
        self.openSpace = openSpace
        self.riskScore = riskScore
        self.createdById = createdById
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
        self.updatedDate = updatedDate
        self.confirmedCases = confirmedCases

    def __repr__(self):
        return f"<Event {self.placeName} {self.address} {self.numPeople}>"

    def serialize(self):
        return {
            'placeName': self.placeName,
            'address': self.address,
            'numPeople': self.numPeople,
            'socialDistancing': self.socialDistanceRating,
            'maskComplianceRating': self.maskComplianceRating,
            'openSpace': self.openSpace,
            'riskScore': self.riskScore,
            'createdById': self.createdById,
            'checkInDate': self.checkInDate,
            'checkOutDate': self.checkOutDate,
            'updatedDate': self.updatedDate,
            'confirmedCases': self.confirmedCases
        }

@app1.route('/')
def hello_world():
    return 'Hello, World!'


@app1.route('/render-login', methods=['GET'])
def render_login():
    if request.method == 'GET':
        return render_template('login.html')

@app1.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data['username']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
           login_user(user)
           resp = jsonify(user.to_json())
           resp.headers['Access-Control-Allow-Credentials'] = 'true'
           resp.headers['Access-Control-Allow-Headers'] = "Content-Type"
           return resp
        else:
           return jsonify({"status": 401,
                        "reason": "Username or Password is Invalid"})

@app1.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'User is successfully logged out'}})

@app1.route('/render-home', methods=['GET'])
def render_home():
    if request.method == 'GET':
        return render_template('home.html')

@app1.route('/user_info', methods=['GET'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200,
                "message": current_user.to_json()}
    else:
        resp = {"result": 401,
                "message": "Log in to access User info"}
    return jsonify(**resp)

@app1.route('/signup', methods=['POST'])
def handle_user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = User(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],
                        address=data['address'], age=data['age'], password=data['password'], hasSymptoms=data['hasSymptoms'])
            db1.session.add(user)
            db1.session.commit()
            return {"message": f"User {user.firstName} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    else:
        return {"error": "The request Method is not valid. Expecting a POST Request"}

 
if __name__ == '__main__':
    from event_route import event
    from user_route import user
    from relationship_route import relationship
    from event_scoring_route import event_scoring
    from user_scoring_route import user_scoring
    app1.register_blueprint(event)
    app1.register_blueprint(user)
    app1.register_blueprint(relationship)
    app1.register_blueprint(event_scoring)
    app1.register_blueprint(user_scoring)
    app1.run(debug=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id).first()
