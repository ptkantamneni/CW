from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager,
                         login_user, logout_user,
                         login_required, UserMixin, current_user)

from sqlalchemy import Integer, String, Date, Boolean, Float, DateTime

# import event_route
    
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
    testResult = db1.Column(String, nullable=True)
    testDate = db1.Column(Date, nullable=True)
    hasSymptoms = db1.Column(Boolean, nullable=True)
    symptomsOnSetDate = db1.Column(Date, nullable=True)

    def __init__(self, firstName, lastName, email, password, address, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.address = address
        self.age = age

    def __repr__(self):
        return f"<User {self.name}>"

    def to_json(self):
        return {"name": self.firstName,
                "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

@app1.route('/')
def hello_world():
    return 'Hello, World!'

@app1.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data['username']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
           login_user(user)
           return jsonify(user.to_json())
        else:
           return jsonify({"status": 401,
                        "reason": "Username or Password is Invalid"})

@app1.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'User is successfully logged out'}})

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
                        address=data['address'], age=data['age'], password=data['password'])
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
    app1.register_blueprint(event)
    app1.register_blueprint(user)
    app1.register_blueprint(relationship)
    app1.run(debug=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id).first()
