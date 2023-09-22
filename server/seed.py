

#!/usr/bin/env python3

from random import shuffle
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for _ in range(4)]

shuffle(usernames)  

def make_messages():
    Message.query.delete()
    messages = []

    for i in range(20):
        username = usernames[i % len(usernames)] 
        message = Message(
            body=fake.sentence(),
            username=username,
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        make_messages()

