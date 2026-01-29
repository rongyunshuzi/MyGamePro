# config.py
from loguru import logger
import sys

# 日志配置
logger.remove()     # 移除默认配置
logger.add(
    sys.stdout,
    level="SUCCESS",    # 添加控制台处理器，只显示WARNING及以上级别
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True
)

# 主机服务器配置

HOST = "192.168.0.168"
MALL_SERVER = "ws://{}:8091".format(HOST)
GAME_SERVER = "ws://{}:8092".format(HOST)
AUTHENTICATION_SERVER = "http://{}:8083".format(HOST)
