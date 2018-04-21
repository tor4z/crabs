import logging

class Log:
    def __init__(self, name=None, format=None, level=None, file=None):
        self._name = name
        self._format = format or "[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
        self._level = level or logging.INFO
        self._file = file
        self._logger = logging.getLogger(self._name)
        if self._file is None:
            lh = logging.StreamHandler()
        else:
            lh = logging.FileHandler(self._file)
        lh.setFormatter(logging.Formatter(self._format))
        self._logger.setLevel(self._level)
        self._logger.addHandler(lh)

    def info(self, *args, **kwargs):
        self._logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self._logger.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        self._logger.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self._logger.warning(*args, **kwargs)

    def fatal(self, *args, **kwargs):
        self._logger.fatal(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self._logger.critical(*args, **kwargs)

    def exception(self, *args, **kwargs):
        self._logger.exception(*args, **kwargs)