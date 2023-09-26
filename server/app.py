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
       for message in Message.query.order_by('created_at').all():
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at, 
                "updated_at": message.updated_at
            } 
            messages.append(message_dict)

            response = make_response(
                jsonify(messages), 200
            )

            return response
        
    elif request.method == 'POST':

        username = request.form.get("username")
        body = request.form.get("body")

      
        existing_message = Message.query.filter_by(username=username).first()

        if existing_message:
            
            existing_message.body = body
            db.session.commit()
        else:
           
            new_message = Message(username=username, body=body)
            db.session.add(new_message)
            db.session.commit()

        response_body = {
            "message": "Message created or updated successfully."
        }
        response = make_response(jsonify(response_body), 200)
        return response


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        response_body = {
            "note": "The message you seek is currently absent. Please try again never."
        }
        response = make_response(jsonify(response_body), 404)

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
                jsonify(message), 200
            )

            return response
        elif request.method == 'PATCH':

            for field in request.form:
             if field != 'username':  
                    setattr(message, field, request.form.get(field))

                    new_username = request.form.get("username")
            if new_username != message.username:
                existing_message = Message.query.filter_by(username=new_username).first()
                if existing_message:
                    response_body = {
                        "error": "Username already exists."
                    }
                    response = make_response(jsonify(response_body), 400)
                    return response
                else:
                    message.username = new_username

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
                jsonify(response_body), 200
            )

            return response


if __name__ == '__main__':
    app.run(port=3000)

