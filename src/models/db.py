"""DB session module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from abc import ABCMeta, abstractmethod
from sqlalchemy_utils import database_exists
from src.config import Configurations as Config
from src.models.base import Base
from src.utils.logger import logger

config = Config()


class Database(metaclass=ABCMeta):
    """Implement the Database inteface."""

    @abstractmethod
    def connect(self):
        """Return the session object."""
        pass

    @property
    @abstractmethod
    def uri(self):
        """Database uri."""
        pass

    @abstractmethod
    def is_alive(self):
        """Check for the connection."""
        pass


class SQLiteDB(Database):
    """SQLite database implementation ONLY FOR THE TESTING PURPOSE."""

    @property
    def uri(self):
        """Database uri."""
        return "sqlite:////tmp/dummy.db"

    def connect(self):
        """Return the session object."""
        from sqlalchemy.interfaces import PoolListener

        # Enforcing Foreign Keys support in sqlite3
        class ForeignKeysListener(PoolListener):
            def connect(self, dbapi_con, con_record):
                dbapi_con.execute('PRAGMA foreign_keys=ON')

        if self.is_alive:
            engine = create_engine(
                self.uri, poolclass=NullPool,
                listeners=[ForeignKeysListener()],
                echo=config.DB_CONFIG.SQLALCHEMY_LOG)
            Base.metadata.bind = engine
            Session = sessionmaker(bind=engine)
            return Session()

    def is_alive(self):
        """Check for the connection."""
        try:
            return database_exists(self.uri)
        except Exception as exc:
            logger.error(exc, exc_info=True)
            return False


db_session = SQLiteDB().connect()
