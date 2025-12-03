import time
from services import GameServer
from statistic import MoneyComingStatistic
from logconfig import logger


class MoneyComing(GameServer):
    statistic = MoneyComingStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.in_room = False
        self.server.add_message_callback(12082, 2, self.spin_message_callback)

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
                    "gameId": 1007,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2082,
                "type": 2,
                "content": {
                    "score": 100,
                }
            }
        )


if __name__ == '__main__':
    money_coming = MoneyComing()
    money_coming.ready()

    try:

        while money_coming.statistic.round_count < 1000:
            time.sleep(0.1)
            money_coming.spin()
    except KeyboardInterrupt as e:
        logger.warning("用户手动退出")

    finally:
        money_coming.statistic.see()



