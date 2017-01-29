from flask import Flask, request, render_template
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings
from init import create_app, db
from sklearn.naive_bayes import GaussianNB
from training import train_classifier
from sklearn.exceptions import NotFittedError
import json
import os
from threading import Thread
import cPickle
from basic_request import client_id, get_airbnb_listing, listing_id_example, get_airbnb_listing_info

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
mem_cache_dict = {}


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
        sessionId = request.json['sessionId']

        if intentName == "StartAparmentSearch":
            if set(("budget", "city", "date-period", "rooms")) <= set(params):
                save_user_parameters(sessionId, params)
                suggestion = pick_a_suggestion(sessionId)
                return format_response(suggestion)
                
        if intentName == "SuggestionFeedback":
            positive = params['Positive'] != ''
            context = result['contexts'][0]['parameters']
            save_suggestion_feedback(sessionId, context, positive)
            suggestion = pick_a_suggestion(sessionId)
            return format_response(suggestion)

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
    gauss_object = Classifiers.query.filter_by(user_id=user.id).first()
    gauss_clf = gauss_object.pickled_classifier

    classified = 1 if feedback else 0
    visited = UserVisitedListings(user_id=user.id,listing=context['id'], like=feedback)

    train_classifier([context['description']], [classified], gauss_clf)
    Classifiers.query.filter_by(user_id=user.id).update(dict(pickled_classifier=gauss_clf))
    db.session.add(visited)
    db.session.commit()

def make_description(info):
    return info['description'] + ' ' + info['neighborhood_overview'] + ' ' + info['space'] + ' ' + info['name']

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

    # Make predictions
    user = User.query.filter_by(session_id=sessionId).first()
    gauss_object = Classifiers.query.filter_by(user_id=user.id).first()
    gauss_clf = gauss_object.pickled_classifier

    seenListings = UserVisitedListings.query.filter_by(user_id=user.id).all()
    seenIds = [listing.listing for listing in seenListings]

    highestScore = -1
    highestResult = None
    noneHit = 0
    scanned = 0

    for result in results:
        if int(result['listing']['id']) in seenIds:
            continue

        detailedDescription, isHit = get_airbnb_listing_info_cache(result['listing']['id'])
        if not isHit:
            noneHit = noneHit + 1

        if noneHit > 2:
            thread = Thread(target = download_all, args = ([results]))
            thread.start()
            break

        scanned = scanned + 1
        if scanned > 5:
            break

        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = cPickle.load(f)
        description = make_description(detailedDescription)
        vectors =vectorizer.transform([description])

        # Use description to make prediction
        try:
            score = gauss_clf.predict(vectors.toarray())
        except NotFittedError:
            score = 0
        
        if highestScore < score:
            highestScore = score
            highestResult = result

    return results[0] if highestResult == None else highestResult

def get_airbnb_listing_info_cache(airbnb_id):
    params = {
        "listing_id": airbnb_id,
        "locale": "en-US"
    }

    if airbnb_id in mem_cache_dict:
        print 'cache hit'
        return mem_cache_dict[airbnb_id], 1

    print 'cache miss'
    listing = get_airbnb_listing_info(client_id, **params)
    mem_cache_dict[airbnb_id] = listing
    return listing, 0

def download_all(listings):
    print 'Starting download!'
    for listing in listings:
        print 'Download ', listing['listing']['id']
        get_airbnb_listing_info_cache(listing['listing']['id'])

    print 'Downloaded finished'

def format_response(suggestion):
    url = "https://airbnb.ca/rooms/" + str(suggestion['listing']['id'])
    text = "I have something for you: "+url

    listingInfo, isHit = get_airbnb_listing_info_cache(suggestion['listing']['id'])

    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": listingInfo['name'],
                        "image_url": listingInfo['picture_url'],
                        "subtitle": listingInfo['summary'],
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": url,
                                "title": "View Details"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return json.dumps({
        "speech": text,
        "displayText": text,
        "data": { "facebook": facebook_message },
        "contextOut": [{ 
            "name": "apt-description",
            "lifespan": 3,
            "parameters": {
                "description": make_description(listingInfo),
                "id": listingInfo['id']
            }
        }]
    })

if __name__ == "__main__":
    manager.run()
