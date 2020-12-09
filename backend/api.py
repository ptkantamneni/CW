from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Date, Boolean, Float, DateTime

# import event_route
    
app1 = Flask(__name__)

cors = CORS(app1)

#db initialization - don't change the order
app1.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://newuser:12345@localhost:5432/covidwatchers"
db1 = SQLAlchemy()
db1.init_app(app1)
migrate = Migrate(app1, db1)

class User(db1.Model):
    __tablename__ = 'user'
    id = db1.Column(Integer, primary_key=True)
    firstName = db1.Column(String)
    lastName = db1.Column(String)
    email = db1.Column(String)
    address = db1.Column(String)
    age = db1.Column(Integer)
    testResult = db1.Column(String, nullable=True)
    testDate = db1.Column(Date, nullable=True)
    hasSymptoms = db1.Column(Boolean, nullable=True)
    symptomsOnSetDate = db1.Column(Date, nullable=True)

    def __init__(self, firstName, lastName, email, address, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.address = address
        self.age = age

    def __repr__(self):
        return f"<User {self.name}>"


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
    checkInDate = db1.Column(DateTime)
    checkOutDate = db1.Column(DateTime)
    updatedDate = db1.Column(DateTime)

    def __init__(self, placeName, address, numPeople, socialDistanceRating, maskComplianceRating, openSpace, riskScore, createdById, checkInDate, checkOutDate, updatedDate):
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

    def __repr__(self):
        return f"<Event {self.placeName} {self.address} {self.numPeople}>"

@app1.route('/')
def hello_world():
    return 'Hello, World!'

# @app.route('/signup', methods=['POST'])
# def signup():
#     if request.method == 'POST':
#         return perform_signup()
#
# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         return perform_login()
#
# @app.route('/getUserData', methods=['GET'])
# def getUserData():
#     if request.method == 'GET':
#         return perform_login()

@app1.route('/signup', methods=['POST'])
def handle_user():
    try: 
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                user = User(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],
                        address=data['address'], age=data['age'])
                db1.session.add(user)
                db1.session.commit()
                return {"message": f"User {user.firstName} has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}
    except Exception as e:
        print(e)
 
if __name__ == '__main__':
    from event_route import event
    from user_route import user
    from relationship_route import relationship
    app1.register_blueprint(event)
    app1.register_blueprint(user)
    app1.register_blueprint(relationship)
    app1.run(debug=True)
