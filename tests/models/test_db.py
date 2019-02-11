from src.models.db import SQLiteDB
from src.models.base import Base
from src.models.series import Series, SeriesSchema
from datetime import datetime, timedelta
from src.models.tournaments import Tournaments, TournamentsSchema
import pytest


@pytest.fixture
def session(request):
    SQLiteDB.uri = "sqlite:////tmp/test.db"
    session = SQLiteDB().connect()
    Base.metadata.create_all()
    return session


@pytest.mark.usefixtures('session')
class TestDBModel:

    def test_create_series_entry(self, session):
        series_schema = SeriesSchema()
        series_obj, error = series_schema.load(
            dict(name="example series",
                 date_start=str(datetime.today()),
                 date_end=str(datetime.today() + timedelta(days=30))))
        assert not error
        session.add(series_obj)
        session.commit()
        assert series_obj.id > 0

    def test_fetch_series_entries(self, session):
        series_schema = SeriesSchema()
        result = session.query(Series).all()
        series_obj, error = series_schema.dump(result, many=True)
        assert not error
        assert len(series_obj) > 0
        assert not set(series_obj[0].keys()) - \
            {'name', 'date_start', 'date_end', 'id'}

    def test_create_tournaments_entry(self, session):
        tournaments_schema = TournamentsSchema()
        series_schema = SeriesSchema()
        result = session.query(Series).first()
        series_obj, error = series_schema.dump(result)
        _id = series_obj.get('id')
        assert _id is not None
        assert not error
        tournaments_obj, error = tournaments_schema.load(dict(
            series_id=_id,
            name='Test Tournament',
            city='Bangalore',
            country='India',
            date_start=str(datetime.today()),
            date_end=str(datetime.today() + timedelta(days=30))
        ))
        assert not error
        session.add(tournaments_obj)
        session.commit()
        assert tournaments_obj.id > 0

    def test_fetch_tournaments_entries(self, session):
        tournaments_schema = TournamentsSchema()
        result = session.query(Tournaments).all()
        tournaments_obj, error = tournaments_schema.dump(result, many=True)
        assert not error
        assert len(tournaments_obj) > 0
        assert not set(tournaments_obj[0].keys()) - \
            {'name', 'date_start', 'date_end', 'id', 'series_id', 'country', 'city'}
