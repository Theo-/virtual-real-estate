from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
from sklearn.naive_bayes import GaussianNB
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://admin:M%m65=N3s-A&ZR3t@mchacks2017.c5se38qdaeio.us-east-1.rds.amazonaws.com:3306/mchacks'


# Creating Database
db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.metadata.create_all(db)

# Used to create database session
Session = sessionmaker()
Session.configure(bind=db)

gauss_clf = 0


@app.before_request
def check_id():
    if request.method == 'POST':
        sess_id = request.args['sessionId']
        session = Session()
        user = session.query(User).filter_by(session_id = sess_id).all()
        if len(user) == 0:
            create_new_user(sess_id)
        else:
            gauss_clf = session.query(Classifiers).filter_by(user_id=user[0].id).first()
        print "printing CLF"
        print gauss_clf


@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        json_text = json.dumps({"id": request.args['sessionId']})
        return json_text

@app.after_request
def header(response):
    response.headers['Content-type'] = ' application/json'
    return response

def create_new_user(sess_id):
    session = Session() # add a new user
    gauss_clf = GaussianNB()
    print "printing CLF"
    print gauss_clf
    user = User(session_id=sess_id)
    session.add(user)
    user_id = session.query(User).filter_by(session_id = sess_id).all()[0].id
    classifier = Classifiers(user_id=user_id,pickled_classifier=gauss_clf)
    session.add(classifier)
    session.commit()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)
