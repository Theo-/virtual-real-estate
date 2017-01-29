from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
from app import db
from sklearn.naive_bayes import GaussianNB

Session = sessionmaker()
Session.configure(bind=db)

def create_user(session_id):
    gauss_clf = GaussianNB()
    user = User(session_id=sess_id)
    db.session.add(user)
    user_id = User.filter_by(session_id = sess_id).all()[0].id
    classifier = Classifiers(user_id=user_id,pickled_classifier=gauss_clf)
    db.session.add(classifier)
    db.session.commit()

def find_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def delete_user(id):
    user = find_user(id)
    user.delete()
    db.session.commit()
