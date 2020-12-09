
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)
db = SQLAlchemy()


def init_app():
    db.init_app(app)


init_app()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5432/covidwatchers"
migrate = Migrate(app, db)


@app.route('/')
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

@app.route('/signup', methods=['POST'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            user = User(firstName=data['firstName'])
            db.session.add(user)
            db.session.commit()
            return {"message": f"User {user.firstName} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

 
if __name__ == '__main__':
    app.run(debug=True)
