import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import settings

LOG_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Root logger
logger = logging.getLogger("flow_manager")
logger.setLevel(LOG_LEVEL)

# Console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(LOG_LEVEL)
ch.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(ch)

# Optional rotating file handler (uncomment to enable)
# fh = RotatingFileHandler("flow_manager.log", maxBytes=10_000_000, backupCount=5)
# fh.setLevel(LOG_LEVEL)
# fh.setFormatter(logging.Formatter(LOG_FORMAT))
# logger.addHandler(fh)

# Avoid duplicate logs in Uvicorn setup
logger.propagate = False
