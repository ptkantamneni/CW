from sqlalchemy import Column, Integer, String, Date, BOOLEAN
import datetime
import database

class BaseModel(database.db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class User(BaseModel, database.db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    address = Column(String)
    age = Column(Integer)
    testResult = Column(String)
    testDate = Column(Date)
    hasSymptoms = Column(BOOLEAN)
    symptomsOnSetDate = Column(Date)
