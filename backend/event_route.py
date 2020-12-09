# CRUD operations for events
from flask import Blueprint, request, jsonify
from api import db1 as db, Event

event = Blueprint('event', __name__, url_prefix = '/event')

@event.route('/helloEvent')
def hello():
    return "Hello Event"


@event.route('/createEvent', methods = ['POST'])
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

        db.session.add(event)
        db.session.commit()
        return "Successfully created event"
    
    return "SWWE"


@event.route('/getEvent', methods = ['GET'])
def getEvent():
    if(request.method == 'GET'):
        event = Event.query.filter_by(id=request.args.get('id', default=-1)).first()
        return {} if event is None else jsonify(event.serialize())

    return 'SWWE'


@event.route('updateEvent', methods = ['PUT'])
def updateEvent():
    if(request.method == 'PUT'):
        newData = request.get_json()
        eventsUpdated = Event.query.filter_by(id=request.args.get('id', default=-1)).update(newData)
        db.session.commit()
        return jsonify({'eventsUpdated': eventsUpdated})
    
    return 'SWWE'


@event.route('deleteEvent', methods = ['DELETE'])
def deleteEvent():
    if(request.method == 'DELETE'):
        eventsDeleted = Event.query.filter_by(id=request.args.get('id')).delete()
        db.session.commit()
        return jsonify({'eventsDeleted': eventsDeleted}) 

    return 'SWWE'
    
