import concurrent.futures
import time
from services import GameServer
from statistic import CashWheelStatistic
from logconfig import logger


class CashWheel(GameServer):
    statistics = CashWheelStatistic()

    def __init__(self, account=None, password=None):
        GameServer.__init__(self, account, password)
        self.server.add_message_callback(12222, 2, self.spin_message_callback)

    @classmethod
    def spin_message_callback(cls, message):
        logger.debug(message)
        CashWheel.statistics.analyze(message['content'])

    def ready(self):
        time.sleep(1)
        self.server.send_message(
            {
                "protocolId": 1,
                "type": 2,
                "content": {
                    "gameId": 1013,
                    "gameType": 1000
                }
            }
        )
        time.sleep(2)
        self.game_init()

    def spin(self):
        self.server.send_message(
            {
                "protocolId": 2132,
                "type": 2,
                "content": {
                    "score": 500
                }
            }
        )
        time.sleep(0.1)

    @classmethod
    def spins(cls, round_count):
        cash_wheel = CashWheel()
        cash_wheel.ready()
        while cls.statistics.round_count < round_count:
            cash_wheel.spin()

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
    CashWheel.persistent_spin(user_number=10, round_count=1000)
