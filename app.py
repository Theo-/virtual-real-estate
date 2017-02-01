from flask import Flask, request, render_template, session
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings
from init import create_app, db
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from training import train_classifier
from sklearn.exceptions import NotFittedError
import json
import os
import facebook
from threading import Thread
import cPickle
from basic_request import client_id, get_airbnb_listing, listing_id_example, get_airbnb_listing_info

# Facebook app details
FB_APP_ID = '904739326295400'
FB_APP_NAME = 'AirBnBro - Test1'
FB_APP_SECRET = '72cd0d0e1c5bec1c6596aef227770d3f'
FB_PAGE_ACCESS_TOKEN = 'EAAM22woofWgBAEr43VgSqHZALYIzF8ziNT0otpfDEYYGlBi2zgBQsObklpkgsdo8ZCyuJOwE2zneH13EEGuNgNtuZARTVkcSO1x2uVaguz7vdBj3ZCCHAAkkhMhW2z7sPPFjQUY35dZC4WNURqNNqRqtlPZAKjIZAKpjZAqNLfjY2gZDZD'

# Creating app, migration tool and manager
app = create_app()
migrate = Migrate(app, db)

# creating a manager for database.
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Creating server command manager.
server = Server(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
manager.add_command("runserver", Server(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))),threaded=True,debug=True)

# Load vecotrizer
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = cPickle.load(f)

gauss_clf = 0
mem_cache_dict = {}


@app.before_request
def check_id():
    if request.method == 'POST':
        if session.get('user'):
            g.user = session.get('user')
            return

        result = facebook.get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID,
                                  app_secret=FB_APP_SECRET)
        if result:
            graph = GraphAPI(result['access_token'])
            profile = graph.get_object('me')

            print str(profile['id'])

    if request.method == "GET":
        if set(["hub.challenge", "hub.mode", "hub.verify_token"]).issubset(request.args) and request.args["hub.verify_token"] == "airbnbrotest":
            return request.args["hub.challenge"]
        else:
            return "Could not authenticate"

@app.route('/', methods=["POST"] )
def get_con():
    if request.method == "POST":
        return json.dumps(gen_response("thomas", 567))

@app.after_request
def header(response):
    response.headers['Content-type'] = 'application/json'
    return response


def gen_response(name, user_id):
    response = {
        "recipient": {
            "id": "USER_ID"
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "https://petersapparel.parseapp.com/img/shirt.png",
                    "is_reusable": True
                }
            }
        }
    }
    
    return response


if __name__ == "__main__":
    manager.run()
