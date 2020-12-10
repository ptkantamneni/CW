from flask import Blueprint, request, jsonify, session
from api import db1, Relationship, User

relationship = Blueprint('relationship', __name__, url_prefix = '/relationship')

def authUser():
    if not "userId" in session:
        raise Exception("User not authenticated")
    return session["userId"]

@relationship.route('/helloRelationship')
def hello():
    return "Hello Relationship"

@relationship.route('/getRelationship', methods=['GET'])
def getRelationshipsForUser():
    user_id = authUser()
    #user = db1.session.query(User).filter_by(id=user_id)

    #user = getUserByEmail(request.args.get('email'))
    relationship_list = db1.session.query(Relationship).filter_by(userId=user_id)
    return jsonify([r.to_json() for r in relationship_list])

@relationship.route('/getFriendsUserInfo', methods=['GET'])
def getFriendsUserInfo():
    user_id = authUser()
    #user = db1.session.query(User).filter_by(id=user_id)

    #user = getUserByEmail(request.args.get('email'))
    friends = []
    relationship_list = db1.session.query(Relationship).filter_by(userId=user_id)
    for r in relationship_list:
        friend_info = db1.session.query(User).filter_by(id=r.friendId).first()
        friends.append(friend_info)

    return jsonify([f.to_json() for f in friends])

@relationship.route('/addRelationship', methods=['POST'])
def addRelationshipByEmail():
    if request.method == 'POST':
        user_id = authUser()
        if request.is_json:
            data = request.get_json()
            #email = data['email']
            #current_user_info = api.user_info() 
            #user = getUserByEmail(email)

            friend_email = data['friendEmail']
            friend = getUserByEmail(friend_email)
            if friend is None:
                return {"error": f"Friend with email {friend_email} not found"}
            relationship = Relationship(userId=user_id, friendId=friend.id, relationshipType=data['relationshipType'])
            db1.session.add(relationship)
            db1.session.commit()
            return {"message": f"Relationship between user: {relationship.userId} and userId: {relationship.friendId} has been created successfully."}

        else:
            return {"error": "The request payload is not in JSON format"}

@relationship.route('/deleteRelationship', methods=['DELETE'])
def deleteRelationshipByEmail():
    #user = getUserByEmail(request.args.get('email'))
    user_id = authUser()

    friend_email = request.args.get('friendEmail')
    friend = getUserByEmail(friend_email)
    if friend is None:
        return {"error": f"Friend with email {friend_email} not found"}
    relationship = Relationship.query.filter(Relationship.userId == user_id).filter(Relationship.friendId == friend.id).first()
    if relationship is None:
        return {"error": f"Relationship with {friend_email} not found"} 
    db1.session.delete(relationship)
    db1.session.commit() 
    return {"message": f"Relationship between user: {user_id} and friend: {friend_email} has been deleted successfully."} 

def getUserByEmail(email):
    return db1.session.query(User).filter_by(email=email).first()

