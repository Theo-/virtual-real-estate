from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import PickleType
from sqlalchemy_utils import URLType

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
    user_id = Column("user_id",Integer,ForeignKey("users.id"),nullable=False)
    like = Column(Boolean,nullable=False)
