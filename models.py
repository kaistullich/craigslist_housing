import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# base class inherited for all mappings
Base = declarative_base()


class CraigslistHousing(Base):
    """ Table will store all necessary info related to a listing """
    __tablename__ = 'allListings'

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(String(5), nullable=False)
    url = Column(String(250), nullable=False)

    def __str__(self):
        """String representation of the object"""
        return '<CraigslistHousing id={}/>'.format(self.id)

    def __repr__(self):
        """String representation of the object"""
        return '<CraigslistHousing id={}/>'.format(self.id)


# create SQLAlchemy engine
engine = create_engine('sqlite:///{}'.format(os.path.join(os.getcwd(), 'craigslistHousingListings.db')))

# create all tables in the engine
Base.metadata.create_all(engine)

# session obj to allow connection to the DB
Session = sessionmaker(bind=engine)
session = Session()
