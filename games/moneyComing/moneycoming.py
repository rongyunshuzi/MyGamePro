import time
from services import GameServer
from statistic import MoneyComingStatistic
from logconfig import logger
import random
import concurrent.futures.thread


class MoneyComing(GameServer):
    statistics = MoneyComingStatistic()

    def __init__(self):
        GameServer.__init__(self)
        self.in_room = False
        self.server.add_message_callback(12082, 2, self.spin_message_callback)

    def join_room_message_callback(self, message):
        logger.success('join_room_message_callback:{}'.format(message))
        self.in_room = True

    @classmethod
    def spin_message_callback(cls, message):
        logger.success(message)
        cls.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message({
            "protocolId": 1,
            "type": 2,
            "content": {
                "gameId": 1007,
                "gameType": 1000
            }
        })
        time.sleep(2)
        self.game_init()

    def spin(self):
        self.server.send_message({
            "protocolId": 2082,
            "type": 2,
            "content": {
                "score": 10000,
            }
        })

    @classmethod
    def spins(cls, round_count):
        money_coming = MoneyComing()
        money_coming.ready()
        while cls.statistics.round_count < round_count:
            money_coming.spin()
            time.sleep(random.uniform(0.01, 0.2))

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
    MoneyComing.persistent_spin(user_number=10, round_count=2000)
