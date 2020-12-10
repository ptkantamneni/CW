from flask import Blueprint, request, jsonify, session
from api import db1, Relationship, User, Event

event_scoring = Blueprint('event_scoring', __name__, url_prefix = '/score')

def authUser():
    if not "userId" in session:
        raise Exception("User not authenticated")
    return session["userId"]

@event_scoring.route('/helloEventScoring')
def hello():
    return "Hello Scoring"

@event_scoring.route('/event_scoring', methods=['GET'])
def getScoreForEventId():
    event_id = request.args.get('eventId')
    event_score = calculateScoreForEventId(event_id)
    return {"message": f"Event score for id {event_id} is {event_score}"}

def calculateScoreForEventId(event_id):
    event = db1.session.query(Event).filter_by(id=event_id).first()
    eventScore = 1.0
    if(event.openSpace):
        social_dist_w = 1.4
        mask_comp_w = 1.4
        people_w = 1.2
        eventScore = calculateEventScore(event, social_dist_w, mask_comp_w, people_w)

    else:
        social_dist_w = 1.35
        mask_comp_w = 1.35
        people_w = 1.3
        eventScore = calculateEventScore(event, social_dist_w, mask_comp_w, people_w)

    return round(eventScore,3)

def calculateEventScore(event, social_dist_w, mask_comp_w, people_w):
    denom = social_dist_w + mask_comp_w + people_w
    print(f"scoring as openSpace: {event.openSpace} socialDistanceRating: {event.socialDistanceRating} maskComplianceRating: {event.maskComplianceRating} numPeople: {event.numPeople}")
    event_score = ((social_dist_w * (6 - event.socialDistanceRating)) + (mask_comp_w * (6 - event.maskComplianceRating)) + (people_w * event.numPeople)) / denom
    additional_risk = calculateAdditionalRisk(event, event_score)

    print(f"event_score: {event_score} additional_risk: {additional_risk}")
    return event_score + additional_risk

def calculateAdditionalRisk(event, event_score):
    highest_add_risk = 5.0 - event_score
    switcher={
            1:5,
            2:10,
            3:25,
            4:100,
            5:200
        }
    max_people = switcher.get(event.numPeople)
    confirmed_cases = event.confirmedCases
    if(confirmed_cases is None):
        confirmed_cases = 0
    if(confirmed_cases > max_people):
        confirmed_cases = max_people

    cases_pct = confirmed_cases / max_people
    add_risk = highest_add_risk * cases_pct
    return add_risk




