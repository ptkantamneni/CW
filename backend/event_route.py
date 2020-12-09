from flask import Blueprint, request
# from flask_sqlalchemy import SQLAlchemy
from api import db1, Event

event = Blueprint('event', __name__)

@event.route('/helloEvent')
def hello():
    return "Hello Event"


@event.route('/create_event', methods = ['POST'])
def createEvent():
    if(request.method == 'POST' and request.is_json):
        data = request.get_json()
        event = Event(
            data['placeName'],
            data['address'],
            data['numPeople'],
            data['socialDistanceRating'],
            data['maskComplianceRating'],
            data['openSpace'],
            data['riskScore'],
            data['createdById'],
            data['checkInDate'],
            data['checkOutDate'],
            data['updatedDate']
            )
        