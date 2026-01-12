
import logging
import structlog
from config.settings import settings
from pathlib import Path
from datetime import datetime

class LoggerSetup:
    def __init__(self, level: str = "INFO", json_output: bool = False):
        self.level = level.upper()
        self.json_output = json_output
        self.log_dir = settings.data.logs
        self._configure()

    def _configure(self):
        today = datetime.now().strftime("%Y-%m-%d")
        file_handler = logging.FileHandler(Path(self.log_dir, f"{today}.log"))
        file_handler.setLevel(self.level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)

        logging.basicConfig(
            format="%(message)s",
            level=self.level,
            handlers=[file_handler, console_handler]
        )

        renderer = (
            structlog.processors.JSONRenderer()
            if self.json_output else
            structlog.dev.ConsoleRenderer()
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_log_level,
                structlog.processors.format_exc_info,
                renderer,
            ],
            wrapper_class=structlog.make_filtering_bound_logger(self.level),
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self):
        return structlog.get_logger()


# Project-wide logger
logger = LoggerSetup(json_output=False).get_logger()