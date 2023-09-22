from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
       messages = []
       for message in Message.query.all():
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at, 
                "updated_at": message.updated_at
            } 
            messages.append(message_dict)

            response = make_response(
                messages, 200
            )

            return response
        
    elif request.method == 'POST':
        new_message = Message(
            username=request.form.get("username"),
            body=request.form.get("body"),
        )

        db.session.add(new_message)
        db.session.commit()

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        response_body = {
            "note": "The message you seek is currently absent. Please try again never."
        }
        response = make_response(response_body, 404)

        return response
    else:
        if request.method == 'GET':
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at, 
                "updated_at": message.updated_at
            }
            message.append(message_dict)

            response = make_response(
                message, 200
            )

            return response
        elif request.method == 'PATCH':
            for body in request.form:
                setattr(message, body, request.form.get(body))
            
            db.session.add(message)
            db.session.commit()
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "note":"Message deleted."
            }
            response = make_response(
                response_body, 200
            )

            return response



if __name__ == '__main__':
    app.run(port=5555)
