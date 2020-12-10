from flask import Blueprint, request, jsonify
from api import db1, Relationship, User

relationship = Blueprint('relationship', __name__, url_prefix = '/relationship')

@relationship.route('/helloRelationship')
def hello():
    return "Hello Relationship"

@relationship.route('/getRelationship', methods=['GET'])
def getRelationshipsForEmail():
    user = getUserByEmail(request.args.get('email'))
    relationship_list = db1.session.query(Relationship).filter_by(userId=user.id)
    return jsonify([r.to_json() for r in relationship_list])

@relationship.route('/addRelationship', methods=['POST'])
def addRelationshipByEmail():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data['email']
            #current_user_info = api.user_info() 
            user = getUserByEmail(email)

            friend_email = data['friendEmail']
            friend = getUserByEmail(friend_email)
            if friend is None:
                return {"error": f"Friend with email {friend_email} not found"}
            relationship = Relationship(userId=user.id, friendId=friend.id, relationshipType=data['relationshipType'])
            db1.session.add(relationship)
            db1.session.commit()
            return {"message": f"Relationship between user: {relationship.userId} and userId: {relationship.friendId} has been created successfully."}

        else:
            return {"error": "The request payload is not in JSON format"}

@relationship.route('/deleteRelationship', methods=['DELETE'])
def deleteRelationshipByEmail():
    user = getUserByEmail(request.args.get('email'))

    friend_email = request.args.get('friendEmail')
    friend = getUserByEmail(friend_email)
    if friend is None:
        return {"error": f"Friend with email {friend_email} not found"}
    relationship = Relationship.query.filter(Relationship.userId == user.id).filter(Relationship.friendId == friend.id).first()
    if relationship is None:
        return {"error": f"Relationship with {friend_email} not found"} 
    db1.session.delete(relationship)
    db1.session.commit() 
    return {"message": f"Relationship between user: {user.email} and friend: {friend_email} has been deleted successfully."} 

def getUserByEmail(email):
    return db1.session.query(User).filter_by(email=email).first()
