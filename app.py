from flask import Flask, request, render_template
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings
from init import create_app, db
from sklearn.naive_bayes import GaussianNB
from training import train_classifier
import json
import os

# Creating app, migration tool and manager
app = create_app()
migrate = Migrate(app, db)

# creating a manager for database.
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Creating server command manager.
server = Server(host="0.0.0.0", port=int(os.environ['PORT']))
manager.add_command("runserver", Server(host="0.0.0.0", port=int(os.environ['PORT'])),threaded=True,debug=True)


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
        if set(("budget", "city", "date-period", "rooms")) <= set(params):
            #save_user_parameters(params)
            return json.dumps(params['budget'])

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

if __name__ == "__main__":
    manager.run()
