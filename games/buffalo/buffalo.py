import time

from logconfig import logger
from services import GameServer
from statistic import BuffaloStatistic
import concurrent.futures


class BuffaloGame(GameServer):
    statistics = BuffaloStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.initialized = False
        self.server.add_message_callback(12142, 2, self.spin_message_callback)
        self.server.add_message_callback(11010, 2, self.jackpot_message_callback)
        self.server.add_message_callback(12141, 2, self.buffalo_init_message_callback)

    @classmethod
    def spin_message_callback(cls, message):
        logger.success(message)
        BuffaloGame.statistics.analyze(message['content'])

    def jackpot_message_callback(self, message):
        pass
        # logger.success(message)

    def buffalo_init_message_callback(self, message):
        self.initialized = True
        pass

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1014,
                    "gameType": 1000
                }
            }
        )

        time.sleep(1)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2142,
                "type": 2,
                "content": {
                    "score": 20
                }
            }
        )

    @classmethod
    def spins(cls, round_count):
        buffalo = BuffaloGame()
        buffalo.ready()
        while cls.statistics.round_count < round_count:
            buffalo.spin()
            time.sleep(.1)

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
    BuffaloGame.persistent_spin(user_number=100, round_count=10000)

