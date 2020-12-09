from flask import Blueprint, request, jsonify
from api import db1, Relationship, User, Event

event_scoring = Blueprint('event_scoring', __name__)

@event_scoring.route('/helloScoring')
def hello():
    return "Hello Scoring"

@event_scoring.route('/event_scoring', methods=['GET'])
def getScoreForEventId():
    eventId = request.args.get('eventId')
    event = db1.session.query(Event).filter_by(id=eventId).first()
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
    
    return {"message": f"Event score for id {eventId} is {eventScore}"}    

def calculateEventScore(event, social_dist_w, mask_comp_w, people_w):
    denom = social_dist_w + mask_comp_w + people_w
    print(f"scoring as openSpace: {event.openSpace} socialDistanceRating: {event.socialDistanceRating} maskComplianceRating: {event.maskComplianceRating} numPeople: {event.numPeople}")

    return ((social_dist_w * (6 - event.socialDistanceRating)) + (mask_comp_w * (6 - event.maskComplianceRating)) + (people_w * event.numPeople)) / denom

