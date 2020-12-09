from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/helloUser')
def hello():
    return "Hello User"