from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings
from app import db
from sklearn.naive_bayes import GaussianNB

Session = sessionmaker()
Session.configure(bind=db)

def find_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def delete_user(id):
    user = find_user(id)
    user.delete()
    db.session.commit()
