"""Tournaments db models."""
from sqlalchemy import Column, Integer, String, ForeignKey, Date, inspect
from sqlalchemy.orm import relationship, backref
from marshmallow import Schema, fields, post_load, validates_schema
from src.models.base import Base
from src.models.series import Series, SeriesSchema
from src.utils.logger import logger
from src.utils.exceptions import HTTPError


class Tournaments(Base):
    """Tournaments database model."""

    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    date_start = Column(Date)
    date_end = Column(Date)
    series_id = Column(Integer, ForeignKey(Series.id))
    series = relationship(Series)


class TournamentsSchema(Schema):
    """Schema for the Tournaments Model."""

    id = fields.Integer(dump_only=True)
    series_id = fields.Integer(required=True)
    name = fields.String(required=True)
    city = fields.String(required=True)
    country = fields.String(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    @post_load
    def create_tournaments(self, data):
        """Create a Tournaments Object."""
        return Tournaments(**data)

    @validates_schema
    def validate_dates(self, data):
        """Validate the dates."""
        if data.get('date_start') > data.get('date_end'):
            raise HTTPError(400, "Start date can not be after end date.")

    def filter_by_series(self, session, series_name):
        result = session.query(Tournaments, Series).join(
            Series).filter(Series.name.like("%{}%".format(series_name))).all()
        series_schema = SeriesSchema()
        response = []
        for t_row, s_row in result:
            t_obj, t_err = self.dump(t_row)
            s_obj, s_err = series_schema.dump(s_row)
            if not t_err and not s_err:
                t_obj['series'] = s_obj
                response.append(t_obj)
            else:
                logger.error(
                    "Tournament Error: {}, Series Error: {}".format(t_err, s_err))
        return response

    def all(self, session):
        result = session.query(Tournaments, Series).join(Series).all()
        series_schema = SeriesSchema()
        response = []
        for t_row, s_row in result:
            t_obj, t_err = self.dump(t_row)
            s_obj, s_err = series_schema.dump(s_row)
            if not t_err and not s_err:
                t_obj['series'] = s_obj
                response.append(t_obj)
            else:
                logger.error(
                    "Tournament Error: {}, Series Error: {}".format(t_err, s_err))
        return response

    def filter_by_date_range(self, session, date_start, date_end):
        result = session.query(Tournaments, Series).join(Series)\
            .filter(Tournaments.date_start >= date_start)\
            .filter(Tournaments.date_end <= date_end)\
            .all()

        series_schema = SeriesSchema()
        response = []
        for t_row, s_row in result:
            t_obj, t_err = self.dump(t_row)
            s_obj, s_err = series_schema.dump(s_row)
            if not t_err and not s_err:
                t_obj['series'] = s_obj
                response.append(t_obj)
            else:
                logger.error(
                    "Tournament Error: {}, Series Error: {}".format(t_err, s_err))
        return response
