from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
from app import db

Session = sessionmaker()
Session.configure(bind=db)

def create_user(session_id):
    new_user = User(session_id=session_id)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def find_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def delete_user(id):
    user = find_user(id)
    user.delete()
    db.session.commit()
