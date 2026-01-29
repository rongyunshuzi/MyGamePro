import time
from services import GameServer
from statistic import FortuneGemsStatistic
from config import logger


class FortuneGems(GameServer):
    statistics = FortuneGemsStatistic()

    def __init__(self):
        GameServer.__init__(self)
        self.in_room = False
        self.server.add_message_callback(12062, 2, self.spin_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        FortuneGems.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1006,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self, is_extra_spin=0):
        self.server.send_message(
            {
                "protocolId": 2062,
                "type": 2,
                "content": {
                    "score": 40,
                    "isExtraSpin": is_extra_spin
                }
            }
        )