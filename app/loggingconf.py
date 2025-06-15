import logging
from logging.config import dictConfig

def setuplogging(logfile: str = "./log/api.log") -> None:
    dictConfig(
        {
            "version": 1,
            "disableexistingloggers": False,  # оставляем uvicorn-овские
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                },
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "default",
                    "filename": logfile,
                    "encoding": "utf-8",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {         # корневой логер, к которому подключён uvicorn
                "level": "INFO",
                "handlers": ["file", "console"],
            },
        }
    )