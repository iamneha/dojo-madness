"""Base declarations model."""
from sqlalchemy.ext.declarative import declarative_base


class BaseModelMixin(object):
    """Subclasses of this class will gain some helper methods."""

    def to_dict(self):
        """Convert table to dictionary."""
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        return d


Base = declarative_base(cls=BaseModelMixin)
