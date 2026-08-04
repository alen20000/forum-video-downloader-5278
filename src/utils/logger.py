import src.config as config
import logging


def setup_logging():
    config.LOGGING_PATH.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.LOGGING_PATH/"log.log", encoding="utf-8")
        ]
    )