"""Logging utility for package."""

import datetime
import logging
import daiquiri
from src.config import Configurations as Config

config = Config()

formatter = daiquiri.formatter.ColorExtrasFormatter(
    fmt=(daiquiri.formatter.DEFAULT_EXTRAS_FORMAT +
         " [%(filename)s:%(lineno)s F:%(funcName)s()]"))

daiquiri.setup(
    level=config.LOG_LEVEL,
    outputs=(
        daiquiri.output.TimedRotatingFile('/tmp/errors.log',
                                          level=logging.WARNING,
                                          interval=datetime.timedelta(hours=48)),
        daiquiri.output.Stream(formatter=formatter)
    )
)

logger = daiquiri.getLogger(__name__)
