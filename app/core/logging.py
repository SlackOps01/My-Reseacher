from rich.logging import RichHandler
import logging

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

logger = logging.getLogger(__name__)
