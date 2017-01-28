from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
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


@app.before_request
def check_id():
    print request
    if request.method == 'POST':
        sess_id = request.args['sessionId']
        session = Session()
        user = session.query(User).filter_by(session_id = sess_id).all()
        if len(user) == 0:
            create_new_user(sess_id)
        else:
            gauss_clf = session.query(Classifiers).filter_by(user_id=user[0].id).first()

@app.route('/testdatabase', methods = ["POST"] )
def testdatabase():
    if request.method == "POST":
        id = request.args['ID']
        session_id = request.args['SESS_ID']
        user = User(session_id=session_id)
        session = Session()
        session.add(user)
        session.commit()
        return "HAHAHA"

@app.route('/testdatabase2',methods = ["POST"])
def testdatabase2():
    dictionary_obj = {"Hello World":"This is me","HAHA":"HAHA"}
    if request.method == "POST":
        # Example of adding a pickled object
        user_id = request.form['user_id']
        classifier = Classifiers(user_id=user_id,pickled_classifier=dictionary_obj)
        session = Session()
        session.add(classifier)
        session.commit()
        return "WORKED"


@app.route('/gettest_pickled')
def testdatabase3():
    session = Session()
    results = session.query(Classifiers).all()
    qar = [ result.pickled_classifier   for result in results]
    print(qar)
    return "HEHE"


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
    user = User(session_id=sess_id)
    session.add(user)
    user_id = session.query(User).filter_by(session_id = sess_id).all()[0].id
    classifier = Classifiers(user_id=user_id,pickled_classifier=gauss_clf)
    session.add(classifier)
    session.commit()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)
