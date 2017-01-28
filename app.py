from flask import Flask, request
from sqlalchemy import create_engine, Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import PickleType
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import sessionmaker

import json
import os

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


# Creates the models
Base.metadata.create_all(db)


@app.route('/testdatabase', methods =["POST"] )
def testdatabase():
    if request.method == "POST":
        id = request.form['ID']
        session_id = request.form['SESS_ID']
        user = User(session_id=session_id)
        session = Session()
        session.add(user)
        session.commit()
        return "HAHAHA"


@app.before_request
def check_id():
    if request.method == 'POST':
        check_id()

@app.route('/', methods =["POST"] )
def get_con():
    if request.method == "POST":
        json_text = json.dumps({"id": request.args['sessionId']})

        return json_text

@app.after_request
def header(response):
    response.headers['Content-type'] = ' application/json'
    return response

def check_id(sess_id):
    #Session.query(users).filter()


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=int(os.environ['PORT']),threaded=True,debug=True)
