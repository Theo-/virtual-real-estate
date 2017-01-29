from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import PickleType
from sqlalchemy_utils import URLType
from flask_sqlalchemy import SQLAlchemy
from init import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    session_id = db.Column(db.String(300)) # 300 chosen randomly.


class Classifiers(db.Model):
    __tablename__ = "classifiers"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column('user_id',db.Integer)
    pickled_classifier = db.Column(db.PickleType)

class Listing(db.Model):
    __tablename__="listing"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(300))
    location = db.Column(db.String(300))
    city = db.Column(db.String(300))
    description = db.Column(db.String(1000))
    number_rooms = db.Column(db.Integer)
    star_rating = db.Column(db.Integer)
    price = db.Column(db.Integer)
    property_type = db.Column(db.String(300))


class ListingImage(db.Model):
    __tablename__="listing_image"
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(URLType(300))


class ListingMappedImages(db.Model):
    '''
    Use this to join images to their corresponding listing image
    '''
    __tablename__ = "listing_mapped_images"
    id = db.Column(db.Integer,primary_key=True)
    listing = db.Column(db.Integer)
    listing_image = db.Column(db.Integer)


class UserVisitedListings(db.Model):
    __tablename__="user_visited_listings"
    id = db.Column(db.Integer,primary_key=True)
    listing = db.Column(db.Integer)
    user_id = db.Column('user_id',db.Integer)
    like = db.Column('like',db.Boolean)
