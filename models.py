<<<<<<< HEAD
from app import db
=======
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import PickleType
from sqlalchemy_utils import URLType
>>>>>>> 014a1d3a2051c3fc158fd0481c986d15ac00c5e5

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    session_id = db.Column(db.String(300),nullable=False) # 300 chosen randomly.
    

class Classifiers(db.Model):
    __tablename__ = "classifiers"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column('user_id',db.Integer,db.ForeignKey("users.id"),nullable=False)
    pickled_classifier = db.Column(db.PickleType,nullable=False)

class Listing(db.Model):
    __tablename__="listing"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(300),nullable=False)
    location = db.Column(db.String(300),nullable=False)
    city = db.Column(db.String(300),nullable=False)
    description = db.Column(db.String(1000),nullable=False)
    number_rooms = db.Column(db.Integer,nullable=False)
    star_rating = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    property_type = db.Column(db.String(300),nullable=False)


class ListingImage(db.Model):
    __tablename__="listing_image"
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.URLType(300),nullable=False)


class ListingMappedImages(db.Model):
    '''
    Use this to join images to their corresponding listing image
    '''
    __tablename__ = "listing_mapped_images"
    id = db.Column(db.Integer,primary_key=True)
    listing = db.Column(db.Integer,db.ForeignKey("listing.id"),nullable=False)
    listing_image = db.Column(db.Integer,db.ForeignKey("listing_image.id"),nullable=False)


class UserVisitedListings(db.Model):
    __tablename__="user_visited_listings"
<<<<<<< HEAD
    id = db.Column(db.Integer,primary_key=True)
    listing = db.Column(db.Integer,db.ForeignKey("listing.id"),nullable=False)
    user_id = db.Column('user_id',db.Integer,db.ForeignKey("users.id"),nullable=False)
=======
    id = Column(Integer,primary_key=True)
    listing = Column(Integer,ForeignKey("listing.id"),nullable=False)
    user_id = Column("user_id",Integer,ForeignKey("users.id"),nullable=False)
    like = Column(Boolean,nullable=False)
>>>>>>> 014a1d3a2051c3fc158fd0481c986d15ac00c5e5
