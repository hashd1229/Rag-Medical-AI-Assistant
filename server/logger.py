import logging

from fastapi import logger

def setup_logger(name = "MedicalAssistant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] --- [%(message)s]")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


logger = setup_logger()

logger.info("RAG Process Started")
logger.debug("Debugging")
logger.error("Fail to Load")
logger.critical("Critical message")