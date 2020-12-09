from flask import Blueprint

event = Blueprint('event', __name__)

@event.route('/helloEvent')
def hello():
    return "Hello Event"