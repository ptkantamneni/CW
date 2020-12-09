from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Date, BOOLEAN


app1 = Flask(__name__)
db1 = SQLAlchemy()
db1.init_app(app1)
app1.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://newuser:12345@localhost:5432/covidwatchers"
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
    hasSymptoms = db1.Column(BOOLEAN, nullable=True)
    symptomsOnSetDate = db1.Column(Date, nullable=True)

    def __init__(self, firstName, lastName, email, address, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.address = address
        self.age = age

    def __repr__(self):
        return f"<User {self.name}>"

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

 
if __name__ == '__main__':
    app1.run(debug=True)
