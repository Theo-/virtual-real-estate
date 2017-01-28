from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Classifiers, Listing, ListingImage, ListingMappedImages, UserVisitedListings, Base
from app import db

Session = sessionmaker()
Session.configure(bind=db)

def create_user(session_id):
    session = Session()
    new_user = User(session_id=session_id)
    session.add(new_user)
    session.commit()
    return new_user

def find_user(id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    return user

def delete_user(id):
    user = find_user(id)
    session = Session()
    
    