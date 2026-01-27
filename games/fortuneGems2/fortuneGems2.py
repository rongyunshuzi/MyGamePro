import time
from services import GameServer
from .statistic import FortuneGems2Statistic
from logconfig import logger


class FortuneGems2Game(GameServer):
    statistics = FortuneGems2Statistic()

    def __init__(self):
        GameServer.__init__(self)
        self.in_room = False
        self.server.add_message_callback(12022, 2, self.spin_message_callback)
        self.server.add_message_callback(12021, 2, self.fortune_gems2_initialize_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def fortune_gems2_initialize_message_callback(cls, message):
        logger.success('game_initialize:{}'.format(message))

    @classmethod
    def spin_message_callback(cls, message):
        logger.success(message)
        FortuneGems2Game.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message({
            "protocolId": 1,
            "type": 2,
            "content": {
                "gameId": 1004,
                "gameType": 1000
            }
        })
        time.sleep(2)
        self.game_init()

    def spin(self, is_extra_spin=1):
        self.server.send_message({
            "protocolId": 2022,
            "type": 2,
            "content": {
                "score": 20000,
                "isExtraSpin": is_extra_spin
            }
        })