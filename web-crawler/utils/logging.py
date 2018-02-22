import logging
from utils import logger_handler

def getLogger(name):
    log = logging.getLogger(name)
    log.setLevel('DEBUG')
    log.addHandler(logger_handler.LoggerHandler())
    return log