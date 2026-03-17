import logging
import colorlog
import os
from config.paths import LOG_FILE_PATH, TMP_DIR
from typeguard import typechecked


class Logger:
    """
    A singleton class for creating and accessing a logger with both console and file handlers.
    The logger will output colored logs to the console and regular logs to a file.
    Console logs will be color-coded based on the log level with UTF-8 encoding.
    Each run will clear the log file.

    Attributes:
        _instance (Logger): The singleton instance of the Logger class.
        logger (logging.Logger): The logger object.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.__setup_logger()
            cls.debug(cls._instance, "Logger initialized.")
        return cls._instance

    def __setup_logger(self):
        stdout_formatter = colorlog.ColoredFormatter(
            "(%(asctime)s) - %(log_color)s%(levelname)s%(reset)s: %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            secondary_log_colors={},
            style="%",
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(stdout_formatter)

        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        self.logger = logging.getLogger("api")
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)

        if os.path.exists(LOG_FILE_PATH):
            open(LOG_FILE_PATH, "w", encoding='utf-8').close()

    @typechecked
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    @typechecked
    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    @typechecked
    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    @typechecked
    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @typechecked
    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


logger = Logger()
