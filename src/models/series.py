"""Series db models."""
from sqlalchemy import Column, String, Date, Integer
from marshmallow import Schema, fields, post_load, validates_schema
from src.models.base import Base
from src.utils.exceptions import HTTPError
from src.utils.logger import logger


class Series(Base):
    """Series database model."""

    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    date_start = Column(Date)
    date_end = Column(Date)


class SeriesSchema(Schema):
    """Schema for the Series Model."""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    @post_load
    def create_series(self, data):
        """Create a series Object."""
        return Series(**data)

    @validates_schema
    def validate_dates(self, data):
        """Validate the dates."""
        if data.get('date_start') > data.get('date_end'):
            raise HTTPError(400, "Start date can not be after end date.")

    def all(self, session):
        result = session.query(Series).all()
        obj, err = self.dump(result, many=True)
        if not err:
            return obj
        logger.error("ERROR: {}".format(err))
        return []
