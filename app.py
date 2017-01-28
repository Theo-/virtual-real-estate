from flask import Flask, request
from sqlalchemy import create_engine, Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import PickleType
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import URLType
import json
import os
import pickle

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://admin:M%m65=N3s-A&ZR3t@mchacks2017.c5se38qdaeio.us-east-1.rds.amazonaws.com:3306/mchacks'

db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])


# Used to create database session
Session = sessionmaker()
Session.configure(bind=db)

# Creating the Models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    session_id = Column(String(300),nullable=False) # 300 chosen randomly.

class Classifiers(Base):
    __tablename__ = "classifiers"
    id = Column(Integer,primary_key=True)
    user_id = Column('user_id',Integer,ForeignKey("users.id"),nullable=False)
    pickled_classifier = Column(PickleType,nullable=False)

class Listing(Base):
    __tablename__="listing"
    id = Column(Integer,primary_key=True)
    title = Column(String(300),nullable=False)
    location = Column(String(300),nullable=False)
    city = Column(String(300),nullable=False)
    description = Column(String(1000),nullable=False)
    number_rooms = Column(Integer,nullable=False)
    star_rating = Column(Integer,nullable=False)
    price = Column(Integer,nullable=False)
    property_type = Column(String(300),nullable=False)


class ListingImage(Base):
    __tablename__="listing_image"
    id = Column(Integer,primary_key=True)
    url = Column(URLType(300),nullable=False)


class ListingMappedImages(Base):
    '''
    Use this to join images to their corresponding listing image
    '''
    __tablename__ = "listing_mapped_images"
    id = Column(Integer,primary_key=True)
    listing = Column(Integer,ForeignKey("listing.id"),nullable=False)
    listing_image = Column(Integer,ForeignKey("listing_image.id"),nullable=False)


class UserVisitedListings(Base):
    __tablename__="user_visited_listings"
    id = Column(Integer,primary_key=True)
    listing = Column(Integer,ForeignKey("listing.id"),nullable=False)
    user_id = Column('user_id',Integer,ForeignKey("users.id"),nullable=False)

# Creates the models
Base.metadata.create_all(db)

@app.before_request
def check_id():
    if request.method == 'POST':
        sess_id = request.args['sessionId']
        session = Session()
        var = session.query(User).filter_by(session_id = sess_id).all()
        if len(var) == 0:
            user = User(session_id=sess_id)
            session.add(user)
            session.commit()


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

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)
