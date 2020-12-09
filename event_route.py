# CRUD operations for events
from flask import Blueprint, request, jsonify
from api import db1 as db, Event, User
from datetime import datetime, timedelta
import event_scoring_route

event = Blueprint('event', __name__, url_prefix = '/event')

@event.route('/hello_event')
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
            data['updatedDate'],
            0
            )

        db.session.add(event)
        db.session.commit()
        return "Successfully created event"
    
    return "SWWE"


@event.route('/get_event', methods = ['GET'])
def getEvent():
    if(request.method == 'GET'):
        event = Event.query.filter_by(id=request.args.get('id', default=-1)).first()
        return {} if event is None else jsonify(event.serialize())

    return 'SWWE'


@event.route('update_event', methods = ['PUT'])
def updateEvent():
    if(request.method == 'PUT'):
        newData = request.get_json()
        eventsUpdated = Event.query.filter_by(id=request.args.get('id', default=-1)).update(newData)
        db.session.commit()
        return jsonify({'eventsUpdated': eventsUpdated})
    
    return 'SWWE'


@event.route('delete_event', methods = ['DELETE'])
def deleteEvent():
    if(request.method == 'DELETE'):
        eventsDeleted = Event.query.filter_by(id=request.args.get('id')).delete()
        db.session.commit()
        return jsonify({'eventsDeleted': eventsDeleted}) 

    return 'SWWE'
    
@event.route('/getAllEventsForAddress', methods = ['GET'])
def getAllEventsAtAddressBetweenTime():
    address = request.args.get('address')
    check_in_date = request.args.get('checkInDate')
    check_out_date = request.args.get('checkOutDate')
    events = getAllEventsHelper(address, check_in_date, check_out_date)
    for event in events:
        print(event)
    return jsonify([e.serialize() for e in events])

@event.route('/updateAllEventsScoreAffectedUser', methods = ['POST'])
def updateAffectedEvents():
    user_id = request.args.get('userId')
    updateEventsForUserWithCovid(user_id)

    return "Updated event scores success"

def getAllEventsHelper(address, check_in_date, check_out_date):
    events = db.session.query(Event).filter(Event.address == address).filter((Event.checkInDate <= check_out_date) & (Event.checkOutDate >= check_in_date))
    return events

def incCasesAndGetAllEventsHelper(address, check_in_date, check_out_date):
    events = db.session.query(Event).filter(Event.address == address).filter((Event.checkInDate <= check_out_date) & (Event.checkOutDate >= check_in_date)).update({'confirmedCases': Event.confirmedCases + 1})
    print("events updated")
    db.session.commit()

    eventsList = db.session.query(Event).filter(Event.address == address).filter((Event.checkInDate <= check_out_date) & (Event.checkOutDate >= check_in_date))
    return eventsList

def getPast2WeekEventsForUserHelper(user_id, date):
    two_weeks_ago = date - timedelta(days=14)
    events = db.session.query(Event).filter(Event.createdById == user_id).filter((Event.checkInDate <= date) & (Event.checkOutDate >= two_weeks_ago))
    return events

def updateEventsForUserWithCovid(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if(user.testResult):
        # if postiive, fetch previous events for user in past 14 weeks
        user_events = getPast2WeekEventsForUserHelper(user.id, user.testDate)
        # increment count for each event
        for event in user_events:
            print("event: ")
            print(event.serialize())
            same_time_events = incCasesAndGetAllEventsHelper(event.address, event.checkInDate, event.checkOutDate)
            for same_event in same_time_events:
                print("same_event: ")
                print(same_event.serialize())
                # increment and update numCases
                db.session.commit()
                event_to_update_score = Event.query.filter_by(id=same_event.id).first()

                new_score = event_scoring_route.calculateScoreForEventId(event_to_update_score.id)
                Event.query.filter_by(id=same_event.id).update({'riskScore': new_score})
                db.session.commit()
