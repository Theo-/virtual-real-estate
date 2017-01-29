from flask import Flask, request, render_template
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings
from init import create_app, db
from sklearn.naive_bayes import GaussianNB
from training import train_classifier
import json
import os
from basic_request import client_id, get_airbnb_listing, listing_id_example

# Creating app, migration tool and manager
app = create_app()
migrate = Migrate(app, db)

# creating a manager for database.
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Creating server command manager.
server = Server(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
manager.add_command("runserver", Server(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))),threaded=True,debug=True)


gauss_clf = 0


@app.before_request
def check_id():
    if request.method == 'POST':
        sess_id = request.json['sessionId']
        user = User.query.filter_by(session_id = sess_id).all()
        if len(user) == 0:
            gauss_clf = create_new_user(sess_id)
        else:
            gauss_clf = Classifiers.query.filter_by(user_id=user[0].id).first()

@app.route('/', methods=["POST"] )
def get_con():
    if request.method == "POST":
        result = request.json['result']
        params = result['parameters']
        intentName = result['metadata']['intentName']

        if intentName == "StartAparmentSearch":
            if set(("budget", "city", "date-period", "rooms")) <= set(params):
                sessionId = request.json['sessionId']
                save_user_parameters(sessionId, params)
                suggestion = pick_a_suggestion(sessionId)
                return format_response(suggestion)
                
        if intentName == "SuggestionFeedback":
            positive = params['Position'] != ''
            save_suggestion_feedback()

@app.after_request
def header(response):
    response.headers['Content-type'] = 'application/json'
    return response

def create_new_user(sess_id):
    gauss_clf = GaussianNB()
    user = User(session_id=sess_id)
    db.session.add(user)
    user_id = User.query.filter_by(session_id = sess_id).all()[0].id
    classifier = Classifiers(user_id=user_id,pickled_classifier=gauss_clf)
    db.session.add(classifier)
    db.session.commit()
    return gauss_clf

def save_user_parameters(sessionId, params):
    user = User.query.filter_by(session_id=sessionId).update(dict(city=params['city'],date_period=params['date-period'],number_rooms=params['rooms'],budget=params['budget']['amount']))
    return db.session.commit()

def save_suggestion_feedback(sessionId, context, feedback):
    user = User.query.filter_by(session_id=sessionId).first()
    apartment_details = get_list

    description = make_description(suggestion)
    classified = 1 if feedback else 0
    visited = UserVisitedListings(user_id=user.id,listing=context['listing']['id'], like=feedback)

    train_classifier([description], [feedback], gauss_clf)

def make_description(suggest):
    return suggestion['listing']['public_address'] + " " + suggestion['listing']['name'] + " " + suggestion['listing']['room_type'] + " " + suggestion['listing']['localized_city'] + " " + suggestion['listing']['neighborhood']

def pick_a_suggestion(sessionId):
    user = User.query.filter_by(session_id=sessionId).first()
    price_min = user.budget - 100
    price_max = user.budget + 100

    params = {
        "locale":"en-US",
        "currency":"USD",
        "min_bedrooms": user.number_rooms,
        "price_max": price_max,
        "price_min": price_min,
        "location": user.city,
        "_limit": "50"
    }

    results = get_airbnb_listing(client_id, **params)

    return results[0]

def format_response(suggestion):
    text = "I have something for you: https://fr.airbnb.ca/rooms/" + str(suggestion['listing']['id'])

    print suggestion

    return json.dumps({
        "speech": text,
        "displayText": text,
        "contextOut": { "id": str(suggestion['listing']['id']) }
    })

if __name__ == "__main__":
    manager.run()
