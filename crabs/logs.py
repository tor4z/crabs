import logging

class Log:
    def __init__(self, name=None, format=None, level=None, file=None):
        self._name = name
        self._format = format or "[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
        self._level = level or logging.INFO
        self._file = file
        self._logger_ = None
        self._statistics = {
            "Info": 0,
            "Debug": 0,
            "Error": 0,
            "Warning": 0,
            "Fatal": 0,
            "Critical": 0,
            "Exception": 0
        }

    def set_name(self, name):
        self._name = name

    def set_format(self, format):
        self._format = format

    def set_level(self, level):
        self._level = level

    def set_file(self, file):
        self._file = file

    @property
    def _logger(self):
        if self._logger_ is None:
            self._logger_ = logging.getLogger(self._name)
            if self._file is None:
                lh = logging.StreamHandler()
            else:
                lh = logging.FileHandler(self._file)
            lh.setFormatter(logging.Formatter(self._format))
            self._logger_.setLevel(self._level)
            self._logger_.addHandler(lh)
        return self._logger_
    
    @property
    def statistics(self):
        string = ""
        for key in self._statistics:
            val = self._statistics[key]
            if val > 0:
                string += "{0}({1}) ".format(key, val)
        return string

    def info(self, *args, **kwargs):
        self._statistics["Info"] += 1
        self._logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self._statistics["Debug"] += 1
        self._logger.debug(*args, **kwargs)

    def error(self, *args, **kwargs):
        self._statistics["Error"] += 1
        self._logger.error(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self._statistics["Warning"] += 1
        self._logger.warning(*args, **kwargs)

    def fatal(self, *args, **kwargs):
        self._statistics["Fatal"] += 1
        self._logger.fatal(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self._statistics["Critical"] += 1
        self._logger.critical(*args, **kwargs)

    def exception(self, *args, **kwargs):
        self._statistics["Exception"] += 1
        self._logger.exception(*args, **kwargs)