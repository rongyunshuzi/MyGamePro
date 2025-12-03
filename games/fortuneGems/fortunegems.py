import concurrent.futures
import time
from services import GameServer
from statistic import FortuneGemsStatistic
from logconfig import logger


class FortuneGems(GameServer):
    statistics = FortuneGemsStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
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

    @classmethod
    def spins(cls, round_count):
        game = FortuneGems()
        game.ready()
        while cls.statistics.round_count < round_count:
            game.spin()
            time.sleep(0.1)

    @classmethod
    def persistent_spin(cls, user_number, round_count):
        with concurrent.futures.ThreadPoolExecutor(max_workers=user_number) as executor:
            try:
                tasks = [executor.submit(cls.spins, round_count) for _ in range(user_number)]
                for task in tasks:
                    task.result()
            except KeyboardInterrupt:
                logger.warning("用户手动退出")

            finally:
                cls.statistics.see()

if __name__ == '__main__':
    FortuneGems.persistent_spin(user_number=10, round_count=1000)

