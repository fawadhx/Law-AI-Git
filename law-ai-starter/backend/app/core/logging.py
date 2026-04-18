from __future__ import annotations

import json
import logging
from logging.config import dictConfig

from app.core.config import Settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }
        if hasattr(record, "request_id"):
            payload["request_id"] = getattr(record, "request_id")
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(settings: Settings) -> None:
    formatter_name = "json" if settings.app_log_json else "default"
    config: dict[str, object] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            },
            "json": {
                "()": "app.core.logging.JsonFormatter",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": formatter_name,
            }
        },
        "root": {
            "level": settings.app_log_level.upper(),
            "handlers": ["console"],
        },
    }
    dictConfig(config)
