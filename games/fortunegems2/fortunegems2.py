import time
from services import GameServer
from statistic import FortuneGems2Statistic
from logconfig import logger


class FortuneGems2(GameServer):
    fortune_gems_2_statistics = FortuneGems2Statistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.in_room = False
        self.server.add_message_callback(12022, 2, self.spin_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        FortuneGems2.fortune_gems_2_statistics.analyze(message['content'])


    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1004,
                    "gameType": 1000
                }
            }
        )
        time.sleep(1)
        self.game_init()

    def spin(self, is_extra_spin=0):
        self.server.send_message(
            {
                "protocolId": 2022,
                "type": 2,
                "content": {
                    "score": 40,
                    "isExtraSpin": is_extra_spin
                }
            }
        )


if __name__ == '__main__':
    fortune_gems2 = FortuneGems2()
    fortune_gems2.ready()

    try:

        while fortune_gems2.fortune_gems_2_statistics.round_count < 1000:
            time.sleep(0.1)
            fortune_gems2.spin()
    except KeyboardInterrupt as e:
        logger.error(e)

    finally:
        fortune_gems2.fortune_gems_2_statistics.see()
