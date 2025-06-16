from config import LOG_CONFIG_API, setup_logger
logging_api = setup_logger('api', LOG_CONFIG_API)
import uvicorn
from api import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_config=None)
