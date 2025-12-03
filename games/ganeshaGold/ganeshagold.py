import time
from services import GameServer
from statistic import GaneshaGoldStatistic
from logconfig import logger


class GaneshaGold(GameServer):
    statistic = GaneshaGoldStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.in_room = False
        self.server.add_message_callback(12102, 2, self.spin_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        cls.statistic.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1008,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2102,
                "type": 2,
                "content": {
                    "score": 200,
                }
            }
        )


if __name__ == '__main__':
    ganesha_gold = GaneshaGold()
    ganesha_gold.ready()

    try:

        while ganesha_gold.statistic.round_count < 1000:
            time.sleep(0.1)
            ganesha_gold.spin()
    except KeyboardInterrupt as e:
        logger.warning("用户手动退出")

    finally:
        ganesha_gold.statistic.see()
