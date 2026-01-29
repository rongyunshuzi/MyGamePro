import time
from services import GameServer
from statistic import CashWheelStatistic
from config import logger


class CashWheel(GameServer):
    statistics = CashWheelStatistic()

    def __init__(self):
        GameServer.__init__(self)
        self.server.add_message_callback(12222, 2, self.spin_message_callback)

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        CashWheel.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1013,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2132,
                "type": 2,
                "content": {
                    "score": 500
                }
            }
        )
        time.sleep(0.1)