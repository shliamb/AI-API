import uvicorn

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(name)s %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "api_file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/log/api.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
        "uvicorn_file": {
            "formatter": "default", 
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/log/uvicorn.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "loggers": {
        "api": {"handlers": ["api_file"], "level": "INFO", "propagate": False},
        "uvicorn": {"handlers": ["uvicorn_file"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["uvicorn_file"], "level": "INFO", "propagate": False},
    }
}


if __name__ == "__main__":
    from api import app
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=LOG_CONFIG)




# Пояснительная бригада:
#/log/api.log - логи из FastAPI
#/log/uvicorn.log - логи uvicorn (запросы HTTP)