from flask import Blueprint

relationship = Blueprint('relationship', __name__)

@relationship.route('/helloRelationship')
def hello():
    return "Hello Relationship"