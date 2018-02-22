import logging

class LoggerHandler(logging.StreamHandler):
    
    def __init__(self):
        logging.StreamHandler.__init__(self)
        fmt = '[%(asctime)s][%(filename)s][%(levelname)s]:\t%(message)s'
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)