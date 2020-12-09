from flask import Blueprint, request, jsonify
from api import db1 as db, User, Event
from datetime import datetime, timedelta

user_scoring = Blueprint('user_scoring', __name__, url_prefix = '/score')

@user_scoring.route('/hello_user_scoring')
def hello():
    return 'Hello User Scoring'

@user_scoring.route('/user_scoring', methods = ['GET'])
def getScoreForUserId():
    if(request.method == 'GET'):
        user = User.query.filter_by(id=request.args.get('userId')).first()
        last_14days_events = db.session.query(Event).filter(Event.createdById==request.args.get('userId'), Event.updatedDate >= getDate14DayAgo()).all()
        
        age_w = 1.1
        num_events_w = 1.4
        avg_event_score_w = 1.2
        symptoms_w = 1.3

        avg_event_s = sum([event.serialize()['riskScore'] for event in last_14days_events]) / len(last_14days_events)
        age_s = getAgeScore(user.age)
        num_events_s = getNumEventsScore(len(last_14days_events))
        symptoms_s = getSymptomsScore(user.hasSymptoms)

        return {"userScore": (age_w * age_s + num_events_w * num_events_s + avg_event_score_w * avg_event_s + symptoms_w * symptoms_s) / (age_w + num_events_w + avg_event_score_w + symptoms_w)}

    return 'SWWE'



def getDate14DayAgo():
    return datetime.now() - timedelta(days=14)

def getAgeScore(age):
    if(age >= 0 and age <= 10):
        return 1
    elif(age >= 11 and age <= 17):
        return 2
    elif(age >= 18 and age <= 34):
        return 5
    elif(age >= 35 and age <= 49):
        return 4
    elif(age >= 50 and age <= 59):
        return 3
    else:
        return 2

def getNumEventsScore(numEvents):
    if(numEvents == 0):
        return 1
    elif(numEvents == 1 or numEvents == 2):
        return 2
    elif(numEvents >= 3 and numEvents <= 5):
        return 3
    elif(numEvents >= 6 and numEvents <= 10):
        return 4
    else:
        return 5

def getSymptomsScore(hasSymptoms):
    return 3 if(hasSymptoms) else 1