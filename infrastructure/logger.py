import sys
from loguru import logger
from src.config.config import settings

# Configure Logger
log_file_path = settings.BASE_DIR / "logs" / "test_execution.log"

logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    log_file_path,
    rotation="10 MB",
    retention="1 week",
    compression="zip",
    level="DEBUG"
)

def get_logger(name: str):
    return logger.bind(name=name)
