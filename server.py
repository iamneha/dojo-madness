#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gunicorn server."""

from gunicorn.app.base import Application
from src.config import Configurations as Config
import multiprocessing
from src.apis.routes import app

config = Config()


def number_of_workers():
    """Return the number_of_workers [(cores * 2) +1 ]."""
    return (multiprocessing.cpu_count() * 2) + 1


def init_db():
    """Initialize the database with the tables.

    NOTE: this is a temporary solution
    """
    import src.apis.routes as rt
    from src.models.base import Base

    Base.metadata.create_all()
    return rt


class APIServer(Application):
    """APIServer applicaiton."""

    def init(self, parser, opts, args):
        """Initialize the all parameters."""
        init_db()
        return {
            'bind': '{0}:{1}'.format(config.HOST, config.PORT),
            'workers': number_of_workers(),
            'reload': config.RELOAD
        }

    def load(self):
        """Load the application."""
        return app


if __name__ == "__main__":
    api_server = APIServer()
    api_server.run()
