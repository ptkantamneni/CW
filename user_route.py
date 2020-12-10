# CRUD operations for events
from flask import Blueprint, request, jsonify, session
from api import db1 as db, Event, User
from datetime import datetime, timedelta
import user_scoring_route
import event_route

user = Blueprint('user', __name__, url_prefix = '/user')

def authUser():
    if not "userId" in session:
        raise Exception("User not authenticated")
    return session["userId"]

@user.route('/helloUser')
def hello():
    user_id = authUser()
    return f"Hello User {user_id}"

@user.route('getUserById', methods = ['GET'])
def getUserForId():
    return db.session.query(User).filter_by(id=request.args.get('uid')).first().to_json()


@user.route('/updateScore', methods = ['POST'])
def updateScore():
    user_id = authUser()
    return updateUserScore(user_id)

def updateUserScore(user_id):
    user_score = user_scoring_route.calculateScoreForId(user_id)
    
    db.session.query(User).filter_by(id=user_id).update({'riskScore': user_score})
    db.session.commit()
    return f"updated user_score: {user_score}"


@user.route('/addTestResult', methods = ['POST'])
def addTestResult():
    #user_id = request.args.get('userId')
    user_id = authUser()
    #test_result = bool(request.args.get('testResult'))
    #test_date = request.args.get('testDate')
    data = request.get_json()

    test_result = bool(data['testResult'])
    test_date = data['testDate']
    
    db.session.query(User).filter_by(id=user_id).update({'testResult': test_result, 'testDate': test_date})
    db.session.commit()

    if test_result is True:
        event_route.updateEventsForUserWithCovid(user_id)

    return f"updated test results"
