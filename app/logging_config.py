import logging
import sys


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s"
LOG_DEFAULT_HANDLERS = ["console"]

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        },

    },
    "loggers": {
        "": { # Корневой логгер
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
            "propagate": False, # Не передавать сообщения родительским логгерам
        },
        "uvicorn.error": {
            "level": "INFO",
             "handlers": LOG_DEFAULT_HANDLERS,
             "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": LOG_DEFAULT_HANDLERS,
            "propagate": False,
        },
        "app": {
             "handlers": LOG_DEFAULT_HANDLERS,
             "level": "DEBUG",
             "propagate": False,
        },

         "sqlalchemy.engine": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "WARNING",
            "propagate": False,
         },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)