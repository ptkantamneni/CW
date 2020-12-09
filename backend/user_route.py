# CRUD operations for events
from flask import Blueprint, request, jsonify
from api import db1 as db, Event, User
from datetime import datetime, timedelta
import user_scoring_route

user = Blueprint('user', __name__)

@user.route('/helloUser')
def hello():
    return "Hello User"


@user.route('/user/updateScore', methods = ['POST'])
def updateScore():
    user_id = request.args.get('userId')
    return updateUserScore(user_id)

def updateUserScore(user_id):
    user_score = user_scoring_route.calculateScoreForId(user_id)
    
    db.session.query(User).filter_by(id=user_id).update({'riskScore': user_score})
    db.session.commit()
    return f"updated user_score: {user_score}"

