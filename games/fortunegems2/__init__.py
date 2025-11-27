import asyncio
import time

from logconfig import logger
from services import GameServer
from statistic import CowStatistic


class CowGame(GameServer):
    cow_statistics = CowStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.in_room = False
        self.server.add_message_callback(12072, 2, self.spin_message_callback)
        self.server.add_message_callback(11010, 2, self.jackpot_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        CowGame.cow_statistics.analyze(message['content'])

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
                    "score": 20
                }
            }
        )


if __name__ == '__main__':
    cow = CowGame()
    cow.ready()

    try:

        while cow.cow_statistics.round_count < 1000:
            time.sleep(0.1)
            cow.spin()
    except KeyboardInterrupt as e:
        logger.error(e)

    finally:
        cow.cow_statistics.see()