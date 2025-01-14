import logging

class LoggerFactory(object):
    _logger: logging = None

    def configureLogger(logger: logging.Logger):
        if LoggerFactory._logger is None:
            LoggerFactory._logger = logger
    
    @staticmethod
    def info(msg: str):
        LoggerFactory._logger.info(msg)
    
    @staticmethod
    def error(msg: str):
        LoggerFactory._logger.error(msg)