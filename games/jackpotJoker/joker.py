import time
from services import GameServer
from statistic import JokerStatistic
from config import logger


class Joker(GameServer):
    statistics = JokerStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.server.add_message_callback(12042, 2, self.spin_message_callback)

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        Joker.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1010,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self, is_extra_spin=0, is_free_game=0):
        self.server.send_message(
            {
                "protocolId": 2042,
                "type": 2,
                "content": {
                    "score": 100,
                    "isExtraSpin": is_extra_spin,
                    "isFreeGame": is_free_game
                }
            }
        )


if __name__ == '__main__':
    thor = Joker()
    thor.ready()

    try:
        while thor.statistics.round_count < 1000:
            time.sleep(0.1)
            thor.spin()
    except KeyboardInterrupt as e:
        logger.warning("用户手动退出")

    finally:
        thor.statistics.see()
