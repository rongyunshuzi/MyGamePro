import concurrent.futures
import random
import time

from logconfig import logger
from services import GameServer
from .statistic import SafariStatistic


class SafariGame(GameServer):
    statistics = SafariStatistic()

    def __init__(self):
        GameServer.__init__(self)
        self.in_room = False
        self.server.add_message_callback(12072, 2, self.spin_message_callback)
        self.server.add_message_callback(11010, 2, self.jackpot_message_callback)
        self.server.add_message_callback(12071, 2, self.safari_initialize_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def safari_initialize_message_callback(cls, message):
        logger.success('game_initialize:{}'.format(message))

    @classmethod
    def spin_message_callback(cls, message):
        logger.success(message)
        cls.statistics.analyze(message['content'])

    @classmethod
    def jackpot_message_callback(cls, message):
        logger.debug(message)

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1011,
                    "gameType": 1000
                }
            }
        )
        time.sleep(1)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2072,
                "type": 2,
                "content": {
                    "score": 1000
                }
            }
        )
