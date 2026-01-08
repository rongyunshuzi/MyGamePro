# logconfig.py
from loguru import logger
import sys

# 移除默认配置
logger.remove()

# 添加控制台处理器，只显示WARNING及以上级别
logger.add(
    sys.stdout,
    level="SUCCESS",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True
)